import os
import requests
import time

# CONFIGURATION
DOWNLOAD_DIR = "nega_background"
NUM_PHOTOS_PER_CATEGORY = 5  # How many photos you want per category

# Categories you asked for
PHOTO_CATEGORIES = ["cat", "construction", "music", "abstract", "nature"]
DOODLE_CATEGORIES = ["cat", "cello", "guitar", "bridge", "saw", "hammer"] 

def download_lorem_flickr(category, count):
    """Downloads random photos from Lorem Flickr (usually text-free stock photos)"""
    category_dir = os.path.join(DOWNLOAD_DIR)
    os.makedirs(category_dir, exist_ok=True)
    
    print(f"--- Downloading {count} photos for '{category}' ---")
    for i in range(count):
        # URL pattern: https://loremflickr.com/{width}/{height}/{keywords}
        url = f"https://loremflickr.com/640/480/{category}/all"
        
        try:
            # We must allow redirects because loremflickr redirects to the actual image source
            response = requests.get(url, allow_redirects=True, timeout=10)
            if response.status_code == 200:
                file_path = os.path.join(category_dir, f"{category}_{i+1}.jpg")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Saved: {file_path}")
            else:
                print(f"Failed to fetch image {i+1}")
            
            # Sleep briefly to be polite to the server
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error: {e}")

def download_quickdraw_doodles(category):
    """Downloads Google Quick Draw datasets (Perfect text-free doodles)"""
    # Quick Draw stores data in .npy files on Google Cloud
    base_url = "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/"
    file_name = f"{category}.npy"
    url = base_url + file_name
    
    output_dir = os.path.join(DOWNLOAD_DIR, "doodles")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, file_name)
    
    if os.path.exists(output_path):
        print(f"dataset {file_name} already exists.")
        return

    print(f"--- Downloading Doodle Dataset: {category} (approx 100MB each) ---")
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded: {file_name}")
            print("NOTE: These are .npy files. You need Python (numpy) to view/extract images from them.")
        else:
            print(f"Category '{category}' not found in Quick Draw dataset.")
    except Exception as e:
        print(f"Error downloading {category}: {e}")

if __name__ == "__main__":
    # 1. Download Photos
    for cat in PHOTO_CATEGORIES:
        download_lorem_flickr(cat, NUM_PHOTOS_PER_CATEGORY)

    # 2. Download Doodles
    #for doodle in DOODLE_CATEGORIES:
    #    download_quickdraw_doodles(doodle)
        
    print("\nDone! Check the 'dataset_no_text' folder.")
