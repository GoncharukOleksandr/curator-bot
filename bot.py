import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
import os
from aiogram import Bot

API_TOKEN = os.environ.get("gith_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Структура груп
groups = {
    "КН-22": [
        "1. Алмаєв Олександр Романович",
        "2. Бабіюк Артем Сергійович",
        "3. Бездольний Кирило Олександрович",
        "4. Бєльченко Владислав Сергійович",
        "5. Бомко Данило Миколайович",
        "6. Буріко Гліб Володимирович",
        "7. Вакацієнко Нікіта Ярославович",
        "8. Гончарук Олександр Святославович",
        "9. Горячківський Кирило Ігорович",
        "10. Долинко Антон Станіславович",
        "11. Дорошок Олена Олегівна",
        "12. Засядьвовк Богдан Дмитрович",
        "13. Іванченко Дмитро Андрійович",
        "14. Калашник Олександр Володимирович",
        "15. Катков Олег Данилович",
        "16. Кіхоть Максим Вікторович",
        "17. Кічура Максим Григорович",
        "18. Кохан Ігор Олександрович",
        "19. Криця Олександр Віталійович",
        "20. Кузнєцов Микола Олександрович",
        "21. Кучер Денис Миколайович",
        "22. Лаврентьєв Олексій Сергійович",
        "23. Лозінський Олександр Сергійович",
        "24. Осадчий Владислав Костянтинович",
        "25. Пащенко Данило Віталійович",
        "26. Пилипенко Вікторія Сергіївна",
        "27. Півненко Олександр Михайлович",
        "28. Решетицька Наталія Сергіївна",
        "29. Рудь Ігор Вадимович",
        "30. Рябовол Всеволод Володимирович",
        "31. Скок Кирило Ігорович",
        "32. Сурженко Володимир Олександрович",
        "33. Теліга Антон Володимирович",
        "34. Ткаченко Роман Едуардович",
        "35. Фідря Максим Олександрович",
        "36. Чабан Олександр Олександрович",
        "37. Червоний Єгор Владиславович",
        "38. Щиченко Олексій Андрійович"
    ],
    "КН-23мб": [
        "1. Балакан Олександр Сергійович",
        "2.  Рябокобила Сергій Олександрович"
    ],
    "КІ22-1": [],  # нова група, студенти поки що не додані
    "КІ22-2": [],
    "КІ23мб": [],
    "КБ22-1": [],
    "КБ22-2": [],
    "КБ23мб": []
}

# Встановлюємо команди бота (Persistent Menu)
async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="🏠 Головне меню"),
    ]
    await bot.set_my_commands(commands)

# Функція для головного меню
def main_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📌 Про бота", callback_data="about")],
            [InlineKeyboardButton(text="📋 Список груп", callback_data="groups")],
            [InlineKeyboardButton(text="📝 Показати всі групи", callback_data="list_all")]
        ]
    )
    return keyboard

# /start — показує головне меню
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привіт! Я бот куратора. Оберіть дію:", reply_markup=main_menu())

# Callback "Про бота"
@dp.callback_query(lambda c: c.data == "about")
async def about_callback(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]]
    )
    await callback_query.message.edit_text(
        "Я бот, який допомагає куратору: можу показати інформацію про групи та студентів.",
        reply_markup=keyboard
    )
    await callback_query.answer()

# Callback "Показати всі групи"
@dp.callback_query(lambda c: c.data == "list_all")
async def list_all_callback(callback_query: types.CallbackQuery):
    text = ""
    for group_name, students in groups.items():
        text += f"{group_name}:\n"
        text += "\n".join(students) + "\n\n"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]]
    )
    await callback_query.message.edit_text(text.strip(), reply_markup=keyboard)
    await callback_query.answer()

# Callback "Список груп"
@dp.callback_query(lambda c: c.data == "groups")
async def groups_callback(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=group, callback_data=f"group:{group}")]
            for group in groups.keys()
        ] + [[InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]]
    )
    await callback_query.message.edit_text("Оберіть групу:", reply_markup=keyboard)
    await callback_query.answer()

# Callback для конкретної групи
@dp.callback_query(lambda c: c.data.startswith("group:"))
async def group_callback(callback_query: types.CallbackQuery):
    group_name = callback_query.data.split(":")[1]
    student_list = "\n".join(groups[group_name])
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="groups")]]
    )
    await callback_query.message.edit_text(
        f"Список студентів {group_name}:\n\n{student_list}",
        reply_markup=keyboard
    )
    await callback_query.answer()

# Callback для повернення на головне меню
@dp.callback_query(lambda c: c.data == "back_main")
async def back_main_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Головне меню. Оберіть дію:", reply_markup=main_menu())
    await callback_query.answer()

async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
