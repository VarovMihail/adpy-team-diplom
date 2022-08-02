import vk_api
#from main_ORM import gender, city, min_age, max_age
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from config import bot_token, person_token
from vkinder_class import VKinder

keyboard = VkKeyboard(inline=True)
keyboard.add_button('start', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('next', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('like', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('list', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('stop', color=VkKeyboardColor.NEGATIVE)

session_vk = vk_api.VkApi(token=bot_token)  # Подключаем токен и longpoll

def replay(id, text, attachments):  # Создадим функцию для ответа на сообщения в лс группы
    session_vk.method('messages.send', {'user_id': id,
                                     'message': text,
                                     'random_id': 0,
                                     'attachment': ','.join(attachments),
                                     'keyboard': keyboard.get_keyboard()
                                     })

def replay_without_keyboard(id, text):  # Ответ без клавиатуры
    session_vk.method('messages.send', {'user_id': id,
                                     'message': text,
                                     'random_id': 0})


