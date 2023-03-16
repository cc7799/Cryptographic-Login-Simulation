import html
import os
from typing import List

from database import Database as Db
from database import DB_FILENAME


def initialize_database():
    """
    Creates the database if it does not already exist
    """
    if not os.path.exists(DB_FILENAME):
        Db.setup()


def get_range_selection(options_text: str, option_range: List[int], failure_text: str = None):
    """
    Gets user input and validates that it is an integer and within option_range[min, max], inclusive
    :param options_text: The text to be shown to the user
    :param option_range: The range of values that should be accepted in the form [min, max]
    :param failure_text: The text to be shown to the user if their input fails
    :return: The first valid selected option
    """
    if failure_text is None:
        failure_text = "That is not a valid option. Please enter an integer from " \
                       + str(option_range[0]) + " - " + str(option_range[1]) + "."
    while True:
        try:
            selected = int(input(options_text))
        except ValueError:
            print(failure_text)
        else:
            if option_range[0] <= selected <= option_range[1]:
                return selected
            else:
                print(failure_text)


def get_input(input_text: str):
    """
    Sanitizes text input of html tags
    :param input_text: The string to be sanitized
    :return: The input string with sanitized html tags
    """
    return html.escape(input(input_text))
