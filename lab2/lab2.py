import math
from itertools import combinations
import copy

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

    def __eq__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return self.num == other.num and self.den == other.den

    def __repr__(self):
        return str(self.num) if self.den == 1 else f"{self.num}/{self.den}"

def print_matrix(matrix, message=""):
    if message:
        print(f"--- {message} ---")
    for row in matrix:
        print("  ".join(f"{str(x):>10}" for x in row))
    print("-" * 50)

def compute_rank(matrix_in):
    A = copy.deepcopy(matrix_in)
    m = len(A)
    n = len(A[0])
    row = 0
    for col in range(n):
        if row >= m: break
        pivot = -1
        for i in range(row, m):
            if A[i][col].num != 0:
                pivot = i
                break
        if pivot == -1: continue
        
        A[row], A[pivot] = A[pivot], A[row]
        div = A[row][col]
        for j in range(col, n):
            A[row][j] = A[row][j] / div
        
        for i in range(m):
            if i != row:
                factor = A[i][col]
                if factor.num != 0:
                    for j in range(col, n):
                        A[i][j] = A[i][j] - factor * A[row][j]
        row += 1
    
    rank = 0
    for i in range(m):
        if any(x.num != 0 for x in A[i]):
            rank += 1
    return rank

def get_basic_solution(original_matrix, basis_indices):
    matrix = copy.deepcopy(original_matrix)
    m = len(matrix)
    n_vars = len(matrix[0]) - 1
    
    for step, col_idx in enumerate(basis_indices):
        pivot_row = -1
        for r in range(step, m):
            if matrix[r][col_idx].num != 0:
                pivot_row = r
                break 
        
        if pivot_row == -1:
            return None # Эти столбцы зависимы

        matrix[step], matrix[pivot_row] = matrix[pivot_row], matrix[step]
        
        pivot_val = matrix[step][col_idx]
        for c in range(len(matrix[0])):
            matrix[step][c] = matrix[step][c] / pivot_val
        
        for r in range(m):
            if r != step:
                factor = matrix[r][col_idx]
                if factor.num != 0:
                    for c in range(len(matrix[0])):
                        matrix[r][c] = matrix[r][c] - (factor * matrix[step][c])
    
    for r in range(len(basis_indices), m):
        if matrix[r][n_vars].num != 0:
            return None 

    solution = [Fraction(0)] * n_vars
    for i, col_idx in enumerate(basis_indices):
        solution[col_idx] = matrix[i][n_vars]
    
    return solution, matrix

def solve_all_bases(matrix):
    m = len(matrix)
    n_vars = len(matrix[0]) - 1
    
    print_matrix(matrix, "ИСХОДНАЯ МАТРИЦА")
    
    rank_augmented = compute_rank(matrix)
    
    coeff_matrix = [row[:-1] for row in matrix]
    rank_coeff = compute_rank(coeff_matrix)
    
    print(f"Ранг матрицы коэффициентов (rA): {rank_coeff}")
    print(f"Ранг расширенной матрицы (rAb): {rank_augmented}")
    
    if rank_coeff != rank_augmented:
        print("Система несовместна (rA != rAb). Базисных решений нет.")
        return

    r = rank_coeff
    if r == 0:
        print("Ранг равен 0. Система тривиальна.")
        return

    all_combinations = list(combinations(range(n_vars), r))
    print(f"Размер базиса: {r}. Всего комбинаций: {len(all_combinations)}\n")

    count = 0
    for combo in all_combinations:
        basis_display = ", ".join([f"x{i+1}" for i in combo])
        print(f"ПРОВЕРКА БАЗИСА: ({basis_display})")
        
        result = get_basic_solution(matrix, combo)
        
        if result:
            sol, final_m = result
            count += 1
            print_matrix(final_m, f"Матрица для базиса {basis_display}")
            res_str = [f"x{i+1} = {sol[i]}" for i in range(n_vars)]
            print(f"РЕШЕНИЕ: {', '.join(res_str)}")
        else:
            print("Набор столбцов зависим или решение не существует.")
        print("="*40)

    print(f"\nИТОГО найдено базисных решений: {count}")

def load_matrix(filename):
    matrix = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        first_line = lines[0].split()
        
        if len(first_line) == 2:
            data_lines = lines[1:]
        else:
            data_lines = lines
            
        for line in data_lines:
            if line.strip():
                row = line.replace('-', ' -').split()
                matrix.append([Fraction(int(x)) for x in row])
    return matrix

if __name__ == "__main__":
    try:
        data = load_matrix("input.txt")
        solve_all_bases(data)
    except FileNotFoundError:
        print("Ошибка: Файл input.txt не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")
        