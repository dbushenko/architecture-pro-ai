# RAG Bot с Online API

## Описание

Бот использует:
- Векторный индекс из Task3 (на базе модели all-MiniLM-L6-v2) для поиска релевантных документов
- Онлайн-модель (через OpenRouter API) для генерации осмысленных ответов
- Автоматическое применение методик улучшения качества ответов: Chain-of-Thought и Few-Shot Learning
- Структурированный подход к формированию осмысленных ответов на основе найденной информации

## Файлы проекта

- `rag_bot_qwen_api.py` - основной файл с реализацией RAG-бота с онлайн-генерацией
- `openrouter_creds.json` - файл с API-токеном для доступа к онлайн-модели

## Подготовка

Прежде чем запустить бота, вам нужно получить API-ключ от OpenRouter и сохранить его в файле `openrouter_creds.json` в формате:
```json
{
  "api_key": "ваш_openrouter_api_ключ"
}
```

## Запуск

Для запуска RAG-бота:

```bash
cd Task4
source ../.venv/bin/activate  # Активировать виртуальное окружение
python rag_bot_qwen_api.py
```

## Методы анализа

Программа автоматически применяет оба метода:
1. **Chain-of-Thought**: Анализ вопроса по шагам с логическим выводом ответа
2. **Few-Shot Learning**: Использование примеров структуры ответов для формирования подходящего ответа

## Зависимости

- langchain
- langchain-huggingface
- langchain-community
- transformers
- torch
- faiss-cpu
- requests

## Примеры диалогов с ответами

(.venv) dim@Aldan3L:~/Work/architecture-pro-ai/Task4$ python rag_bot_qwen_api.py 
Привет! Это RAG-бот с автоматическим применением методик Chain-of-Thought и Few-Shot Learning.
Используется онлайн-модель deepseek для генерации осмысленных ответов на основе найденного контекста.
Вы можете задавать вопросы, и бот найдет релевантную информацию из базы знаний.

Улучшенный RAG-бот успешно инициализирован!
Загружен индекс с 12167 векторами.
Используется онлайн-модель для генерации ответов.
Введите ваш вопрос: где живет Zephon?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: где живет Zephon?

Найденные документы:
1. Yoda_2.txt: Zephon survives the attempt on his life.

2. Yoda_2.txt: Zephon and Kantam Sy speak with Lula Talisola.

3. Yoda_2.txt: Zephon began to dream, the dream of pain, suffering, anger, hate, and suddenly, he awoke once again. Realizing the predicament he was in, Zephon began...

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Проанализировав предоставленный контекст с использованием метода Chain-of-Thought:

**Анализ вопроса:** Пользователь спрашивает о месте жительства Zephon.

**Анализ контекста:** 
- Документ 1: Упоминает, что Zephon выжил после покушения на его жизнь
- Документ 2: Описывает разговор Zephon с Kantam Sy и Lula Talisola
- Документ 3: Содержит ключевую информацию - Zephon описывает себя как "trapped on Swamp World" (запертым на Болотном Мире)

**Синтез информации:** Единственное прямое указание на местоположение Zephon в предоставленном контексте находится в Документе 3, где он описывает себя как запертого на "Swamp World" (Болотном Мире).

**Ответ:** Согласно предоставленному контексту, Zephon находится на Болотном Мире (Swamp World), где он описывает себя как "запертого" на этой планете.
--------------------------------------------------------------------------------
Введите ваш вопрос: какие основные события в жизни Mordain?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: какие основные события в жизни Mordain?

Найденные документы:
1. Luke_Skywalker_2.txt: Mordain-Fall entered a psychic duel with the Queen to force her to submit. Aphra allowed Eternal Rur from the crystal to enter his mind to assist him....

2. Luke_Skywalker_2.txt: Mordain-Fall's intructions to set a charge and instead rig the entire Spike to explode and destroy the planet. He told R2 to stop and told the Partisa...

3. Ben_Solo_2.txt: ―Kaelan Draxius, about Korrak Vex'ion Mordain-Fall had a premonition that his nephew would herald death, destruction, and the end of everything he lov...

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Проанализировав предоставленные документы, я могу выделить следующие основные события в жизни Mordain-Fall:

## Основные события в жизни Mordain-Fall:

1. **Психическая дуэль с Королевой**: Mordain-Fall вступил в психическую дуэль с Королевой, чтобы заставить ее подчиниться.

