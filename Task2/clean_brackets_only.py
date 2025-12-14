#!/usr/bin/env python3
"""
Скрипт для удаления только квадратных скобок и их содержимого из всех файлов в Task2/knowledge_base/**
"""
import os
import re
from pathlib import Path


def clean_text_only_brackets(text):
    """
    Удаляет только квадратные скобки и их содержимое, не удаляя одиночные строки
    
    Args:
        text (str): Входной текст
        
    Returns:
        str: Очищенный текст
    """
    # Удаляем квадратные скобки и всё их содержимое (включая многострочные)
    # Используем DOTALL флаг, чтобы . соответствовал символу новой строки
    text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)
    
    # Убираем лишние последовательности пустых строк
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Заменяем множественные пустые строки на одну
    text = re.sub(r'\n{3,}', '\n\n', text)  # Убираем более 2 пустых строк подряд
    
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
        
        cleaned_content = clean_text_only_brackets(original_content)
        
        # Сохраняем изменения, если контент изменился
        if original_content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            print(f"Обработан файл: {file_path.name} (квадратные скобки удалены)")
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