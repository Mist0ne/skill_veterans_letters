# flake8: noqa: E501
import random
from typing import Dict, List
from . import main_phrases, letters


class Skill:
    def __init__(self) -> None:
        self._sessionStorage: Dict = dict()  # Хранилище данных о сессиях.

    # Функция для непосредственной обработки диалога.
    def handle_dialog(self, req, res) -> None:
        res['version'] = req['version']
        res['session'] = req['session']
        res['response'] = {
            'end_session': False
        }

        user_id = req['session']['user_id']
        original_utterance = req['request']['original_utterance'].lower()

        # Обрабатываем вход в скилл
        if req['session']['new']:
            self._sessionStorage[user_id] = {
                'suggests': ['Дальше']
            }
            random_welcome_phrase = random.choice(main_phrases.welcome_texts)
            random_next_phrase = random.choice(main_phrases.go_next_letter_phrases)
            letters_order = generate_letters_order()

            res['response']['text'] = random_welcome_phrase['text'] + "\n\n" + main_phrases.rules_text['text'] + "\n\n" \
                                      + letters.letters[letters_order[0]]['text'] + "\n\n" + random_next_phrase['text']
            res['response']['tts'] = random_welcome_phrase['tts'] + "\n" + main_phrases.rules_text['tts'] + "\n" + \
                                     letters.letters[letters_order[0]]['tts'] + "\n" + random_next_phrase['tts']
            res['response']['buttons'] = self.get_suggests(user_id)
            res['session_state'] = {'letters_order': letters_order, 'letter_id': 0}
            return

        elif original_utterance in main_phrases.stop_synonims:
            random_phrase = random.choice(main_phrases.exit_texts)
            res['response']['text'] = random_phrase['text']
            res['response']['tts'] = random_phrase['tts']
            res['response']['end_session'] = True
            return

        elif original_utterance in main_phrases.previous_letter_synonims and req['state']['session']['letter_id'] != 0:
            random_next_phrase = random.choice(main_phrases.go_next_letter_phrases)
            res['response']['text'] = letters.letters[req['state']['session']['letters_order'][req['state']['session']['letter_id'] - 1]]['text'] + "\n\n" + \
                                      random_next_phrase['text']
            res['response']['tts'] = letters.letters[req['state']['session']['letters_order'][req['state']['session']['letter_id'] - 1]]['tts'] + "\n" + \
                                      random_next_phrase['tts']
            if req['state']['session']['letter_id'] - 1 == 0:
                self._sessionStorage[user_id] = {
                    'suggests': [
                        'Дальше'
                    ]
                }
            else:
                self._sessionStorage[user_id] = {
                    'suggests': [
                        'Дальше',
                        'Назад'
                    ]
                }
            res['response']['buttons'] = self.get_suggests(user_id)
            res['session_state'] = {'letters_order': req['state']['session']['letters_order'],
                                    'letter_id': req['state']['session']['letter_id'] - 1}
            return

        else:
            random_next_phrase = random.choice(main_phrases.go_next_letter_phrases)
            if req['state']['session']['letter_id'] + 1 == len(letters.letters) - 1:
                new_order = generate_letters_order()
                res['response']['text'] = letters.letters[new_order[0]]['text'] + "\n\n" + \
                                          random_next_phrase['text']
                res['response']['tts'] = letters.letters[new_order[0]]['tts'] + "\n" + \
                                         random_next_phrase['tts']
                self._sessionStorage[user_id] = {
                    'suggests': [
                        'Дальше'
                    ]
                }
                res['session_state'] = {'letters_order': new_order, 'letter_id': 0}
            else:
                res['response']['text'] = letters.letters[req['state']['session']['letters_order'][req['state']['session']['letter_id'] + 1]]['text'] + "\n\n" + \
                                          random_next_phrase['text']
                res['response']['tts'] = letters.letters[req['state']['session']['letters_order'][req['state']['session']['letter_id'] + 1]]['tts'] + "\n" + \
                                         random_next_phrase['tts']
                self._sessionStorage[user_id] = {
                    'suggests': [
                        'Дальше',
                        'Назад'
                    ]
                }
                res['session_state'] = {'letters_order': req['state']['session']['letters_order'],
                                        'letter_id': req['state']['session']['letter_id'] + 1}

            res['response']['buttons'] = self.get_suggests(user_id)
            return

    # Функция возвращает подсказки для ответа.
    def get_suggests(self, user_id: str) -> List:
        session = self._sessionStorage.get(user_id) or {'suggests': []}

        suggests: List = [
            {'title': suggest, 'hide': True}
            for suggest in session['suggests']
        ]

        return suggests


skill: Skill = Skill()


def generate_letters_order():
    order = list(range(len(letters.letters)))
    random.shuffle(order)
    return order
