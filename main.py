import os
import sys
import random
import dotenv
from PIL import ImageDraw, ImageFont, Image
from helper.image_processing import apply_artifact, rand_brightness_contrast, apply_motion_blur, apply_color_jitter
from helper.get_color import get_contrast_color
from helper.get_random import get_random_background, get_random_font, get_random_img_padding, get_random_line_spacing, get_random_word_padding, get_random_font_size
from helper.yolo_coord import convert_to_yolo_format
from helper.utils import read_text_file, save_label, save_xml_label
from helper.xml_generator import generate_xml_content
# from helper.khmer_text_sorter import sort_text2sub
from helper.khnormal import khnormal, testsyl
from helper.get_negative_sample import get_negative_sample, get_negative_sample_text

dotenv.load_dotenv()


# === CONFIGURATION ===

# IMAGE SIZE
image_size_str = os.getenv("IMAGE_SIZE", "775,550")
image_size_list = list(map(int, image_size_str.split(',')))[:2]
IMAGE_SIZE = image_size_list[0], image_size_list[1]

# IMAGE SCALE
MIN_IMG_SCALE = float(os.getenv("MIN_IMG_SCALE", 0.5))
MAX_IMG_SCALE = float(os.getenv("MAX_IMG_SCALE", 2.0))

# DIRECTORIES
FONT_DIR = os.getenv("FONT_DIR", "fonts/")
SAVE_DIR = os.getenv("SAVE_DIR", "synthetic_images/")
LABEL_DIR = os.getenv("LABEL_DIR", "synthetic_labels/")
XML_DIR = os.getenv("XML_DIR", "synthetic_xml_labels/")
BACKGROUND_IMAGES_DIR = os.getenv("BACKGROUND_IMAGES_DIR", "background/")
NEGATIVE_IMAGES_DIR = os.getenv("NEGATIVE_IMAGES_DIR", "nega_background/")

POSSIBILITIES_FOR_END_NOW = float(os.getenv("POSSIBILITIES_FOR_END_NOW", 0.1))
POSSIBILITIES_FOR_NEGATIVE_SAMPLE = float(os.getenv("POSSIBILITIES_FOR_NEGATIVE_SAMPLE", 0.2))
POSSIBILITIES_FOR_COMPLETE_NEGATIVE_SAMPLE = float(os.getenv("POSSIBILITIES_FOR_COMPLETE_NEGATIVE_SAMPLE", 0.1))

# FONT SIZE
MIN_FONT_SIZE = int(os.getenv("MIN_FONT_SIZE", 20))
MAX_FONT_SIZE = int(os.getenv("MAX_FONT_SIZE", 100))

# IMAGE PADDING
MIN_IMG_PADDING = int(os.getenv("MIN_IMG_PADDING", 10))
MAX_IMG_PADDING = int(os.getenv("MAX_IMG_PADDING", 100))

# LINE SPACING
MIN_LINE_SPACING = int(os.getenv("MIN_LINE_SPACING", 6))
MAX_LINE_SPACING = int(os.getenv("MAX_LINE_SPACING", 30))

# WORD PADDING
MIN_WORD_PADDING = int(os.getenv("MIN_WORD_PADDING", 2))
MAX_WORD_PADDING = int(os.getenv("MAX_WORD_PADDING", 10))

# TEXT FILE
TEXT_FILE = os.getenv("TEXT_FILE", "Khmer Dictionary 2022.txt")
TEXT_WORDS = read_text_file(TEXT_FILE)

# PARAGRAPH LENGTH
MIN_PARAG_LENGTH = int(os.getenv("MIN_PARAG_LENGTH", 1))
MAX_PARAG_LENGTH = int(os.getenv("MAX_PARAG_LENGTH", 5000))

# BOUNDING BOX PADDING
BBOX_WIDTH_PADDING = int(os.getenv("BBOX_WIDTH_PADDING", 1))  # Adjust as needed
BBOX_HEIGHT_PADDING = int(os.getenv("BBOX_HEIGHT_PADDING", 2))  # Adjust as needed

# ARTIFACTS
ARTIFACT_POSSIBILITIES = float(os.getenv("ARTIFACT_POSSIBILITIES", 0.5))
jpeg_compression_range_str = os.getenv("JPEG_COMPRESSION_RANGE", "50,90")
JPEG_COMPRESSION_RANGE = tuple(map(int, jpeg_compression_range_str.split(',')))

