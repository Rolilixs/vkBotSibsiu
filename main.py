import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from text_message import *


bot = vk_api.VkApi(token=TOKEN)  # Доработать момент с токеном
longpolling = VkLongPoll(bot)


def send_msg(user_id: int, message_text, keyboard=None, attachment=None):    # Функция посылающая сообщение

    bot.method('messages.send', {'user_id': user_id,
                                 'attachment': attachment,
                                 'message': message_text,
                                 'keyboard': keyboard,
                                 'random_id': vk_api.utils.get_random_id()})


def keyboard_create(keyboard_name, array):
    for i in range(len(array) - 1):
        keyboard_name.add_button(array[i])
        keyboard_name.add_line()
    keyboard_name.add_button(array[-1], VkKeyboardColor.NEGATIVE if array != k_main_menu else VkKeyboardColor.DEFAULT)


main_menu_keyb = VkKeyboard()
organizations_keyb = VkKeyboard()
support_keyb = VkKeyboard()


keyboard_create(main_menu_keyb, k_main_menu)
keyboard_create(organizations_keyb, k_organizations)
keyboard_create(support_keyb, k_support)


for event in longpolling.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        text_message = event.text.lower()

        if text_message in ["start", "начать", "главное меню"]:
            id_random = vk_api.utils.get_random_id()
            bot.method('messages.send', {
                'user_id': event.user_id,
                'message': (message_mm if text_message == "главное меню" else message_welcome),
                'keyboard': main_menu_keyb.get_keyboard(),
                'random_id': id_random})

        elif text_message == "организации":
            id_random = vk_api.utils.get_random_id()
            bot.method('messages.send', {'user_id': event.user_id,
                                         'message': "Раздел \"Организации\":",
                                         'keyboard': organizations_keyb.get_keyboard(),
                                         'random_id': id_random})

        elif text_message == "помощь":
            id_random = vk_api.utils.get_random_id()
            bot.method('messages.send', {'user_id': event.user_id,
                                         'message': "Раздел \"Помощь\":",
                                         'keyboard': support_keyb.get_keyboard(),
                                         'random_id': id_random})

        elif text_message == "профком":
            send_msg(event.user_id, message_info_profkom)
        elif text_message == "ксс":
            send_msg(event.user_id, message_info_kss)
        elif text_message == "робототехника":
            send_msg(event.user_id, message_info_robotech)
        elif text_message == "карта":
            send_msg(event.user_id, "Карта", attachment="photo-198388604_457239018")
        elif text_message == "как...":  # need to add more func
            send_msg(event.user_id, how_reset_password)
