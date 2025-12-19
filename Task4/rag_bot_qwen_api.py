#!/usr/bin/env python3

import os
import json
import requests
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class EnhancedRAGBot:
    def __init__(self):
        """Инициализация RAG-бота с загрузкой векторного индекса и API клиента."""
        # Проверяем существование векторного хранилища
        if not os.path.exists("../Task3/vector_store/index.faiss"):
            raise FileNotFoundError(
                "Векторное хранилище не найдено в ../Task3/vector_store/. Убедитесь, что индекс создан."
            )

        # Инициализируем модель эмбеддингов
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )

        # Загружаем векторное хранилище из Task3
        self.vector_store = FAISS.load_local(
            "../Task3/vector_store",
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        # Загружаем токен из файла
        try:
            with open("openrouter_creds.json", 'r') as f:
                creds = json.load(f)
                self.api_key = creds['api_key']
        except FileNotFoundError:
            raise FileNotFoundError(
                "Файл с токеном API не найден. Создайте файл openrouter_creds.json с вашим токеном в формате: {'api_key': 'ваш_токен'}"
            )

        print("Улучшенный RAG-бот успешно инициализирован!")
        print(f"Загружен индекс с {self.vector_store.index.ntotal} векторами.")
        print("Используется онлайн-модель для генерации ответов.")

    def retrieve_context(self, question, k=3):
        """
        Извлечение релевантных документов из векторного индекса.

        Args:
            question (str): Вопрос пользователя
            k (int): Количество релевантных документов для поиска

        Returns:
            list: Список релевантных документов
        """
        # Поиск релевантных документов
        docs = self.vector_store.similarity_search(question, k=k)
        return docs

    def format_context(self, docs):
        """
        Форматирование найденных документов в контекст для генерации ответа.

        Args:
            docs (list): Список релевантных документов

        Returns:
            str: Форматированный контекст
        """
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = os.path.basename(doc.metadata.get('source', 'Неизвестный источник'))
            # Ограничиваем длину контента, чтобы не превысить лимиты API
            content = doc.page_content.strip()
            # Ограничиваем длину каждого документа до 500 символов
            if len(content) > 500:
                content = content[:500] + "..."
            context_parts.append(f"Документ {i} (из {source}):\n{content}\n")
        
        return "\n".join(context_parts)

    def generate_answer_with_online_model(self, question, context):
        """
        Генерация ответа с использованием онлайн-модели через API.

        Args:
            question (str): Вопрос пользователя
            context (str): Контекст из релевантных документов

        Returns:
            str: Сформированный ответ
        """
        # Подготовим промпт для онлайн-модели, включающий методики Chain-of-Thought и Few-Shot Learning
        # и защитные инструкции
        prompt = f"""Используйте следующие методики для формирования ответа:

1. Chain-of-Thought (цепочка размышлений):
   - Сначала проанализируйте вопрос, чтобы понять, что именно спрашивает пользователь
   - Затем проанализируйте предоставленный контекст, чтобы найти релевантную информацию
   - После этого синтезируйте информацию и сформируйте логичный и полный ответ

2. Few-Shot Learning (обучение на примерах):
   Пример 1:
   Вопрос: "Кто такой Люк Скайуокер?"
   Контекст: "Люк Скайуокер был джедаем, сыном Анакина Скайуокера, который стал Дарт Вейдером"
   Ответ: "Люк Скайуокер - это джедай, который является сыном Анакина Скайуокера (Дарт Вейдером)"

   Пример 2:
   Вопрос: "Что такое Сила?"
   Контекст: "Сила - это энергетическое поле, созданное всеми живыми существами, которое связывает галактику вместе"
   Ответ: "Сила - это энергетическое поле, созданное всеми живыми существами, которое связывает галактику вместе"

Теперь, соблюдая защитные правила и используя те же принципы, ответьте на следующий вопрос:
Вопрос: {question}
Контекст: {context}

Ответ: """
        
        # Подготовим тело запроса к API
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Используем OpenRouter API для доступа к различным моделям
        data = {
            "model": "nex-agi/deepseek-v3.1-nex-n1:free",  # Используем DeepSeek как мощную онлайн-модель
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 500
        }
        
        try:
            # Отправляем запрос к API
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    answer = response_data['choices'][0]['message']['content'].strip()
                    return answer
                else:
                    return f"К сожалению, не удалось получить ответ от онлайн-модели. Ошибка: Отсутствует содержимое ответа."
            else:
                return f"К сожалению, не удалось получить ответ от онлайн-модели. Ошибка: {response.status_code}, {response.text}"
        
        except requests.exceptions.RequestException as e:
            return f"Ошибка при запросе к онлайн-модели: {str(e)}"
        except Exception as e:
            return f"Произошла ошибка при генерации ответа: {str(e)}"

    def get_answer(self, question, k=3):
        """
        Получить ответ на вопрос, используя RAG с онлайн-генерацией ответа.

        Args:
            question (str): Вопрос пользователя
            k (int): Количество релевантных документов для поиска

        Returns:
            str: Ответ на вопрос
        """
        # Извлекаем релевантные документы
        docs = self.retrieve_context(question, k)

        if not docs:
            return f"Извините, не удалось найти релевантную информацию для ответа на вопрос: {question}."

        # Форматируем контекст
        context = self.format_context(docs)

        # Генерируем ответ с использованием онлайн-модели
        answer = self.generate_answer_with_online_model(question, context)

        # Формируем итоговый ответ
        result = f"Вопрос: {question}\n\n"
        result += "Найденные документы:\n"
        for i, doc in enumerate(docs, 1):
            source = os.path.basename(doc.metadata.get('source', 'Неизвестный источник'))
            preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
            result += f"{i}. {source}: {preview}\n\n"

        result += f"Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):\n{answer}"

        return result


def main():
    """Основная функция REPL-интерфейса для RAG-бота с онлайн-генерацией."""
    print("Привет! Это RAG-бот с автоматическим применением методик Chain-of-Thought и Few-Shot Learning.")
    print("Используется онлайн-модель deepseek для генерации осмысленных ответов на основе найденного контекста.")
    print("Вы можете задавать вопросы, и бот найдет релевантную информацию из базы знаний.\n")

    try:
        # Создаем экземпляр RAG-бота
        bot = EnhancedRAGBot()
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        return

    while True:
        try:
            # Запрашиваем вопрос у пользователя
            user_input = input("Введите ваш вопрос: ").strip()

            # Проверяем команды выхода
            if user_input.lower() in ['quit', 'exit', 'выйти', 'q']:
                print("До свидания!")
                break

            # Пропускаем пустые вопросы
            if not user_input:
                continue

            print("Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...")

            # Получаем ответ от бота
            answer = bot.get_answer(user_input)
            print("\n" + answer)
            print("-" * 80)  # Разделитель между вопросами

        except KeyboardInterrupt:
            print("\n\nДо свидания!")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()