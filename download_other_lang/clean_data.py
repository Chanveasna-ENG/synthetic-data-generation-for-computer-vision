import os

# List of files to process (matching the names from the download step)
files = [
    "chinese.txt", "english.txt", "french.txt", "german.txt", 
    "italian.txt", "russian.txt", "spanish.txt", "portuguese.txt", 
    "arabic.txt", "thai.txt", "vietnamese.txt", "lao.txt", 
    "hindi.txt", "burmese.txt", "japanese.txt", "korean.txt"
]

# Directory where files are located (change '.' to 'data/negative_text' if needed)
directory = "negative_text_files"

def clean_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (File not found)")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by comma to get list
        words = content.split(',')
        
        # Clean whitespace and remove empty strings
        # Use set() to remove duplicates automatically
        unique_words = set(word.strip() for word in words if word.strip())
        
        # Sort the words (optional, but helps organization)
        sorted_words = sorted(list(unique_words))

        # Write back to file, joined by newlines
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted_words))
            
        print(f"Processed {filepath}: {len(sorted_words)} unique words.")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Run the loop
if __name__ == "__main__":
    print("Starting cleanup...")
    for filename in files:
        path = os.path.join(directory, filename)
        clean_file(path)
    print("Cleanup complete.")

"""
Starting cleanup...
Processed negative_text_files/chinese.txt: 406588 unique words.
Processed negative_text_files/english.txt: 466434 unique words.
Processed negative_text_files/french.txt: 336528 unique words.
Processed negative_text_files/german.txt: 1707903 unique words.
Processed negative_text_files/italian.txt: 661563 unique words.
Processed negative_text_files/russian.txt: 171552 unique words.
Processed negative_text_files/spanish.txt: 636598 unique words.
Processed negative_text_files/portuguese.txt: 1108873 unique words.
Processed negative_text_files/arabic.txt: 5691498 unique words.
Processed negative_text_files/thai.txt: 71181 unique words.
Processed negative_text_files/vietnamese.txt: 5531 unique words.
Processed negative_text_files/lao.txt: 3230 unique words.
Processed negative_text_files/hindi.txt: 393946 unique words.
Processed negative_text_files/burmese.txt: 3648 unique words.
Processed negative_text_files/japanese.txt: 44492 unique words.
Processed negative_text_files/korean.txt: 366502 unique words.
Cleanup complete.
"""