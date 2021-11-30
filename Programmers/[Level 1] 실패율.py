## 내풀이

def solution(N, stages):

    result = {}

    for x in range(1, N+1):
        if len([i for i in stages if i >= x]) == 0: # 통과 못한 스테이지 고려
            result[x] = 0
        else:
            result[x] = stages.count(x) / len([i for i in stages if i >= x])
    
    answer = sorted(result,key=(lambda x: result[x]), reverse = True)
    return answer
  
  
## 깔끔한 풀이

def solution(N, stages):
    result = {}
    denominator = len(stages)
    for stage in range(1, N+1):
        if denominator != 0:
            count = stages.count(stage)
            result[stage] = count / denominator
            denominator -= count
        else:
            result[stage] = 0
    return sorted(result, key=lambda x : result[x], reverse=True)
