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
        
        # Проверяем, существует ли уже JSON файл
        if not os.path.exists(json_path):
            # Если JSON файла нет, создаем новый и записываем данные
            template_content["name"] = filename.replace(".vpk", "")  # Вставляем имя файла без расширения
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(template_content, json_file, ensure_ascii=False, indent=4)

print("JSON файлы созданы для всех .vpk файлов, которые еще не имеют соответствующего JSON.")