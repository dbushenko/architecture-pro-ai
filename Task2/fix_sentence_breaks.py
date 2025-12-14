#!/usr/bin/env python3
"""
Скрипт для объединения разбитых предложений, удаляя лишние символы новой строки
из всех файлов в Task2/knowledge_base/**
"""
import os
import re
from pathlib import Path


def fix_sentence_breaks(text):
    """
    Исправляет разбитые предложения, объединяя строки внутри предложений
    и оставляя разрывы между абзацами
    
    Args:
        text (str): Входной текст
        
    Returns:
        str: Текст с исправленными разрывами строк
    """
    lines = text.split('\n')
    result_lines = []
    current_paragraph = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # Если строка пустая, значит, это конец абзаца
        if not stripped_line:
            # Добавляем текущий абзац к результату
            if current_paragraph:
                paragraph = ' '.join(current_paragraph)
                result_lines.append(paragraph)
                current_paragraph = []
            # Добавляем пустую строку как разделитель абзацев
            result_lines.append('')
        else:
            # Проверяем, заканчивается ли строка знаком препинания, 
            # который обычно завершает предложение
            ends_with_sentence_end = re.search(r'[.!?。！？、]$', stripped_line)
            
            # Если строка заканчивается на предложение, добавляем в абзац и завершаем
            if ends_with_sentence_end:
                current_paragraph.append(stripped_line)
                paragraph = ' '.join(current_paragraph)
                result_lines.append(paragraph)
                current_paragraph = []
            else:
                # Иначе, это, скорее всего, часть предложения, продолжаем накапливать
                current_paragraph.append(stripped_line)
    
    # Добавляем последний абзац, если он есть
    if current_paragraph:
        paragraph = ' '.join(current_paragraph)
        result_lines.append(paragraph)
    
    # Убираем лишние пустые строки
    result_lines = [line for i, line in enumerate(result_lines) 
                   if line != '' or (i > 0 and result_lines[i-1] != '')]
    
    # Снова добавляем одну пустую строку между абзацами
    final_lines = []
    for i, line in enumerate(result_lines):
        final_lines.append(line)
        # Если текущая строка не последняя, и текущая строка не пустая, и следующая строка не пустая,
        # и текущая строка содержит только слово/фразу, возможно заголовок
        if (i < len(result_lines) - 1 and 
            line != '' and 
            result_lines[i+1] != '' and
            not re.match(r'^[A-Z][a-z]+$', line)):  # не добавляем, если строка - заголовок
            
            # Но если следующая строка начинается с заглавной буквы и текущая не завершена предложением,
            # то это, скорее всего, абзац, продолжаем
            pass
    
    # Для простоты, просто объединим с одной пустой строкой между абзацами
    fixed_text = '\n'.join(result_lines)
    
    # Убираем лишние пробелы и окончательно форматируем
    fixed_text = re.sub(r'\n\s*\n', '\n\n', fixed_text)  # Только одна пустая строка между абзацами
    fixed_text = fixed_text.strip()
    
    return fixed_text


def fix_sentence_breaks_advanced(text):
    """
    Улучшенный вариант - объединяет строки внутри абзацев, разделяя только разные абзацы
    
    Args:
        text (str): Входной текст
        
    Returns:
        str: Текст с исправленными разрывами строк
    """
    # Заменяем последовательности непустых строк, не заканчивающихся точками, на одну строку с пробелом
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i].strip()
        
        # Если строка пустая, просто добавляем её
        if not current_line:
            result.append('')
            i += 1
            continue
        
        # Начинаем собирать абзац - ищем последовательность строк, 
        # не заканчивающихся на точку/восклицательный/вопросительный знак
        paragraph = current_line
        
        # Продолжаем добавлять следующие строки, пока не найдем строку, 
        # которая заканчивается на знак окончания предложения или пустая
        j = i + 1
        while j < len(lines):
            next_line = lines[j].strip()
            
            # Если следующая строка пустая или строка заканчивается на знак окончания предложения
            if not next_line or re.search(r'[.!?。！？。]$', paragraph):
                break
            
            # Добавляем следующую строку к абзацу
            if next_line:
                paragraph += ' ' + next_line
            j += 1
        
        result.append(paragraph)
        
        # Если следующая строка была пуста, добавляем её как разделитель абзацев
        if j < len(lines) and not lines[j].strip():
            result.append('')
            j += 1
        
        i = j
    
    # Убираем лишние пустые строки
    final_result = []
    for line in result:
        if line == '' and (not final_result or final_result[-1] == ''):
            # Пропускаем множественные пустые строки
            continue
        final_result.append(line)
    
    # Убираем лишние пробелы и возвращаем результат
    return '\n'.join(final_result).strip()


def process_file(file_path):
    """
    Обрабатывает один файл: объединяет разбитые предложения и сохраняет изменения
    
    Args:
        file_path (Path): Путь к файлу
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        
        cleaned_content = fix_sentence_breaks_advanced(original_content)
        
        # Сохраняем изменения, если контент изменился
        if original_content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            print(f"Обработан файл: {file_path.name} (разбитые предложения объединены)")
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
    print("Объединение разбитых предложений...")
    
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