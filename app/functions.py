import os
import shutil
import json

# Пути к папкам
MODDED_GAMEINFO_PATH = "modded_gameinfo/gameinfo.gi"
REGULAR_GAMEINFO_PATH = "regular_gameinfo/gameinfo.gi"
ADDONS_DIR = "addons"
CONFIG_FILE = "config.json"

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
    return addon_filename, "Описание не найдено."

def copy_addons(selected_addons, target_folder):
    for addon in selected_addons:
        addon_path = os.path.join(ADDONS_DIR, addon)
        if os.path.exists(addon_path):
            shutil.copy(addon_path, target_folder)

def delete_addons(selected_addons, target_folder):
    for addon in selected_addons:
        addon_path = os.path.join(target_folder, addon)
        if os.path.exists(addon_path):
            os.remove(addon_path)

def replace_gameinfo(deadlock_folder, ref_var):
    gameinfo_path = os.path.join(deadlock_folder, "game", "citadel", "gameinfo.gi")
    reference_path = MODDED_GAMEINFO_PATH if ref_var == "modded" else REGULAR_GAMEINFO_PATH

    if os.path.exists(gameinfo_path):
        with open(gameinfo_path, 'r') as file:
            current_content = file.read()
        with open(reference_path, 'r') as ref_file:
            new_content = ref_file.read()

        if current_content != new_content:
            shutil.copy(reference_path, gameinfo_path)
    else:
        shutil.copy(reference_path, gameinfo_path)
