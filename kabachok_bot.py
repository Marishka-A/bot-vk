from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

# Токен сообществаbot-vk
bot = Bot(token="vk1.a.C9P1ZR9v0FpreNyEYn0CZ3WQEKk5Pmg_iWetXtS9jb62ogmEkg8ZdRmkArwOSnDG29cLBnSHKhKcG5IVbJWOytCC47ly8LslfluAKl0ACAYbheS0pTCmvUzdVLTF-giF4UXVTd31ft8Johv63cjhjbagd0QojlQDUAIwvuBrgVy4ZO9nxefsDM82o4BW_0PqYSB_aYXS6xAzbDuPVzwmVQ")

# Ответ на кнопку "Начать" или команду /start
@bot.on.private_message(text=["начать", "/start"])
async def start(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("О чем это сообщество"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Будут ли другие овощи"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()  # Новая строка кнопок
    keyboard.add(Text("Когда будет новый пост"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("А кабачок правда настоящий?"), color=KeyboardButtonColor.NEGATIVE)
    keyboard.row()
    keyboard.add(Text("Когда кабачок съедят"), color=KeyboardButtonColor.SECONDARY)

    await message.answer(
        "Приветствую в *«Обществе любителей кабачков»*! \n\n"
        "Что ты хочешь узнать? Выбери вариант:",
        keyboard=keyboard
    )

# Ответы на вопросы
@bot.on.private_message(text="О чем это сообщество")
async def about(message: Message):
    await message.answer(
        "*О чем это сообщество?*\n\n"
        "Мы — фанатики кабачков во всех их проявлениях!\n"
        "Здесь мы делимся:\n"
        "▪ Рецептами из кабачков\n"
        "▪ Фото выращенных кабачков\n"
        "▪ Мемами про кабачки\n"
        "▪ Научными фактами о кабачках\n\n"
        "Присоединяйся к культу!"
    )

@bot.on.private_message(text="Будут ли другие овощи")
async def other_vegetables(message: Message):
    await message.answer(
        "*Будут ли другие овощи?*\n\n"
        "Нет. Только кабачки. Только хардкор.\n\n"
        "Но если очень хочется, напиши нам в *предложения* (может, добавим огурцы... но это не точно)."
    )

@bot.on.private_message(text="Когда будет новый пост")
async def new_post(message: Message):
    await message.answer(
        "*Когда будет новый пост?*\n\n"
        "Кабачок — существо непредсказуемое.\n"
        "Но обычно новые посты выходят:\n"
        "▪ По средам (рецепты)\n"
        "▪ По субботам (фото урожая)\n\n"
        "Подпишись, чтобы не пропустить!"
    )

@bot.on.private_message(text="А кабачок правда настоящий?")
async def real_kabachok(message: Message):
    await message.answer(
        "*А кабачок правда настоящий?*\n\n"
        "*Шёпотом*: Между нами... наш кабачок — *государственная тайна*.\n"
        "Но если серьёзно — да, он настоящий, и он следит за тобой."
    )

@bot.on.private_message(text="Когда кабачок съедят")
async def eat_kabachok(message: Message):
    await message.answer(
        "*Когда кабачок съедят?*\n\n"
        "Никогда.\n"
        "Кабачок — *вечен*. Он переживёт всех нас.\n\n"
        "P.S. Но если ты предложишь интересный рецепт, мы *возможно* его попробуем..."
    )

# Дополнительная шутка на случай неизвестного сообщения
@bot.on.private_message()
async def unknown(message: Message):
    await message.answer(
        "Извини, я понимаю только кабачковый язык.\n"
        "Попробуй нажать одну из кнопок или напиши /start!"
    )

# Запуск бота
print("🥒 Бот 'Общество любителей кабачков' запущен!")
bot.run_forever()