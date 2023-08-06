import sys
import json


def create_string_question(question, choices=None):
    """ Create a question that has to be answered by a string (part of the choices list if not None).

    Args:
        question: String
        choices: None or list of string elements

    Returns: String

    """
    sys.stdout.write(question + list_to_string(choices) + "\n")
    while True:
        choice = input().lower()
        if choices is None:
            valid = type('')
            if type(choice) == valid:
                return choice
            else:
                sys.stdout.write("Please respond with a string type.\n")
        else:
            if choice in choices:
                return choice
            else:
                sys.stdout.write("Please respond with one of the following: " + list_to_string(choices) + "\n")


def create_float_question(question):
    """ Create a question that has to be answered by a float.

    Args:
        question: String

    Returns: float

    """
    sys.stdout.write(question)
    while True:
        choice = input()
        valid = type('1.0')
        if type(choice) == valid:
            return choice
        else:
            sys.stdout.write("Please respond with a float type.\n")


def create_string_or_float_question(question):
    """ Create a question that has to be answered by a string or a float.

    Args:
        question: String

    Returns: float or string

    """
    sys.stdout.write(question)
    while True:
        choice = input().lower()
        valid_float = type('1.0')
        valid_string = type('')
        if type(choice) == valid_float or type(choice) == valid_string:
            return choice
        else:
            sys.stdout.write("Please respond with a float or string type.\n")


def create_json_question(question):
    """ Create a question that has to be answered by a json.

    Args:
        question: String

    Returns: Boolean

    """
    sys.stdout.write(question)
    while True:
        choice = input().lower()
        try:
            choice = json.loads(choice)
            return choice
        except ValueError:
            sys.stdout.write("Please respond with in a JSON format.\n")


def create_boolean_question(question):
    """ Create a question that has to be answered by yes or no.

    Args:
        question: String

    Returns: Boolean

    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    prompt = " [y/n] "
    sys.stdout.write(question + prompt)
    while True:
        choice = input().lower()
        if choice in valid:
            if not valid[choice]:
                return False
            if valid[choice]:
                return True
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def list_to_string(l):
    """ Parse a list of string elements in a readable format.

    Args:
        l: List

    Returns: String

    """
    str = ""
    if l is None:
        return str
    for elt in l:
        str += elt + ", "
    return str[:-2]