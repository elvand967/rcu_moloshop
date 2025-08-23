# moloshop/assets/compiler_scss.py

import sys
from pathlib import Path
import sass

# === Импорт BASE_DIR из Django settings ===
try:
    sys.path.append(str(Path(__file__).resolve().parent.parent))  # ../moloshop/
    from config.settings.base import BASE_DIR
except ImportError as e:
    print("❌ Ошибка импорта BASE_DIR из config.settings.base")
    print("ℹ️ Убедитесь, что запускаете скрипт из директории moloshop или moloshop/assets")
    raise e

print("🔧 Запускаем компиляцию SCSS → CSS...\n")

apps_dir = BASE_DIR / 'apps'
core_partials_path = BASE_DIR / 'apps/core/static/core/scss/partials'  # Путь к глобальным partials

for app_path in apps_dir.iterdir():
    if not app_path.is_dir():
        continue

    app_name = app_path.name
    app_static_dir = app_path / 'static' / app_name
    scss_dir = app_static_dir / 'scss'
    css_dir = app_static_dir / 'css'

    # Создаём директории, если не существуют
    if not scss_dir.exists():
        scss_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 [created] {scss_dir}")

    if not css_dir.exists():
        css_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 [created] {css_dir}")

    # Для core компилируем два файла-точки входа
    if app_name == 'core':
        files_to_compile = {
            'global_core.scss': 'global_core.css',
            'core.scss': 'core.css',
        }

        for scss_filename, css_filename in files_to_compile.items():
            scss_path = scss_dir / scss_filename
            css_path = css_dir / css_filename

            if not scss_path.exists():
                print(f"❌ [core] Не найден SCSS-файл {scss_filename}, пропускаем компиляцию.")
                continue

            try:
                compiled_css = sass.compile(
                    filename=str(scss_path),
                    output_style='compressed',
                    include_paths=[str(scss_dir), str(core_partials_path)]  # Добавлен core_partials для глобальных partials
                )
                css_path.write_text(compiled_css, encoding='utf-8')
                print(f"✅ [core] {scss_filename} → {css_filename}")
            except sass.CompileError as e:
                print(f"❌ [core] Ошибка компиляции {scss_filename}: {e}")

    else:
        # Для остальных приложений — классика: один SCSS → один CSS
        scss_file = scss_dir / f'{app_name}.scss'
        css_file = css_dir / f'{app_name}.css'

        # Создаём заглушку, если файла нет
        if not scss_file.exists():
            scss_file.write_text(
                f"// SCSS для приложения {app_name}\n\nbody {{\n  // background-color: #f9f9f9;\n}}\n",
                encoding='utf-8'
            )
            print(f"📝 [created] {scss_file.name}")

        try:
            compiled_css = sass.compile(
                filename=str(scss_file),
                output_style='compressed',
                include_paths=[str(scss_dir), str(core_partials_path)]  # Добавляем core_partials, чтобы были доступны глобальные partials
            )
            css_file.write_text(compiled_css, encoding='utf-8')
            print(f"✅ [{app_name}] {scss_file.name} → {css_file.name}")
        except sass.CompileError as e:
            print(f"❌ [{app_name}] Ошибка компиляции: {e}")

print("\n🎉 Компиляция завершена.")