2. **Взаимодействие с Eternal Rur**: Он позволил Eternal Rur из кристалла войти в его разум, чтобы помочь в дуэли. Rur советовал ему использовать симбиота в своих интересах.

3. **Отказ от советов Rur**: Mordain-Fall понял, что Rur не является настоящим Хранителем Силы, а лишь человеком со знаниями одного из них, и проигнорировал его совет.

4. **Противодействие Партизанам**: Когда Партизаны решили взорвать всю Планету, Mordain-Fall пытался остановить их, считая это несправедливым.

5. **Имитация сдачи**: Он притворился, что сдается, в то время как R2 выпустил газ, что позволило им скрыться.

6. **Пророчество о племяннике**: Mordain-Fall имел предвидение, что его племянник принесет смерть, разрушение и конец всему, что он любил.

Эти события показывают Mordain-Fall как персонажа, который сталкивается с моральными дилеммами, обладает психическими способностями и пытается противостоять разрушительным силам.
--------------------------------------------------------------------------------
Введите ваш вопрос: какие основные характеристики персонажа Zephon?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: какие основные характеристики персонажа Zephon?

Найденные документы:
1. Yoda_2.txt: Zephon survives the attempt on his life.

2. Yoda_2.txt: of responsibility and understanding, Zephon began his journey home.

3. Yoda_2.txt: Zephon and Kantam Sy speak with Lula Talisola.

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Проанализирую вопрос и предоставленный контекст, используя метод Chain-of-Thought:

**Анализ вопроса:** Пользователь спрашивает об основных характеристиках персонажа Zephon.

**Анализ контекста:**
- Документ 1: "Zephon survives the attempt on his life" - Zephon выжил после покушения на его жизнь
- Документ 2: "of responsibility and understanding, Zephon began his journey home" - Zephon, обладая чувством ответственности и пониманием, начал свой путь домой
- Документ 3: "Zephon and Kantam Sy speak with Lula Talisola" - Zephon общается с другими персонажами

**Синтез информации:**
На основе предоставленного контекста можно выделить следующие основные характеристики персонажа Zephon:

**Основные характеристики Zephon:**

1. **Жизнестойкость и способность к выживанию** - Zephon смог пережить покушение на свою жизнь, что свидетельствует о его физической и/или психологической устойчивости

2. **Чувство ответственности** - Контекст указывает на то, что Zephon обладает развитым чувством ответственности, что является важной чертой его характера

3. **Способность к глубокому пониманию** - Zephon характеризуется как персонаж, способный к пониманию ситуаций и, возможно, других людей

4. **Социальная активность** - Zephon взаимодействует с другими персонажами (Kantam Sy и Lula Talisola), что указывает на его коммуникативные способности и вовлеченность в социальные связи

5. **Наличие цели/мотивации** - Тот факт, что он "начал свой путь домой", suggests у него есть определенная цель или мотивация, направляющая его действия

Эти характеристики основаны исключительно на предоставленных фрагментах текста из документов Yoda_2.txt.
--------------------------------------------------------------------------------
Введите ваш вопрос: в каких отношениях находятся Mordain-Fall и Kaelan Draxius?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: в каких отношениях находятся Mordain-Fall и Kaelan Draxius?

Найденные документы:
1. Luke_Skywalker_2.txt: ―Kaelan Draxius Sensing the darkness within Korrak Vex'ion, Mordain-Fall instinctively moved to strike down his nephew.

2. Ben_Solo_2.txt: ―Kaelan Draxius, about Korrak Vex'ion Mordain-Fall had a premonition that his nephew would herald death, destruction, and the end of everything he lov...

3. Luke_Skywalker_2.txt: ―Kaelan Draxius, during the operations on Er'Kit Following the attack on the Mako-Ta Space Docks , Mordain-Fall was promoted to the rank of commander.

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Давайте проанализирую вопрос и предоставленный контекст, используя цепочку размышлений:

**Анализ вопроса:**
Пользователь спрашивает о том, в каких отношениях находятся Mordain-Fall и Kaelan Draxius.

