#!/bin/bash

# Функция для замены имен в файле
replace_names_in_file() {
    local input_file="$1"
    local output_file="$2"

    # Копируем оригинальный файл
    cp "$input_file" "$output_file"

    # Читаем JSON файл и извлекаем пары "ключ": "значение"
    # Используем более точный способ парсинга JSON
    python3 -c "
import json
import re
import sys

# Читаем файлы
with open('names.json', 'r', encoding='utf-8') as f:
    name_mapping = json.load(f)

# Получаем пути к файлам из аргументов
input_file = sys.argv[1]
output_file = sys.argv[2]

# Читаем содержимое файла
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем имена (отсортированные по длине, чтобы избежать частичных совпадений)
sorted_names = sorted(name_mapping.keys(), key=len, reverse=True)
for original_name in sorted_names:
    new_name = name_mapping[original_name]
    # Экранируем специальные символы для регулярного выражения
    escaped_original = re.escape(original_name)
    content = re.sub(escaped_original, new_name, content)

# Записываем изменённое содержимое в новый файл
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)
" "$input_file" "$output_file"
}

# Получаем список всех .txt файлов, кроме names_2.txt, names.json и файлов с суффиксами _1, _2
for file in *.txt; do
    if [[ "$file" != "names_2.txt" && "$file" != "names.json" && "$file" != "names.txt" && "$file" != *_1.txt && "$file" != *_2.txt ]]; then
        echo "Обработка файла: $file"
        output_file="${file%.txt}_2.txt"
        replace_names_in_file "$file" "$output_file"
        echo "Создан файл: $output_file"
    fi
done

echo "Все файлы с замененными именами созданы!"