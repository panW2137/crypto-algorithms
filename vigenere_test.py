import subprocess
import itertools
import time
import random

# --- LEGALNE ZNAKI ---
alphabet = [
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9',
]

KEY_LENGTH = 3

PLAINTEXT_PATH = "plaintext.txt"
ENCRYPTED_PATH = "encrypted.txt"
DECRYPTED_PATH = "decrypted.txt"

# --- WIADOMOŚĆ TESTOWA ---
TEST_MESSAGE = """Towarzysze
Szyfr Vigenere sluzy narodowi i Partii
1234567890
abc ABC
., 
Niech matematyka i jednosc ludu prowadzi nas do wspolnego dobrobytu
"""

# --- BANER XI ---
XI_QUOTES = [
    "„Chiński sen to sen o potędze narodu i szczęściu każdego obywatela.”",
    "„Nowoczesna technologia to fundament siły państwa i dobrobytu narodu.”",
    "„Kiedy nauka służy ludowi, naród staje się niezwyciężony.”",
    "„Każdy programista jest budowniczym nowej ery socjalizmu.”",
    "„Innowacja to najważniejsza siła napędowa rozwoju.”"
]

BANNER = r"""
⣿⣿⣿⣿⣿⠟⠋⠄⠄⠄⠄⠄⠄⠄⢁⠈⢻⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⡀⠭⢿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⠄⢀⣾⣿⣿⣿⣷⣶⣿⣷⣶⣶⡆⠄⠄⠄⣿⣿⣿⣿
⣿⣿⣿⣿⡇⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠄⠄⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣇⣼⣿⣿⠿⠶⠙⣿⡟⠡⣴⣿⣽⣿⣧⠄⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣾⣿⣿⣟⣭⣾⣿⣷⣶⣶⣴⣶⣿⣿⢄⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⣩⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣹⡋⠘⠷⣦⣀⣠⡶⠁⠈⠁⠄⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣍⠃⣴⣶⡔⠒⠄⣠⢀⠄⠄⠄⡨⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣦⡘⠿⣷⣿⠿⠟⠃⠄⠄⣠⡇⠈⠻⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠟⠋⢁⣷⣠⠄⠄⠄⠄⣀⣠⣾⡟⠄⠄⠄⠄⠉⠙⠻
⡿⠟⠋⠁⠄⠄⠄⢸⣿⣿⡯⢓⣴⣾⣿⣿⡟⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠄⣿⡟⣷⠄⠹⣿⣿⣿⡿⠁⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⣸⣿⡷⡇⠄⣴⣾⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⣿⣿⠃⣦⣄⣿⣿⣿⠇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⢸⣿⠗⢈⡶⣷⣿⣿⡏⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄

 ✯ PRZEWODNICZĄCY XI JINPING CZUWA NAD TESTAMI ✯
"""

# --- TWORZENIE TEKSTU JAWNEGO ---
with open(PLAINTEXT_PATH, "w", encoding="utf-8") as f:
    f.write(TEST_MESSAGE)

print(BANNER)
print(random.choice(XI_QUOTES))
print("\nWielki Test Szyfru Vigenère’a Ludowej Republiki")
print("Pod przewodem Partii – ku doskonałości algorytmicznej!\n")
time.sleep(1)

# --- STATYSTYKA ---
failed_encryptions = []
failed_decryptions = []
mismatch_texts = []

count_failed_enc_overflow = 0
count_failed_dec_overflow = 0
count_mismatch_overflow = 0

# --- WSZYSTKIE KOMBINACJE KLUCZY 5-znakowych ---
total_combinations = len(alphabet) ** KEY_LENGTH
print(f"Szacowana liczba kluczy: {total_combinations}")
progress_step = total_combinations // 10
progress_next = progress_step

processed = 0

for key_tuple in itertools.product(alphabet, repeat=KEY_LENGTH):
    key = ''.join(key_tuple)
    
    # SZYFROWANIE
    enc = subprocess.run(
        ["./vigenere.out", "e", key, PLAINTEXT_PATH, ENCRYPTED_PATH],
        capture_output=True
    )
    
    if enc.returncode == 1:
        if len(failed_encryptions) < 100:
            failed_encryptions.append(f"{key}")
        else:
            count_failed_enc_overflow += 1
        processed += 1
        if processed >= progress_next:
            perc = (processed / total_combinations) * 100
            print(f"Postęp: {int(perc)}%")
            progress_next += progress_step
        continue
    
    # DESZYFROWANIE
    dec = subprocess.run(
        ["./vigenere.out", "d", key, ENCRYPTED_PATH, DECRYPTED_PATH],
        capture_output=True
    )
    
    if dec.returncode == 1:
        if len(failed_decryptions) < 100:
            failed_decryptions.append(f"{key}")
        else:
            count_failed_dec_overflow += 1
        processed += 1
        if processed >= progress_next:
            perc = (processed / total_combinations) * 100
            print(f"Postęp: {int(perc)}%")
            progress_next += progress_step
        continue
    
    # SPRAWDZENIE TEKSTU
    with open(DECRYPTED_PATH, "r", encoding="utf-8") as f:
        decrypted_text = f.read()
    
    if decrypted_text != TEST_MESSAGE:
        if len(mismatch_texts) < 100:
            mismatch_texts.append(f"{key}")
        else:
            count_mismatch_overflow += 1

    processed += 1
    if processed >= progress_next:
        perc = (processed / total_combinations) * 100
        print(f"Postęp: {int(perc)}%")
        progress_next += progress_step

# --- RAPORT KOŃCOWY W DUCHU PARTII ---
print("\n==============================")
print("📜 CENTRALNY RAPORT KOMISJI DS. SZYFRU VIGENÈRE’A LUDOWEJ REPUBLIKI")
print("==============================")

def print_limited_party(title, lst, overflow_count):
    print(f"\n{title}")
    if lst:
        for item in lst:
            print(f"  ✪ {item}")
        if overflow_count:
            print(f"  + {overflow_count} innych nieugiętych błędów do analizy przez Akademię Nauk")
    else:
        print("  ✅ Wszystkie jednostki algorytmiczne pracowały z oddaniem Partii!")

print_limited_party(
    "🔴 Błędy szyfrowania (program nie mógł wykonać zadania) — pełne komendy:",
    failed_encryptions, count_failed_enc_overflow
)

print_limited_party(
    "⚙️ Błędy deszyfrowania (szyfrowanie powiodło się, deszyfrowanie odmówiło współpracy) — klucze:",
    failed_decryptions, count_failed_dec_overflow
)

print_limited_party(
    "🔎 Niezgodności po deszyfrowaniu (tekst różni się od pierwotnego) — klucze:",
    mismatch_texts, count_mismatch_overflow
)

print("\n==============================")
print("🎉 OPERACJA 'CZERWONY ALGORYTM' ZAKOŃCZONA! 🎉")
print("Pod nieustającym przewodnictwem Xi Jinpinga, algorytmy i inżynierowie ludu pracują ku wspólnemu dobrobytowi.")
print("Niech żyje jedność Partii, nauki i technologii! 🚩")
print("==============================\n")
