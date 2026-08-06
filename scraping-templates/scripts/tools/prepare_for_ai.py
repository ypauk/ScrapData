from pathlib import Path
from bs4 import BeautifulSoup

# Пути
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
PROMPT_TEMPLATE = ROOT_DIR / "prompts" / "01_analyze_project.md"
INPUT_DIR = ROOT_DIR.parent / "starter-project" / "AI_INPUT"
OUTPUT_FILE = ROOT_DIR.parent / "starter-project" / "AI_OUTPUT" / "final_prompt_for_ai.md"

def simplify_html(file_path):
    """Очищает HTML, оставляя только критически важную для парсинга структуру."""
    try:
        content = file_path.read_text(encoding='utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        
        # Удаляем ненужные теги, создающие шум
        for tag in soup(["script", "style", "noscript", "svg", "meta", "link", "footer", "nav", "iframe"]):
            tag.decompose()
            
        # Оставляем только важные атрибуты для поиска селекторов
        allowed_attrs = {'class', 'id', 'data-test-id', 'href', 'src', 'name'}
        for tag in soup.find_all(True):
            attrs = dict(tag.attrs)
            for attr in attrs:
                if attr not in allowed_attrs:
                    del tag[attr]
                    
        return f"\n\n--- СЖАТЫЙ HTML: {file_path.name} ---\n{soup.prettify()}"
    except Exception as e:
        return f"\n\n--- ОШИБКА ПРИ ОБРАБОТКЕ HTML {file_path.name}: {e} ---\n"

def build_prompt():
    # 1. Загрузка шаблона
    if not PROMPT_TEMPLATE.exists():
        print(f"❌ Ошибка: Шаблон промпта не найден: {PROMPT_TEMPLATE}")
        return

    with open(PROMPT_TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 2. Собираем контекст из всех файлов в AI_INPUT
    context_data = ""
    if INPUT_DIR.exists():
        all_files = [f for f in INPUT_DIR.iterdir() if f.is_file() and f.suffix in ['.txt', '.html', '.md', '.json']]
        # description.txt всегда первый
        all_files.sort(key=lambda x: (x.name != 'description.txt', x.name))
        
        for file_path in all_files:
            if file_path.suffix == '.html':
                context_data += simplify_html(file_path)
            else:
                context_data += f"\n\n--- ФАЙЛ: {file_path.name} ---\n"
                try:
                    context_data += file_path.read_text(encoding='utf-8')
                except Exception as e:
                    context_data += f"Ошибка чтения: {e}"
    
    # 3. Соединяем
    final_prompt = template.replace("{{CLIENT_DESCRIPTION}}", context_data)
    
    # 4. Сохраняем
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_prompt)
        
    print(f"✅ Готово! Файл промпта создан: {OUTPUT_FILE}")

if __name__ == "__main__":
    build_prompt()