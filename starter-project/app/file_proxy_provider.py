#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Proxy Provider.

Эталонная реализация `ProxyProvider` (см. `app/proxy_manager.py`),
загружающая список прокси из локального текстового файла.

Назначение этого модуля — подтвердить, что архитектура Proxy Manager
действительно провайдер-независима: Proxy Manager работает с
`FileProxyProvider` точно так же, как и с `EnvProxyProvider`, не зная
ничего о том, что прокси читаются из файла.

File Proxy Provider:

* берет путь к файлу и схему по умолчанию из Configuration Manager
  (`config.PROXY_FILE`, `config.PROXY_FILE_DEFAULT_SCHEME`);
* поддерживает несколько распространенных форматов записи прокси
  (см. `_parse_line()`);
* пропускает пустые строки, комментарии (`#`) и некорректные записи без
  падения всего приложения — только с предупреждением в лог;
* возвращает нормализованный список прокси в виде готовых URL
  (`http://[user:pass@]host:port`), из которого `get_proxy()` отдает
  первый доступный (без ротации/выбора — это ответственность будущих
  задач Proxy Rotation / Proxy Selection, см. `framework/ROADMAP.md`).

File Proxy Provider НЕ выбирает, НЕ ротирует, НЕ валидирует и НЕ проверяет
здоровье прокси, НЕ выполняет HTTP-запросы и ничего не знает о других
провайдерах (Webshare, BrightData и т.д.) — вся эта логика вне его
ответственности.
"""

from pathlib import Path
from typing import List, Optional

from app import config
from app.proxy_manager import ProxyProvider

# Схемы, которые считаются уже полными URL и не требуют достройки
# (запись используется как есть, без подстановки PROXY_FILE_DEFAULT_SCHEME).
_KNOWN_SCHEMES = ("http://", "https://", "socks5://", "socks4://")


def _parse_line(line: str, default_scheme: str) -> Optional[str]:
    """
    Разбирает одну строку файла прокси и возвращает нормализованный URL.

    Поддерживаемые форматы:
        ip:port
        ip:port:username:password
        http://ip:port
        http://username:password@ip:port
        socks5://username:password@ip:port
        (и другие схемы из `_KNOWN_SCHEMES`, переданные как есть)

    Args:
        line (str): Сырая строка из файла (без завершающего перевода строки).
        default_scheme (str): Схема, подставляемая для записей без схемы
            (`ip:port` / `ip:port:username:password`).

    Returns:
        Optional[str]: Нормализованный URL прокси, либо `None`, если строка
            пуста, является комментарием или не удалось разобрать формат.
    """
    entry = line.strip()
    if not entry or entry.startswith("#"):
        return None

    # Уже полный URL — используем как есть.
    if entry.startswith(_KNOWN_SCHEMES):
        return entry

    # ip:port или ip:port:username:password
    parts = entry.split(":")
    if len(parts) == 2:
        host, port = parts
        if not (host and port.isdigit()):
            return None
        return f"{default_scheme}://{host}:{port}"

    if len(parts) == 4:
        host, port, username, password = parts
        if not (host and port.isdigit() and username and password):
            return None
        return f"{default_scheme}://{username}:{password}@{host}:{port}"

    return None


class FileProxyProvider(ProxyProvider):
    """
    Провайдер, читающий список прокси из локального файла.

    Хранит загруженные прокси в памяти (список) и последовательно
    возвращает первый из них через `get_proxy()`. Выбор/ротация конкретного
    прокси из списка — задача будущего компонента Proxy Rotation, а не
    этого провайдера.
    """

    def __init__(self, path: Path = None, default_scheme: str = None):
        """
        Args:
            path (Path, optional): Путь к файлу со списком прокси.
                По умолчанию — `config.PROXY_FILE`.
            default_scheme (str, optional): Схема для записей без явной
                схемы (`ip:port`). По умолчанию — `config.PROXY_FILE_DEFAULT_SCHEME`.
        """
        self.path = path or config.PROXY_FILE
        self.default_scheme = default_scheme or config.PROXY_FILE_DEFAULT_SCHEME
        self._proxies: List[str] = self._load()

    def _load(self) -> List[str]:
        """
        Загружает и парсит файл прокси.

        Returns:
            List[str]: Список успешно распознанных прокси (пустой, если
                файл отсутствует, пуст или не содержит валидных записей).
        """
        if not self.path.exists():
            print(f"[{__file__}] Файл прокси не найден: {self.path}")
            return []

        if self.path.stat().st_size == 0:
            print(f"[{__file__}] Файл прокси пуст: {self.path}")
            return []

        try:
            raw_lines = self.path.read_text(encoding="utf-8").splitlines()
        except Exception as e:
            print(f"[{__file__}] Ошибка при чтении файла прокси {self.path.name}: {e}")
            return []

        proxies: List[str] = []
        for line_number, raw_line in enumerate(raw_lines, start=1):
            parsed = _parse_line(raw_line, self.default_scheme)
            if parsed:
                proxies.append(parsed)
            elif raw_line.strip() and not raw_line.strip().startswith("#"):
                print(f"[{__file__}] Предупреждение: пропущена невалидная строка "
                      f"{line_number} в {self.path.name}: '{raw_line.strip()}'")

        print(f"[{__file__}] Загружено прокси из {self.path.name}: {len(proxies)}")
        return proxies

    def get_proxy(self) -> Optional[str]:
        """
        Возвращает первый прокси из загруженного списка, либо `None`,
        если список пуст.
        """
        return self._proxies[0] if self._proxies else None

    def get_all_proxies(self) -> List[str]:
        """
        Возвращает полный список успешно загруженных прокси. Полезно для
        будущего Proxy Rotation, чтобы не парсить файл повторно.

        Returns:
            List[str]: Список нормализованных URL прокси.
        """
        return list(self._proxies)

    def reload(self) -> List[str]:
        """
        Повторно читает файл прокси с диска и обновляет внутренний список.

        Returns:
            List[str]: Обновленный список загруженных прокси.
        """
        self._proxies = self._load()
        return self.get_all_proxies()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    provider = FileProxyProvider()
    print(f"[{__file__}] Путь к файлу прокси: {provider.path}")
    print(f"[{__file__}] Все загруженные прокси: {provider.get_all_proxies()}")
    print(f"[{__file__}] Активный прокси (get_proxy): {provider.get_proxy()}")

    # Демонстрация интеграции с Proxy Manager без изменения его кода/API.
    from app.proxy_manager import ProxyManager

    ProxyManager.set_provider(provider)
    print(f"[{__file__}] ProxyManager.get_proxy() после смены провайдера: {ProxyManager.get_proxy()}")
    print(f"[{__file__}] ProxyManager.to_requests_dict(): {ProxyManager.to_requests_dict()}")
