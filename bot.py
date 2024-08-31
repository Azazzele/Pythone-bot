from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import datetime
import random
import requests
import time

# Замените 'YOUR_API_TOKEN' на токен, который вы получили от BotFather
API_TOKEN = 'YOUR_API_TOKEN'

# Замените 'YOUR_WEATHER_API_KEY' на ваш API-ключ для получения погоды
WEATHER_API_KEY = 'YOUR_WEATHER_API_KEY'

# Замените 'YOUR_NEWS_API_KEY' на ваш API-ключ для получения новостей
NEWS_API_KEY = 'YOUR_NEWS_API_KEY'

# Замените 'YOUR_CURRENCY_API_KEY' на ваш API-ключ для получения курсов валют
CURRENCY_API_KEY = 'YOUR_CURRENCY_API_KEY'

# Временные данные для секундомера
stopwatch_start_time = None
stopwatch_elapsed_time = 0

# Список фактов о мире
facts = [
    "Земля вращается вокруг своей оси со скоростью около 1670 км/ч.",
    "В Антарктиде более 70% пресной воды на Земле.",
    "Солнце содержит 99.86% массы всей Солнечной системы.",
    "Человеческое тело состоит примерно на 60% из воды."
]

# Список цитат
quotes = [
    "Будьте тем изменением, которое хотите видеть в мире. — Махатма Ганди",
    "Сложности — это то, что делает жизнь интересной, и преодоление их делает жизнь значимой. — Джошуа Дж. Марион",
    "Жизнь — это то, что происходит, пока вы заняты планированием других вещей. — Джон Леннон"
]

# Список анекдотов
jokes = [
    "Почему программисты не могут ходить в лес? Потому что они боятся диких ошибок.",
    "Какой код всегда работает? Код на Java.",
    "Почему программисты так любят чай? Потому что он помогает им всегда быть на высоте!"
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я ваш новый бот. Используйте /help для списка команд.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        '/start - Начать общение с ботом\n'
        '/help - Получить помощь\n'
        '/time - Узнать текущее время\n'
        '/fact - Получить случайный факт\n'
        '/echo [сообщение] - Получить сообщение обратно\n'
        '/weather [город] - Узнать погоду в указанном городе\n'
        '/random [min] [max] - Получить случайное число в диапазоне от min до max\n'
        '/ask [вопрос] - Получить ответ на ваш вопрос\n'
        '/calculate [выражение] - Выполнить математическое выражение\n'
        '/quote - Получить случайную мотивационную цитату\n'
        '/joke - Получить случайный анекдот\n'
        '/news - Получить заголовки последних новостей\n'
        '/wiki [поиск] - Получить краткую информацию из Википедии\n'
        '/stopwatch - Запустить и остановить секундомер\n'
        '/day - Узнать текущий день недели\n'
        '/currency [валюта] - Узнать текущий курс валют'
    )

def current_time(update: Update, context: CallbackContext) -> None:
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update.message.reply_text(f'Текущее время: {now}')

def random_fact(update: Update, context: CallbackContext) -> None:
    fact = random.choice(facts)
    update.message.reply_text(f'Факт: {fact}')

def echo(update: Update, context: CallbackContext) -> None:
    message = ' '.join(context.args)
    if message:
        update.message.reply_text(f'Вы сказали: {message}')
    else:
        update.message.reply_text('Пожалуйста, укажите сообщение после команды /echo')

def weather(update: Update, context: CallbackContext) -> None:
    if context.args:
        city = ' '.join(context.args)
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        
        if data.get('cod') != 200:
            update.message.reply_text('Не удалось получить данные о погоде. Проверьте название города.')
            return

        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        update.message.reply_text(f'Погода в {city}: {weather_description}, температура {temperature}°C')
    else:
        update.message.reply_text('Пожалуйста, укажите название города после команды /weather')

def random_number(update: Update, context: CallbackContext) -> None:
    try:
        min_num = int(context.args[0])
        max_num = int(context.args[1])
        if min_num > max_num:
            update.message.reply_text('Минимальное значение должно быть меньше максимального.')
            return
        number = random.randint(min_num, max_num)
        update.message.reply_text(f'Случайное число от {min_num} до {max_num}: {number}')
    except (IndexError, ValueError):
        update.message.reply_text('Пожалуйста, укажите два числа: минимальное и максимальное значение.')

