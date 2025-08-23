
# moloshop/assets/my_scripts/generate_folder_structure.py

'''
🗂 GUI-скрипт для генерации отчёта по структуре каталогов с исключениями
'''

import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

# Предустановленные папки, содержимое которых отображаем, но скрываем (с пометкой)
DEFAULT_NAME_EXCLUSIONS = [
    ".idea", ".venv", ".git", "__pycache__", "migrations", "media"
]

def print_tree(path, abs_exclusions, name_exclusions,
               prefix="", is_last=True, output_lines=None):
    """
    Строит дерево каталогов с двумя типами исключений:
    - abs_exclusions: абсолютные пути -- полное исключение из отчёта (не выводятся)
    - name_exclusions: папки по имени -- показываются с пометкой [содержимое скрыто], содержимое не раскрывается
    """
    if output_lines is None:
        output_lines = []

    abs_path = os.path.abspath(path)
    name = os.path.basename(path)

    # Полное исключение абсолютных путей
    if abs_path in abs_exclusions:
        return output_lines

    show_only_folder = name in name_exclusions and os.path.isdir(path)
    connector = "└── " if is_last else "├── "

    if name == "":
        output_lines.append(abs_path.upper())
    else:
        output_lines.append(
            f"{prefix}{connector}{name}{' [содержимое скрыто]' if show_only_folder else ''}"
        )

    if show_only_folder:
        return output_lines

    new_prefix = prefix + ("    " if is_last else "│   ")

    try:
        entries = os.listdir(path)
    except PermissionError:
        output_lines.append(f"{new_prefix}<Недостаточно прав для {name}>")
        return output_lines

    entries = [
        e for e in entries
        if os.path.abspath(os.path.join(path, e)) not in abs_exclusions
    ]

    dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(path, e))]
    dirs.sort()
    files.sort()

    for i, file in enumerate(files):
        is_last_file = (i == len(files) - 1) and (len(dirs) == 0)
        file_connector = "└── " if is_last_file else "├── "
        output_lines.append(f"{new_prefix}{file_connector}{file}")

    for i, directory in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1)
        print_tree(
            os.path.join(path, directory),
            abs_exclusions,
            name_exclusions,
            new_prefix,
            is_last_dir,
            output_lines,
        )
    return output_lines


def generate_tree_report(base_path, abs_exclusions, name_exclusions, output_file):
    lines = print_tree(base_path, abs_exclusions, name_exclusions)
    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return lines


def launch_gui():
    def rel_path(path):
        base = base_path_var.get()
        try:
            return os.path.relpath(path, start=base)
        except Exception:
            return path

    def abs_path(path):
        base = base_path_var.get()
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(base, path))

    # Унифицированный список исключений:
    # Кортежи формата: ("abs", полный_путь) или ("name", имя_папки)
    exceptions = []

    def update_exceptions_listbox():
        exceptions_listbox.delete(0, tk.END)
        base = base_path_var.get()
        for ex_type, val in exceptions:
            if ex_type == "abs":
                try:
                    rp = os.path.relpath(val, base)
                    display_val = rp if not rp.startswith("..") else val
                except Exception:
                    display_val = val
                display = f"{display_val}  [полное исключение]"
            else:  # ex_type == "name"
                display = f"{val}  [содержимое скрыто]"
            exceptions_listbox.insert(tk.END, display)

    def select_folder():
        path = filedialog.askdirectory()
        if path:
            base_path_var.set(path)
            exceptions.clear()
            # Инициализируем с дефолтным списком папок с сокрытым содержимым (тип "name")
            for name_excl in DEFAULT_NAME_EXCLUSIONS:
                exceptions.append(("name", name_excl))
            update_exceptions_listbox()
            refresh_explorer(path)

    def add_abs_exclusion():
        base_path = base_path_var.get()
        if not base_path:
            messagebox.showwarning("Ошибка", "Сначала выберите базовую директорию.")
            return
        excl_path = filedialog.askdirectory(initialdir=base_path, title="Выберите папку для полного исключения")
        if not excl_path:
            excl_path = filedialog.askopenfilename(initialdir=base_path, title="Выберите файл для полного исключения")

        if excl_path:
            abs_p = os.path.abspath(excl_path)
            if ("abs", abs_p) not in exceptions:
                exceptions.append(("abs", abs_p))
                update_exceptions_listbox()

    def add_name_exclusion():
        val = simpledialog.askstring("Добавить имя папки", "Введите имя папки для скрытия содержимого:")
        if val:
            val = val.strip()
            if val and ("name", val) not in exceptions:
                exceptions.append(("name", val))
                update_exceptions_listbox()

    def remove_exception():
        selection = exceptions_listbox.curselection()
        if selection:
            idx = selection[0]
            exceptions.pop(idx)
            update_exceptions_listbox()

    def clear_exceptions():
        exceptions.clear()
        # Восстановим дефолтные папки с скрытым содержимым
        for name_excl in DEFAULT_NAME_EXCLUSIONS:
            exceptions.append(("name", name_excl))
        update_exceptions_listbox()

    def generate():
        base_path = base_path_var.get()
        if not base_path:
            messagebox.showwarning("Ошибка", "Выберите папку.")
            return
        output = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile="folder_structure.txt",
            title="Сохранить отчёт как...",
        )
        if not output:
            return
        abs_excl = [v for t, v in exceptions if t == "abs"]
        name_excl = [v for t, v in exceptions if t == "name"]
        lines = generate_tree_report(base_path, abs_excl, name_excl, output)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "\n".join(lines))
        messagebox.showinfo("Готово", f"Файл '{output}' создан.")

    def refresh_explorer(path):
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Выбран путь: {path}\n")

    root = tk.Tk()
    root.title("Дерево каталогов с исключениями / Папки с скрытым содержимым")
    root.geometry("950x720")

    tk.Label(root, text="Рабочая директория:").pack(anchor="w", padx=10, pady=(10, 0))
    base_path_var = tk.StringVar()
    tk.Entry(root, textvariable=base_path_var).pack(fill="x", padx=10)
    tk.Button(root, text="Выбрать папку", command=select_folder).pack(padx=10, pady=5)

    tk.Label(root, text="Исключения / Папки с скрытым содержимым:").pack(anchor="w", padx=10)
    exclusions_frame = tk.Frame(root)
    exclusions_frame.pack(fill="x", padx=10)

    exceptions_listbox = tk.Listbox(exclusions_frame, height=8, activestyle='dotbox')
    exceptions_listbox.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(exclusions_frame, orient="vertical")
    exceptions_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=exceptions_listbox.yview)
    scrollbar.pack(side="right", fill="y")

    btn_frame = tk.Frame(exclusions_frame)
    btn_frame.pack(side="left", padx=5)

    tk.Button(btn_frame, text="Добавить абсолютное исключение", command=add_abs_exclusion).pack(fill="x", pady=2)
    tk.Button(btn_frame, text="Добавить имя папки (скрыть содержимое)", command=add_name_exclusion).pack(fill="x", pady=2)
    tk.Button(btn_frame, text="Удалить выбранное", command=remove_exception).pack(fill="x", pady=2)
    tk.Button(btn_frame, text="Сбросить (по умолчанию)", command=clear_exceptions).pack(fill="x", pady=2)

    tk.Button(root, text="Создать файл отчёта", command=generate, bg="#4CAF50", fg="white").pack(pady=10)

    output_text = ScrolledText(root, height=30)
    output_text.pack(fill="both", expand=True, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    launch_gui()
