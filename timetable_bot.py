import datetime
import os
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CommandHandler,
                          Updater,
                          Filters,
                          MessageHandler,
                          CallbackQueryHandler)

TIMETABLE_HONEST_WEEK = {
    1: ['08:00 Физическая культура',
        '11:30 Аналитическая геометрия и линейная алгебра.',
        '13:25 Деловое общение и культура речи'],
    2: ['11:30 Механика лаб.',
        '15:30 Информатика'],
    3: ['08:00 Физическая культура',
        '11:30 Механика'],
    4: ['08:00 История России',
        '09:45 Механика',
        '11:30 Информатика',
        '13:25 Основы Российской Государственности'],
    5: ['08:00 Деловое общение и культура речи',
        '09:45 Математический анализ',
        '11:30 Английский язык'],
    6: ['09:45 Математический анализ',
        '11:30 Аналитическая геометрия и линейная алгебра ']
}
TIMETABLE_ODD_WEEK = {
    1: ['08:00 Физическая культура',
        '11:30 Аналитическая геометрия и линейная алгебра.',
        '13:25 Английский язык.'],
    2: ['09:45 Основы Российской Государственности',
        '11:30 Механика лаб.',
        '15:30 Информатика',
        '16:55 Информатика'],
    3: ['08:00 Физическая культура',
        '11:30 Механика'],
    4: ['08:00 История России',
        '09:45 Механика',
        '11:30 Информатика',
        '13:25 Основы Российской Государственности'],
    5: ['08:00 Математический анализ',
        '09:45 Математический анализ',
        '11:30 История'],
    6: ['08:00 Математический анализ',
        '09:45 Математический анализ',
        '11:30 Аналитическая геометрия и линейная алгебра ']
}

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = 850792184
current_date = datetime.date.today()

week_number = current_date.isocalendar()[1]
week_day = current_date.isocalendar()[2]
print(current_date.strftime("%d.%m.%Y"))
print("Номер недели:", week_number)
print("День недели:", week_day)


def get_timetable_on_day():
    if week_day == 7:
        lessons_string = 'В воскресенье занятий нет.'
    else:
        if week_number % 2 == 0:
            list_of_lessons = TIMETABLE_ODD_WEEK[week_day]
            lessons_string = '\n'.join(list_of_lessons)
        else:
            list_of_lessons = TIMETABLE_HONEST_WEEK[week_day]
            lessons_string = '\n'.join(list_of_lessons)
    return lessons_string


def get_timetable_on_week():
    week_days = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота'
    }
    lessons_string_on_week = ''
    if week_number % 2 == 0:
        for day in TIMETABLE_ODD_WEEK:
            lessons_string_on_day = week_days[day]
            list_of_lessons = TIMETABLE_ODD_WEEK[day]
            for lesson in list_of_lessons:
                lessons_string_on_day += f'\n {lesson}'
            lessons_string_on_week += f'\n\n {lessons_string_on_day}'
    else:
        for day in TIMETABLE_ODD_WEEK:
            lessons_string_on_day = week_days[day]
            list_of_lessons = TIMETABLE_HONEST_WEEK[day]
            for lesson in list_of_lessons:
                lessons_string_on_day += f'\n {lesson}'
            lessons_string_on_week += f'\n\n {lessons_string_on_day}'
    return lessons_string_on_week


text = get_timetable_on_week()

bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)


def say_hi(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id,
                             text='Привет, {}!'.format(name))


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    keyboard = [
        [InlineKeyboardButton("Расписание на день",
                              callback_data="get_timetable_day"),
         InlineKeyboardButton("Расписание на неделю",
                              callback_data="get_timetable_week")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что вы включили меня, {}!'.format(name),
        reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    if query.data == "get_timetable_day":
        query.edit_message_text(text=get_timetable_on_day())
    if query.data == "get_timetable_week":
        query.edit_message_text(text=get_timetable_on_week())


def send_timetable(update, context):
    timetable = get_timetable_on_day()
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=timetable)


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('get_timetable',
                                              send_timetable))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

updater.start_polling()
updater.idle()
