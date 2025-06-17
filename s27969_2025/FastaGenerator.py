import random  # do generowania wartości losowych
import argparse  # do obsługi linii poleceń
import re  # do zabezpieczenia nazwy pliku przed niebezpiecznymi znakami
import sys  # do zakończenia programu w razie błędnych danych

# Funkcja: generuje sekwencję DNA o zadanej długości, nie wliczając w nią imienia
# ORIGINAL:
# def generate_sequence(length):
#     nucleotides = ['A', 'C', 'G', 'T']
#     return ''.join(random.choice(nucleotides) for _ in range(length))
# MODIFIED (oddzielna zmienna dla sekwencji i rozszerzona walidacja długości):
def generate_sequence(length):  # length: liczba nukleotydów do wygenerowania
    if length <= 0:
        print("Błąd: długość sekwencji musi być większa od zera.")
        sys.exit(1)
    nucleotides = ['A', 'C', 'G', 'T']  # możliwe nukleotydy
    seq = ''.join(random.choice(nucleotides) for _ in range(length))
    return seq

# Funkcja: wstawia imię w losowym miejscu sekwencji, bez zmiany statystyk
# ORIGINAL:
# def insert_name(seq, name):
#     pos = random.randint(0, len(seq))
#     return seq[:pos] + name + seq[pos:]
# MODIFIED (zabezpieczenie pustego imienia):
def insert_name(seq, name):
    if not name:
        return seq  # jeśli imię puste, nie wstawiamy nic
    pos = random.randint(0, len(seq))
    return seq[:pos] + name + seq[pos:]

# Funkcja: oblicza udział procentowy każdego nukleotydu i stosunek CG do AT
def compute_stats(seq):
    counts = {n: seq.count(n) for n in 'ACGT'}  # zliczanie nukleotydów
    total = sum(counts.values()) or 1  # unikamy dzielenia przez zero
    freqs = {n: counts[n] / total * 100 for n in counts}
    cg = counts['C'] + counts['G']
    at = counts['A'] + counts['T'] or 1
    ratio_cg = cg / (at) * 100
    return freqs, ratio_cg

# ---- Główna część programu ----
def main():
    """
    Parsuje argumenty, generuje sekwencję, wstawia imię, liczy statystyki i zapisuje FASTA.
    """
    parser = argparse.ArgumentParser(description='Generator sekwencji DNA w formacie FASTA')
    parser.add_argument('-l', '--length', type=int, help='długość sekwencji DNA', required=False)
    parser.add_argument('-n', '--name', type=str, help='Twoje imię do wstawienia', required=False)
    parser.add_argument('-i', '--id', dest='seq_id', type=str, help='ID sekwencji', required=False)
    parser.add_argument('-d', '--description', type=str, help='Opis sekwencji', required=False)
    parser.add_argument('-s', '--seed', type=int, help='ziarno RNG (opcjonalne)', required=False)
    args = parser.parse_args()

    # Ustawianie ziarna RNG (ULEPSZENIE 1: powtarzalność wyników)
    if args.seed is not None:
        # ORIGINAL:
        # random.seed()
        # MODIFIED (zapewnienie deterministycznej powtarzalności):
        random.seed(args.seed)

    # Pobieranie długości sekwencji
    if args.length is None:
        try:
            length = int(input("Podaj długość sekwencji: "))
        except ValueError:
            print("Błąd: podano niepoprawną liczbę.")
            sys.exit(1)
    else:
        length = args.length

    # Pobieranie ID sekwencji
    if args.seq_id is None:
        seq_id = input("Podaj ID sekwencji: ").strip()
    else:
        seq_id = args.seq_id.strip()
    # ORIGINAL:
    # (brak walidacji)
    # MODIFIED (tylko [A-Za-z0-9_-]):
    if not re.match(r'^[A-Za-z0-9_-]+$', seq_id):
        print("Błąd: ID może zawierać tylko litery, cyfry, '_' i '-'.")
        sys.exit(1)
      
    # Walidacja ID (tylko znaki alfanumeryczne, podkreślenia i myślniki)
    if not re.match(r'^[A-Za-z0-9_-]+$', seq_id):
        print("Błąd: ID może zawierać tylko litery, cyfry, '_' i '-'.")
        sys.exit(1)

    # Pobieranie opisu sekwencji
    if args.description is None:
        description = input("Podaj opis sekwencji: ").strip()
    else:
        description = args.description.strip()

    # Pobieranie imienia do wstawienia
    if args.name is None:
        name = input("Podaj imię: ").strip()
    else:
        name = args.name.strip()

    # Generowanie sekwencji i wstawienie imienia
    seq = generate_sequence(length)  # sekwencja z nukleotydów
    fasta_seq = insert_name(seq, name)  # dodanie imienia w losowym miejscu

    # Obliczanie statystyk (imiona nie są nukleotydami, więc nie wpływają na stats)
    freqs, ratio_cg = compute_stats(seq)

    # Przygotowanie nazwy pliku i zabezpieczenie przed niebezpiecznymi znakami
    safe_id = re.sub(r'[^A-Za-z0-9_-]', '_', seq_id)
    filename = f"{safe_id}.fasta"

    # Zapis do pliku FASTA
    with open(filename, 'w', encoding='utf-8') as out:
        out.write(f">{seq_id} {description}\n")  # nagłówek FASTA
        out.write(fasta_seq + "\n")  # sekwencja z imieniem

    # Wyświetlenie informacji o pliku i statystyk
    print(f"Sekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    for n, pct in freqs.items():  # iteracja po nukleotydach
        print(f"{n}: {pct:.1f}%")
    print(f"%CG: {ratio_cg:.1f}")
