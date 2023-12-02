def solve(data):
    captcha = data.strip()
    print(solution(captcha, offset=1))
    print(solution(captcha, offset=len(captcha) // 2))


def solution(captcha, offset):
    digit_pairs = zip(captcha, captcha[offset:] + captcha[:offset])
    return sum(int(a) for a, b in digit_pairs if a == b)
