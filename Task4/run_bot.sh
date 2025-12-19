#!/bin/bash
# Скрипт для запуска Hugging Face RAG-бота с использованием онлайн-модели Qwen через API для генерации ответов

cd "$(dirname "$0")"
source ../.venv/bin/activate
python rag_bot_qwen_api.py