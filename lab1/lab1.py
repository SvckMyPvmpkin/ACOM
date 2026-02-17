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
    def __eq__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return self.num == other.num and self.den == other.den
    def __lt__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return self.num * other.den < other.num * self.den
    def __repr__(self):
        return str(self.num) if self.den == 1 else f"{self.num}/{self.den}"

def print_matrix(matrix, message):
    print(f"\n>>> {message}")
    for row in matrix:
        print("  ".join(f"{str(x):>10}" for x in row))
    print("-" * 50)

def load_matrix(filename):
    matrix = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                matrix.append([Fraction(int(x)) for x in line.split()])
    return matrix

def solve_jordan_gauss(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) - 1
    
    print_matrix(matrix, "ИСХОДНАЯ МАТРИЦА")

    pivot_row = 0
    for j in range(cols):
        if pivot_row >= rows: break

        print(f"\n=== РАБОТАЕМ СО СТОЛБЦОМ №{j+1} ===")

        max_val = abs(matrix[pivot_row][j])
        max_idx = pivot_row
        for i in range(pivot_row + 1, rows):
            if abs(matrix[i][j]) > max_val:
                max_val = abs(matrix[i][j])
                max_idx = i

        if max_val == Fraction(0):
            print(f"Столбец {j+1} содержит только нули ниже строки {pivot_row+1}. Пропускаем.")
            continue

        if max_idx != pivot_row:
            print(f"ПЕРЕМЕЩЕНИЕ: Меняем строку {pivot_row+1} со строкой {max_idx+1} (т.к. {matrix[max_idx][j]} — макс. элемент)")
            matrix[pivot_row], matrix[max_idx] = matrix[max_idx], matrix[pivot_row]
            print_matrix(matrix, "Матрица после перестановки строк")

        pivot_element = matrix[pivot_row][j]
        if pivot_element != Fraction(1):
            print(f"ДЕЛЕНИЕ: Делим строку {pivot_row+1} на ведущий элемент {pivot_element}, чтобы получить 1")
            for k in range(j, cols + 1):
                old_val = matrix[pivot_row][k]
                matrix[pivot_row][k] = old_val / pivot_element
                print(f"  R{pivot_row+1}[{k+1}]: {old_val} / {pivot_element} = {matrix[pivot_row][k]}")
            print_matrix(matrix, f"Матрица после нормализации строки {pivot_row+1}")

        for i in range(rows):
            if i != pivot_row:
                factor = matrix[i][j]
                if factor == Fraction(0):
                    continue
                
                print(f"ИСКЛЮЧЕНИЕ: Обнуляем элемент в строке {i+1}, используя коэффициент {factor}")
                print(f"Формула: Строка({i+1}) = Строка({i+1}) - ({factor} * Строка({pivot_row+1}))")
                
                for k in range(j, cols + 1):
                    old_val = matrix[i][k]
                    subtrahend = factor * matrix[pivot_row][k] # То, что вычитаем
                    matrix[i][k] = old_val - subtrahend
                    print(f"  R{i+1}[{k+1}]: {old_val} - ({factor} * {matrix[pivot_row][k]}) = {matrix[i][k]}")
                
                print_matrix(matrix, f"Результат после обработки строки {i+1}")

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

    determined_vars = 0
    var_indices = []
    for j in range(cols):
        ones, zeros, pos = 0, 0, -1
        for i in range(rows):
            if matrix[i][j] == Fraction(1):
                ones += 1
                pos = i
            elif matrix[i][j] == Fraction(0):
                zeros += 1
        if ones == 1 and (ones + zeros) == rows:
            determined_vars += 1
            var_indices.append((j, pos))

    if determined_vars < cols:
        print("\nРЕЗУЛЬТАТ: Система имеет бесконечно много решений.")
    else:
        print("\nРЕЗУЛЬТАТ: Единственное решение:")
        for j, pos in sorted(var_indices):
            print(f"x{j+1} = {matrix[pos][cols]}")

if __name__ == "__main__":
    try:
        data = load_matrix("input.txt")
        solve_jordan_gauss(data)
    except FileNotFoundError:
        print("Создайте файл input.txt!")