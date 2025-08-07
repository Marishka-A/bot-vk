import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
from difflib import get_close_matches

vk_session = vk_api.VkApi(token='vk1.a.LOtB_SWD4PIi9ScEmh8rZpOTtYWEDMLPc1WFuJ2q5_Leu7uWO9OVLZCuw-MpJEd1UmxJz4SlpAD_P4Agd7dRqrAWsDRFXS4dr0HcyBWohPtF7TUTabvV_RjdxfD5zwUcHxTvqqhtB1Rt8Oo8Wsl_tAYarEHMBwoLQQ22tqzCuicbxGa_Y1YWhHWzuMqbt6VtDcan7LXjq_ip9APECEiifw')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, '231834033')
user_states = {}

yes_questions = {
    "Можно ли взять несколько проектов": "Да",
    "Это бесплатно": "Да",
    "Нужно ли регистрироваться": "Да",
    "Доступны ли проекты для студентов любого вуза": "Да",
    "Можно ли изменить проект после выбора": "Да",
    "Есть ли вебинары по проектам": "Да",
    "Я получу сертификат": "Да"
}

no_questions = {
    "Обязательно ли обладать какими либо навыками на высоком уровне": "Нет",
    "Нужно ли платить за участие": "Нет",
    "Можно ли участвовать без вуза": "Нет",
    "Закрыт ли прием заявок": "Нет",
    "Будут ли ставить оценки": "Нет"
}

special_questions = {
    "кто может участвовать в программе":
        "Школьники, студенты бакалавриата, специалитета, магистратуры и аспирантуры всех вузов России, "
        "а также научные руководители и преподаватели, которые хотят использовать кейсы VK в обучении студентов.",

    "где можно использовать решения задач":
        "Задачи от VK можно использовать в практической части выпускных квалификационных, курсовых и "
        "научно-исследовательских работ, а также взять за основу домашних заданий.",

    "как получить необходимые данные для решения задачи":
        "Выбери задачу, пройди регистрацию — и тебе откроется доступ к материалам, "
        "которые понадобятся в процессе работы над задачей.",

    "как формировались задачи":
        "Все задачи на витрине — исследовательские и носят экспериментальный характер, "
        "составлены с учётом актуального бизнес-контекста. Задачи сформулированы таким образом, "
        "чтобы у участников была возможность реализовать свой талант, работая над интересными проектными кейсами.",

    "кому я могу задать вопросы":
        "Следи за расписанием вебинаров на странице проекта — ты сможешь задать вопросы по задаче экспертам VK.\n\n"
        "Если у тебя есть организационные вопросы, задай их на обучающей платформе.",

    "я не могу найти подходящую задачу что делать":
        "В банке задач появляются новые интересные кейсы от департаментов VK, следи за обновлениями.",

    "помощь полезные материалы подробность":
        "Скачайте презентацию c сайта https://education.vk.company/education_projects, "
        "чтобы подробнее узнать об использовании кейсов от VK в студенческих работах."
}

all_questions = {**yes_questions, **no_questions, **special_questions}

def get_start_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Начать", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()


def get_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Популярные вопросы", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Свой вопрос", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Помощь", color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def get_questions_keyboard():
    keyboard = VkKeyboard(one_time=False)
    questions = list(all_questions.keys())
    for i, question in enumerate(questions[:10]):  # Ограничиваем 10 кнопками
        keyboard.add_button(question, color=VkKeyboardColor.POSITIVE)
        if i % 2 == 1 and i != len(questions[:10]) - 1:
            keyboard.add_line()
    keyboard.add_line()
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


# Поиск похожих вопросов
def find_similar_questions(user_question):
    all_q = list(all_questions.keys())
    matches = get_close_matches(user_question, all_q, n=3, cutoff=0.5)
    return matches


# Обработка сообщений
def process_message(user_id, message):
    message = message.lower()
    random_id = random.randint(1, 10 ** 9)

    # Приветствие для новых пользователей
    if user_id not in user_states:
        send_welcome(user_id)
        return

    # Обработка команд меню
    if message == "начать":
        user_states[user_id] = 'active'
        vk.messages.send(
            user_id=user_id,
            message="Добро пожаловать! Вот как использовать бота:\n\n"
                    "1. Для начала ознакомтесь с частными вопросами из 'Популярных вопросов'. Чаще всего именно они помогают разобраться с возникшей проблемой\n"
                    "2. Если не нашли ответ, то попробуйте написать свой вопрос. Для этого выберите 'Свой вопрос'\n"
                    "3. Используйте 'Помощь' если не получилось найти ответ",
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    elif message == "популярные вопросы":
        vk.messages.send(
            user_id=user_id,
            message="Выберите вопрос из списка:",
            keyboard=get_questions_keyboard(),
            random_id=random_id
        )
        return

    elif message == "свой вопрос":
        vk.messages.send(
            user_id=user_id,
            message="Напишите свой вопрос в чат, и я постараюсь на него ответить.",
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    elif message == "помощь":
        vk.messages.send(
            user_id=user_id,
            message="Инструкция по использованию бота:\n\n"
                    "1. Выберите 'Популярные вопросы' для списка частых вопросов\n"
                    "2. Напишите свой вопрос в чат или выберите 'Свой вопрос'\n"
                    "3. Бот ответит на ваш вопрос или предложит похожие варианты",
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    elif message == "назад":
        vk.messages.send(
            user_id=user_id,
            message="Возвращаемся в главное меню",
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    # Проверка точных совпадений
    if message in yes_questions:
        vk.messages.send(
            user_id=user_id,
            message=yes_questions[message],
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    if message in no_questions:
        vk.messages.send(
            user_id=user_id,
            message=no_questions[message],
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    if message in special_questions:
        vk.messages.send(
            user_id=user_id,
            message=special_questions[message],
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    # Поиск похожих вопросов
    similar = find_similar_questions(message)
    if similar:
        if len(similar) == 1:
            # Если найден один похожий вопрос
            answer = all_questions[similar[0]]
            vk.messages.send(
                user_id=user_id,
                message=f"Возможно, вы имели в виду:\n\n{similar[0]}\n\n{answer}",
                keyboard=get_main_keyboard(),
                random_id=random_id
            )
        else:
            # Если найдено несколько похожих вопросов
            questions_list = "\n".join([f"• {q}" for q in similar])
            vk.messages.send(
                user_id=user_id,
                message=f"Возможно, вы имели в виду один из этих вопросов:\n\n{questions_list}\n\n"
                        "Выберите нужный вопрос или уточните свой запрос.",
                keyboard=get_main_keyboard(),
                random_id=random_id
            )
    else:
        # Если вопрос не найден
        vk.messages.send(
            user_id=user_id,
            message="Я не нашел ответа на ваш вопрос. Попробуйте:\n"
                    "1. Посмотреть 'Популярные вопросы'\n"
                    "2. Переформулировать свой вопрос\n"
                    "3. Обратиться в поддержку",
            keyboard=get_main_keyboard(),
            random_id=random_id
        )


# Приветственное сообщение
def send_welcome(user_id):
    user_states[user_id] = 'new'
    vk.messages.send(
        user_id=user_id,
        message="Привет! Я бот VK Education Projects. Нажмите кнопку 'Начать', чтобы продолжить.",
        keyboard=get_start_keyboard(),
        random_id=random.randint(1, 10 ** 9)
    )


# Основной цикл
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_user:
            user_id = event.message.from_id
            message = event.message.text
            process_message(user_id, message)

    # Обработка нажатия кнопки "Начать"
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('command') == 'start':
            process_message(event.user_id, "начать")