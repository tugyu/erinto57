import re
from itertools import chain

def parse_magic_squares(file_content):
    """
    Feldolgozza a bemeneti fájl tartalmát, és kinyeri a bűvös összegeket
    és a hozzájuk tartozó négyzeteket.
    """
    magic_squares = []
    current_magic_sum = None
    current_numbers = []

    lines = file_content.splitlines()
    for line in lines:
        sum_match = re.search(r'Bűvös összeg: (\d+)', line)
        if sum_match:
            # Ha már van egy beolvasott négyzet, mentsük el
            if len(current_numbers) == 9:
                square = [current_numbers[i:i+3] for i in range(0, 9, 3)]
                magic_squares.append({"sum": current_magic_sum, "square": square})
            
            # Új adatok beállítása
            current_magic_sum = int(sum_match.group(1))
            current_numbers = []
            
        # Számok keresése a sorokban
        numbers_in_line = re.findall(r'(\d+)', line)
        # Az első szám a sor indexe, azt kihagyjuk, ha a formátum (x, y, z)
        # A mostani fájlban csak számok vannak, így egyszerűsítünk
        if len(numbers_in_line) == 3 and 'Bűvös összeg' not in line:
            current_numbers.extend([int(n) for n in numbers_in_line])
            
    # Az utolsó négyzet elmentése a fájl végén
    if len(current_numbers) == 9:
        square = [current_numbers[i:i+3] for i in range(0, 9, 3)]
        magic_squares.append({"sum": current_magic_sum, "square": square})
        
    return magic_squares

def find_strong_magic_square_optimized(square, magic_sum):
    """
    Optimalizált keresés a felhasználói logika alapján.
    """
    # 1. Ellenőrizzük, hogy a bűvös összeg osztható-e 3-mal
    if magic_sum % 3 != 0:
        return None
    
    center_value = magic_sum // 3
    
    # 2. Megkeressük a leendő középső elem pozícióját
    center_pos = None
    all_numbers = list(chain.from_iterable(square))
    if center_value not in all_numbers:
        return None # Ha a szükséges középső elem nincs is a számok között

    for r in range(3):
        for c in range(3):
            if square[r][c] == center_value:
                center_pos = (r, c)
                break
        if center_pos:
            break
            
    # 3. Átrendezzük a négyzetet, hogy a megtalált szám középre kerüljön
    # Sorcsere
    square[center_pos[0]], square[1] = square[1], square[center_pos[0]]
    
    # Oszlopcsere
    for r in range(3):
        square[r][center_pos[1]], square[r][1] = square[r][1], square[r][center_pos[1]]
    
    # 4. Ellenőrizzük, hogy az átrendezett négyzet erős bűvös négyzet-e
    # Átlók ellenőrzése
    diag1 = sum(square[i][i] for i in range(3))
    diag2 = sum(square[i][2-i] for i in range(3))
    
    if diag1 == magic_sum and diag2 == magic_sum:
        return square
    
    return None

# Fájl tartalmának beolvasása (az előző lépésből)
file_content = """
Bűvös összeg: 57
(23, 15, 19)
(17, 21, 19)
(17, 21, 19)
Bűvös összeg: 57
(23, 17, 17)
(15, 19, 23)
(19, 21, 17)
Bűvös összeg: 57
(15, 25, 17)
(23, 17, 17)
(19, 15, 23)
Bűvös összeg: 57
(15, 23, 19)
(25, 17, 15)
(17, 17, 23)
Bűvös összeg: 57
(23, 15, 19)
(17, 21, 19)
(17, 19, 19)
"""

# Bűvös négyzetek kinyerése
fn="57.txt"
try:
    fd = open(fn, "r")
    file_content=fd.read()
    fd.close()
except:
    print(f"Cannot read file {fn}")

weak_squares = parse_magic_squares(file_content)
print(f"Összesen {len(weak_squares)} db 'gyenge' bűvös négyzetet vizsgálunk.\n")

found_count = 0
for data in weak_squares:
    strong_square = find_strong_magic_square_optimized(data["square"], data["sum"])
    if strong_square:
        found_count += 1
        print("--- TALÁLAT! ---")
        print(f"Bűvös összeg: {data['sum']}")
        print("Eredeti 'gyenge' négyzet:")
        for row in data['square']:
            print(f"  {row}")
        print("\nÁtalakítva 'erős' bűvös négyzetté:")
        for row in strong_square:
            print(f"  {row}")
        print("-" * 16 + "\n")

if found_count == 0:
    print("A fájlban található 'gyenge' bűvös négyzetek egyikéből sem alakítható ki 'erős' bűvös négyzet ezzel a módszerrel.")