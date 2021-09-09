def solution(new_id):
    import re
    
    # 1단계
    first = new_id.lower()

    # 2단계
    second = re.sub(r"[^(\.\|\-\|\_\|\w)]", "", first)

    # 3단계
    third = re.sub(r"([(\.\)]+)", ".", second)

    # 4단계
    fourth = third.lstrip(".").rstrip(".")

    # 5단계
    fifth = re.sub(r"^()$", "a", fourth)

    # 6단계
    sixth = fifth[:15]
    if sixth[-1] == ".":
        sixth = sixth.rstrip(".")

    # 7단계
    while len(sixth) < 3:
        sixth += sixth[-1]

    answer = sixth
    return answer