import tempfile
import unittest
from pathlib import Path

from app import scraper


class ScraperTests(unittest.TestCase):
    def test_load_local_html_reads_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "sample.html"
            path.write_text("<html>hello</html>", encoding="utf-8")
            self.assertEqual(scraper.load_local_html(str(path)), "<html>hello</html>")

    def test_fetch_page_returns_html_from_local_source_when_network_is_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "page.html"
            target.write_text("<html>fallback</html>", encoding="utf-8")
            original_dir = scraper.AI_INPUT_DIR
            scraper.AI_INPUT_DIR = Path(tmp_dir)
            try:
                html = scraper.fetch_page("https://example.com")
            finally:
                scraper.AI_INPUT_DIR = original_dir
            self.assertIn("fallback", html)


if __name__ == "__main__":
    unittest.main()
