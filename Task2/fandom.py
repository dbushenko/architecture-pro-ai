#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import urllib.request
import urllib.parse
import os
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup


def download_file(url, output_path=None):
    """
    Скачивает HTML по указанному URL, извлекает текст из div с классом
    'mw-content-ltr mw-parser-output' и сохраняет только чистый текст.

    Args:
        url (str): URL для скачивания
        output_path (str, optional): Путь для сохранения файла.
                                    Если не указан, файл сохраняется в текущую директорию
                                    с именем, основанным на URL.

    Returns:
        str: Путь к скачанному файлу или None в случае ошибки
    """
    try:
        # Открываем URL
        response = urllib.request.urlopen(url)
        html_content = response.read().decode('utf-8')  # Декодируем в строку

        # Парсим HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Удаляем portable-infobox элементы, так как они не нужны
        for infobox in soup.find_all('div', class_='portable-infobox'):
            infobox.decompose()

        # Удаляем div с id='toc' (таблица содержания), так как он не нужен
        for toc in soup.find_all('div', id='toc'):
            toc.decompose()

        # Удаляем div элементы с классом 'noprint', так как они не нужны
        for noprint in soup.find_all('div', class_='noprint'):
            noprint.decompose()

        # Удаляем div элементы с классом 'mobile-hide', так как они не нужны
        for mobile_hide in soup.find_all('div', class_='mobile-hide'):
            mobile_hide.decompose()

        # Находим div с классом 'mw-body-content'
        content_div = soup.find('div', class_='mw-body-content')

        # Если div не найден, пытаемся найти другие возможные варианты
        if not content_div:
            content_div = soup.find('div', class_='mw-parser-output')
        if not content_div:
            content_div = soup.find('div', class_='content')

        # Если div найден, удаляем контент после h2 с span id='Appearances'
        if content_div:
            # Ищем h2, содержащий span с id='Appearances'
            appearances_header = content_div.find('h2', recursive=True)
            if appearances_header:
                span_appearances = appearances_header.find('span', id='Appearances')
                if span_appearances:
                    # Нашли h2 с span id='Appearances', удаляем все элементы после него
                    next_sibling = appearances_header.next_sibling
                    while next_sibling:
                        next_next_sibling = next_sibling.next_sibling if next_sibling else None
                        if next_sibling.name:  # Это тег, а не текст
                            next_sibling.decompose()
                        next_sibling = next_next_sibling

        # Извлекаем чистый текст из найденного div'а
        if content_div:
            text_content = content_div.get_text(strip=True, separator='\n')
        else:
            # Если div не найден, извлекаем весь текст со страницы (кроме infobox, toc, noprint и mobile-hide)
            text_content = soup.get_text(strip=True, separator='\n')

        # Определяем имя файла, если output_path не задан
        if output_path is None:
            parsed_url = urllib.parse.urlparse(url)
            filename = os.path.basename(parsed_url.path)

            # Если имя файла пустое, используем уникальное имя на основе полного URL
            if not filename:
                # Создаем имя файла на основе домена и пути, убирая недопустимые символы
                safe_url = parsed_url.netloc + parsed_url.path.replace('/', '_')
                filename = "".join(c for c in safe_url if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
            else:
                # Убираем недопустимые символы из базового имени файла
                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()

            # Заменяем расширение на .txt
            if '.' in filename:
                name, ext = os.path.splitext(filename)
                filename = name + '.txt'
            else:
                filename = filename + '.txt'

            output_path = filename or "downloaded_file.txt"

        # Создаем директорию, если она не существует
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Записываем чистый текст в файл
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)

        print(f"Текст успешно извлечен и сохранен: {output_path}")
        return output_path

    except HTTPError as e:
        print(f"Ошибка HTTP: {e.code} - {e.reason}")
        return None
    except URLError as e:
        print(f"Ошибка URL: {e.reason}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def main():
    """Главная функция для обработки аргументов командной строки и запуска скачивания."""
    parser = argparse.ArgumentParser(description='Скачивает файл по указанному URL')
    parser.add_argument('url', help='URL для скачивания')
    parser.add_argument('-o', '--output', help='Путь для сохранения файла')
    
    args = parser.parse_args()
    
    # Скачиваем файл
    download_file(args.url, args.output)


if __name__ == '__main__':
    main()
