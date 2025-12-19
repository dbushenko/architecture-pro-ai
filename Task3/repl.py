#!/usr/bin/env python3

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class RAGBot:
    def __init__(self):
        """Инициализация RAG-бота с загрузкой векторного индекса."""
        # Проверяем существование векторного хранилища
        if not os.path.exists("./vector_store/index.faiss"):
            raise FileNotFoundError(
                "Векторное хранилище не найдено. Запустите сначала build_index.py"
            )
        
        # Инициализируем модель эмбеддингов
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Загружаем векторное хранилище
        self.vector_store = FAISS.load_local(
            "./vector_store",
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        print("RAG-бот успешно инициализирован!")
        print(f"Загружен индекс с {self.vector_store.index.ntotal} векторами.")
        
    def get_answer(self, question, k=3):
        """
        Получить ответ на вопрос, используя семантический поиск.
        
        Args:
            question (str): Вопрос пользователя
            k (int): Количество релевантных документов для поиска
            
        Returns:
            str: Ответ на вопрос
        """
        # Поиск релевантных документов
        docs = self.vector_store.similarity_search(question, k=k)
        
        # Формируем ответ на основе найденных документов
        result = f"Ответ на вопрос: '{question}'\n\n"
        result += f"Найдено {len(docs)} релевантных документов:\n\n"
        
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Неизвестный источник')
            content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            result += f"{i}. Из источника: {os.path.basename(source)}\n"
            result += f"   Фрагмент: {content_preview}\n\n"
            
        return result.strip()
        

def main():
    """Основная функция REPL-интерфейса."""
    print("Привет! Это RAG-бот, задайте свой вопрос.")
    
    try:
        # Создаем экземпляр RAG-бота
        bot = RAGBot()
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        return
    
    while True:
        try:
            # Запрашиваем вопрос у пользователя
            question = input("Введите ваш вопрос: ").strip()
            
            # Проверяем команды выхода
            if question.lower() in ['quit', 'exit', 'выйти', 'q']:
                print("До свидания!")
                break
                
            # Пропускаем пустые вопросы
            if not question:
                continue
                
            # Получаем ответ от бота
            answer = bot.get_answer(question)
            print(answer)
            print("-" * 50)  # Разделитель между вопросами
            
        except KeyboardInterrupt:
            print("\n\nДо свидания!")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()