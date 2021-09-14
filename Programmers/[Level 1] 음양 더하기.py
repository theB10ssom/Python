def solution(absolutes, signs):
    answer = 0
    for i in range(len(absolutes)):
        if signs[i] == 0:
            signs[i] = -1
        answer += absolutes[i] * signs[i]
    return answer
