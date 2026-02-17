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

    def __abs__(self): return Fraction(abs(self.num), self.den)
    def __eq__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return self.num == other.num and self.den == other.den
    def __ne__(self, other): return not self.__eq__(other)
    def __lt__(self, other):
        if not isinstance(other, Fraction): other = Fraction(other)
        return self.num * other.den < other.num * self.den
    def __repr__(self):
        return str(self.num) if self.den == 1 else f"{self.num}/{self.den}"

def print_matrix(matrix, message=""):
    if message:
        print(f"--- {message} ---")
    for row in matrix:
        print("  ".join(f"{str(x):>10}" for x in row))
    print("-" * 50)

def load_matrix(filename):
    matrix = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                # Поддержка отрицательных чисел и базовый парсинг
                row = line.replace('-', ' -').split()
                matrix.append([Fraction(int(x)) for x in row])
    return matrix

def get_basic_solution(original_matrix, basis_indices):
    """
    Пытается найти базисное решение для выбранных индексов столбцов.
    """
    matrix = copy.deepcopy(original_matrix)
    rows = len(matrix)
    cols = len(matrix[0]) - 1
    
    # Порядок столбцов в базисе
    for step, col_idx in enumerate(basis_indices):
        # Поиск ведущего элемента в текущем столбце col_idx (среди строк от step до конца)
        pivot_row = -1
        for r in range(step, rows):
            if matrix[r][col_idx] != Fraction(0):
                pivot_row = r
                break
        
        if pivot_row == -1:
            return None # Эти столбцы линейно зависимы, базиса нет

        # Перестановка строк
        matrix[step], matrix[pivot_row] = matrix[pivot_row], matrix[step]
        
        # Нормализация строки
        pivot_val = matrix[step][col_idx]
        for c in range(len(matrix[0])):
            matrix[step][c] = matrix[step][c] / pivot_val
        
        print_matrix(matrix, f"Шаг {step+1}: Выбран базисный x{col_idx+1}, нормализация строки {step+1}")

        # Исключение остальных элементов в столбце
        for r in range(rows):
            if r != step:
                factor = matrix[r][col_idx]
                if factor != Fraction(0):
                    for c in range(len(matrix[0])):
                        matrix[r][c] = matrix[r][c] - (factor * matrix[step][c])
        
        print_matrix(matrix, f"Результат исключения для столбца x{col_idx+1}")

    # Проверка на совместность (если строк больше, чем базисных переменных)
    for r in range(len(basis_indices), rows):
        if matrix[r][cols] != Fraction(0):
            return None # Система несовместна

    # Формируем решение
    solution = [Fraction(0)] * cols
    for i, col_idx in enumerate(basis_indices):
        solution[col_idx] = matrix[i][cols]
    
    return solution

def solve_all_bases(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) - 1 # количество переменных
    
    print_matrix(matrix, "ИСХОДНАЯ МАТРИЦА")
    
    # Генерируем все комбинации индексов столбцов по m (кол-во уравнений)
    # Если уравнений больше чем ранг, нужно сначала найти ранг. 
    # Но для учебных задач обычно m - это размер базиса.
    all_combinations = list(combinations(range(cols), rows))
    
    solutions_found = 0
    print(f"Всего возможных комбинаций базиса: {len(all_combinations)}\n")

    for combo in all_combinations:
        basis_display = ", ".join([f"x{i+1}" for i in combo])
        print(f"\n{'='*60}")
        print(f"ПРОВЕРКА БАЗИСА: ({basis_display})")
        print(f"{'='*60}")
        
        sol = get_basic_solution(matrix, combo)
        
        if sol is not None:
            solutions_found += 1
            res_str = [f"x{i+1}={sol[i]}" for i in range(len(sol))]
            print(f"\nБАЗИСНОЕ РЕШЕНИЕ НАЙДЕНО: {', '.join(res_str)}")
        else:
            print("\nДанный набор переменных не может быть базисом (матрица вырождена или система несовместна).")

    print(f"\nИТОГО найдено базисных решений: {solutions_found}")

if __name__ == "__main__":
    # Создайте файл input.txt с коэффициентами системы
    # Пример для системы №1:
    # 4 -11 13 6 8 8
    # 7 12 5 3 9 54
    # -6 9 -17 13 7 -16
    # -17 -7 -30 30 -14 -86
    
    try:
        data = load_matrix("input.txt")
        solve_all_bases(data)
    except FileNotFoundError:
        print("Ошибка: Создайте файл input.txt с коэффициентами матрицы.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        