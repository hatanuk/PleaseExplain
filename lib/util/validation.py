
import discord

class Validator:

    ACCEPTED_CHAR = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
                 '[', '{', ']', '}', '\\', '|', ';', ':', '\'', '"', ',', '<', '.', '>', '/', '?']

    @staticmethod
    def validate_string(string):
    # Checks if given string contains only letters, numbers or accepted characters. returns False if valid input
    # Otherwise returns the erroneous character
        index = 0
        for char in string:
            index += 1
            if not char.isalnum() and not char.isdigit() and char != " " and char not in Validator.ACCEPTED_CHAR:
                return index
        return False

