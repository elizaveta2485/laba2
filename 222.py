import telebot
from telebot import types

bot = telebot.TeleBot('6617444090:AAGgIcl8oLf-HWvBTWjc_0ZZ6iG7AYjuGfE')

waiting_for_fio = {}
registered_users = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши свое ФИО:')
    waiting_for_fio[message.chat.id] = True

@bot.message_handler(func=lambda message: True)
def record(message):
    chat_id = message.chat.id

    if chat_id in waiting_for_fio and waiting_for_fio[chat_id]:
        waiting_for_fio[chat_id] = False
        waiting_for_fio[f'fio_{chat_id}'] = message.text
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton('1 км')
        item2 = types.KeyboardButton('15 км (полумарафон)')
        item3 = types.KeyboardButton('21 км (полный марафон)')
        markup.add(item1, item2, item3)
        bot.send_message(chat_id, 'Выбери тип забега из списка:', reply_markup=markup)
    else:
        fio = waiting_for_fio.get(f'fio_{chat_id}', 'Unknown')
        race_type = message.text
        registered_users[chat_id] = {'fio': fio, 'race_type': race_type}
        response = f'Спасибо, {fio}! Вы успешно записаны на марафон с типом забега: {race_type}'
        bot.send_message(chat_id, response)

bot.polling(none_stop=True)
