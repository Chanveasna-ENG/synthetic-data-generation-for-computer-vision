mkdir -p negative_text_files
cd negative_text_files

# Base URL for the raw files
BASE_URL="https://raw.githubusercontent.com/eymenefealtun/all-words-in-all-languages/main"

# Download lists (Mapping generic names to repo specific names)
curl -o chinese.txt "$BASE_URL/Chinese/Chinese.txt"
curl -o english.txt "$BASE_URL/English/English.txt"
curl -o french.txt "$BASE_URL/French/French.txt"
curl -o german.txt "$BASE_URL/German/German.txt"
curl -o italian.txt "$BASE_URL/Italian/Italian.txt"
curl -o russian.txt "$BASE_URL/Russian/Russian.txt"
curl -o spanish.txt "$BASE_URL/Spanish/Spanish.txt"
curl -o portuguese.txt "$BASE_URL/Portuguese/Portuguese.txt"
curl -o arabic.txt "$BASE_URL/Arabic/Arabic.txt"
curl -o thai.txt "$BASE_URL/Thai/Thai.txt"
curl -o vietnamese.txt "$BASE_URL/Vietnamese/Vietnamese.txt"
curl -o lao.txt "$BASE_URL/Lao/Lao.txt"
curl -o hindi.txt "$BASE_URL/Hindi/Hindi.txt"      # Using Hindi for "Indian"
curl -o burmese.txt "$BASE_URL/Myanmar/Myanmar.txt" # Using Myanmar for "Burmese"
curl -o japanese.txt "$BASE_URL/Japanese/Japanese.txt"
curl -o korean.txt "$BASE_URL/Korean/Korean.txt"

echo "Download complete."