# MOTION BLUR
MOTION_BLUR_POSSIBILITIES = float(os.getenv("MOTION_BLUR_POSSIBILITIES", 0.3))
motion_blur_kernel_size_str = os.getenv("MOTION_BLUR_KERNEL_SIZE_RANGE", "3,3")
MOTION_BLUR_KERNEL_SIZE_RANGE = tuple(
    map(int, motion_blur_kernel_size_str.split(',')))

# BRIGHTNESS ADJUSTMENT
alpha_range_str = os.getenv("ALPHA_RANGE", "0.8,1.2")
ALPHA_RANGE = tuple(map(float, alpha_range_str.split(',')))

beta_range_str = os.getenv("BETA_RANGE", "-50,50")
BETA_RANGE = tuple(map(int, beta_range_str.split(',')))

# COLOR JITTER SETTINGS
COLOR_JITTER_POSSIBILITES = float(os.getenv("COLOR_JITTER_POSSIBILITES", 0.3))
HUE_DELTA = int(os.getenv("HUE_DELTA", 10))

sat_scale_str = os.getenv("SAT_SCALE", "0.8,1.2")
SAT_SCALE = tuple(map(float, sat_scale_str.split(',')))

val_scale_str = os.getenv("VAL_SCALE", "0.8,1.2")
VAL_SCALE = tuple(map(float, val_scale_str.split(',')))

MAX_ROTATION = float(os.getenv("MAX_ROTATION", "5.0"))

# NEW PADDING, LINE SPACING, WORD PADDING, FONT SIZE, FONT, Y, X
POSSIBILITIES_FOR_NEW_PADDING = float(os.getenv("POSSIBILITIES_FOR_NEW_PADDING", 0.005))
POSSIBILITIES_FOR_NEW_LINE_SPACING = float(os.getenv("POSSIBILITIES_FOR_NEW_LINE_SPACING", 0.005))
POSSIBILITIES_FOR_NEW_WORD_PADDING = float(os.getenv("POSSIBILITIES_FOR_NEW_WORD_PADDING", 0.005))
POSSIBILITIES_FOR_NEW_FONT_SIZE = float(os.getenv("POSSIBILITIES_FOR_NEW_FONT_SIZE", 0.005))
POSSIBILITIES_FOR_NEW_FONT = float(os.getenv("POSSIBILITIES_FOR_NEW_FONT", 0.005))

POSSIBILITIES_FOR_NEW_Y = float(os.getenv("POSSIBILITIES_FOR_NEW_Y", 0.005))
new_y_range_str = os.getenv("NEW_Y_RANGE", "-5,10")
new_y_range_list = list(map(int, new_y_range_str.split(',')))[:2]
NEW_Y_RANGE = new_y_range_list[0], new_y_range_list[1]

POSSIBILITIES_FOR_NEW_X = float(os.getenv("POSSIBILITIES_FOR_NEW_X", 0.005))
new_x_range_str = os.getenv("NEW_X_RANGE", "-5,10")
new_x_range_list = list(map(int, new_x_range_str.split(',')))[:2]
NEW_X_RANGE = new_x_range_list[0], new_x_range_list[1]

POSSIBILITIES_FOR_NEW_COLOR = float(os.getenv("POSSIBILITIES_FOR_NEW_COLOR", 0.005))

# === END CONFIGURATION ===


def create_text_image_with_bbox() -> tuple[Image.Image, list[list[tuple[str, tuple[float, float, float, float]]]], list[tuple[float, float, float, float]]]:
    """Create an image with text and bounding boxes"""

    text_len = random.randint(MIN_PARAG_LENGTH, MAX_PARAG_LENGTH)
    texts = random.choices(TEXT_WORDS, k=text_len)
    # wordlist_len = len(TEXT_WORDS)
    # texts = TEXT_WORDS[(start := random.randint(0, wordlist_len - text_len)) : start + text_len]

    #texts = ["".join(khnormal(text)) for text in texts] # normalize words
    
    texts = khnormal("".join(texts)) # normalized text in subsyllables
    # texts = testsyl("".join(texts))  # segment texts into subsyllables

    bg = get_random_background(IMAGE_SIZE, BACKGROUND_IMAGES_DIR, MIN_IMG_SCALE, MAX_IMG_SCALE)

    drawn_image, lines, annotations = draw_texts_on_image(texts)

    return drawn_image, lines, annotations