**Анализ контекста:**
- Документ 1: "Sensing the darkness within Korrak Vex'ion, Mordain-Fall instinctively moved to strike down his nephew" - здесь говорится, что Mordain-Fall хотел нанести удар по своему племяннику (Korrak Vex'ion)
- Документ 2: "Mordain-Fall had a premonition that his nephew would herald death..." - снова упоминается, что у Mordain-Fall был племянник
- Документ 3: "Following the attack on the Mako-Ta Space Docks, Mordain-Fall was promoted..." - информация о продвижении Mordain-Fall

**Синтез информации:**
На основе предоставленного контекста я не могу определить отношения между Mordain-Fall и Kaelan Draxius, так как в документах нет прямой информации об их отношениях. В текстах упоминаются:
- Mordain-Fall и его племянник Korrak Vex'ion
- Kaelan Draxius как источник цитат

Отношения между Mordain-Fall и Kaelan Draxius в предоставленных документах не описаны.

**Ответ:** На основе предоставленного контекста невозможно определить, в каких отношениях находятся Mordain-Fall и Kaelan Draxius, так как в документах нет информации об их отношениях.
--------------------------------------------------------------------------------
Введите ваш вопрос: какие родственники есть у Kaelan Draxius?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: какие родственники есть у Kaelan Draxius?

Найденные документы:
1. Ben_Solo_2.txt: ―Korrak Vex'ion, on his apprenticeship under Kaelan Draxius Soloris idolized his uncle, Kaelan Draxius, when he was a child.

2. Luke_Skywalker_2.txt: ―Kaelan Draxius, to Din Djarin Kaelan Draxius takes Grogu as his student.

3. Ben_Solo_2.txt: ―Kaelan Draxius Apart from his mother, Korrak Vex'ion became the first apprentice of his uncle Kaelan Draxius, and proved to be the most gifted studen...

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Анализирую вопрос и предоставленный контекст:

**Вопрос:** Какие родственники есть у Kaelan Draxius?

**Анализ контекста:**

Из Document 1 и Document 3 (Ben_Solo_2.txt):
- "Soloris idolized his uncle, Kaelan Draxius" - это указывает, что у Kaelan Draxius есть племянник по имени Soloris
- "Korrak Vex'ion became the first apprentice of his uncle Kaelan Draxius" - это указывает, что у Kaelan Draxius есть племянник по имени Korrak Vex'ion

**Синтез информации:**

На основе предоставленного контекста, у Kaelan Draxius есть следующие родственники:

**Ответ:** У Kaelan Draxius есть два племянника:
- Soloris (который idolized своего дядю Kaelan Draxius в детстве)
- Korrak Vex'ion (который стал первым учеником своего дяди Kaelan Draxius)

Это вся информация о родственниках Kaelan Draxius, которая содержится в предоставленных документах.
--------------------------------------------------------------------------------
Введите ваш вопрос: кто учитель у Mordain-Fall?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: кто учитель у Mordain-Fall?

Найденные документы:
1. Luke_Skywalker_2.txt: Mordain-Fall to hand her the shards of the bled Kyber crystal from Yoturba. Realizing that she was possessed by a Shadow Spawn spirit, Mordain-Fall of...

2. Qui-Gon_Jinn_2.txt: Mordain-Fall that the Council would allow him to be trained and that Kalesh would be his master. Together, the two mourned the death of their fallen f...

3. Luke_Skywalker_2.txt: Mordain-Fall tried to explain that by failing Ben he felt that he had failed the Force Warden. Zephon admonished Mordain-Fall for still "constantly lo...

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Проанализирую вопрос и предоставленный контекст, используя метод Chain-of-Thought:

**Анализ вопроса:**
Пользователь спрашивает, кто является учителем у Mordain-Fall.

**Анализ контекста:**
- Документ 1: Описывает события с Mordain-Fall, но не упоминает его учителя
- Документ 2: Содержит ключевую информацию: "the Council would allow him to be trained and that Kalesh would be his master" (Совет позволит ему пройти обучение, и Kalesh будет его мастером)
- Документ 3: Упоминает Zephon, который дает наставления Mordain-Fall, но не называется его официальным учителем/мастером

**Синтез информации:**
На основании анализа контекста, в Документе 2 прямо указано, что Kalesh будет мастером (учителем) Mordain-Fall.

**Ответ:**
Учителем Mordain-Fall является Kalesh.
--------------------------------------------------------------------------------
Введите ваш вопрос: где живет Mordain-Fall?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: где живет Mordain-Fall?

Найденные документы:
1. Luke_Skywalker_2.txt: Mordain-Fall's intructions to set a charge and instead rig the entire Spike to explode and destroy the planet. He told R2 to stop and told the Partisa...

2. Darth_Sidious_2.txt: Mordain-Fall, who had just been hailed as a hero for killing Vorthak Drel and rescuing the Multi-Eyed Traderd Arbiter, began having visions of his wif...

3. Luke_Skywalker_2.txt: home on Xerion-7. Mordain-Fall began to reflect on his fear of what the darkness would do to him psychologically, referring both to the literal situat...

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Проанализировав предоставленные документы с использованием метода Chain-of-Thought:

**Анализ вопроса:** Пользователь спрашивает о месте жительства Mordain-Fall.

**Анализ контекста:** 
- Документ 1 описывает действия Mordain-Fall с Partisans, но не упоминает его место жительства
- Документ 2 рассказывает о назначении Mordain-Fall представителем в Circle of Light, но также не содержит информации о месте жительства
- Документ 3 содержит ключевую информацию: "home on Xerion-7" (дом на Ксеррионе-7)

**Синтез информации:** Единственное упоминание о месте жительства Mordain-Fall находится в Документе 3, где указано, что его дом находится на Xerion-7.

**Ответ:** Mordain-Fall живет на планете Xerion-7.

## Примеры диалогов, когда бот не знает ответа

Введите ваш вопрос: кто учитель у Zephon?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: кто учитель у Zephon?

Найденные документы:
1. Yoda_2.txt: Zephon and Kantam Sy speak with Lula Talisola.

2. Yoda_2.txt: Zephon survives the attempt on his life.

3. Yoda_2.txt: of responsibility and understanding, Zephon began his journey home.

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Проанализировав предоставленные документы с использованием Chain-of-Thought подхода:

**Анализ вопроса**: Пользователь спрашивает, кто является учителем у Zephon.

**Анализ контекста**: В предоставленных документах (Yoda_2.txt) содержится следующая информация:
- Zephon общается с Kantam Sy и Lula Talisola
- Zephon выживает после покушения на его жизнь
- Zephon начинает свое путешествие домой

**Синтез информации**: После тщательного анализа всех трех документов, я не нахожу информации о том, кто является учителем Zephon. В предоставленном контексте отсутствуют сведения о его наставнике или учителе.

**Ответ**: На основании предоставленных документов невозможно определить, кто является учителем у Zephon, так как эта информация в контексте отсутствует.
--------------------------------------------------------------------------------
Введите ваш вопрос: как выглядит Mordain-Fall?
Ищу релевантную информацию и формирую осмысленный ответ с использованием онлайн-модели deepseek...

Вопрос: как выглядит Mordain-Fall?

Найденные документы:
1. Luke_Skywalker_2.txt: Mordain-Fall kills the Queen of Ktath'atn.

2. Qui-Gon_Jinn_2.txt: Mordain-Fall that the Council would allow him to be trained and that Kalesh would be his master. Together, the two mourned the death of their fallen f...

3. Luke_Skywalker_2.txt: Mordain-Fall to hand her the shards of the bled Kyber crystal from Yoturba. Realizing that she was possessed by a Shadow Spawn spirit, Mordain-Fall of...

Ответ (сгенерирован онлайн-моделью deepseek с автоматическим применением методов Chain-of-Thought и Few-Shot):
Анализирую предоставленный контекст, чтобы ответить на вопрос о внешности Mordain-Fall.

**Chain-of-Thought анализ:**

1. **Вопрос**: Пользователь спрашивает "как выглядит Mordain-Fall?"
2. **Анализ контекста**: Просматриваю все три документа в поисках описания внешности Mordain-Fall
   - Документ 1: Описывает действия Mordain-Fall (убийство Королевы), но не внешность
   - Документ 2: Описывает события, связанные с обучением и статусом Force Warden, но не внешность
   - Документ 3: Описывает конфликт с женщиной, одержимой духом, но не содержит описания внешности Mordain-Fall

3. **Синтез информации**: Ни в одном из предоставленных документов нет информации о внешности Mordain-Fall

**Ответ:**

На основании предоставленных документов нет информации о том, как выглядит Mordain-Fall. Все три документа описывают действия и события, связанные с Mordain-Fall (убийство Королевы Ktath'atn, его обучение в качестве Force Warden, конфликт с одержимой женщиной), но не содержат описания его физической внешности.
--------------------------------------------------------------------------------