def ask(update: Update, context: CallbackContext) -> None:
    question = ' '.join(context.args)
    if question:
        answers = [
            'Да', 'Нет', 'Возможно', 'Не знаю', 'Попробуйте снова'
        ]
        answer = random.choice(answers)
        update.message.reply_text(f'Ваш вопрос: {question}\nОтвет: {answer}')
    else:
        update.message.reply_text('Пожалуйста, задайте вопрос после команды /ask')

def calculate(update: Update, context: CallbackContext) -> None:
    expression = ' '.join(context.args)
    try:
        result = eval(expression)
        update.message.reply_text(f'Результат: {result}')
    except Exception as e:
        update.message.reply_text(f'Ошибка при вычислении: {e}')

def quote(update: Update, context: CallbackContext) -> None:
    quote = random.choice(quotes)
    update.message.reply_text(f'Цитата: {quote}')

def joke(update: Update, context: CallbackContext) -> None:
    joke = random.choice(jokes)
    update.message.reply_text(f'Анекдот: {joke}')

def news(update: Update, context: CallbackContext) -> None:
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if data.get('status') != 'ok':
        update.message.reply_text('Не удалось получить новости. Проверьте ключ API.')
        return

    articles = data['articles'][:5]
    headlines = [f"{i+1}. {article['title']}" for i, article in enumerate(articles)]
    update.message.reply_text('\n'.join(headlines))

def wiki(update: Update, context: CallbackContext) -> None:
    if context.args:
        search_query = ' '.join(context.args)
        url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{search_query}'
        response = requests.get(url)
        data = response.json()
        
        if 'title' in data and data['title'] == 'Not found':
            update.message.reply_text('Не удалось найти информацию по вашему запросу.')
            return

        title = data.get('title')
        description = data.get('description')
        extract = data.get('extract')
        
        update.message.reply_text(f'{title}\n{description}\n\n{extract}')
    else:
        update.message.reply_text('Пожалуйста, укажите поисковый запрос после команды /wiki')

def stopwatch(update: Update, context: CallbackContext) -> None:
    global stopwatch_start_time, stopwatch_elapsed_time
    command = context.args[0] if context.args else None
    
    if command == 'start':
        if stopwatch_start_time is None:
            stopwatch_start_time = time.time()
            update.message.reply_text('Секундомер запущен.')
        else:
            update.message.reply_text('Секундомер уже запущен.')
    
    elif command == 'stop':
        if stopwatch_start_time is not None:
            stopwatch_elapsed_time = time.time() - stopwatch_start_time
            stopwatch_start_time = None
            update.message.reply_text(f'Секундомер остановлен. Прошло времени: {stopwatch_elapsed_time:.2f} секунд.')
        else:
            update.message.reply_text('Секундомер не запущен.')
    
    elif command == 'reset':
        stopwatch_start_time = None
        stopwatch_elapsed_time = 0
        update.message.reply_text('Секундомер сброшен.')

    else:
        update.message.reply_text('Используйте /stopwatch start для запуска, /stopwatch stop для остановки или /stopwatch reset для сброса.')

def day_of_week(update: Update, context: CallbackContext) -> None:
    now = datetime.datetime.now()
    day_of_week = now.strftime('%A')
    update.message.reply_text(f'Сегодня: {day_of_week}')

def currency(update: Update, context: CallbackContext) -> None:
    if context.args:
        currency_code = context.args[0].upper()
        url = f'https://api.exchangerate-api.com/v4/latest/USD'
        response = requests.get(url)
        data = response.json()
        
        if currency_code in data['rates']:
            rate = data['rates'][currency_code]
            update.message.reply_text(f'Курс валюты {currency_code}: 1 USD = {rate} {currency_code}')
        else:
            update.message.reply_text(f'Неизвестная валюта: {currency_code}')
    else:
        update.message.reply_text('Пожалуйста, укажите код валюты после команды /currency')

def main() -> None:
    # Создаем экземпляр Updater и передаем ему токен API
    updater = Updater(API_TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрация обработчиков команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("time", current_time))
    dp.add_handler(CommandHandler("fact", random_fact))
    dp.add_handler(CommandHandler("echo", echo))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("random", random_number))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("calculate", calculate))
    dp.add_handler(CommandHandler("quote", quote))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(CommandHandler("wiki", wiki))
    dp.add_handler(CommandHandler("stopwatch", stopwatch))
    dp.add_handler(CommandHandler("day", day_of_week))
    dp.add_handler(CommandHandler("currency", currency))

    # Регистрация обработчика текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем бота
    updater.start_polling()

    # Ожидаем завершения работы
    updater.idle()

if __name__ == '__main__':
    main()
