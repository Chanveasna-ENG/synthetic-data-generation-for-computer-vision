import dotenv
import os
import random
from helper.utils import read_text_file

dotenv.load_dotenv()

NEGATIVE_TEXT_FILE_ARABIC = os.getenv("NEGATIVE_TEXT_FILE_ARABIC", "lang_text/arabic.txt")
NEGATIVE_TEXT_FILE_BURMESE = os.getenv("NEGATIVE_TEXT_FILE_BURMESE", "lang_text/burmese.txt")
NEGATIVE_TEXT_FILE_CHINESE = os.getenv("NEGATIVE_TEXT_FILE_CHINESE", "lang_text/chinese.txt")
NEGATIVE_TEXT_FILE_ENGLISH = os.getenv("NEGATIVE_TEXT_FILE_ENGLISH", "lang_text/english.txt")
NEGATIVE_TEXT_FILE_FRENCH = os.getenv("NEGATIVE_TEXT_FILE_FRENCH", "lang_text/french.txt")
NEGATIVE_TEXT_FILE_GERMAN = os.getenv("NEGATIVE_TEXT_FILE_GERMAN", "lang_text/german.txt")
NEGATIVE_TEXT_FILE_INDIAN = os.getenv("NEGATIVE_TEXT_FILE_INDIAN", "lang_text/hindi.txt")
NEGATIVE_TEXT_FILE_ITALIAN = os.getenv("NEGATIVE_TEXT_FILE_ITALIAN", "lang_text/italian.txt")
NEGATIVE_TEXT_FILE_JAPANESE = os.getenv("NEGATIVE_TEXT_FILE_JAPANESE", "lang_text/japanese.txt")
NEGATIVE_TEXT_FILE_KOREAN = os.getenv("NEGATIVE_TEXT_FILE_KOREAN", "lang_text/korean.txt")
NEGATIVE_TEXT_FILE_LAO = os.getenv("NEGATIVE_TEXT_FILE_LAO", "lang_text/lao.txt")
NEGATIVE_TEXT_FILE_PORTUGUESE = os.getenv("NEGATIVE_TEXT_FILE_PORTUGUESE", "lang_text/portuguese.txt")
NEGATIVE_TEXT_FILE_RUSSIAN = os.getenv("NEGATIVE_TEXT_FILE_RUSSIAN", "lang_text/russian.txt")
NEGATIVE_TEXT_FILE_SPANISH = os.getenv("NEGATIVE_TEXT_FILE_SPANISH", "lang_text/spanish.txt")
NEGATIVE_TEXT_FILE_THAI = os.getenv("NEGATIVE_TEXT_FILE_THAI", "lang_text/thai.txt")
NEGATIVE_TEXT_FILE_VIETNAMESE = os.getenv("NEGATIVE_TEXT_FILE_VIETNAMESE", "lang_text/vietnamese.txt")

