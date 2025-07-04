import sqlite3
import random
import database
from helpers.connection import Connect
from pathlib import Path

PATH_TO_DB = Path('vocabulary.db')


def start_test(cursor):
    """Запускает режим тестирования."""
    all_words = database.get_words(cursor)

    if not all_words:
        return

    while True:
        # Выбираем случайное слово
        # TODO: слова не должны выдаваться повторно в рамках одного теста
        english_word, correct_translation = random.choice(list(all_words.items()))

        user_input = input(f"Как переводится '{english_word}'? (или 'стоп'/'exit' для выхода): ").strip().lower()

        if user_input in ('стоп', 'exit'):
            print("Тест завершен.")
            break

        if user_input == correct_translation:
            print("Верно!")
        else:
            print(f"Неправильно. Правильный перевод: '{correct_translation}'.")

        print("-" * 20)  # Разделитель для следующего вопроса


def main_menu(cursor):
    """Главное меню приложения."""
    while True:
        print("\n--- Меню приложения 'Английский для новичков' ---")
        print("1. Добавить слово")
        print("2. Посмотреть слова")
        print("3. Удалить слово")
        print("4. Начать тест")
        print("5. Выход")
        print("-------------------------------------------------")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            english = input("Введите английское слово: ").strip().lower()
            russian = input("Введите русский перевод: ").strip().lower()
            database.add_word(english, russian, cursor)
        elif choice == '2':
            database.view_words(cursor)
        elif choice == '3':
            english = input("Введите английское слово, которое хотите удалить: ").strip().lower()
            database.delete_word(english, cursor)
        elif choice == '4':
            start_test(cursor)
        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 5.")


if __name__ == "__main__":
    with Connect(PATH_TO_DB) as cursor:
        database.init_db(cursor)
        main_menu(cursor)
