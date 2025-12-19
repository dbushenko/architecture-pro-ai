#!/usr/bin/env python3
import json
import re
import os

def replace_names_in_file(input_file, output_file, name_mapping):
    """Заменяет имена в файле согласно заданному соответствию"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Сортируем ключи по длине в убывающем порядке, чтобы избежать частичных совпадений
    # (например, чтобы "Anakin Skywalker" заменилось до "Anakin")
    sorted_keys = sorted(name_mapping.keys(), key=len, reverse=True)
    
    for original_name in sorted_keys:
        new_name = name_mapping[original_name]
        # Используем re.escape для безопасной замены
        content = re.sub(re.escape(original_name), new_name, content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Читаем соответствие имен из JSON-файла
    with open('names.json', 'r', encoding='utf-8') as f:
        name_mapping = json.load(f)

    # Обрабатываем только оригинальные текстовые файлы (без _1, _2, и служебных файлов)
    txt_files = []
    for f in os.listdir('.'):
        if f.endswith('.txt') and not f.endswith('_1.txt') and not f.endswith('_2.txt') and f not in ['names.txt', 'names_2.txt', 'names.json']:
            txt_files.append(f)

    for txt_file in txt_files:
        output_file = txt_file.replace('.txt', '_2.txt')
        print(f"Обработка файла: {txt_file}")
        replace_names_in_file(txt_file, output_file, name_mapping)
        print(f"Создан файл: {output_file}")

    print("Все файлы с замененными именами созданы!")

if __name__ == "__main__":
    main()