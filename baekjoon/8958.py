# OX 퀴즈
import sys
N = int(input())

for i in range(N):
    ans = 0
    put = sys.stdin.readline().rstrip().split('X')
    for o in put:
        ans += sum([i+1 for i in range(len(o))])
    print(ans)
