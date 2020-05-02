def has_whois_in_text(text: str) -> bool:
    return True if "#whois" in text else False


def is_correct_whois(text: str) -> bool:
    words = text.split(' ')
    k = words.index('#whois')
    if len(words) <= k + 2:
        return False
    elif len(words[k + 2].split('-')) > 1:
        return True
    elif len(words) >= k + 3 and len(words[k + 3].split('-')) > 1:
        return True
    else:
        return False

