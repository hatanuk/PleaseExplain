import textwrap
from random import choice

from PIL import Image, ImageFont, ImageDraw

import eng_to_ipa
import nltk

nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')
from nltk import pos_tag
from nltk.tokenize import word_tokenize


def scale_font(text, font, image, percent):
    MIN_SIZE = 5
    DECREMENT = 1

    max_width = int((percent / 100) * image.width)
    print(max_width)

    while font.getbbox(text)[0] > max_width:
        if font.size < MIN_SIZE:
            return font
        new_font_size = font.size - DECREMENT
        font = ImageFont.truetype(font.path, size=new_font_size)

    return font


async def create_def_image(definition: str):
    BG_PATH = "lib/data/image_data/blue3.jpeg"
    OUTPUT_PATH = "lib/data/image_data/image_cache/output.jpeg"
    FONT_PATH = "lib/data/font_data/roboto/Roboto-Black.ttf"

    image = Image.open(BG_PATH)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, 60)

    text_width = font.getbbox(definition)[0]
    percent_factor = 50 if text_width < image.width * 0.6 else 70

    font = scale_font(definition, font, image, percent_factor)

    # Draw text in the center
    draw.text(
        (image.width // 2 - font.getbbox(definition)[0] // 2,
         image.height // 4
         ), definition, font=font)

    image.save(OUTPUT_PATH)


def create_dictionary_image(term, definition):

    # Preparing phonetics
    phonetics = eng_to_ipa.convert(term)

    if "*" in list(phonetics):
        phonetics = None


    FLAVOR_TEXT = ["Hey, it's in the dictionary!",
                   "No, it's not legal in Scrabble. ",
                   "You are welcome.",
                   "Eat. Sleep. Define. Explain. Repeat.",
                   "Making sense of your alphabet soup.",
                   "Your daily dose of diction.",
                   "Don't Google that.",
                   "For the verbally voracious.",
                   "Your lexicon lifeline.",
                   "I didn't even know that was a word."
                   ]

    OUTPUT_PATH = "lib/data/image_data/image_cache/output.png"
    FONT_PATH = "lib/data/font_data/roboto/Roboto-Black.ttf"
    FONT_PATH_PHONETIC = "lib/data/font_data/phonetique-font/Phonetique-nRag.ttf"

    # Create a new image with light blue background
    image = Image.new('RGB', (400, 300), (46, 103, 138))
    draw = ImageDraw.Draw(image)

    title_font = ImageFont.truetype(FONT_PATH, 20)
    text_font = ImageFont.truetype(FONT_PATH, 15)
    footer_font = ImageFont.truetype(FONT_PATH, 10)
    phonetic_font = ImageFont.truetype(FONT_PATH_PHONETIC, 20)

    # Text colors
    title_color = (77, 255, 253)  # light blue
    phonetics_color = (202, 207, 124)  # yellow
    text_color = (255, 255, 255)  # white
    footer_color = (255, 255, 255)  # white

    # Draw the term
    draw.text((20, 20), term, fill=title_color, font=title_font)

    # Take out characters that are invisible in the phonetics font
    phonetics = clean_term(term)

    part_of_speech = get_part_of_speech(term)
    draw.text((20, 49), "[" + phonetics + "]", fill=phonetics_color, font=phonetic_font)
    draw.text((25 + phonetic_font.getbbox("[" + phonetics + "]")[0], 50), " |  " + part_of_speech, fill=phonetics_color,
              font=text_font)

    # Wrap the definition text if it's too long
    wrapped_definition = textwrap.fill(definition, width=45)

    # Draw the definition/
    draw.text((20, 77), wrapped_definition, fill=text_color, font=text_font)

    # Draw the flavor text
    draw.text((15, 250), choice(FLAVOR_TEXT), fill=footer_color, font=footer_font)

    # Draw the footer
    draw.text((15, 275), "@ PleaseExplain", fill=footer_color, font=footer_font)

    # Save the image
    image.save(OUTPUT_PATH)


#

def get_part_of_speech(word):
    # Tokenize the word
    tokenized_word = word_tokenize(word)

    # Get the part of speech tag
    pos_tagged_word = pos_tag(tokenized_word)

    # Get the pos code from the first tuple of the list (first word passed)
    # eg. [("run", "VR")] is what's returned
    pos_tag_code = pos_tagged_word[0][1]

    pos_dict = {"J": "adjective",
                "N": "noun",
                "V": "verb",
                "R": "adverb",
                "I": "preposition",
                "C": "conjunction",
                "P": "pronoun",
                "M": "modal",
                "D": "determiner",
                "E": "existential",
                "F": "foreign word",
                "L": "list marker",
                "T": "preposition",
                "U": "interjection",
                "W": "interrogative"}

    return pos_dict.get(pos_tag_code[0], "noun")


def clean_term(term):
    new_term = []
    for char in list(term.lower()):
        if char != "q" and char != "w" and char != "x":
            new_term.append(char)

    return "".join(new_term)
