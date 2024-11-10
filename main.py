import os
import shutil
import json
from tkinter import Tk, filedialog, Checkbutton, Button, Label, Radiobutton, StringVar, IntVar, Frame, DISABLED, NORMAL, Text, Scrollbar, END
from tkinter import ttk, PhotoImage

# Пути к папкам с эталонными файлами gameinfo.gi и папке addons
MODDED_GAMEINFO_PATH = "modded_gameinfo/gameinfo.gi"
REGULAR_GAMEINFO_PATH = "regular_gameinfo/gameinfo.gi"
ADDONS_DIR = "addons"
CONFIG_FILE = "config.json"  # Файл конфигурации для сохранения пути Deadlock

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("deadlock_folder", "")
    return ""

def save_config(deadlock_folder):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"deadlock_folder": deadlock_folder}, f)

def load_addon_info(addon_filename):
    json_filename = addon_filename.replace(".vpk", ".json")
    json_path = os.path.join(ADDONS_DIR, json_filename)
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data.get("name", addon_filename), data.get("description", "Нет описания.")
    else:
        return addon_filename, "Описание не найдено."

def log_message(message):
    log_text.config(state=NORMAL)
    log_text.insert(END, message + "\n")
    log_text.config(state=DISABLED)
    log_text.see(END)

def clear_log():
    log_text.config(state=NORMAL)
    log_text.delete(1.0, END)
    log_text.config(state=DISABLED)

def show_addons():
    for widget in addons_frame.winfo_children():
        widget.destroy()

    addons_folder = os.path.join(deadlock_folder.get(), "game", "citadel", "addons") if deadlock_folder.get() else None
    addon_files = [f for f in os.listdir(ADDONS_DIR) if f.endswith('.vpk')]
    addon_checkbuttons.clear()

    for addon in addon_files:
        is_present = False
        if addons_folder:
            target_addon_path = os.path.join(addons_folder, addon)
            is_present = os.path.exists(target_addon_path)

        name, description = load_addon_info(addon)
        checkbox_var = IntVar(value=1 if is_present else 0)
        addon_checkbuttons.append((addon, checkbox_var))
        
        display_text = f"{name} - {description}"
        checkbox = Checkbutton(addons_frame, text=display_text, variable=checkbox_var, bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR)
        
        if not deadlock_folder.get():
            checkbox.config(state=DISABLED)
        
        checkbox.pack(anchor="w", pady=2, padx=5)

def select_deadlock_folder():
    folder = filedialog.askdirectory(title="Выберите папку Deadlock")
    if folder:
        deadlock_folder.set(folder)
        save_config(folder)
        update_buttons_state(NORMAL)
        log_message(f"Папка Deadlock выбрана: {folder}")
        show_addons()

def delete_addons():
    if not deadlock_folder.get():
        log_message("Ошибка: Путь к папке Deadlock не задан.")
        return

    addons_folder = os.path.join(deadlock_folder.get(), "game", "citadel", "addons")
    selected_addons = [addon for addon, var in addon_checkbuttons if var.get() == 1]
    
    if not selected_addons:
        log_message("Ошибка: Выберите хотя бы один аддон для удаления.")
        return

    for addon in selected_addons:
        addon_path = os.path.join(addons_folder, addon)
        if os.path.exists(addon_path):
            os.remove(addon_path)
            log_message(f"Аддон '{addon}' удален из целевой папки.")

    show_addons()

def copy_addons_to_deadlock():
    if not deadlock_folder.get():
        log_message("Ошибка: Путь к папке Deadlock не задан.")
        return

    addons_folder = os.path.join(deadlock_folder.get(), "game", "citadel", "addons")
    selected_addons = [addon for addon, var in addon_checkbuttons if var.get() == 1]

    if not selected_addons:
        log_message("Ошибка: Выберите хотя бы один аддон для копирования.")
        return

    for addon in selected_addons:
        addon_path = os.path.join(ADDONS_DIR, addon)
        if os.path.exists(addon_path):
            shutil.copy(addon_path, addons_folder)
            log_message(f"Аддон '{addon}' добавлен в целевую папку.")

    show_addons()

