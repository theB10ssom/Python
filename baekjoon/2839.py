# 설탕배달 문제

N = int(input('enter'))

while N > 0:
  
    x, y = 0, 0
    lim_x = N // 3
    lim_y = N // 5

    result = []
    for y in range(lim_y + 1):
        for x in range(lim_x + 1):
            cal = (3 * x) + (5 * y) == N
            if cal == True:
                result.append(x+y)

    if len(result) >= 1:
        print(min(result))
    else:
        print('-1')