def draw_texts_on_image(
    texts: list[str],
) -> tuple[Image.Image, list[list[tuple[str, tuple[float, float, float, float]]]], list[tuple[float, float, float, float]]]:
    """
    Draws a list of words onto `bg`, flowing them in lines
    with fixed `font_size`. Returns the annotated image
    plus a list of (x, y, w, h) for each drawn word.
    """

    x_padding, y_padding = get_random_img_padding(min_img_padding=MIN_IMG_PADDING, max_img_padding=MAX_IMG_PADDING)
    line_spacing = get_random_line_spacing(min_line_spacing=MIN_LINE_SPACING, max_line_spacing=MAX_LINE_SPACING)
    font_size = get_random_font_size(min_font_size=MIN_FONT_SIZE, max_font_size=MAX_FONT_SIZE)
    word_padding = get_random_word_padding(min_word_padding=MIN_WORD_PADDING, max_word_padding=MAX_WORD_PADDING)
    
    bg = get_random_background(IMAGE_SIZE, BACKGROUND_IMAGES_DIR, MIN_IMG_SCALE, MAX_IMG_SCALE) 
    
    # Default to a random Khmer font
    current_font_path = get_random_font(FONT_DIR)
    ori_font = ImageFont.truetype(current_font_path, font_size)

    oov_text = False
    if random.random() < POSSIBILITIES_FOR_COMPLETE_NEGATIVE_SAMPLE:
        if random.choice(["no_text", "text"]) == "text":
            # Full OOV text: Update texts and switch the font path to the negative font
            texts, nega_font_path = get_negative_sample_text(MIN_PARAG_LENGTH, MAX_PARAG_LENGTH)
            current_font_path = nega_font_path 
            ori_font = ImageFont.truetype(current_font_path, font_size)
            oov_text = True
        else:
            # No text: Return empty immediately
            # Using NEGATIVE_IMAGE_DIR if defined, otherwise standard background logic
            # bg = get_random_background(IMAGE_SIZE, NEGATIVE_IMAGE_DIR, MIN_IMG_SCALE, MAX_IMG_SCALE)
            return bg, [], []

    draw = ImageDraw.Draw(bg)
    annotations = []
    current_line = []
    lines = []

    current_x = x_padding
    current_y = y_padding
    max_line_height = 0

    # Pick a text color that contrasts with the background
    text_color = get_contrast_color(bg, 0, 0, bg.width, bg.height)
    
    for word in texts:
        oov_injection = False
        font = ori_font # Start with the current paragraph font

        # --- Random Events ---
        
        # A. Change Font Size
        # We allow this even for OOV text to have size variation, but we must use current_font_path
        if random.random() < POSSIBILITIES_FOR_NEW_FONT_SIZE:
            font_size = get_random_font_size(min_font_size=MIN_FONT_SIZE, max_font_size=MAX_FONT_SIZE)
            ori_font = ImageFont.truetype(current_font_path, font_size)
            font = ori_font

        # B. Change Font Family (ONLY if not already in a Full OOV paragraph)
        if not oov_text and random.random() < POSSIBILITIES_FOR_NEW_FONT:
            current_font_path = get_random_font(FONT_DIR)
            font = ImageFont.truetype(current_font_path, font_size)
            ori_font = font # Update the base font for subsequent words

        # C. Spacing and Positioning
        if random.random() < POSSIBILITIES_FOR_NEW_PADDING:
            x_padding, y_padding = get_random_img_padding(min_img_padding=MIN_IMG_PADDING, max_img_padding=MAX_IMG_PADDING)
        if random.random() < POSSIBILITIES_FOR_NEW_LINE_SPACING:
            line_spacing = get_random_line_spacing(min_line_spacing=MIN_LINE_SPACING, max_line_spacing=MAX_LINE_SPACING)
        if random.random() < POSSIBILITIES_FOR_NEW_WORD_PADDING:
            word_padding = get_random_word_padding(min_word_padding=MIN_WORD_PADDING, max_word_padding=MAX_WORD_PADDING)
        if random.random() < POSSIBILITIES_FOR_NEW_Y:
            current_y += random.randint(*NEW_Y_RANGE)
        if random.random() < POSSIBILITIES_FOR_NEW_X:
            current_x += random.randint(*NEW_X_RANGE)
        if random.random() < POSSIBILITIES_FOR_NEW_COLOR:
            text_color = get_contrast_color(bg, 0, 0, bg.width, bg.height)
        
        # D. Negative Sample Injection (Hijack)
        # Only inject if we aren't already in a full OOV paragraph
        if not oov_text and random.random() < POSSIBILITIES_FOR_NEGATIVE_SAMPLE:
            word, n_font_path = get_negative_sample()
            # Use the specific font for this negative word, do NOT update ori_font
            font = ImageFont.truetype(n_font_path, font_size)
            oov_injection = True
            
        # E. Sudden Stop
        if random.random() < POSSIBILITIES_FOR_END_NOW:
            break

        # Measure this word
        bbox = font.getbbox(word)
        left, top, right, bottom = bbox  # Unpack the bbox values
        text_width = right - left
        text_height = bottom - top

        # If it doesn’t fit on this line, wrap to next
        if current_x + (text_width + word_padding) > (bg.width - x_padding):
            if current_line:
                lines.append(current_line)
                current_line = []        # Save XML content
            current_x = x_padding
            current_y += max_line_height + line_spacing
            max_line_height = 0

        # If no more vertical space, stop early
        if current_y + (top + text_height) > (bg.height - y_padding):  # Adjust with top offset
            break

        draw.text((current_x, current_y), word, font=font, fill=text_color)
        
        # Calculate padded bounding box
        x = current_x + left - BBOX_WIDTH_PADDING  # Expand left
        y = current_y + top - BBOX_HEIGHT_PADDING  # Expand top
        text_width_padded = text_width + 2 * BBOX_WIDTH_PADDING
        text_height_padded = text_height + 2 * BBOX_HEIGHT_PADDING
        
        # labeling
        label_text = "[OOV]" if (oov_text or oov_injection) else word
        word_info = (label_text, (x, y, text_width_padded, text_height_padded))
        
        current_line.append(word_info)
        annotations.append((x, y, text_width_padded, text_height_padded))

        # Advance the cursor with the full width (including right)
        current_x += (right - left) + word_padding  # Use right - left instead of text_width for consistency
        max_line_height = max(max_line_height, (bottom - top))  # Use actual height

    if current_line:
        lines.append(current_line)

    return bg, lines, annotations



