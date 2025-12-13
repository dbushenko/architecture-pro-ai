import re
import os
import random

def extract_names_from_text(text):
    """Извлекает потенциальные имена и названия из текста"""
    # Паттерн для поиска имен и названий (начинаются с заглавной буквы)
    # Учитываем фамилии с разделителями, а также составные имена
    pattern = r'\b[A-Z][a-z]+(?:[-\s][A-Z][a-z]+)*\b'
    matches = re.findall(pattern, text)
    
    # Отфильтруем слишком короткие слова и часто встречающиеся слова, которые не являются именами
    common_words = {'The', 'And', 'Was', 'With', 'His', 'For', 'Had', 'Not', 'Were', 'Are', 'You', 'He', 'Him', 'She', 'Her', 'They', 'Them', 'We', 'Us', 'It', 'Its', 'This', 'That', 'These', 'Those', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Of', 'In', 'On', 'At', 'To', 'From', 'By', 'About', 'As', 'Into', 'Through', 'During', 'Before', 'After', 'Above', 'Below', 'Up', 'Down', 'Out', 'Off', 'Over', 'Under', 'Again', 'Further', 'Then', 'Once', 'I', 'Me', 'My', 'Myself', 'Our', 'Ours', 'Ourselves', 'Your', 'Yours', 'Yourself', 'Yourselves', 'Their', 'Theirs', 'Herself', 'Himself', 'Itself', 'Who', 'Whom', 'This', 'That', 'What', 'Which', 'When', 'Where', 'Why', 'How', 'Where', 'Whether', 'Because', 'Until', 'While', 'Of', 'To', 'From', 'Up', 'About', 'Into', 'Over', 'After', 'Below', 'Off', 'Out', 'Around', 'Under', 'Again', 'Further', 'Then', 'Once'}
    
    names = set()
    for match in matches:
        # Фильтруем по длине и по общим словам
        if len(match) > 2 and match not in common_words:
            names.add(match)
    
    return names

def extract_all_names():
    """Извлекает все имена и названия из всех .txt файлов в директории"""
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt') and f != 'names.txt']
    all_names = set()
    
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            names = extract_names_from_text(content)
            all_names.update(names)
    
    return all_names

def generate_random_name(original_name):
    """Генерирует рандомное имя/название для замены"""
    # Простой метод: переставляем буквы или создаем фантастическое имя
    parts = original_name.split()
    new_parts = []
    
    for part in parts:
        if len(part) <= 2:
            # Для коротких частей используем фиксированные замены
            replacement = {
                'A': 'Zy', 'B': 'Xo', 'C': 'Wu', 'D': 'Vr', 'E': 'Tq',
                'F': 'Sp', 'G': 'No', 'H': 'Mi', 'I': 'Lk', 'J': 'Jh',
                'K': 'Ig', 'L': 'Hf', 'M': 'Ge', 'N': 'Fd', 'O': 'Ec',
                'P': 'Db', 'Q': 'Ca', 'R': 'Bz', 'S': 'Ay', 'T': 'Xx',
                'U': 'Ww', 'V': 'Vv', 'W': 'Uu', 'X': 'Tt', 'Y': 'Ss', 'Z': 'Rr'
            }.get(part.upper(), 'New')
            new_parts.append(replacement)
        elif len(part) == 3:
            # Для коротких слов: инвертируем буквы
            new_parts.append(part[::-1].capitalize())
        else:
            # Для длинных слов: перемешиваем буквы или используем префикс/суффикс
            shuffled = part[0] + ''.join(random.sample(part[1:-1], len(part[1:-1]))) + part[-1]
            new_parts.append(shuffled)
    
    return ' '.join(new_parts)

def main():
    print("Извлечение имен и названий из текстовых файлов...")
    all_names = extract_all_names()
    
    print(f"Найдено {len(all_names)} уникальных имен/названий")
    
    # Создаем файл names.txt с оригинальными и новыми именами
    with open('names.txt', 'w', encoding='utf-8') as f:
        for original_name in sorted(all_names):
            new_name = generate_random_name(original_name)
            f.write(f"{original_name} -> {new_name}\n")
    
    print("Файл names.txt создан")
    
    # Читаем содержимое names.txt для проверки
    with open('names.txt', 'r', encoding='utf-8') as f:
        name_mapping = {}
        for line in f:
            if ' -> ' in line:
                original, new = line.strip().split(' -> ')
                name_mapping[original] = new
    
    print("Создание новых файлов с замененными именами...")
    
    # Обрабатываем исходные файлы, создаем копии с суффиксом _1
    for txt_file in [f for f in os.listdir('.') if f.endswith('.txt') and f != 'names.txt']:
        with open(txt_file, 'r', encoding='utf-8') as original:
            content = original.read()
        
        # Заменяем имена (самые длинные имена заменяем первыми, чтобы избежать ошибок)
        sorted_names = sorted(name_mapping.keys(), key=len, reverse=True)
        for original_name in sorted_names:
            content = content.replace(original_name, name_mapping[original_name])
        
        # Записываем в новый файл с суффиксом _1
        new_filename = txt_file.replace('.txt', '_1.txt')
        with open(new_filename, 'w', encoding='utf-8') as new_file:
            new_file.write(content)
    
    print("Все файлы с замененными именами созданы")

if __name__ == "__main__":
    main()