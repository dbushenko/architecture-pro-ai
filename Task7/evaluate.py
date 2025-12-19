#!/usr/bin/env python3
"""
Скрипт для оценки производительности RAG-бота
Сравнивает результаты с эталонными ответами из golden-answers.jsonl
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from statistics import mean


def extract_questions_from_golden_answers(golden_answers_file):
    """
    Извлечение вопросов из эталонного файла
    """
    questions = []
    with open(golden_answers_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    log_entry = json.loads(line)
                    # Извлекаем вопрос из поля message, так как в golden-answers.jsonl
                    # формат отличается от обычного
                    message_data = json.loads(log_entry['message'])
                    question = message_data['question']
                    # Убираем префикс "Вопрос: " из строки
                    if question.startswith('Вопрос: '):
                        question = question[8:]  # 8 - длина строки "Вопрос: "
                    questions.append(question)
                except json.JSONDecodeError as e:
                    print(f"Ошибка при разборе JSON в строке: {line}, ошибка: {e}")
                    continue
    return questions


def run_bot_with_questions(questions, output_file):
    """
    Запуск бота с заданными вопросами и запись результатов в лог
    """
    # Удаляем старый файл логов, если он существует
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Создаем временный файл с вопросами
    temp_questions_file = "temp_questions.txt"
    with open(temp_questions_file, 'w', encoding='utf-8') as f:
        for question in questions:
            f.write(question + '\n')
    
    try:
        # Используем python из виртуального окружения
        python_path = os.path.abspath("../../.venv/bin/python")
        if not os.path.exists(python_path):
            # Если не находим python в стандартном месте, пробуем использовать текущий интерпретатор
            python_path = sys.executable

        # Запускаем бота с файлом вопросов
        cmd = [python_path, "rag_bot.py", temp_questions_file]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd='.')  # 10 минут таймаут

        if result.returncode != 0:
            print(f"Ошибка при запуске бота: {result.stderr}")
            print(f"Вывод бота: {result.stdout}")
            return False

        print("Бот успешно завершил обработку вопросов.")
        return True

    except subprocess.TimeoutExpired:
        print("Таймаут при выполнении бота")
        return False
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        return False
    finally:
        # Удаляем временный файл с вопросами
        if os.path.exists(temp_questions_file):
            os.remove(temp_questions_file)


def load_logs_from_jsonl(log_file):
    """
    Загрузка логов из файла в формате JSONL
    """
    logs = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    log_entry = json.loads(line)
                    logs.append(log_entry)
                except json.JSONDecodeError as e:
                    print(f"Ошибка при разборе JSON в строке: {line}, ошибка: {e}")
                    continue
    return logs


def extract_message_data_from_logs(logs):
    """
    Извлечение данных из поля message для логов бота
    """
    results = []
    for log_entry in logs:
        if 'message' in log_entry:
            try:
                message_data = json.loads(log_entry['message'])
                results.append(message_data)
            except json.JSONDecodeError as e:
                print(f"Ошибка при разборе message в логе: {log_entry}, ошибка: {e}")
                continue
    return results


def calculate_similarity(current_results, golden_results):
    """
    Вычисление схожести между текущими и эталонными результатами
    """
    if len(current_results) != len(golden_results):
        print(f"Предупреждение: количество результатов не совпадает. Текущие: {len(current_results)}, эталонные: {len(golden_results)}")

    similarities = {
        'chunks_found_similarity': [],
        'successful_answer_similarity': [],
        'knows_answer_similarity': [],
        'completeness_indicator_diff': []
    }

    # Создаем словари, нормализуя вопросы (убирая префиксы)
    def normalize_question(q):
        # Убираем префикс "Вопрос: ", если он есть
        if q.startswith('Вопрос: '):
            return q[8:]  # 8 - длина строки "Вопрос: "
        return q

    current_by_question = {normalize_question(item['question']): item for item in current_results}
    golden_by_question = {normalize_question(item['question']): item for item in golden_results}

    # Для вопросов, которые есть в обеих коллекциях
    common_questions = set(current_by_question.keys()) & set(golden_by_question.keys())

    for question in common_questions:
        curr = current_by_question[question]
        gold = golden_by_question[question]

        # Сравниваем chunks_found
        similarities['chunks_found_similarity'].append(1 if curr['chunks_found'] == gold['chunks_found'] else 0)

        # Сравниваем successful_answer
        similarities['successful_answer_similarity'].append(1 if curr['successful_answer'] == gold['successful_answer'] else 0)

        # Сравниваем knows_answer
        similarities['knows_answer_similarity'].append(1 if curr['knows_answer'] == gold['knows_answer'] else 0)

        # Сравниваем completeness_indicator (разница)
        diff = abs(curr['completeness_indicator'] - gold['completeness_indicator'])
        similarities['completeness_indicator_diff'].append(diff)

    # Вычисляем средние значения
    avg_chunks_found_similarity = mean(similarities['chunks_found_similarity']) if similarities['chunks_found_similarity'] else 0
    avg_successful_answer_similarity = mean(similarities['successful_answer_similarity']) if similarities['successful_answer_similarity'] else 0
    avg_knows_answer_similarity = mean(similarities['knows_answer_similarity']) if similarities['knows_answer_similarity'] else 0
    avg_completeness_diff = mean(similarities['completeness_indicator_diff']) if similarities['completeness_indicator_diff'] else float('inf')

    return {
        'avg_chunks_found_similarity': avg_chunks_found_similarity,
        'avg_successful_answer_similarity': avg_successful_answer_similarity,
        'avg_knows_answer_similarity': avg_knows_answer_similarity,
        'avg_completeness_diff': avg_completeness_diff,
        'total_matching_questions': len(common_questions),
        'current_total_questions': len(current_results),
        'golden_total_questions': len(golden_results)
    }


def generate_report(similarity_results, current_results, golden_results, output_file):
    """
    Генерация отчета о тестировании
    """
    report = []
    report.append("=" * 80)
    report.append("ОТЧЕТ О ТЕСТИРОВАНИИ RAG-БОТА")
    report.append("=" * 80)
    report.append(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    report.append("СТАТИСТИКА СРАВНЕНИЯ:")
    report.append(f"- Совпадение по нахождению чанков:      {similarity_results['avg_chunks_found_similarity']:.2%}")
    report.append(f"- Совпадение по успешности ответа:      {similarity_results['avg_successful_answer_similarity']:.2%}")
    report.append(f"- Совпадение по знанию ответа:           {similarity_results['avg_knows_answer_similarity']:.2%}")
    report.append(f"- Средняя разница в индикаторе полноты: {similarity_results['avg_completeness_diff']:.4f}")
    report.append("")
    
    report.append(f"Обработано совпадающих вопросов: {similarity_results['total_matching_questions']}")
    report.append(f"Всего текущих результатов:      {similarity_results['current_total_questions']}")
    report.append(f"Всего эталонных результатов:    {similarity_results['golden_total_questions']}")
    report.append("")
    
    # Детальный анализ по каждому вопросу
    report.append("ДЕТАЛЬНОЕ СРАВНЕНИЕ:")
    report.append("-" * 80)

    # Создаем словари, нормализуя вопросы (убирая префиксы)
    def normalize_question(q):
        # Убираем префикс "Вопрос: ", если он есть
        if q.startswith('Вопрос: '):
            return q[8:]  # 8 - длина строки "Вопрос: "
        return q

    # Нормализуем для сопоставления
    current_by_normalized = {normalize_question(item['question']): item for item in current_results}
    golden_by_normalized = {normalize_question(item['question']): item for item in golden_results}

    # Получаем список нормализованных вопросов, которые есть в обоих наборах
    common_questions = sorted(set(current_by_normalized.keys()) & set(golden_by_normalized.keys()))

    for question in common_questions:
        curr = current_by_normalized[question]
        gold = golden_by_normalized[question]

        # Показываем оригинальный вопрос (без префикса, как в текущей нормализации)
        report.append(f"Вопрос: {question}")
        report.append(f"  Наши результаты:     chunks_found={curr['chunks_found']}, successful_answer={curr['successful_answer']}, knows_answer={curr['knows_answer']}, completeness={curr['completeness_indicator']:.3f}")
        report.append(f"  Эталонные результаты: chunks_found={gold['chunks_found']}, successful_answer={gold['successful_answer']}, knows_answer={gold['knows_answer']}, completeness={gold['completeness_indicator']:.3f}")

        # Определяем, насколько близки результаты
        chunks_match = "✓" if curr['chunks_found'] == gold['chunks_found'] else "✗"
        success_match = "✓" if curr['successful_answer'] == gold['successful_answer'] else "✗"
        knows_match = "✓" if curr['knows_answer'] == gold['knows_answer'] else "✗"
        completeness_diff = abs(curr['completeness_indicator'] - gold['completeness_indicator'])
        completeness_match = "✓" if completeness_diff < 0.1 else "✗"  # разница менее 0.1 считается приемлемой

        report.append(f"  Совпадения: [{chunks_match}] chunks_found, [{success_match}] successful_answer, [{knows_match}] knows_answer, [{completeness_match}] completeness")
        report.append("")
    
    report.append("=" * 80)
    
    # Объединяем все строки в один текст
    report_text = '\n'.join(report)
    
    # Выводим в консоль
    print(report_text)
    
    # Записываем в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\nОтчет сохранен в файл: {output_file}")


def main():
    # Файлы
    golden_answers_file = "golden-answers.jsonl"
    log_file = "logs.jsonl"
    report_file = "evaluation_report.txt"
    
    print("Запуск оценки производительности RAG-бота...")
    
    # Извлекаем вопросы из эталонного файла
    print("Извлечение вопросов из эталонного файла...")
    questions = extract_questions_from_golden_answers(golden_answers_file)
    
    if not questions:
        print(f"Не удалось извлечь вопросы из {golden_answers_file}")
        return
    
    print(f"Найдено {len(questions)} вопросов для тестирования")
    
    # Запускаем бота с вопросами
    print("Запуск бота с тестовыми вопросами...")
    success = run_bot_with_questions(questions, log_file)
    
    if not success:
        print("Не удалось запустить бота")
        return
    
    # Ждем немного, чтобы лог-файл успел создаться
    time.sleep(1)
    
    if not os.path.exists(log_file):
        print(f"Файл логов {log_file} не был создан")
        return
    
    # Загружаем текущие результаты
    print("Загрузка текущих результатов из лога...")
    current_logs = load_logs_from_jsonl(log_file)
    current_results = extract_message_data_from_logs(current_logs)
    
    # Загружаем эталонные результаты
    print("Загрузка эталонных результатов...")
    golden_logs = load_logs_from_jsonl(golden_answers_file)
    golden_results = []
    for log_entry in golden_logs:
        if 'message' in log_entry:
            try:
                message_data = json.loads(log_entry['message'])
                golden_results.append(message_data)
            except json.JSONDecodeError:
                continue
    
    if not current_results:
        print("Текущие результаты пусты")
        return
    
    if not golden_results:
        print("Эталонные результаты пусты")
        return
    
    # Вычисляем схожесть
    print("Вычисление схожести результатов...")
    similarity_results = calculate_similarity(current_results, golden_results)
    
    # Генерируем отчет
    print("Генерация отчета...")
    generate_report(similarity_results, current_results, golden_results, report_file)
    
    print("\nОценка завершена!")


if __name__ == "__main__":
    main()