if __name__ == "__main__":
    sys.argv = sys.argv[1:]

    _from = int(sys.argv[0])
    _to = int(sys.argv[1])
    _step = int(sys.argv[2])

    for i in range(_from, _to, _step):
        img, lines, bbox = create_text_image_with_bbox()

        img = apply_artifact(img, posssibility=ARTIFACT_POSSIBILITIES,
                             possible_compression=JPEG_COMPRESSION_RANGE)
        img = apply_motion_blur(img, posssibility=MOTION_BLUR_POSSIBILITIES,
                                possible_size=MOTION_BLUR_KERNEL_SIZE_RANGE)
        img = rand_brightness_contrast(
            img, alpha_range=ALPHA_RANGE, beta_range=BETA_RANGE)

        img = apply_color_jitter(img, possibility=COLOR_JITTER_POSSIBILITES, 
                                 hue_delta=HUE_DELTA, sat_scale=SAT_SCALE, val_scale=VAL_SCALE)

        bbox = convert_to_yolo_format(bbox, img.width, img.height, IMAGE_SIZE)
        
        os.makedirs(SAVE_DIR, exist_ok=True)
        os.makedirs(LABEL_DIR, exist_ok=True)
        os.makedirs(XML_DIR, exist_ok=True)

        image_filename = f"img_{i:05d}.png"
        img.save(os.path.join(SAVE_DIR, image_filename))

        label_filename = f"img_{i:05d}.txt"
        save_label(bbox, os.path.join(LABEL_DIR, label_filename))

        xml_content = generate_xml_content(
            lines=lines,
            image_filename=image_filename,
            image_size=img.size
        )

        xml_filename = f"img_{i:05d}.xml"
        save_xml_label(xml_content, os.path.join(XML_DIR, xml_filename))

        print(f"Saved {image_filename} and {label_filename} and {xml_filename}")
