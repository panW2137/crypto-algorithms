import subprocess
import time
import random

# --- PARAMETRY PLANU TESTOWEGO ---
MIN_A = -100
MAX_A = 100
MIN_B = -100
MAX_B = 100

PLAINTEXT_PATH = "plaintext.txt"
ENCRYPTED_PATH = "encrypted.txt"
DECRYPTED_PATH = "decrypted.txt"

# --- WIADOMOŚĆ TESTOWA ---
TEST_MESSAGE = """Towarzysze!
Szyfr liniowy służy narodowi i budowie socjalizmu.
1234567890
abc ABC
., 
Niech matematyka i jedność ludu prowadzą nas do wspólnego dobrobytu!
"""

# --- CYTATY PRZEWODNICZĄCEGO XI ---
XI_QUOTES = [
    "„Chiński sen to sen o potędze narodu i szczęściu każdego obywatela.”",
    "„Nowoczesna technologia to fundament siły państwa i dobrobytu narodu.”",
    "„Kiedy nauka służy ludowi, naród staje się niezwyciężony.”",
    "„Każdy programista jest budowniczym nowej ery socjalizmu.”",
    "„Innowacja to najważniejsza siła napędowa rozwoju.”"
]

# --- BANER Z WIZERUNKIEM DUCHOWYM PRZEWODNICZĄCEGO XI ---
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

print(BANNER)
print(random.choice(XI_QUOTES))
print("\n🇨🇳 Wielki Test Szyfru Liniowego Ludowej Republiki Chin 🇨🇳")
print("Pod przewodem Partii – ku doskonałości algorytmicznej!\n")
time.sleep(1)

# --- TWORZENIE TEKSTU JAWNEGO ---
with open(PLAINTEXT_PATH, "w", encoding="utf-8") as f:
    f.write(TEST_MESSAGE)

# --- STATYSTYKA ---
failed_decryptions = []  # szyfrowanie OK, deszyfrowanie błędne
rejected_count = 0       # szyfrowanie zakończone porażką
mismatch_keys = []       # różnice w treści po deszyfracji

print("🔧 Rozpoczynamy Operację 'Czerwony Algorytm'!\n")

# --- WIELKI MARSZ PRZEZ KLUCZE ---
for A in range(MIN_A, MAX_A + 1):
    for B in range(MIN_B, MAX_B + 1):
        # SZYFROWANIE
        enc = subprocess.run(
            ["./linear.out", "e", str(A), str(B), PLAINTEXT_PATH, ENCRYPTED_PATH],
            capture_output=True
        )
        if enc.returncode == 1:
            rejected_count += 1
            continue  # klucz odrzucony – błędny element usunięty z mas

        # DESZYFROWANIE
        dec = subprocess.run(
            ["./linear.out", "d", str(A), str(B), ENCRYPTED_PATH, DECRYPTED_PATH],
            capture_output=True
        )
        if dec.returncode == 1:
            failed_decryptions.append((A, B))
            continue

        # SPRAWDZENIE TEKSTU
        with open(DECRYPTED_PATH, "r", encoding="utf-8") as f:
            decrypted_text = f.read()

        if decrypted_text != TEST_MESSAGE:
            mismatch_keys.append((A, B))

# --- RAPORT KOŃCOWY ---
print("\n==============================")
print("📜 RAPORT KOMISJI CENTRALNEJ DS. ALGORYTMÓW I BEZPIECZEŃSTWA NARODOWEGO")
print("==============================")

print("\n🔴 Klucze (A, B), które zniekształciły wiadomość Narodu:")
if mismatch_keys:
    for key in mismatch_keys:
        print(f"  ✗ A={key[0]}, B={key[1]} – wymaga dalszej analizy przez Akademię Nauk!")
else:
    print("  ✅ Wszystkie klucze zachowały wierność idei ludu!")

print("\n⚙️ Klucze (A, B), które nie sprostały zadaniu przy deszyfrowaniu:")
if failed_decryptions:
    for key in failed_decryptions:
        print(f"  ⚠️ A={key[0]}, B={key[1]} – zidentyfikowano słabość w procesie deszyfracji!")
else:
    print("  💪 Wszystkie jednostki deszyfrujące pracowały z oddaniem!")

print(f"\n🛑 Liczba odrzuconych kluczy (błąd przy szyfrowaniu): {rejected_count}")
print("    (Błędy te zostaną przeanalizowane w duchu samokrytyki i postępu technicznego.)")

print("\n==============================")
print("🎉 ZAKOŃCZONO TEST!")
print("Pod przewodnictwem Xi Jinpinga – ku doskonałości nauki i kodu! 🚩")
print("Niech żyje jedność algorytmów, inżynierów i Partii!")
print("==============================\n")

