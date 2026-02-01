import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Вставь сюда свой токен (не забудь потом скрыть его)
TOKEN = "7909234577:AAFq9CMjzlEgnhO_Uz2bKYbCGudbqhAWoX8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Создаем строитель клавиатуры
    builder = InlineKeyboardBuilder()

    # В цикле создаем 10 кнопок
    for i in range(1, 11):
        builder.button(
            text=f"Кнопка {i}", 
            callback_data=f"btn_{i}"
        )

    # Указываем, сколько кнопок будет в ряду (например, по 2)
    builder.adjust(2)

    await message.answer(
        "Привет! Вот твои 10 кнопок:",
        reply_markup=builder.as_markup()
    )

# Обработка нажатия на любую из кнопок
@dp.callback_query(F.data.startswith("btn_"))
async def callback_handler(callback: types.CallbackQuery):
    # Получаем номер кнопки из callback_data
    button_number = callback.data.split("_")[1]
    
    await callback.message.answer(f"Ты нажал на кнопку номер {button_number}!")
    await callback.answer() # Закрываем "часики" на кнопке

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
