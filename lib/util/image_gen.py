import textwrap
from random import choice
import re

from PIL import Image, ImageFont, ImageDraw

import eng_to_ipa
import nltk

nltk.download('averaged_perceptron_tagger_eng')
nltk.download('universal_tagset')
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


def create_dictionary_image(term, definition, usage_count):

    phonetics = eng_to_ipa.convert(term)

    if "*" in list(phonetics):
        phonetics = None


    FLAVOR_TEXT = [
                   "No, it's not legal in Scrabble. ",
                   "You are welcome.",
                   "Don't Google that.",
                   "Hilarious.",
                   "Very true!",
                   "You made that up, didn't you? Haha.. that's the point..."
                   ]

    OUTPUT_PATH = "lib/data/image_data/image_cache/output.png"
    FONT_PATH = "lib/data/font_data/roboto/Roboto-Black.ttf"
    FONT_PATH_PHONETIC = "lib/data/font_data/phonetique-font/Phonetique-nRag.ttf"

    image = Image.new('RGB', (400, 300), (46, 103, 138))
    draw = ImageDraw.Draw(image)

    title_font = ImageFont.truetype(FONT_PATH, 20)
    text_font = ImageFont.truetype(FONT_PATH, 15)
    footer_font = ImageFont.truetype(FONT_PATH, 10)
    phonetic_font = ImageFont.truetype(FONT_PATH_PHONETIC, 20)

    # text colors
    title_color = (77, 255, 253)  # light blue
    phonetics_color = (202, 207, 124)  # yellow
    text_color = (255, 255, 255)  # white
    footer_color = (255, 255, 255)  # white
    counter_color = (255, 255, 255)  # white

    # drawing the term
    draw.text((20, 20), term, fill=title_color, font=title_font)

    # taking out characters that are invisible in the phonetics font
    phonetics = _clean_term(term)

    part_of_speech = get_part_of_speech(term)
    draw.text((20, 49), "[" + phonetics + "]", fill=phonetics_color, font=phonetic_font)
    
    if part_of_speech is not None:
        draw.text((25 + phonetic_font.getlength("[" + phonetics + "]"), 50), " |  " + part_of_speech, fill=phonetics_color,
              font=text_font)

    wrapped_definition = textwrap.fill(definition, width=45)

    # drawing the definition/
    draw.text((20, 77), wrapped_definition, fill=text_color, font=text_font)

    # drawing the flavor text
    draw.text((15, 250), choice(FLAVOR_TEXT), fill=footer_color, font=footer_font)

    # drawing the footer
    draw.text((15, 275), "@ PleaseExplain", fill=footer_color, font=footer_font)

    # drawing usage counter
    print(usage_count)
    if isinstance(usage_count, int):
        usage_count_text = f"{usage_count:,}"
        text_width = footer_font.getlength(usage_count_text)
        draw.text((400 - (text_width + 25), 275), usage_count_text, fill=counter_color, font=footer_font)

    return image



def get_part_of_speech(word):
    # Tokenize the word
    tokenized_word = word_tokenize(word)
    print(tokenized_word)

    # Get the part of speech tag
    pos_tagged_word = pos_tag(tokenized_word, tagset='universal')

    # Get the pos code from the first tuple of the list (first word passed)
    # eg. [("run", "VR")] is what's returned
    pos_tag_code = pos_tagged_word[0][1]
    print(pos_tag_code)

    pos_dict =  {"NOUN": "noun",
    "VERB": "verb",
    "ADJ": "adjective",
    "ADV": "adverb",
    "PRON": "pronoun",
    "DET": "determiner",
    "ADP": "adposition", 
    "NUM": "numeral",
    "CONJ": "conjunction",
    "PRT": "particle",
    "INTJ": "interjection",   
    "X": "foreign word",    
    "." : "punctuation"
    }

    return pos_dict.get(pos_tag_code, None)


def _clean_term(term):
    new_term = _collapse_repeats(
        _sub_non_phonetics(
            _strip_non_alphanum(term.lower())))

    return new_term

def _strip_non_alphanum(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s)

def _sub_non_phonetics(s):
    # q, w and x are invisible in the font face
    s = re.sub(r'q', 'k', s)
    s = re.sub(r'x', 'ks', s)
    s = re.sub(r'w', 'u', s)
    return(s)

def _collapse_repeats(s):
    return re.sub(r'(.)\1+', r'\1', s)