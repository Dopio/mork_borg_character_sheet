# mork_borg_character_sheet/run.py
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import uvicorn
    # Передаём приложение как строку для импорта
    uvicorn.run(
        "backend.app.main:app",  # ← ВАЖНО: строка для импорта!
        host="127.0.0.1",
        port=8000,
        reload=True
    )
