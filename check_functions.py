def has_whois_in_text(text: str) -> bool:
    return True if "#whois" in text else False


def is_correct_whois(text: str) -> bool:
    words = text.split(' ')
    start_template = words.index('#whois')
    if len(words) >= start_template + 3:
        if (
                len(words[start_template + 1].split('-')) > 1
                or len(words[start_template + 2].split('-')) > 1
                or len(words[start_template + 3].split('-')) > 1
        ):
            return True
        else:
            return False
    else:
        return False

