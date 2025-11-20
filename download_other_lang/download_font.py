import requests
import zipfile
import io
import os

# 1. Map ENV Variables to the specific folder names in the Google Fonts GitHub Repo
# Repository Structure: fonts-main/ofl/[font_directory_name]/[FontName]-Regular.ttf
REPO_MAP = {
    "ARABIC": "notosansarabic",
    "BURMESE": "notosansmyanmar",
    "CHINESE": "notosanssc",        # Simplified Chinese
    "ENGLISH": "notosans",          # Base Latin/English
    "FRENCH": "notosans",           # Base Latin/French
    "GERMAN": "notosans",           # Base Latin/German
    "INDIAN": "notosansdevanagari", # Hindi
    "ITALIAN": "notosans",          # Base Latin/Italian
    "JAPANESE": "notosansjp",
    "KOREAN": "notosanskr",
    "LAO": "notosanslao",
    "PORTUGUESE": "notosans",       # Base Latin/Portuguese
    "RUSSIAN": "notosans",          # Base Latin/Russian (Cyrillic)
    "SPANISH": "notosans",          # Base Latin/Spanish
    "THAI": "notosansthai",
    "VIETNAMESE": "notosans"        # Base Latin/Vietnamese
}

# 2. Define Output Paths
TARGETS = [
    ("ARABIC", "lang_font/arabic.ttf"),
    ("BURMESE", "lang_font/burmese.ttf"),
    ("CHINESE", "lang_font/chinese.ttf"),
    ("ENGLISH", "lang_font/english.ttf"),
    ("FRENCH", "lang_font/french.ttf"),
    ("GERMAN", "lang_font/german.ttf"),
    ("INDIAN", "lang_font/hindi.ttf"),
    ("ITALIAN", "lang_font/italian.ttf"),
    ("JAPANESE", "lang_font/japanese.ttf"),
    ("KOREAN", "lang_font/korean.ttf"),
    ("LAO", "lang_font/lao.ttf"),
    ("PORTUGUESE", "lang_font/portuguese.ttf"),
    ("RUSSIAN", "lang_font/russian.ttf"),
    ("SPANISH", "lang_font/spanish.ttf"),
    ("THAI", "lang_font/thai.ttf"),
    ("VIETNAMESE", "lang_font/vietnamese.ttf"),
]

GITHUB_ZIP_URL = "https://github.com/google/fonts/archive/main.zip"

def stream_extract_fonts():
    print(f"🔌 Connecting to GitHub Archive (this may take a moment)...")
    
    try:
        # Stream the download to avoid loading 1GB into RAM
        r = requests.get(GITHUB_ZIP_URL, stream=True)
        r.raise_for_status()

        # We use io.BytesIO to create a file-like object in memory
        # Note: Python's zipfile requires the file to be seekable, so we download chunks
        # For a 1GB file, downloading to a temp file is safer than RAM.
        
        import tempfile
        with tempfile.TemporaryFile() as tmp:
            print("⬇️  Downloading repo stream to temporary file...")
            for chunk in r.iter_content(chunk_size=8192):
                tmp.write(chunk)
            
            print("📦 Scan and Extract...")
            tmp.seek(0)
            
            with zipfile.ZipFile(tmp) as z:
                all_files = z.namelist()
                
                for env_key, output_path in TARGETS:
                    folder_name = REPO_MAP[env_key]
                    
                    # Construct the search path inside the zip
                    # Pattern: fonts-main/ofl/notosans/NotoSans-Regular.ttf
                    # We look for a file that matches the folder and ends in Regular.ttf
                    
                    # Filter for files in the specific directory
                    candidates = [f for f in all_files if f"ofl/{folder_name}/" in f and f.endswith("-Regular.ttf")]
                    
                    # If no Regular found, try finding ANY .ttf in that folder (fallback)
                    if not candidates:
                        candidates = [f for f in all_files if f"ofl/{folder_name}/" in f and f.endswith(".ttf")]
                    
                    if candidates:
                        # Pick the shortest name (usually "NotoSans-Regular.ttf" vs "NotoSans-Condensed.ttf")
                        candidates.sort(key=len)
                        source_path = candidates[0]
                        
                        # Extraction
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        with z.open(source_path) as source, open(output_path, "wb") as target:
                            target.write(source.read())
                        print(f"✅ Extracted: {source_path} -> {output_path}")
                    else:
                        print(f"❌ Error: Could not find font for {env_key} (Folder: {folder_name})")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    stream_extract_fonts()


"""
🔥 python3 download_font.py
🔌 Connecting to GitHub Archive (this may take a moment)...
⬇️  Downloading repo stream to temporary file...
📦 Scan and Extract...
✅ Extracted: fonts-main/ofl/notosansarabic/NotoSansArabic[wdth,wght].ttf -> lang_font/arabic.ttf
✅ Extracted: fonts-main/ofl/notosansmyanmar/NotoSansMyanmar[wdth,wght].ttf -> lang_font/burmese.ttf
✅ Extracted: fonts-main/ofl/notosanssc/NotoSansSC[wght].ttf -> lang_font/chinese.ttf
✅ Extracted: fonts-main/ofl/notosans/NotoSans[wdth,wght].ttf -> lang_font/english.ttf
✅ Extracted: fonts-main/ofl/notosans/NotoSans[wdth,wght].ttf -> lang_font/french.ttf
✅ Extracted: fonts-main/ofl/notosans/NotoSans[wdth,wght].ttf -> lang_font/german.ttf
✅ Extracted: fonts-main/ofl/notosansdevanagari/NotoSansDevanagari[wdth,wght].ttf -> lang_font/hindi.ttf
✅ Extracted: fonts-main/ofl/notosans/NotoSans[wdth,wght].ttf -> lang_font/italian.ttf
✅ Extracted: fonts-main/ofl/notosansjp/NotoSansJP[wght].ttf -> lang_font/japanese.ttf
✅ Extracted: fonts-main/ofl/notosanskr/NotoSansKR[wght].ttf -> lang_font/korean.ttf
✅ Extracted: fonts-main/ofl/notosanslao/NotoSansLao[wdth,wght].ttf -> lang_font/lao.ttf
✅ Extracted: fonts-main/ofl/notosans/NotoSans[wdth,wght].ttf -> lang_font/portuguese.ttf
✅ Extracted: fonts-main/ofl/notosans/NotoSans[wdth,wght].ttf -> lang_font/russian.ttf
✅ Extracted: fonts-main/ofl/notosans/NotoSans[wdth,wght].ttf -> lang_font/spanish.ttf
✅ Extracted: fonts-main/ofl/notosansthai/NotoSansThai[wdth,wght].ttf -> lang_font/thai.ttf
✅ Extracted: fonts-main/ofl/notosans/NotoSans[wdth,wght].ttf -> lang_font/vietnamese.ttf


"""
