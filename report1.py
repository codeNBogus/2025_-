import sys
import random
from copy import deepcopy
from math import isclose

# ---------------- 행렬 유틸 ----------------
def minor_matrix(A, r, c):
    return [row[:c] + row[c+1:] for i, row in enumerate(A) if i != r]

def det_recursive(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    s = 0.0
    for j in range(n):
        cofactor_sign = -1.0 if (j % 2) else 1.0
        s += cofactor_sign * A[0][j] * det_recursive(minor_matrix(A, 0, j))
    return s

def pretty_print_matrix(M, name=None, decimals=6):
    if name:
        print(f"\n[{name}]")
    fmt = f"{{:.{decimals}f}}"
    for row in M:
        print(" ".join(fmt.format(x) for x in row))

def matrices_equal(A, B, tol=1e-9):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False
    for i in range(len(A)):
        for j in range(len(A[0])):
            if not isclose(A[i][j], B[i][j], rel_tol=1e-9, abs_tol=tol):
                return False
    return True

# ---------------- 역행렬 계산 ----------------
def adjugate_inverse(A):
    n = len(A)
    d = det_recursive(A)
    if isclose(d, 0.0, abs_tol=1e-12):
        raise ValueError("행렬식이 0이므로 역행렬이 존재하지 않습니다. (수반행렬법)")
    C = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            m = minor_matrix(A, i, j)
            C[i][j] = ((-1.0) ** (i + j)) * det_recursive(m)
    adj = [[C[j][i] for j in range(n)] for i in range(n)]
    inv = [[adj[i][j] / d for j in range(n)] for i in range(n)]
    return inv

def gauss_jordan_inverse(A):
    n = len(A)
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(deepcopy(A))]

    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if isclose(aug[pivot_row][col], 0.0, abs_tol=1e-12):
            raise ValueError("행렬식이 0이므로 역행렬이 존재하지 않습니다. (가우스-조던)")
        if pivot_row != col:
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        pivot = aug[col][col]
        for j in range(2*n):
            aug[col][j] /= pivot

        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            for j in range(2*n):
                aug[r][j] -= factor * aug[col][j]

    return [row[n:] for row in aug]

# ---------------- 입력 기능 ----------------
def read_square_matrix():
    """사용자 직접 입력"""
    try:
        n = int(input("정수 n (n×n 정방행렬 크기): ").strip())
        if n <= 0:
            raise ValueError
    except ValueError:
        print("n은 양의 정수여야 합니다.")
        sys.exit(1)

    A = []
    print(f"{n}×{n} 행렬을 행 단위로 입력하세요 (공백 구분):")
    for i in range(n):
        row = input().strip().split()
        if len(row) != n:
            print(f"{i+1}번째 행의 원소 개수가 {n}이 아닙니다.")
            sys.exit(1)
        A.append([float(x) for x in row])
    return A

def random_matrix(n, low=-5, high=5):
    """무작위 n×n 행렬 생성"""
    return [[float(random.randint(low, high)) for _ in range(n)] for _ in range(n)]

def generate_random_matrix():
    """무작위 생성 선택 시 동작"""
    try:
        n = int(input("무작위 행렬 크기 n: ").strip())
        if n <= 0:
            raise ValueError
    except ValueError:
        print("n은 양의 정수여야 합니다.")
        sys.exit(1)

    try:
        low = int(input("원소 하한 (기본 -5): ").strip() or "-5")
        high = int(input("원소 상한 (기본 5): ").strip() or "5")
        if low > high:
            low, high = high, low
    except ValueError:
        print("정수 범위를 올바르게 입력해주세요.")
        sys.exit(1)

    seed_in = input("시드 값(엔터시 무작위): ").strip()
    if seed_in:
        random.seed(int(seed_in))

    A = random_matrix(n, low, high)
    print("\n[무작위로 생성된 행렬]")
    pretty_print_matrix(A, decimals=0)
    return A

# ---------------- 계산 및 비교 ----------------
def compute_and_compare(A):
    try:
        inv1 = adjugate_inverse(A)
        pretty_print_matrix(inv1, "역행렬 (행렬식/수반행렬법)")
    except ValueError as e:
        print(f"\n{e}")
        inv1 = None

    try:
        inv2 = gauss_jordan_inverse(A)
        pretty_print_matrix(inv2, "역행렬 (가우스-조던)")
    except ValueError as e:
        print(f"\n{e}")
        inv2 = None

    print("\n[결과 비교]")
    if inv1 is None and inv2 is None:
        print("두 방법 모두 역행렬이 존재하지 않습니다.")
    elif inv1 is None or inv2 is None:
        print("한 방법만 역행렬을 계산했습니다.")
    else:
        print("두 결과가 동일합니다." if matrices_equal(inv1, inv2) else "두 결과가 다릅니다.")

# ---------------- 메인 ----------------
def main():
    print("=== 역행렬 계산 프로그램 ===")
    print("1) 행렬 직접 입력")
    print("2) 무작위 행렬 생성")
    mode = input("선택 (1 또는 2): ").strip()

    if mode == "1":
        A = read_square_matrix()
    elif mode == "2":
        A = generate_random_matrix()
    else:
        print("잘못된 선택입니다.")
        sys.exit(1)

    compute_and_compare(A)

if __name__ == "__main__":
    main()
