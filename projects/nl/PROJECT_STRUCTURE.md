# Структура проекта: UPWORK-ALL

```text
UPWORK-ALL/
├── 📁 archive/
├── 📁 memory/
│   └── 📄 9. Самая важная папка.txt
├── 📁 projects/
│   └── 📁 autoria-project/
│       ├── 📁 AI_INPUT/
│       │   ├── 📁 screenshots/
│       │   ├── 📄 answers.txt
│       │   ├── 📄 cookies.json
│       │   ├── 📄 description.txt
│       │   ├── 📄 headers.json
│       │   ├── 📄 network.har
│       │   ├── 📄 notes.txt
│       │   ├── 📄 page.html
│       │   └── 📄 traceback.txt
│       ├── 📁 AI_OUTPUT/
│       ├── 📁 app/
│       │   ├── 📄 browser.py
│       │   ├── 📄 config.py
│       │   ├── 📄 exporter.py
│       │   ├── 📄 main.py
│       │   ├── 📄 parser.py
│       │   ├── 📄 scraper.py
│       │   └── 📄 utils.py
│       ├── 📁 docs/
│       │   └── 📄 здесь пилим документацию.txt
│       ├── 📁 input/
│       ├── 📁 output/
│       ├── 📁 tests/
│       ├── 📁 workflows/
│       │   ├── 📄 new_project.md
│       │   └── 📄 Вот чего сейчас не хватает..txt
│       ├── 📄 .env
│       ├── 📄 docker-compose.yml
│       ├── 📄 Dockerfile
│       ├── 📄 project_state.json
│       ├── 📄 PROJECT_STRUCTURE.md
│       ├── 📄 README.md
│       ├── 📄 requirements.txt
│       └── 📄 Как добиться не писать лишний код.txt
├── 📁 scraping-templates/
│   ├── 📁 examples/
│   │   ├── 📁 amazon/
│   │   ├── 📁 login_site/
│   │   ├── 📁 news_site/
│   │   └── 📄 Я бы сделал больше..txt
│   ├── 📁 knowledge/
│   │   ├── 📄 api.md
│   │   ├── 📄 bs4.md
│   │   ├── 📄 cloudflare.md
│   │   ├── 📄 docker.md
│   │   ├── 📄 playwright.md
│   │   ├── 📄 scrapy.md
│   │   ├── 📄 selenium.md
│   │   └── 📄 ИИ можно сразу скормить этот файл..txt
│   ├── 📁 prompts/
│   │   ├── 📄 01_analysis_prompt.md
│   │   ├── 📄 02_project_prompt.md
│   │   ├── 📄 03_scraper_prompt.md
│   │   ├── 📄 04_parser_prompt.md
│   │   ├── 📄 05_debug_prompt.md
│   │   ├── 📄 05_refactor.md
│   │   ├── 📄 06_docker_prompt.md
│   │   ├── 📄 06_review.md
│   │   ├── 📄 07_optimize.md
│   │   └── 📄 08_create_tests.md
│   ├── 📁 scripts/
│   │   └── 📁 tools/
│   │       ├── 📄 create_project.py
│   │       ├── 📄 dump_full_project.py
│   │       ├── 📄 dump_structure.py
│   │       ├── 📄 my_project_structure.txt
│   │       └── 📄 prepare_for_ai.py
│   ├── 📁 snippets/
│   │   └── 📄 Туда можно складывать маленькие куски.txt
│   ├── 📁 templates/
│   │   ├── 📁 api/
│   │   ├── 📁 beautifulsoup/
│   │   ├── 📁 docker/
│   │   │   └── 📄 Dockerfile
│   │   ├── 📁 infinite_scroll/
│   │   ├── 📁 login/
│   │   ├── 📁 pagination/
│   │   ├── 📁 playwright/
│   │   ├── 📁 project/
│   │   └── 📁 scrapy/
│   └── 📄 AI_rules.md
├── 📁 starter-project/
│   ├── 📁 AI_INPUT/
│   │   ├── 📁 screenshots/
│   │   ├── 📄 answers.txt
│   │   ├── 📄 cookies.json
│   │   ├── 📄 description.txt
│   │   ├── 📄 headers.json
│   │   ├── 📄 network.har
│   │   ├── 📄 notes.txt
│   │   ├── 📄 page.html
│   │   └── 📄 traceback.txt
│   ├── 📁 AI_OUTPUT/
│   │   ├── 📄 01_analysis_answer.md
│   │   ├── 📄 01_analysis_prompt.md
│   │   ├── 📄 02_project_answer.md
│   │   ├── 📄 02_project_prompt.md
│   │   ├── 📄 03_scraper_answer.py
│   │   ├── 📄 03_scraper_prompt.md
│   │   ├── 📄 04_parser_answer.py
│   │   ├── 📄 04_parser_prompt.md
│   │   ├── 📄 05_debug_prompt.md
│   │   ├── 📄 5_debug_answer.md
│   │   └── 📄 Я бы сделал еще одну папку.txt
│   ├── 📁 app/
│   │   ├── 📄 browser.py
│   │   ├── 📄 config.py
│   │   ├── 📄 exporter.py
│   │   ├── 📄 main.py
│   │   ├── 📄 parser.py
│   │   ├── 📄 scraper.py
│   │   └── 📄 utils.py
│   ├── 📁 docs/
│   │   └── 📄 здесь пилим документацию.txt
│   ├── 📁 input/
│   ├── 📁 output/
│   │   ├── 📄 output_results.csv
│   │   └── 📄 output_results.json
│   ├── 📁 tests/
│   ├── 📁 workflows/
│   │   ├── 📄 new_project.md
│   │   └── 📄 Вот чего сейчас не хватает..txt
│   ├── 📄 .env
│   ├── 📄 docker-compose.yml
│   ├── 📄 Dockerfile
│   ├── 📄 PROJECT_STRUCTURE.md
│   ├── 📄 README.md
│   ├── 📄 requirements.txt
│   └── 📄 Как добиться не писать лишний код.txt
├── 📄 ai_workflow.py
├── 📄 check-list.txt
├── 📄 export_for_ai.py
├── 📄 my_project_structure.txt
├── 📄 Единый формат передачи задачи ИИ.txt
└── 📄 САМОЕ ГЛАВНОЕ.txt
```
