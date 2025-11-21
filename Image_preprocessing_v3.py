import os
from PIL import Image
import xml.etree.ElementTree as ET
from tqdm import tqdm
import torch
from torchvision import transforms
import json

# =====================================================================================
# CONFIGURATION
# =====================================================================================
class Config:
    BASE_DIR = ""
    OUTPUT_DIR = "chunked_data"
    
    # Input directories
    TRAIN_XML_DIR = os.path.join(BASE_DIR, "xml_labels", "train")
    VAL_XML_DIR = os.path.join(BASE_DIR, "xml_labels", "val")
    IMAGE_DIR = os.path.join(BASE_DIR, "images")

    # Target image size
    IMG_HEIGHT = 40
    IMG_WIDTH = 64

    # How many samples to save in each chunk file
    CHUNK_SIZE = 100000

# =====================================================================================
# CUSTOM TRANSFORMER (from train.py)
# =====================================================================================
class ResizeAndPad:
    def __init__(self, height, width, fill=(0, 0, 0)):
        self.height = height
        self.width = width
        self.fill = fill

    def __call__(self, img):
        original_width, original_height = img.size
        target_aspect = self.width / self.height
        original_aspect = original_width / original_height
        if original_aspect > target_aspect:
            new_width = self.width
            new_height = int(new_width / original_aspect)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            new_img = Image.new(img.mode, (self.width, self.height), self.fill)
            paste_y = (self.height - new_height) // 2
            new_img.paste(img, (0, paste_y))
        else:
            new_height = self.height
            new_width = int(new_height * original_aspect)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            new_img = Image.new(img.mode, (self.width, self.height), self.fill)
            paste_x = (self.width - new_width) // 2
            new_img.paste(img, (paste_x, 0))
        return new_img

# =====================================================================================
# MAIN PRE-PROCESSING LOGIC
# =====================================================================================
def preprocess_to_chunks(xml_dir, base_image_dir, output_dir, chunk_size):
    os.makedirs(output_dir, exist_ok=True)
    
    split = os.path.basename(xml_dir)
    transform = transforms.Compose([
        ResizeAndPad(Config.IMG_HEIGHT, Config.IMG_WIDTH),
        transforms.ToTensor() # This converts PIL image to tensor with values [0, 1]
    ])

    images_buffer = []
    labels_buffer = []
    chunk_index = 0
    total_samples = 0

    chunks_metadata = []

    print(f"--- Starting chunk processing for '{split}' split ---")
    xml_files = sorted(os.listdir(xml_dir))

    for xml_file in tqdm(xml_files, desc=f"Processing {split} XMLs"):
        if not xml_file.endswith('.xml'): continue
        xml_path = os.path.join(xml_dir, xml_file)
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            image_name = root.find('image').text
            image_path = os.path.join(base_image_dir, split, image_name)
            if not os.path.exists(image_path): continue

            with Image.open(image_path).convert('RGB') as main_image:
                for word in root.findall('.//word'):
                    text = word.find('text').text
                    if not text: continue
                    
                    bbox = word.find('bbox')
                    coords = (int(bbox.get('x1')), int(bbox.get('y1')), int(bbox.get('x2')), int(bbox.get('y2')))
                    
                    # Crop, resize, pad, and convert to tensor
                    cropped_image = main_image.crop(coords)
                    image_tensor = transform(cropped_image)
                    
                    # Convert to uint8 (0-255) to save space. We will normalize during training.
                    images_buffer.append((image_tensor * 255).to(torch.uint8))
                    labels_buffer.append(text)
                    total_samples += 1

                    # When the buffer is full, save a chunk
                    if len(images_buffer) >= chunk_size:
                        chunk_filename = os.path.join(output_dir, f"{split}_chunk_{chunk_index}.pt")
                        print(f"\nSaving chunk {chunk_index} with {len(images_buffer)} samples to {chunk_filename}...")
                        torch.save({
                            'images': torch.stack(images_buffer),
                            'labels': labels_buffer
                        }, chunk_filename)
                        chunks_metadata.append({
                            "path": chunk_filename,
                            "num_samples": len(images_buffer)
                        })

                        # Clear buffers
                        images_buffer = []
                        labels_buffer = []
                        chunk_index += 1

        except ET.ParseError:
            print(f"Warning: Could not parse {xml_file}, skipping.")
            continue

    # Save any remaining data in the last chunk
    if images_buffer:
        chunk_filename = os.path.join(output_dir, f"{split}_chunk_{chunk_index}.pt")
        print(f"\nSaving final chunk {chunk_index} with {len(images_buffer)} samples to {chunk_filename}...")
        torch.save({
            'images': torch.stack(images_buffer),
            'labels': labels_buffer
        }, chunk_filename)
        chunks_metadata.append({
            "path": chunk_filename,
            "num_samples": len(images_buffer)
        })

    
    manifest_filename = f"{split}_manifest.json"
    manifest_path = os.path.join(output_dir, manifest_filename)
    
    manifest_data = {
        "chunks": chunks_metadata,
        "total_samples": total_samples
    }
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, indent=2)

    print(f"--- Finished processing for '{split}'. Total samples: {total_samples}. ---")


if __name__ == '__main__':
    conf = Config()
    preprocess_to_chunks(conf.TRAIN_XML_DIR, conf.IMAGE_DIR, os.path.join(conf.OUTPUT_DIR, "train"), conf.CHUNK_SIZE)
    preprocess_to_chunks(conf.VAL_XML_DIR, conf.IMAGE_DIR, os.path.join(conf.OUTPUT_DIR, "val"), conf.CHUNK_SIZE)
    print("\nPreprocessing to chunks complete!")
