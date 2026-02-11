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
        if other.num == 0: raise ZeroDivisionError("Деление на ноль (дробь с числителем 0).")
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
    print(f"\n{message}")
    for row in matrix:
        print("  ".join(f"{str(x):>8}" for x in row))

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
    
    print_matrix(matrix, "ИСХОДНАЯ МАТРИЦА:")

    pivot_row = 0
    for j in range(cols):
        if pivot_row >= rows: break

        max_val = abs(matrix[pivot_row][j])
        max_idx = pivot_row
        for i in range(pivot_row + 1, rows):
            if abs(matrix[i][j]) > max_val:
                max_val = abs(matrix[i][j])
                max_idx = i

        if max_val == Fraction(0):
            continue

        matrix[pivot_row], matrix[max_idx] = matrix[max_idx], matrix[pivot_row]

        pivot_element = matrix[pivot_row][j]
        matrix[pivot_row] = [x / pivot_element for x in matrix[pivot_row]]

        for i in range(rows):
            if i != pivot_row:
                factor = matrix[i][j]
                matrix[i] = [matrix[i][k] - factor * matrix[pivot_row][k] for k in range(cols + 1)]
        
        pivot_row += 1
        print_matrix(matrix, f"ШАГ {pivot_row} (исключение по столбцу {j+1}):")

    for i in range(rows):
        is_all_zeros_coeffs = True
        for j in range(cols):
            if matrix[i][j] != Fraction(0):
                is_all_zeros_coeffs = False
                break
        
        if is_all_zeros_coeffs and matrix[i][cols] != Fraction(0):
            print("\nРЕЗУЛЬТАТ: Система не имеет решений (найдено противоречие 0 = " + str(matrix[i][cols]) + ").")
            return

    determined_vars = 0
    var_indices = []
    for j in range(cols):
        ones = 0
        one_pos = -1
        zeros = 0
        for i in range(rows):
            if matrix[i][j] == Fraction(1):
                ones += 1
                one_pos = i
            elif matrix[i][j] == Fraction(0):
                zeros += 1

        if ones == 1 and (ones + zeros) == rows:
            determined_vars += 1
            var_indices.append((j, one_pos))

    if determined_vars < cols:
        print("\nРЕЗУЛЬТАТ: Система имеет бесконечно много решений (не все переменные определены).")
    else:
        print("\nРЕЗУЛЬТАТ: Единственное решение:")
        for j, pos in sorted(var_indices):
            print(f"x{j+1} = {matrix[pos][cols]}")


if __name__ == "__main__":
    try:
        data = load_matrix("input.txt")
        solve_jordan_gauss(data)
    except FileNotFoundError:
        print("Создайте файл input.txt с данными системы!")