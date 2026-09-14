
def _build_grid(key: str) -> list:
    key = key.upper().replace("J", "I")  # fusionne I/J
    seen = set()
    grid_letters = []

    # 1. Ajoute les lettres de la clé, sans doublons
    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            grid_letters.append(char)

    # 2. Complète avec le reste de l'alphabet (sans J)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            grid_letters.append(char)

    # 3. Transforme la liste plate en grille 5x5
    grid = [grid_letters[i:i + 5] for i in range(0, 25, 5)]
    return grid


def _find_position(grid: list, letter: str) -> tuple:
    """Trouve la position (ligne, colonne) d'une lettre dans la grille."""
    for row in range(5):
        for col in range(5):
            if grid[row][col] == letter:
                return row, col
    return None


def _prepare_text(text: str) -> list:
    """Découpe le texte en paires, en gérant les lettres doublées et l'ajout de X."""
    text = text.upper().replace("J", "I")
    letters = [char for char in text if char.isalpha()]

    pairs = []
    i = 0
    while i < len(letters):
        a = letters[i]
        if i + 1 < len(letters):
            b = letters[i + 1]
            if a == b:
                pairs.append((a, "X"))  # double lettre → insère X
                i += 1
            else:
                pairs.append((a, b))
                i += 2
        else:
            pairs.append((a, "X"))  # lettre seule à la fin → complète avec X
            i += 1
    return pairs

def playfair_encrypt(text: str, key: str) -> str:
    grid = _build_grid(key)
    pairs = _prepare_text(text)
    result = ""

    for a, b in pairs:
        row_a, col_a = _find_position(grid, a)
        row_b, col_b = _find_position(grid, b)

        if row_a == row_b:
            # même ligne → décale à droite
            result += grid[row_a][(col_a + 1) % 5]
            result += grid[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            # même colonne → décale vers le bas
            result += grid[(row_a + 1) % 5][col_a]
            result += grid[(row_b + 1) % 5][col_b]
        else:
            # rectangle → échange les colonnes
            result += grid[row_a][col_b]
            result += grid[row_b][col_a]

    return result


def playfair_decrypt(text: str, key: str) -> str:
    grid = _build_grid(key)
    pairs = [(text[i], text[i + 1]) for i in range(0, len(text), 2)]
    result = ""

    for a, b in pairs:
        row_a, col_a = _find_position(grid, a)
        row_b, col_b = _find_position(grid, b)

        if row_a == row_b:
            result += grid[row_a][(col_a - 1) % 5]
            result += grid[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            result += grid[(row_a - 1) % 5][col_a]
            result += grid[(row_b - 1) % 5][col_b]
        else:
            result += grid[row_a][col_b]
            result += grid[row_b][col_a]

    return result
