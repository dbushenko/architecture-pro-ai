#!/usr/bin/env python3
"""
Скрипт для удаления отдельных строк, которые, вероятно, были внутри квадратных скобок, 
а также любые оставшиеся квадратные скобки из всех файлов в Task2/knowledge_base/**
"""
import os
import re
from pathlib import Path


def clean_text_completely(text):
    """
    Полностью очищает текст от квадратных скобок и их содержимого, 
    а также удаляет отдельные строки, которые вероятно были внутри скобок
    
    Args:
        text (str): Входной текст
        
    Returns:
        str: Очищенный текст
    """
    # Удаляем квадратные скобки и всё их содержимое (включая многострочные)
    text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)
    
    # Разбиваем на строки для дополнительной очистки
    lines = text.split('\n')
    
    # Убираем пустые строки и строки, которые состоят только из пробелов
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Пропускаем пустые строки и строки, которые, вероятно, были внутри скобок
        # Это могут быть числа, слова типа Source, и т.д.
        if stripped and not re.match(r'^[\d\W_]+$', stripped) and stripped.lower() not in ['source']:
            cleaned_lines.append(line)
        elif not stripped:
            # Добавляем только одну пустую строку вместо нескольких подряд
            if not cleaned_lines or cleaned_lines[-1] != '':
                cleaned_lines.append('')
    
    # Объединяем обратно
    text = '\n'.join(cleaned_lines)
    
    # Удаляем лишние последовательности новых строк
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Убираем лишние пробелы по краям
    text = text.strip()
    
    return text


def process_file(file_path):
    """
    Обрабатывает один файл: очищает текст и сохраняет изменения
    
    Args:
        file_path (Path): Путь к файлу
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        
        cleaned_content = clean_text_completely(original_content)
        
        # Сохраняем изменения, если контент изменился
        if original_content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            print(f"Обработан файл: {file_path.name} (полная очистка завершена)")
        else:
            print(f"Файл не изменился: {file_path.name}")
            
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path.name}: {e}")


def main():
    # Путь к директории с файлами
    knowledge_base_dir = Path("knowledge_base")
    
    if not knowledge_base_dir.exists():
        print(f"Директория {knowledge_base_dir} не существует")
        return
    
    print(f"Обработка файлов в директории: {knowledge_base_dir}")
    
    # Получаем все .txt файлы рекурсивно
    txt_files = list(knowledge_base_dir.rglob("*.txt"))
    
    print(f"Найдено файлов: {len(txt_files)}")
    
    files_processed = 0
    for file_path in txt_files:
        process_file(file_path)
        files_processed += 1
    
    print(f"\nОбработка завершена. Обработано файлов: {files_processed}")


if __name__ == "__main__":
    main()