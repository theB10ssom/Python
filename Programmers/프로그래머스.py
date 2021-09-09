lottos = [44, 1, 0, 0, 31, 25]
win_nums = [31, 10, 45, 1, 6, 19]

len_0 = lottos.count(0)

min = 6 - len(set(win_nums) - set(lottos))
max = min + len_0

answer = list(map(lambda x : 6 if x < 2 else 6 - x + 1 ,[max, min]))
print(answer)