NEGATIVE_TEXT_FONT_ARABIC = os.getenv("NEGATIVE_TEXT_FONT_ARABIC", "lang_font/arabic.ttf")
NEGATIVE_TEXT_FONT_BURMESE = os.getenv("NEGATIVE_TEXT_FONT_BURMESE", "lang_font/burmese.ttf")
NEGATIVE_TEXT_FONT_CHINESE = os.getenv("NEGATIVE_TEXT_FONT_CHINESE", "lang_font/chinese.ttf")
NEGATIVE_TEXT_FONT_ENGLISH = os.getenv("NEGATIVE_TEXT_FONT_ENGLISH", "lang_font/english.ttf")
NEGATIVE_TEXT_FONT_FRENCH = os.getenv("NEGATIVE_TEXT_FONT_FRENCH", "lang_font/french.ttf")
NEGATIVE_TEXT_FONT_GERMAN = os.getenv("NEGATIVE_TEXT_FONT_GERMAN", "lang_font/german.ttf")
NEGATIVE_TEXT_FONT_INDIAN = os.getenv("NEGATIVE_TEXT_FONT_INDIAN", "lang_font/hindi.ttf")
NEGATIVE_TEXT_FONT_ITALIAN = os.getenv("NEGATIVE_TEXT_FONT_ITALIAN", "lang_font/italian.ttf")
NEGATIVE_TEXT_FONT_JAPANESE = os.getenv("NEGATIVE_TEXT_FONT_JAPANESE", "lang_font/japanese.ttf")
NEGATIVE_TEXT_FONT_KOREAN = os.getenv("NEGATIVE_TEXT_FONT_KOREAN", "lang_font/korean.ttf")
NEGATIVE_TEXT_FONT_LAO = os.getenv("NEGATIVE_TEXT_FONT_LAO", "lang_font/lao.ttf")
NEGATIVE_TEXT_FONT_PORTUGUESE = os.getenv("NEGATIVE_TEXT_FONT_PORTUGUESE", "lang_font/portuguese.ttf")
NEGATIVE_TEXT_FONT_RUSSIAN = os.getenv("NEGATIVE_TEXT_FONT_RUSSIAN", "lang_font/russian.ttf")
NEGATIVE_TEXT_FONT_SPANISH = os.getenv("NEGATIVE_TEXT_FONT_SPANISH", "lang_font/spanish.ttf")
NEGATIVE_TEXT_FONT_THAI = os.getenv("NEGATIVE_TEXT_FONT_THAI", "lang_font/thai.ttf")
NEGATIVE_TEXT_FONT_VIETNAMESE = os.getenv("NEGATIVE_TEXT_FONT_VIETNAMESE", "lang_font/vietnamese.ttf")

lang_list = [
    (NEGATIVE_TEXT_FILE_ARABIC, NEGATIVE_TEXT_FONT_ARABIC),
    (NEGATIVE_TEXT_FILE_BURMESE, NEGATIVE_TEXT_FONT_BURMESE),
    (NEGATIVE_TEXT_FILE_CHINESE, NEGATIVE_TEXT_FONT_CHINESE),
    (NEGATIVE_TEXT_FILE_ENGLISH, NEGATIVE_TEXT_FONT_ENGLISH),
    (NEGATIVE_TEXT_FILE_FRENCH, NEGATIVE_TEXT_FONT_FRENCH),
    (NEGATIVE_TEXT_FILE_GERMAN, NEGATIVE_TEXT_FONT_GERMAN),
    (NEGATIVE_TEXT_FILE_INDIAN, NEGATIVE_TEXT_FONT_INDIAN),
    (NEGATIVE_TEXT_FILE_ITALIAN, NEGATIVE_TEXT_FONT_ITALIAN),
    (NEGATIVE_TEXT_FILE_JAPANESE, NEGATIVE_TEXT_FONT_JAPANESE),
    (NEGATIVE_TEXT_FILE_KOREAN, NEGATIVE_TEXT_FONT_KOREAN),
    (NEGATIVE_TEXT_FILE_LAO, NEGATIVE_TEXT_FONT_LAO),
    (NEGATIVE_TEXT_FILE_PORTUGUESE, NEGATIVE_TEXT_FONT_PORTUGUESE),
    (NEGATIVE_TEXT_FILE_RUSSIAN, NEGATIVE_TEXT_FONT_RUSSIAN),
    (NEGATIVE_TEXT_FILE_SPANISH, NEGATIVE_TEXT_FONT_SPANISH),
    (NEGATIVE_TEXT_FILE_THAI, NEGATIVE_TEXT_FONT_THAI),
    (NEGATIVE_TEXT_FILE_VIETNAMESE, NEGATIVE_TEXT_FONT_VIETNAMESE)
]

def get_negative_sample_text(minn, maxx):
    text_file, font = random.choice(lang_list)
    text_len = random.randint(minn, maxx)
    text_words = read_text_file(text_file)
    text = random.choices(text_words, k=text_len)
    return text, font

def get_negative_sample():
    text_file, font = random.choice(lang_list)
    text_words = read_text_file(text_file)
    word = random.choice(text_words)
    return word, font