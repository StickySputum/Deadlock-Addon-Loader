from tkinter import Tk, filedialog, Checkbutton, Button, Label, Radiobutton, StringVar, IntVar, Frame, Text, Scrollbar, END, DISABLED, NORMAL, PhotoImage
from app.functions import load_config, save_config, load_addon_info, copy_addons, delete_addons, replace_gameinfo
import os

# Основные настройки для темной темы
BG_COLOR = "#2E2E2E"
TEXT_COLOR = "#D3D3D3"
BUTTON_COLOR = "#444444"

class DeadlockAddonManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Addon Manager")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.icon = PhotoImage(file="images/icon.png")
        self.root.iconphoto(True, self.icon)

        # Переменные
        self.addon_checkbuttons = []
        self.deadlock_folder = StringVar(value=load_config())
        self.ref_var = StringVar(value="regular")

        # Инициализация GUI
        self.setup_gui()

    def setup_gui(self):
        # Верхняя панель с кнопками
        top_frame = Frame(self.root, bg=BG_COLOR)
        top_frame.pack(pady=10, padx=10, fill="x")

        Button(top_frame, text="Выбрать папку Deadlock", command=self.select_deadlock_folder, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=5)
        self.delete_button = Button(top_frame, text="Удалить выбранные аддоны", command=self.delete_selected_addons, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.delete_button.grid(row=0, column=1, padx=5)
        self.add_button = Button(top_frame, text="Добавить аддоны в целевую папку", command=self.add_selected_addons, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.add_button.grid(row=0, column=2, padx=5)

        if not self.deadlock_folder.get():
            self.update_buttons_state(DISABLED)

        # Панель для выбора gameinfo
        gameinfo_frame = Frame(self.root, bg=BG_COLOR)
        gameinfo_frame.pack(pady=5, padx=10, fill="x")

        Label(gameinfo_frame, text="Выберите тип 'gameinfo.gi':", bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w")
        Radiobutton(gameinfo_frame, text="Обычный", variable=self.ref_var, value="regular", bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, sticky="w")
        Radiobutton(gameinfo_frame, text="Модифицированный", variable=self.ref_var, value="modded", bg=BG_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, sticky="w")

        Button(gameinfo_frame, text="Заменить gameinfo.gi", command=self.replace_gameinfo, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=1, column=1, padx=10)

        # Панель для отображения аддонов
        self.addons_frame = Frame(self.root, bg=BG_COLOR)
        self.addons_frame.pack(pady=5, padx=10, fill="both")

        # Панель для логов
        Label(self.root, text="Логи действий:", bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 0))
        log_text_frame = Frame(self.root, bg=BG_COLOR)
        log_text_frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.log_text = Text(log_text_frame, wrap="word", state=DISABLED, bg="#333333", fg=TEXT_COLOR, height=15)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar = Scrollbar(log_text_frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        Button(self.root, text="Очистить логи", command=self.clear_log, bg=BUTTON_COLOR, fg=TEXT_COLOR).pack(pady=(5, 10))

        # Отображение аддонов
        self.show_addons()

    def log_message(self, message):
        self.log_text.config(state=NORMAL)
        self.log_text.insert(END, message + "\n")
        self.log_text.config(state=DISABLED)
        self.log_text.see(END)

    def clear_log(self):
        self.log_text.config(state=NORMAL)
        self.log_text.delete(1.0, END)
        self.log_text.config(state=DISABLED)

    def update_buttons_state(self, state):
        self.delete_button.config(state=state)
        self.add_button.config(state=state)

    def select_deadlock_folder(self):
        folder = filedialog.askdirectory(title="Выберите папку Deadlock")
        if folder:
            self.deadlock_folder.set(folder)
            save_config(folder)
            self.update_buttons_state(NORMAL)
            self.log_message(f"Папка Deadlock выбрана: {folder}")
            self.show_addons()

    def show_addons(self):
        # Очистка старых виджетов
        for widget in self.addons_frame.winfo_children():
            widget.destroy()

        # Список аддонов и переменные
        self.addon_checkbuttons.clear()
        addon_files = [f for f in os.listdir("addons") if f.endswith('.vpk')]

        for addon in addon_files:
            name, description = load_addon_info(addon)
            is_present = False
            if self.deadlock_folder.get():
                addons_folder = os.path.join(self.deadlock_folder.get(), "game", "citadel", "addons")
                target_addon_path = os.path.join(addons_folder, addon)
                is_present = os.path.exists(target_addon_path)

            checkbox_var = IntVar(value=1 if is_present else 0)
            self.addon_checkbuttons.append((addon, checkbox_var))

            display_text = f"{name} - {description}"
            checkbox = Checkbutton(self.addons_frame, text=display_text, variable=checkbox_var, bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR)
            if not self.deadlock_folder.get():
                checkbox.config(state=DISABLED)
            checkbox.pack(anchor="w", pady=2, padx=5)

    def delete_selected_addons(self):
        if not self.deadlock_folder.get():
            self.log_message("Ошибка: Путь к папке Deadlock не задан.")
            return

        addons_folder = os.path.join(self.deadlock_folder.get(), "game", "citadel", "addons")
        selected_addons = [addon for addon, var in self.addon_checkbuttons if var.get() == 1]

        if not selected_addons:
            self.log_message("Ошибка: Выберите хотя бы один аддон для удаления.")
            return

        delete_addons(selected_addons, addons_folder)
        for addon in selected_addons:
            self.log_message(f"Аддон '{addon}' удален из целевой папки.")
        self.show_addons()

    def add_selected_addons(self):
        if not self.deadlock_folder.get():
            self.log_message("Ошибка: Путь к папке Deadlock не задан.")
            return

        addons_folder = os.path.join(self.deadlock_folder.get(), "game", "citadel", "addons")
        selected_addons = [addon for addon, var in self.addon_checkbuttons if var.get() == 1]

        if not selected_addons:
            self.log_message("Ошибка: Выберите хотя бы один аддон для копирования.")
            return

        copy_addons(selected_addons, addons_folder)
        for addon in selected_addons:
            self.log_message(f"Аддон '{addon}' добавлен в целевую папку.")
        self.show_addons()

    def replace_gameinfo(self):
        if not self.deadlock_folder.get():
            self.log_message("Ошибка: Путь к папке Deadlock не задан.")
            return

        replace_gameinfo(self.deadlock_folder.get(), self.ref_var.get())
        self.log_message("Файл 'gameinfo.gi' успешно заменен.")
