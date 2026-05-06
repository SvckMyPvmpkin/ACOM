import os
from fractions import Fraction

class ArtificialBasis:
    def __init__(self, filename):
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден!")
            return
            
        with open(filename, 'r') as f:
            all_rows = [[Fraction(x) for x in line.split()] for line in f if line.strip()]
        
        self.n = len(all_rows[0]) - 1
        self.raw_matrix = all_rows[:-1]
        self.m = len(self.raw_matrix)
        
        z_raw = all_rows[-1]
        self.z_coeffs = z_raw + [Fraction(0)] * (self.n - len(z_raw))
        
        self.table = []
        self.basis = []
        
        self._print_original_data()
        self._build_initial_table()

    def _print_original_data(self):
        print("Исходная система")
        z_terms = [f"{self.z_coeffs[j]}x{j+1}" for j in range(self.n) if self.z_coeffs[j] != 0]
        z_orig = " + ".join(z_terms).replace("+ -", "- ") if z_terms else "0"
        print(f"Z = {z_orig} -> max\n")
        for i in range(self.m):
            eq = " + ".join([f"{self.raw_matrix[i][j]}x{j+1}" for j in range(self.n)])
            print(f"{eq.replace('+ -', '- ')} = {self.raw_matrix[i][-1]}")
        print("-" * 42 + "\n")

    def _build_initial_table(self):
        for i in range(self.m):
            row_coeffs = self.raw_matrix[i][:-1]
            artif_part = [Fraction(0)] * self.m
            artif_part[i] = Fraction(1)
            b_val = self.raw_matrix[i][-1]
            self.table.append(row_coeffs + artif_part + [b_val])
            self.basis.append(self.n + i)
        
        z_row = [-c for c in self.z_coeffs] + [Fraction(0)] * (self.m + 1)
        self.table.append(z_row)
        
        m_row = [Fraction(0)] * (self.n + self.m + 1)
        for i in range(self.m):
            for j in range(len(m_row)):
                m_row[j] -= self.table[i][j]
        
        for i in range(self.m):
            m_row[self.n + i] = Fraction(0)
            
        self.table.append(m_row)

    def print_table(self, step, pivot_col=None):
        print(f"\nТаблица {step}")
        x_headers = [f"x{i+1}" for i in range(self.n + self.m)]
        header_parts = [f"{'б.п.':<5}", f"{'1':^9}"] + [f"{h:^9}" for h in x_headers] + [f"{'СО':^9}"]
        header = " | ".join(header_parts)
        print(header)
        print("-" * len(header))
        
        for i in range(len(self.table)):
            if i < self.m: label = f"x{self.basis[i]+1}"
            elif i == self.m: label = "Z"
            else: label = "M"
            
            b_val = self.table[i][-1]
            coeffs = self.table[i][:-1]
            
            co_str = ""
            if pivot_col is not None and i < self.m:
                val_in_pivot = self.table[i][pivot_col]
                if val_in_pivot > 0:
                    co_str = str(b_val / val_in_pivot)
            
            row_vals = [label.ljust(5), f"{str(b_val):^9}"] + [f"{str(c):^9}" for c in coeffs] + [f"{co_str:^9}"]
            print(" | ".join(row_vals))

    def solve(self):
        step = 1
        while True:
            m_idx = len(self.table) - 1
            z_idx = len(self.table) - 2
            pivot_col = -1
            min_val = 0
            
            for j in range(self.n):
                if self.table[m_idx][j] < min_val:
                    min_val = self.table[m_idx][j]
                    pivot_col = j

            if pivot_col == -1:
                for j in range(self.n):
                    if self.table[z_idx][j] < min_val:
                        min_val = self.table[z_idx][j]
                        pivot_col = j
            
            self.print_table(step, pivot_col if pivot_col != -1 else None)
            
            if pivot_col == -1: 
                break

            pivot_row = -1
            min_ratio = float('inf')
            for i in range(self.m):
                if self.table[i][pivot_col] > 0:
                    ratio = self.table[i][-1] / self.table[i][pivot_col]
                    if ratio < min_ratio:
                        min_ratio = ratio
                        pivot_row = i
            
            if pivot_row == -1:
                print("\nФункция не ограничена!")
                return

            self._do_pivot(pivot_row, pivot_col)
            self.basis[pivot_row] = pivot_col
            step += 1
            
        self._format_output()

    def _do_pivot(self, row, col):
        pv = self.table[row][col]
        self.table[row] = [x / pv for x in self.table[row]]
        for r in range(len(self.table)):
            if r != row:
                multiplier = self.table[r][col]
                self.table[r] = [self.table[r][j] - multiplier * self.table[row][j] for j in range(len(self.table[0]))]

    def _format_output(self):
        x_results = [Fraction(0)] * self.n
        for i in range(self.m):
            if self.basis[i] < self.n:
                x_results[self.basis[i]] = self.table[i][-1]
        res_x_str = ", ".join([str(x) for x in x_results])
        final_z = self.table[self.m][-1]
        print(f"\nОтвет: Zmax ({res_x_str}) = {final_z}")

if __name__ == "__main__":
    ArtificialBasis("input.txt").solve()
    