def replace_gameinfo():
    if not deadlock_folder.get():
        log_message("Ошибка: Путь к папке Deadlock не задан.")
        return

    gameinfo_path = os.path.join(deadlock_folder.get(), "game", "citadel", "gameinfo.gi")
    reference_path = MODDED_GAMEINFO_PATH if ref_var.get() == "modded" else REGULAR_GAMEINFO_PATH

    if os.path.exists(gameinfo_path):
        with open(gameinfo_path, 'r') as file:
            current_content = file.read()
        with open(reference_path, 'r') as ref_file:
            new_content = ref_file.read()

        if current_content != new_content:
            shutil.copy(reference_path, gameinfo_path)
            log_message("Файл 'gameinfo.gi' заменен.")
    else:
        shutil.copy(reference_path, gameinfo_path)
        log_message("Файл 'gameinfo.gi' добавлен.")

def update_buttons_state(state):
    delete_button.config(state=state)
    add_button.config(state=state)

# Основные настройки для темной темы
BG_COLOR = "#2E2E2E"
TEXT_COLOR = "#D3D3D3"
BUTTON_COLOR = "#444444"
HIGHLIGHT_COLOR = "#007ACC"

# Создание GUI
root = Tk()
root.title("Deadlock Addon Manager")
root.configure(bg=BG_COLOR)

root.resizable(False, False)

icon = PhotoImage(file="images/icon.png")
root.iconphoto(True, icon)


# Переменные
addon_checkbuttons = []
deadlock_folder = StringVar(value=load_config())
ref_var = StringVar(value="regular")

# Фрейм для выбора папки и кнопок
top_frame = Frame(root, bg=BG_COLOR)
top_frame.pack(pady=10, padx=10, fill="x")

Button(top_frame, text="Выбрать папку Deadlock", command=select_deadlock_folder, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=5)

delete_button = Button(top_frame, text="Удалить выбранные аддоны", command=delete_addons, bg=BUTTON_COLOR, fg=TEXT_COLOR)
delete_button.grid(row=0, column=1, padx=5)
add_button = Button(top_frame, text="Добавить аддоны в целевую папку", command=copy_addons_to_deadlock, bg=BUTTON_COLOR, fg=TEXT_COLOR)
add_button.grid(row=0, column=2, padx=5)

if not deadlock_folder.get():
    update_buttons_state(DISABLED)

# Фрейм для выбора gameinfo
gameinfo_frame = Frame(root, bg=BG_COLOR)
gameinfo_frame.pack(pady=5, padx=10, fill="x")

Label(gameinfo_frame, text="Выберите тип 'gameinfo.gi':", bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w")
Radiobutton(gameinfo_frame, text="Обычный", variable=ref_var, value="regular", bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR).grid(row=1, column=0, sticky="w")
Radiobutton(gameinfo_frame, text="Модифицированный", variable=ref_var, value="modded", bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR).grid(row=2, column=0, sticky="w")

Button(gameinfo_frame, text="Заменить gameinfo.gi", command=replace_gameinfo, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=1, column=1, padx=10)

# Фрейм для отображения аддонов
addons_frame = Frame(root, bg=BG_COLOR)
addons_frame.pack(pady=5, padx=10, fill="both")

# Окно для логирования
Label(root, text="Логи действий:", bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 0))

# Увеличиваем поле логов и делаем его расширяемым
log_text_frame = Frame(root, bg=BG_COLOR)
log_text_frame.pack(pady=5, padx=10, fill="both", expand=True)

log_text = Text(log_text_frame, wrap="word", state=DISABLED, bg="#333333", fg=TEXT_COLOR, height=15)
log_text.pack(side="left", fill="both", expand=True)
scrollbar = Scrollbar(log_text_frame, command=log_text.yview)
log_text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Кнопка для очистки логов
Button(root, text="Очистить логи", command=clear_log, bg=BUTTON_COLOR, fg=TEXT_COLOR).pack(pady=(5, 10))

show_addons()
root.mainloop()
