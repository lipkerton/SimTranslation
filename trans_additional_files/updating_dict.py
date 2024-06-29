import pickle

from constants import path_for_main_dict


def updating_dict(rus_key, temporary_dict):
    print(f'Вы выбрали слово: {rus_key}')
    temporary_dict[rus_key] = input('Теперь введите новый перевод: ')
    print('Перевод сохранен.')


ENTER_KEY = input(
    'Введите русское слово, перевод которого'
    'вы хотели бы поменять (или добавить): '
)
saved_dict = open(path_for_main_dict, 'rb')
boss_dict = pickle.load(saved_dict)
temporary_dict = dict()

while ENTER_KEY != 'End':
    updating_dict(ENTER_KEY, temporary_dict)
    ENTER_KEY = input(
        'Введите новое русское слово для перевода'
        'или напишите "End" для завершения программы: '
    )

boss_dict.update(temporary_dict)
saved_dict.close()
saved_dict = open(path_for_main_dict, 'wb')
pickle.dump(boss_dict, saved_dict)
saved_dict.close()
