import asyncio
import gspread
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import schedule

# Укажите токен вашего Telegram-бота
BOT_TOKEN = "7909234577:AAFq9CMjzlEgnhO_Uz2bKYbCGudbqhAWoX8"

# Ссылка на Google Таблицу
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1R_xoCQ_y-Ev2tMFS9YoBcpidDbcnH7y3NKVPpxaP8gE/edit"

# Авторизационные данные в формате JSON
json_credentials = {
    "type": "service_account",
    "project_id": "regal-campus-447421-g9",
    "private_key_id": "37403018115fcd2e108849e093345f66e670bf90",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCq1XAa2sNPUwpg\nZ6LNhPhurGrBX+oZYhBm7gWW6UjubxwtwsMKOkRf5AFHkJDL32UVw9egWxFktKyO\n6fhvgmWdZ/A4q/7FjNVNaTaBADTZIXsXp/36kDBl+D56oxWCjYwYXsVvbd6N6ked\nPwG/eWhx13aEw6FjdOSCpFNr2qCQf91decNGeKD2y7maE3xs5jjvTBxfhcUlq7ca\nvG6CcNX5DNOFf2I9Z57RCJhjleC6GNhS7I2CNLlufXgUqQ54HNev1967OvxidO6A\nV3iqHbX2JAH3KZleW0mnAISRijrJXmaOCZjsYZldx6ZN1OdASgGy8SdKGMwhyrEX\naRTvxts1AgMBAAECggEACXcqjz5cUIaeHlHXtjH+LumsP5swJihmFsHs+tvhr95l\nrg5qzqQEWljQjlXPBBDUccSIa8jn+Y++OOvzWUBdH3/dElLLWshPIEsqWzL2+qnt\nf1XOT4YSPHApDBQBstpjbw0/PMmWaYAX6DlPwDt6o0YoObp6NH/LUobG3YS/XUo1\nNJ9KLt1AYhxEcUo41JIwKFGd3ZeRQKPWzZ+lPPG3UgXUNY4p55jEsprd9YbYOSGK\nXVOECtezHA62vJ28atlseqI4rZDd54spWXgOXnY3ezzmDrP8zb5MQ3WPIsC6Tcl2\nmTG+Nypbuc0W6VEv5OtnIogepLqBrn4TqCm44Q63+QKBgQDdFoEt9TetEqNkOYaQ\nESR7s1yay5SvawZznh7NXWYjnDCT60IacuVijxx0N9FsrEoryqZOEHVpvZlSlLMp\nMhqDcFEx0mQuuzggLiEIvaAV2dfit/CUv152Ip4n++10Dk7zyADEmUxVf+4eIqMW\n+yr6G57lAR6tq2RFdF4qaTYGDQKBgQDFz2eiFaI5XDl/DkQx5x1atgnTGG6VlRAk\n8harKrheze4xFnxGND7IPhNemsg5nKM6qwDwVi7GGAI2FEHkLLqOMcO9r4mpZ8ic\n/2+JCbBfBoECxph0rkdcaIgtgRbS7Q+G49TgvSTRXWDJgqjRnp3WDWy4EIgp2SIv\nM8StqkjHyQKBgHF4b2yLArxNaJaz/6BJbBQhBlJcUj+GCpWkfeKhIR79tuD0ScUR\nWzGuicgMLew8sQSwyZIfWGOg7+Q2dY2bLYhwSPvtI4XoiPHbOxElYdhVKjwuc8ek\nQHMZaVrULhb2kQcFi39bvpXTRv8of9P3rSMYsgCPBpPT926+PuY9gYCxAoGAcSTX\nFCDnr4OO55vTae/WHIKvT+1To3+lwlwuly1SU/faXH2OC+HqX0MSdTR3fmyX+QDD\nArVo/6nP6frgTZFADAFvAtqbFSjl2NdKhsnh9hiURnAt19+vta2c5tpFodQy42cB\n5qKJoq+Uou53fZ8KjNsU6puaJsWqBfHId8VE5/ECgYEAtAvlcnvP/hX4XZ3kKfHV\nau94H6gQcn3fxVOPKg8KaXHi7zk7EFYLJU63372u4LA01Wx4SCLyW2UolrHwOe/2\nAx7OkHqNPGzk3VQL5WBgIQCj6k2935CeizeTcgu0W8BcRxna3BG2RN5EoVyxK2pm\ny7t0nhXNo+93wQVsbQ1GEBw=\n-----END PRIVATE KEY-----\n",
    "client_email": "wbdrive@regal-campus-447421-g9.iam.gserviceaccount.com",
    "client_id": "107917407367559744911",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/wbdrive%40regal-campus-447421-g9.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  # Создаём диспетчер

# Хранилище данных из таблицы
table_data = ""
last_sent_data = ""  # Переменная для хранения последнего отправленного сообщения
chat_id = None  # Переменная для хранения ID чата
last_message_id = None  # Переменная для хранения ID последнего отправленного сообщения

# Функция для получения данных из Google Таблицы
def fetch_table_data():
    global table_data, last_sent_data
    try:
        gc = gspread.service_account_from_dict(json_credentials)
        sheet = gc.open_by_url(SPREADSHEET_URL).sheet1
        data = sheet.get_all_values()

        for row in data:
            if row and row[0] == '11246':
                parking = row[1] if len(row) > 1 else "Нет данных"
                boxes = row[2] if len(row) > 2 else "Нет данных"
                barcode = row[3] if len(row) > 3 else "Нет данных"
                table_data = f"Коробки: {boxes}\nШК: {barcode}\nПарковка: {parking}\nНомер маршрута: 11246"
                break
        else:
            table_data = "Данные для маршрута 11246 не найдены."

        # Отправка обновления только если данные изменились
        if table_data != last_sent_data:
            last_sent_data = table_data
            if chat_id:  # Проверяем, установлен ли chat_id
                asyncio.create_task(send_update(chat_id))

    except Exception as e:
        table_data = f"Ошибка при чтении данных: {e}"

# Функция для отправки обновления
async def send_update(chat_id):
    global last_message_id  # Используем глобальную переменную для хранения ID сообщения

    # Удаляем предыдущее сообщение, если оно существует
    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id, last_message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")

    # Отправляем новое сообщение и сохраняем его ID
    message = await bot.send_message(chat_id, "Текущие данные из таблицы:\n" + table_data)
    last_message_id = message.message_id  # Сохраняем ID нового сообщения

# Команда /start: приветствие
@dp.message(Command("start"))
async def start_handler(message: Message):
    global chat_id  # Используем глобальную переменную chat_id
    chat_id = message.chat.id  # Сохраняем chat_id
    await message.answer("Добро пожаловать! Я подключен к вашей Google Таблице.")
    await message.answer("Текущие данные из таблицы:\n" + table_data)

# Новая команда /fetch_data
@dp.message(Command("fetch_data"))
async def fetch_data_handler(message: Message):
    global chat_id  # Используем глобальную переменную chat_id
    chat_id = message.chat.id  # Сохраняем chat_id
    fetch_table_data()  # Получаем данные из таблицы
    await message.answer("Данные обновлены:\n" + table_data)
    await send_update(chat_id)  # Отправляем обновление в тот же чат

# Настройка расписания обновления данных
def schedule_task():
    schedule.every(30).seconds.do(fetch_table_data)  # Изменено на 30 секунд

# Фоновая задача для обновления данных каждые 30 секунд
async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)  # Проверяем задачи каждую секунду


# Основная функция
# Ваши импорты и остальной код...

async def main():
    fetch_table_data()  # Первоначальное получение данных
    schedule_task()  # Настраиваем расписание

    dp.message.register(start_handler)  # Регистрируем обработчик для команды /start
    dp.message.register(fetch_data_handler)  # Регистрируем обработчик для команды /fetch_data

    asyncio.create_task(scheduler())  # Запускаем фоновую задачу для обновления данных
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхук, если он есть
    await dp.start_polling(bot)  # Запускаем бота

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Произошла ошибка: {e}. Перезапуск бота...")
            asyncio.sleep(5)  # Подождите перед перезапуском
