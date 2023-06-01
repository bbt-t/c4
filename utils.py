def make_question(q: str, border: str):

    result = input(
        f"{border}\n{q}?\n{border}\n"
    )
    return result


def string_to_bool(choice: str) -> bool:
    translate = {
        '1': True,
        '2': False,
    }

    result = translate.get(choice)
    if result is None:
        raise ValueError("нужно ввести или 1 - если ДА или 2 - НЕТ")
    return result
