import itertools
from collections import defaultdict
import time

def get_canonical_key(grid):
    """
    Legenerálja egy érvényes táblázat egyedi, kanonikus azonosítóját.
    Ez figyelembe veszi a sor-, oszlopcseréket és a transzponálást is.
    """
    # 1. Sorok kanonikus formája
    rows = [tuple(sorted(row)) for row in grid]
    canonical_rows = tuple(sorted(rows))

    # 2. Oszlopok kanonikus formája (a transzponált sorai)
    transposed_grid = list(zip(*grid))
    cols = [tuple(sorted(col)) for col in transposed_grid]
    canonical_cols = tuple(sorted(cols))

    # 3. A kettő közül a kisebb lesz az egyedi kulcs
    return min(canonical_rows, canonical_cols)

def find_strong_magic_grid_optimized(grid, magic_sum):
    """
    Optimalizált keresés a felhasználói logika alapján.
    """
    # 1. Ellenőrizzük, hogy a bűvös összeg osztható-e 3-mal
    if magic_sum % 3 != 0:
        return None
    
    center_value = magic_sum // 3
    
    # 2. Megkeressük a leendő középső elem pozícióját
    center_pos = None
    all_numbers = list(itertools.chain.from_iterable(grid))
    if center_value not in all_numbers:
        return None # Ha a szükséges középső elem nincs is a számok között

    for r in range(3):
        for c in range(3):
            if grid[r][c] == center_value:
                center_pos = (r, c)
                break
        if center_pos:
            break
            
    # 3. Átrendezzük a négyzetet, hogy a megtalált szám középre kerüljön
    # Sorcsere
    grid[center_pos[0]], grid[1] = grid[1], grid[center_pos[0]]
    
    # Oszlopcsere
    for r in range(3):
        grid[r][center_pos[1]], grid[r][1] = grid[r][1], grid[r][center_pos[1]]
    
    # 4. Ellenőrizzük, hogy az átrendezett négyzet erős bűvös négyzet-e
    # Átlók ellenőrzése
    diag1 = sum(grid[i][i] for i in range(3))
    diag2 = sum(grid[i][2-i] for i in range(3))
    
    if diag1 == magic_sum and diag2 == magic_sum:
        return grid
    
    return None



def find_truly_fundamental_solutions():
    """
    Megkeresi az összes, matematikailag korrektül definiált alapmegoldást.
    """
    print("Program indítása a precízen definiált alapmegoldások keresésére...")
    start_time = time.time()

    # Előkészületek (ugyanaz, mint korábban)
    digits = (1, 2, 3, 4, 5)
    all_numbers = sorted([int("".join(map(str, p))) for p in itertools.permutations(digits)])
    sums_map = defaultdict(list)
    for triplet in itertools.combinations(all_numbers, 3):
        s = sum(triplet)
        sums_map[s].append(triplet)
    
    print("Az előkészületek befejeződtek, a keresés indul...")

    # Ebben tároljuk a kanonikus kulcsokat, hogy minden alapmegoldást csak egyszer számoljunk.
    found_solutions_keys = set()
    
    # A kiíratáshoz eltároljuk a megoldásokat összeg szerint.
    solutions_by_sum = defaultdict(list)
    strong_solutions_by_sum = defaultdict(list)
    strong_solutions=0

    for s in sorted(sums_map.keys()):
        triplets_for_s = sums_map[s]
        if len(triplets_for_s) < 3:
            continue

        for r1_tuple, r2_tuple, r3_tuple in itertools.combinations(triplets_for_s, 3):
            current_set = set(r1_tuple) | set(r2_tuple) | set(r3_tuple)
            
            if len(current_set) == 9:
                for p_r2 in itertools.permutations(r2_tuple):
                    for p_r3 in itertools.permutations(r3_tuple):
                        
                        if (r1_tuple[0] + p_r2[0] + p_r3[0] == s and
                            r1_tuple[1] + p_r2[1] + p_r3[1] == s and
                            r1_tuple[2] + p_r2[2] + p_r3[2] == s):
                            
                            # Érvényes táblázatot találtunk!
                            grid = [r1_tuple, p_r2, p_r3]
                            
                            # Kiszámítjuk az egyedi kulcsát.
                            key = get_canonical_key(grid)
                            
                            # Ha ez a kulcs még nem szerepel a listában, hozzáadjuk.
                            if key not in found_solutions_keys:
                                found_solutions_keys.add(key)
                                solutions_by_sum[s].append(grid)
                                ngrid=find_strong_magic_grid_optimized(grid,s)
                                if ngrid:
                                    strong_solutions +=1
                                    strong_solutions_by_sum[s].append(ngrid)

    
    end_time = time.time()

    # Eredmények kiíratása
    print("\n" + "="*50)
    print("A KERESÉS BEFEJEZŐDÖTT")
    print("="*50)
    
    num_solutions = len(found_solutions_keys)
    if num_solutions > 0:
        print(f"\nÖsszesen {num_solutions} darab, precízen definiált alapmegoldás létezik.")
        
        for s, grids in sorted(solutions_by_sum.items()):
            print(f"\n--- Bűvös összeg: {s} ({len(grids)} alapmegoldás) ---")
            for i, grid in enumerate(grids):
                print(f"  {i+1}. Alapmegoldás (egyik variánsa):")
                for row in grid:
                    print(f"    {row}")
    else:
        print("\nA program nem talált egyetlen alapmegoldást sem.")
    num_solutions = len(found_solutions_keys)
        

    if strong_solutions > 0:
        for s, grids in sorted(strong_solutions_by_sum.items()):
            print(f"\n--- Bűvös összeg: {s} ({len(grids)} alapmegoldás) ---")
            for i, grid in enumerate(grids):
                print(f"  {i+1}. Tökéletes alapmegoldás (egyik variánsa):")
                for row in grid:
                    print(f"    {row}")
    else:
        print("\nA program nem talált egyetlen tökéletes alapmegoldást sem.")
        
    print(f"\nA teljes keresés {end_time - start_time:.2f} másodpercet vett igénybe.")

# A program futtatása
find_truly_fundamental_solutions()