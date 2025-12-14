#!/usr/bin/env python3
"""
Скрипт для удаления паттернов вида [\nчисло\n] из текстовых файлов
"""
import os
import re
from pathlib import Path


def remove_number_patterns(text):
    """
    Удаляет паттерны вида [\nчисло\n] из текста
    
    Args:
        text (str): Входной текст
        
    Returns:
        str: Текст с удаленными паттернами
    """
    # Паттерн для поиска [\nчисло\n] где \n - это символы новой строки
    # Регулярное выражение: \[\s*\d+\s*\] - ищет [, затем возможно пробелы, затем число, затем возможно пробелы, затем ]
    pattern = r'\[\s*\d+\s*\]'
    
    # Заменяем найденные паттерны на пустую строку
    cleaned_text = re.sub(pattern, '', text)
    
    # Также удаляем лишние пустые строки, которые могут остаться
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)  # Заменяем множественные пустые строки на одну
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)  # Убираем более 2 пустых строк подряд
    
    return cleaned_text.strip()


def process_file(file_path):
    """
    Обрабатывает один файл: удаляет паттерны и сохраняет изменения
    
    Args:
        file_path (str): Путь к файлу
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        
        cleaned_content = remove_number_patterns(original_content)
        
        # Сохраняем изменения, если контент изменился
        if original_content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            print(f"Обработан файл: {file_path} (паттерны удалены)")
        else:
            print(f"Файл не изменился: {file_path}")
            
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")


def process_directory(directory_path, file_pattern="*.txt"):
    """
    Обрабатывает все файлы в директории по заданному шаблону
    
    Args:
        directory_path (str): Путь к директории
        file_pattern (str): Шаблон файлов для обработки
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Директория {directory_path} не существует")
        return
    
    files_processed = 0
    for file_path in directory.rglob(file_pattern):  # rglob для рекурсивного поиска
        if file_path.is_file():
            process_file(file_path)
            files_processed += 1
    
    print(f"\nОбработано файлов: {files_processed}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Удаление паттернов вида [число] из текстовых файлов')
    parser.add_argument('path', help='Путь к файлу или директории для обработки')
    parser.add_argument('--pattern', '-p', default='*.txt', 
                       help='Шаблон файлов для обработки (по умолчанию: *.txt)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Только показать, что будет обработано, без изменений')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file():
        if not args.dry_run:
            process_file(path)
        else:
            print(f"Будет обработан файл: {path}")
    elif path.is_dir():
        if not args.dry_run:
            process_directory(path, args.pattern)
        else:
            print(f"Будут обработаны файлы в директории: {path} по шаблону: {args.pattern}")
            for file_path in path.rglob(args.pattern):
                if file_path.is_file():
                    print(f"  - {file_path}")
    else:
        print(f"Путь {args.path} не существует")


if __name__ == "__main__":
    main()