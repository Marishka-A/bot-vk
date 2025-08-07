import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
from difflib import get_close_matches

ADMIN_ID = '631014462'
TOKEN = 'vk1.a.LOtB_SWD4PIi9ScEmh8rZpOTtYWEDMLPc1WFuJ2q5_Leu7uWO9OVLZCuw-MpJEd1UmxJz4SlpAD_P4Agd7dRqrAWsDRFXS4dr0HcyBWohPtF7TUTabvV_RjdxfD5zwUcHxTvqqhtB1Rt8Oo8Wsl_tAYarEHMBwoLQQ22tqzCuicbxGa_Y1YWhHWzuMqbt6VtDcan7LXjq_ip9APECEiifw'
GROUP_ID = '231834033'

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

user_states = {}
help_requests = {}

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
    "Нужно ли обладать крутыми навыками и знаниями на высоком уровне": "Нет",
    "Нужно ли платить за участие": "Нет",
    "Можно ли участвовать без вуза": "Нет",
    "Закрыт ли прием заявок": "Нет",
    "Будут ли ставить оценки": "Нет"
}

special_questions = {
    "Для кого программа":
        "Школьники, студенты бакалавриата, специалитета, магистратуры и аспирантуры всех вузов России, "
        "а также научные руководители и преподаватели, которые хотят использовать кейсы VK в обучении студентов.",

    "Для чего программа":
        "Задачи от VK можно использовать в практической части выпускных квалификационных, курсовых и "
        "научно-исследовательских работ, а также взять за основу домашних заданий.",

    "Как начать участвовать":
        "Выберите задачу, пройдите регистрацию — и вам откроется доступ к материалам, "
        "которые понадобятся в процессе работы над задачей.",

    "Как формировались задачи":
        "Все задачи на витрине — исследовательские и носят экспериментальный характер, "
        "составлены с учётом актуального бизнес-контекста. Задачи сформулированы таким образом, "
        "чтобы у участников была возможность реализовать свой талант, работая над интересными проектными кейсами.",

    "Если вопрос по проекту":
        "Следите за расписанием вебинаров на странице проекта — вы сможете задать вопросы по задаче экспертам VK.\n\n"
        "Если у вас есть организационные вопросы, задайте их на обучающей платформе.",

    "Ничего не нравится":
        "В банке задач появляются новые интересные кейсы от департаментов VK, следите за обновлениями.",

    "Полезные материалы":
        "Скачайте презентацию c сайта https://education.vk.company/education_projects, "
        "чтобы подробнее узнать об использовании кейсов от VK в студенческих работах."
}

all_questions = {**yes_questions, **no_questions, **special_questions}


def notify_admin(user_id, user_message):
    random_id = random.randint(1, 10 ** 9)
    message = (f"Пользователь @id{user_id} запросил помощь:\n"
               f"Сообщение: {user_message}\n\n"
               "Ответьте на это сообщение, чтобы помочь пользователю.")

    msg = vk.messages.send(
        user_id=ADMIN_ID,
        message=message,
        random_id=random_id
    )

    help_requests[user_id] = {
        'admin_msg_id': msg,
        'user_msg': user_message
    }

def process_admin_reply(event):
    """Обрабатывает ответ администратора на запрос помощи"""
    if event.reply_message and event.reply_message['id'] in [req['admin_msg_id'] for req in help_requests.values()]:
        for user_id, req in help_requests.items():
            if req['admin_msg_id'] == event.reply_message['id']:
                vk.messages.send(
                    user_id=user_id,
                    message=f"Администратор отвечает на ваш запрос:\n\n{event.message.text}",
                    keyboard=get_main_keyboard(),
                    random_id=random.randint(1, 10 ** 9)
                )
                del help_requests[user_id]
                break

