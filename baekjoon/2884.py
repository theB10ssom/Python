#알람시계 문제

H, M = map(int, input().split())

if M >= 45:
    print(f'{H} {M - 45}')
else: # 45분을 빼면 시간을 빼야하는 경우
    if H > 0:
        print(f'{H - 1} {(60 + M) - 45}')
    else: #0시인 경우
        print(f'23 {(60 + M) - 45}')
