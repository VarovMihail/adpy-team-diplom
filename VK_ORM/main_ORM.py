import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from config import bot_token, person_token, database_name, database_username, database_password
from vkinder_class import VKinder
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_orm import create_tables, Users, Black_list, Like_list, insert_into_black_list, \
    insert_into_like_list, insert_into_users
from funk import replay, replay_without_keyboard#, next_person

def next_person(items):  # следующий человек(меняется только после start/next)
    try:
        user_data = next(items)
        first_name, last_name, link = user_data[0].replace('\n', '').split(' ')
        user_name = first_name + ' ' + last_name
    except StopIteration:
        print('КОНЕЦ')
        user1 = VKinder(person_token, gender, city, min_age, max_age, 5)
        my_list = user1.search()
        items = iter(my_list)
        user_data = next(items)
        first_name, last_name, link = user_data[0].replace('\n', '').split(' ')
        user_name = first_name + ' ' + last_name
        #return user_data, user_name, link
    return user_data, user_name, link


if __name__ == '__main__':
    DSN = f"postgresql://{database_username}:{database_password}@localhost:5432/{database_name}"
    engine = sqlalchemy.create_engine(DSN,echo=True)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session_vk = vk_api.VkApi(token=bot_token)  # Подключаем токен и longpoll
    photos = VkUpload(session_vk)  # переменная для загрузки фото
    vk = session_vk.get_api()
    longpoll = VkLongPoll(session_vk)  # сообщаем что хотим исп именно подключение через VkLongPoll

    for event in longpoll.listen():  # Слушаем longpoll(Сообщения)
        attachments = []
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            message = event.text.lower()
            id = event.user_id
            result = [i[0] for i in session.query(Users.id).all()]
            print(f'2 {result = }')
            if id not in result:
                insert_into_users(session, id)
            if message == 'привет':
                replay_without_keyboard(id, 'Укажите пол/город/минимальный возраст/максимальный возраст\n'
                                            'Должно получиться вот так:\nм/Санкт-Петербург/30/40')
            elif len(message.split('/')) == 4:
                replay_without_keyboard(id, 'Сейчас поищу')

                gender, city, min_age, max_age = [i.strip() for i in message.split('/')]
                user1 = VKinder(person_token, gender, city, min_age, max_age, 10)
                my_list = user1.search()
                if not my_list:
                    replay_without_keyboard(id, 'Неверный запрос, попробуйте еще раз')
                else:
                    items = iter(my_list)
                    replay(id, 'start - начать\n'
                               'next - следующий человек\n'
                               'like - добавить в избранное\n'
                               'stop - остановить поиск\n'
                               'list - показать список избранных\n', attachments)
            elif message == 'start' or message == 'next':
                user_data, user_name, link = next_person(items)  # СЛЕДУЮЩИЙ ЧЕЛОВЕК ИЗ СПИСКА
                print(user_data)
                link_list = session.query(Black_list.link).all()
                if link_list:  # если в таблице black_list есть ссылки(она не пустая)
                    link_list = [i[0] for i in session.query(Black_list.link).filter(Black_list.id == id).all()]
                    print(f'{link_list = }')
                    if link not in link_list:  # если ссылки нет в черном списке
                        if len(user_data[1]) != 0:
                            attachments = user_data[1]
                            replay(id, user_data[0], attachments)
                            insert_into_black_list(session, user_name, link, id)
                        else:
                            replay(id, f'{user_data[0]}\nНа странице нет фото')
                            insert_into_black_list(session, user_name, link, id)
                    else:  # если ссылка есть в черном списке
                        while True:
                            user_data, user_name, link = next_person(items)  # СЛЕДУЮЩИЙ ЧЕЛОВЕК ИЗ СПИСКА
                            if link not in link_list:
                                if len(user_data[1]) != 0:
                                    insert_into_black_list(session, user_name, link, id)
                                    attachments = user_data[1]
                                    replay(id, user_data[0], attachments)
                                    break

                else:  # если таблица black_list пустая
                    if len(user_data[1]) != 0:
                        attachments = user_data[1]
                        replay(id, user_data[0], attachments)
                        insert_into_black_list(session, user_name, link, id)
                    else:
                        replay_without_keyboard(id, f'{user_data[0]}\nНа странице нет фото')
                        insert_into_black_list(session, user_name, link, id)
            elif message == 'like':
                link_like_list = [i[0] for i in session.query(Like_list.link).filter(Like_list.id == id).all()]
                if link not in link_like_list:
                    insert_into_like_list(session, user_name, link, id)
                    replay_without_keyboard(id, "Пользователь добавлен в избранное")
                else:
                    replay_without_keyboard(id, "Пользователь уже был добавлен ранее")
            elif message == 'list':
                res = session.query(Like_list.link, Like_list.user_name, ).filter(Like_list.id == id).all()
                print(res)
                link_like_list = [(i[1] + ' ' + i[0]) for i in res]
                print(link_like_list)
                if link_like_list:
                    for el in link_like_list:
                        replay_without_keyboard(id, el)
                else:
                    replay_without_keyboard(id, 'Ваш список пуст')
            elif message == 'stop':
                replay(id, "Чтобы продолжить нажмите START", attachments)
            else:
                replay_without_keyboard(id, 'Меня к такому не готовили\n Лучше напишите привет.')
    session.close()