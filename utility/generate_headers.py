from fake_useragent import UserAgent

def generate(token: str) -> dict[str, str]:
    return {
        "Authorization": token,
        "User-Agent": UserAgent().random
    }
