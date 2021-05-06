# 더하기 사이클

N = input()
if int(N) < 10:
    N = '0' + N

i = 0
while True:
    result = int(N[-2]) + int(N[-1])
    N += str(result)[-1]
    i += 1
    if N[:2] == N[-2:]:
        break
print(i)
