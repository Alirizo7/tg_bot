import django
import os

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

os.environ['DJANGO_SETTINGS_MODULE'] = 'tele_core.settings'
django.setup()

from home.models import User

API_KEY = '6363086604:AAF5MSR2MJ1dpSOwYNRneW70fq28_avtDEo'

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)


def handle_message(update, context):
    user = get_user(update.effective_user.id)
    if user:
        show_main_menu(update, context)
    else:
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("📲Отправить номер", request_contact=True)]],
                                       resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Привет! Пожалуйста, нажмите на кнопку '📲Отправить номер', чтобы отправить свой номер телефона.",
                                 reply_markup=keyboard)


def process_contact(update, context):
    contact = update.message.contact
    user_data = context.user_data

    if contact is not None:
        if 'phone_number' not in user_data:
            phone_number = contact.phone_number
            user_data['phone_number'] = phone_number

            user = User(
                id=update.effective_user.id,
                phone_number=user_data['phone_number']
            )
            user.save()

            keyboard = ReplyKeyboardMarkup([[KeyboardButton("Заказать🛒")],
                                            [KeyboardButton("Мои заказы📖"), KeyboardButton("Кешбек💰")],
                                            [KeyboardButton("Настройки⚙️"), KeyboardButton("Служба Поддержки☎️")]],
                                           resize_keyboard=True)
            update.message.reply_text('Спасибо! Номер сохранен.', reply_markup=keyboard)
    else:
        update.message.reply_text('Пожалуйста, воспользуйтесь кнопкой для отправки номера телефона.')


def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def get_or_create_user(user_id):
    user, created = User.objects.get_or_create(id=user_id)
    return user


def show_main_menu(update, context, from_support=False):
    if from_support:
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("Заказать🛒")],
                                        [KeyboardButton("Мои заказы📖"), KeyboardButton("Кешбек💰")],
                                        [KeyboardButton("Настройки⚙️"), KeyboardButton("Служба Поддержки☎️")]],
                                       resize_keyboard=True)
        update.message.reply_text('Главное меню:', reply_markup=keyboard)
    else:
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("Заказать🛒")],
                                        [KeyboardButton("Мои заказы📖"), KeyboardButton("Кешбек💰")],
                                        [KeyboardButton("Настройки⚙️"), KeyboardButton("Служба Поддержки☎️")]],
                                       resize_keyboard=True)
        update.message.reply_text('Главное меню:', reply_markup=keyboard)


def show_support_menu(update, context):
    keyboard = ReplyKeyboardMarkup([[KeyboardButton("Главное меню")],
                                    [KeyboardButton("📞Позвонить"), KeyboardButton("💬Написать")]],
                                   resize_keyboard=True)
    update.message.reply_text('Меню поддержки:', reply_markup=keyboard)

    dp.add_handler(MessageHandler(Filters.regex('^Главное меню$'), show_main_menu))


def show_cashback_menu(update, context):
    keyboard = ReplyKeyboardMarkup([[KeyboardButton("Главное меню")]],
                                   resize_keyboard=True)
    update.message.reply_text('💰Ваш кешбек: 15 TJK', reply_markup=keyboard)

    dp.add_handler(MessageHandler(Filters.regex('^Главное меню$'), show_main_menu))


def show_settings_menu(update, context):
    keyboard = ReplyKeyboardMarkup([[KeyboardButton("Главное меню"), KeyboardButton("📲Изменить номер")]],
                                   resize_keyboard=True)
    update.message.reply_text('⚙️Меню настройки:', reply_markup=keyboard)

    dp.add_handler(MessageHandler(Filters.regex('^Главное меню$'), show_main_menu))


def change_phone_number(update, context):
    keyboard = ReplyKeyboardMarkup([[KeyboardButton("Главное меню")]], resize_keyboard=True)
    update.message.reply_text("Отправьте или введите ваш новый номер телефона в виде: +998 ** *** ****",
                              reply_markup=keyboard)
    context.user_data['waiting_for_new_number'] = True


def process_new_phone_number(update, context):
    if 'waiting_for_new_number' in context.user_data and context.user_data['waiting_for_new_number']:
        new_phone_number = update.message.text.strip()
        user = get_user(update.effective_user.id)

        if new_phone_number and len(new_phone_number) == 12:
            if user:
                user.phone_number = new_phone_number
                user.save()

                keyboard = ReplyKeyboardMarkup([[KeyboardButton("Главное меню")]], resize_keyboard=True)
                update.message.reply_text(f"Ваш номер телефона успешно изменен на +{new_phone_number}.",
                                          reply_markup=keyboard)
                show_main_menu(update, context)
            else:
                update.message.reply_text("Пользователь не найден.")
        else:
            update.message.reply_text("Вы не ввели правилно номер телефона.")

        context.user_data['waiting_for_new_number'] = False


def support_call(update, context):
    phone_number = '+998997072820'
    keyboard = []
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f'Выберите действие: \n '
        f'📞Позвонить: <a href="tel:{phone_number}">{phone_number}</a>',
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


def support_message(update, context):
    chat_link = f'https://t.me/karimov_alirizo'
    keyboard = [[InlineKeyboardButton(text='💬Напишите нам', url=f'{chat_link}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f'Если у Вас возникли вопросы или предложения, напишите нам. \n ',
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


def go_back(update, context):
    update.message.reply_text('Вы вернулись назад в главное меню.')
    show_main_menu(update, context)


def order_menu(update, context):
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("🚙Доставка"), KeyboardButton("🚶Самовывоз"), KeyboardButton("⬅️Назад")]],
        resize_keyboard=True)
    update.message.reply_text('🛒️Меню заказать:', reply_markup=keyboard)

    dp.add_handler(MessageHandler(Filters.regex('^⬅️Назад$'), go_back))


if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", handle_message))
    dp.add_handler(MessageHandler(Filters.contact, process_contact))
    dp.add_handler(MessageHandler(Filters.regex('^Главное меню$'), show_main_menu))
    dp.add_handler(MessageHandler(Filters.regex('^Кешбек💰$'), show_cashback_menu))
    dp.add_handler(MessageHandler(Filters.regex('^Служба Поддержки☎️$'), show_support_menu))
    dp.add_handler(MessageHandler(Filters.regex('^Настройки⚙️$'), show_settings_menu))
    dp.add_handler(MessageHandler(Filters.regex('^📲Изменить номер$'), change_phone_number))
    dp.add_handler(MessageHandler(Filters.regex('^📞Позвонить$'), support_call))
    dp.add_handler(MessageHandler(Filters.regex('^💬Написать$'), support_message))
    dp.add_handler(MessageHandler(Filters.regex('^Заказать🛒$'), order_menu))
    dp.add_handler(
        MessageHandler(Filters.regex('^⬅️Назад$'), go_back))
    dp.add_handler(MessageHandler(Filters.text, process_new_phone_number))

    updater.start_polling(1.0)
    updater.idle()
