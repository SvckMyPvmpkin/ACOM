import math

class Fraction:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ZeroDivisionError("Знаменатель не может быть нулем.")
        common = math.gcd(abs(numerator), abs(denominator))
        sign = 1 if (numerator > 0) == (denominator > 0) else -1
        if numerator == 0: sign = 1
        self.num = abs(numerator) // common * sign
        self.den = abs(denominator) // common

    def __add__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return Fraction(self.num * other.den + other.num * self.den, self.den * other.den)

    def __sub__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return Fraction(self.num * other.den - other.num * self.den, self.den * other.den)

    def __mul__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return Fraction(self.num * other.num, self.den * other.den)

    def __truediv__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        if other.num == 0: raise ZeroDivisionError("Деление на ноль.")
        return Fraction(self.num * other.den, self.den * other.num)

    def __abs__(self): return Fraction(abs(self.num), self.den)
    def __neg__(self): return Fraction(-self.num, self.den)
    def __eq__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return self.num == other.num and self.den == other.den
    def __lt__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return self.num * other.den < other.num * self.den
    def __repr__(self):
        if self.den == 1: return str(self.num)
        return f"{self.num}/{self.den}"

def print_matrix(matrix, message):
    print(f"\n>>> {message}")
    for row in matrix:
        print("  ".join(f"{str(x):>10}" for x in row))
    print("-" * 50)

def load_matrix(filename):
    matrix = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                matrix.append([Fraction(int(x)) for x in line.split()])
    return matrix

def solve_jordan_gauss(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) - 1 
    
    print_matrix(matrix, "ИСХОДНАЯ МАТРИЦА")

    basis_map = {}
    pivot_row = 0

    for j in range(cols):
        if pivot_row >= rows:
            break

        print(f"\n=== АНАЛИЗИРУЕМ СТОЛБЕЦ x{j+1} ===")

        max_val = abs(matrix[pivot_row][j])
        max_idx = pivot_row
        for i in range(pivot_row + 1, rows):
            if abs(matrix[i][j]) > max_val:
                max_val = abs(matrix[i][j])
                max_idx = i

        if max_val == Fraction(0):
            print(f"Столбец x{j+1} не содержит ведущих элементов ниже строки {pivot_row+1}. Пропускаем (это будет свободная переменная).")
            continue

        if max_idx != pivot_row:
            print(f"ПЕРЕМЕЩЕНИЕ: Меняем строку {pivot_row+1} со строкой {max_idx+1} (т.к. {matrix[max_idx][j]} — макс. элемент)")
            matrix[pivot_row], matrix[max_idx] = matrix[max_idx], matrix[pivot_row]
            print_matrix(matrix, "Матрица после перестановки строк")

        pivot_element = matrix[pivot_row][j]
        if pivot_element != Fraction(1):
            print(f"ДЕЛЕНИЕ: Делим строку {pivot_row+1} на {pivot_element}, чтобы получить ведущую единицу")
            for k in range(j, cols + 1):
                matrix[pivot_row][k] = matrix[pivot_row][k] / pivot_element
            print_matrix(matrix, f"Матрица после нормализации строки {pivot_row+1}")

        for i in range(rows):
            if i != pivot_row:
                factor = matrix[i][j]
                if factor == Fraction(0):
                    continue
                
                print(f"ИСКЛЮЧЕНИЕ: Обнуляем x{j+1} в строке {i+1}")
                print(f"Формула: R{i+1} = R{i+1} - ({factor} * R{pivot_row+1})")
                
                for k in range(j, cols + 1):
                    matrix[i][k] = matrix[i][k] - factor * matrix[pivot_row][k]
                
                print_matrix(matrix, f"Результат после обработки строки {i+1}")

        basis_map[j] = pivot_row
        pivot_row += 1

    for i in range(rows):
        is_all_zeros_coeffs = True
        for j in range(cols):
            if matrix[i][j] != Fraction(0):
                is_all_zeros_coeffs = False
                break
        if is_all_zeros_coeffs and matrix[i][cols] != Fraction(0):
            print(f"\nРЕЗУЛЬТАТ: Система не имеет решений (найдено противоречие 0 = {matrix[i][cols]})")
            return

    free_vars = [j for j in range(cols) if j not in basis_map]
    
    if len(basis_map) < cols:
        print("\nРЕЗУЛЬТАТ: Система имеет бесконечно много решений.")
        print("Общее решение (выраженное через свободные переменные):")
        
        for j in range(cols):
            if j in basis_map:
                r = basis_map[j]
                constant = matrix[r][cols]
                
                parts = []
                if constant != Fraction(0) or not any(matrix[r][fv] != Fraction(0) for fv in free_vars):
                    parts.append(str(constant))
                
                for fv in free_vars:
                    coeff = matrix[r][fv]
                    if coeff == Fraction(0):
                        continue
                    
                    move_coeff = -coeff
                    
                    if not parts:
                        sign = "" if move_coeff.num > 0 else "-"
                    else:
                        sign = " + " if move_coeff.num > 0 else " - "
                    
                    abs_c = abs(move_coeff)
                    c_str = "" if abs_c == Fraction(1) else str(abs_c)
                    
                    parts.append(f"{sign}{c_str}x{fv+1}")
                
                ans_str = "".join(parts).replace("+ -", "- ").strip()
                print(f"x{j+1} = {ans_str}")
            else:
                print(f"x{j+1} — свободная переменная")
    else:
        print("\nРЕЗУЛЬТАТ: Единственное решение:")
        sorted_indices = sorted(basis_map.keys())
        for j in sorted_indices:
            r = basis_map[j]
            print(f"x{j+1} = {matrix[r][cols]}")

if __name__ == "__main__":
    try:
        data = load_matrix("mnozh.txt")
        solve_jordan_gauss(data)
    except FileNotFoundError:
        print("Создайте файл input.txt!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        