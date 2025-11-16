import random

# 집합 A = {1,2,3,4,5}
A = [1, 2, 3, 4, 5]
R = []

# (1) 관계 행렬 입력 or 무작위 생성
print("관계행렬 입력 모드 선택:")
print("1. 직접 입력   2. 무작위 생성")
mode = input("선택 (1 또는 2): ")

if mode == "2":
    R = [[random.randint(0, 1) for _ in range(5)] for _ in range(5)]
    print("\n무작위 생성된 5x5 관계행렬:")
    for row in R:
        print(row)
else:
    print("\n5x5 관계행렬을 행 단위로 입력하세요 (공백 구분):")
    for _ in range(5):
        R.append(list(map(int, input().split())))

# (2) 반사, 대칭, 추이 판별 함수
def is_reflexive(R):
    for i in range(5):
        if R[i][i] != 1:
            return False
    return True

def is_symmetric(R):
    for i in range(5):
        for j in range(5):
            if R[i][j] != R[j][i]:
                return False
    return True

def is_transitive(R):
    for i in range(5):
        for j in range(5):
            if R[i][j] == 1:
                for k in range(5):
                    if R[j][k] == 1 and R[i][k] == 0:
                        return False
    return True

# (3) 동치류 계산 함수
def equivalence_classes(R):
    classes = []
    visited = set()
    for i in range(5):
        if A[i] not in visited:
            eq_class = {A[j] for j in range(5) if R[i][j] == 1}
            classes.append(eq_class)
            visited |= eq_class
    return classes

# (4) 폐포 계산 함수들
def reflexive_closure(R):
    R2 = [row[:] for row in R]
    for i in range(5):
        R2[i][i] = 1
    return R2

def symmetric_closure(R):
    R2 = [row[:] for row in R]
    for i in range(5):
        for j in range(5):
            if R[i][j] == 1:
                R2[j][i] = 1
    return R2

def transitive_closure(R):
    R2 = [row[:] for row in R]
    for k in range(5):
        for i in range(5):
            for j in range(5):
                if R2[i][k] and R2[k][j]:
                    R2[i][j] = 1
    return R2

# (5) 성질 판별
ref = is_reflexive(R)
sym = is_symmetric(R)
trans = is_transitive(R)

print(f"\n반사적: {ref}")
print(f"대칭적: {sym}")
print(f"추이적: {trans}")

# (6) 동치관계 여부
if ref and sym and trans:
    print("\n이 관계는 동치 관계입니다.")
    eq_classes = equivalence_classes(R)
    print("동치류:")
    for i, c in enumerate(eq_classes):
        print(f"[{i+1}] {c}")
else:
    print("\n이 관계는 동치 관계가 아닙니다.")
    print("\n--- 폐포 변환 과정 ---")
    if not ref:
        print("① 반사 폐포 전:")
        print(*R, sep="\n")
        R = reflexive_closure(R)
        print("반사 폐포 후:")
        print(*R, sep="\n")

    if not sym:
        print("\n② 대칭 폐포 전:")
        print(*R, sep="\n")
        R = symmetric_closure(R)
        print("대칭 폐포 후:")
        print(*R, sep="\n")

    if not trans:
        print("\n③ 추이 폐포 전:")
        print(*R, sep="\n")
        R = transitive_closure(R)
        print("추이 폐포 후:")
        print(*R, sep="\n")

    # 폐포 적용 후 다시 판별
    ref = is_reflexive(R)
    sym = is_symmetric(R)
    trans = is_transitive(R)

    if ref and sym and trans:
        print("\n폐포 적용 후 동치 관계가 되었습니다.")
        eq_classes = equivalence_classes(R)
        print("동치류:")
        for i, c in enumerate(eq_classes):
            print(f"[{i+1}] {c}")
    else:
        print("\n폐포 적용 후에도 동치 관계가 아닙니다.")
