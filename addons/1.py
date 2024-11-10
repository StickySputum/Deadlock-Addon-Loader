import os
import json

# Путь к папке с .vpk файлами
addons_dir = "addons"

# Шаблонное содержимое для JSON файлов
template_content = {
    "name": "",
    "description": ""
}

# Проходим по всем файлам в папке addons
for filename in os.listdir(addons_dir):
    if filename.endswith(".vpk"):
        # Создаем имя для нового JSON файла
        json_filename = filename.replace(".vpk", ".json")
        json_path = os.path.join(addons_dir, json_filename)
        
        # Записываем шаблонное содержимое в JSON файл
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(template_content, json_file, ensure_ascii=False, indent=4)

print("JSON файлы созданы для всех .vpk файлов.")