def capitalize_sentence(text):
    if not text:
        return text
    return text[0].upper() + text[1:]

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
    keyboard.add_button("Спасибо, вопрос решился!", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()

def get_special_questions_keyboard():
    keyboard = VkKeyboard(one_time=False)
    questions = list(special_questions.keys())
    for i, question in enumerate(questions):
        keyboard.add_button(question, color=VkKeyboardColor.POSITIVE)
        if i % 2 == 1 and i != len(questions)-1:
            keyboard.add_line()
    keyboard.add_line()
    keyboard.add_button("Спасибо, вопрос решился!", color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()

def find_similar_questions(user_question):
    all_q = list(all_questions.keys())
    matches = get_close_matches(user_question.lower(), [q.lower() for q in all_q], n=3, cutoff=0.5)
    return [q for q in all_q if q.lower() in matches]

def process_message(user_id, message):
    message_lower = message.lower()
    random_id = random.randint(1, 10**9)

    if user_id not in user_states or message_lower == "начать":
        user_states[user_id] = 'active'
        vk.messages.send(
            user_id=user_id,
            message=capitalize_sentence(
                "добро пожаловать! Вот как использовать бота:\n\n"
                "1. Для начала ознакомьтесь с частыми вопросами из 'Популярных вопросов'. "
                "Чаще всего именно они помогают разобраться с возникшей проблемой\n"
                "2. Если не нашли ответ, то попробуйте написать свой вопрос. "
                "Для этого выберите 'Свой вопрос'\n"
                "3. Используйте 'Помощь' если не получилось найти ответ"
            ),
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    elif message_lower == "популярные вопросы":
        vk.messages.send(
            user_id=user_id,
            message="Выберите вопрос из списка:",
            keyboard=get_special_questions_keyboard(),
            random_id=random_id
        )
        return

    elif message_lower == "свой вопрос":
        vk.messages.send(
            user_id=user_id,
            message="Напишите свой вопрос в чат, и я постараюсь на него ответить.",
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    elif message_lower == "помощь":
        vk.messages.send(
            user_id=user_id,
            message=capitalize_sentence(
                "Дождитесь когда вам ответит оператор или загляните на наш сайт https://education.vk.company/education_projects"
            ),
            keyboard=get_main_keyboard(),
            random_id=random_id
        )

        notify_admin(user_id, message)
        return

    elif message_lower == "спасибо, вопрос решился!":
        vk.messages.send(
            user_id=user_id,
            message="Рад был помочь! Возвращайтесь, если возникнут вопросы.",
            keyboard=get_start_keyboard(),
            random_id=random_id
        )
        user_states[user_id] = 'new'
        return

    if message in all_questions:
        answer = all_questions[message]
        vk.messages.send(
            user_id=user_id,
            message=answer if answer[0].isupper() else capitalize_sentence(answer),
            keyboard=get_main_keyboard(),
            random_id=random_id
        )
        return

    similar = find_similar_questions(message)
    if similar:
        if len(similar) == 1:
            answer = all_questions[similar[0]]
            vk.messages.send(
                user_id=user_id,
                message=f"Возможно, вы имели в виду:\n\n{similar[0]}\n\n{answer}",
                keyboard=get_main_keyboard(),
                random_id=random_id
            )
        else:
            questions_list = "\n".join([f"• {q}" for q in similar])
            vk.messages.send(
                user_id=user_id,
                message=f"Возможно, вы имели в виду один из этих вопросов:\n\n{questions_list}\n\n"
                       "Выберите нужный вопрос или уточните свой запрос.",
                keyboard=get_main_keyboard(),
                random_id=random_id
            )
    else:
        vk.messages.send(
            user_id=user_id,
            message=capitalize_sentence(
                "я не нашел ответа на ваш вопрос, попробуйте:\n"
                "1. Посмотреть 'популярные вопросы'\n"
                "2. Переформулировать свой вопрос\n"
                "3. Обратиться в поддержку"
            ),
            keyboard=get_main_keyboard(),
            random_id=random_id
        )


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_user:
            user_id = event.message.from_id

            if user_id == ADMIN_ID:
                process_admin_reply(event)
            else:
                message = event.message.text
                process_message(user_id, message)

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('command') == 'start':
            process_message(event.user_id, "начать")