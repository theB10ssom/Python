# 평균은 넘겠지
import sys
C = int(input())
for i in range(C):
    N = list(map(int, sys.stdin.readline().split()))
    avg = sum(N[1:]) / N[0]
    over = [i for i in N[1:] if i > avg]
    print(f'{(len(over)/N[0]) * 100:.3f}%')
