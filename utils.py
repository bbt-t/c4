def make_question(q: str, border: str) -> str:
    """
    Formation of a request.
    :param q: question
    :param border: visual design
    :return: user answer
    """

    result: str = input(
        f"{border}\n{q}?\n{border}\n"
    )
    return result


def string_to_bool(choice: str) -> bool:
    """
    Translate from string to bool.
    :param choice: string value
    :return: bool value or raise ValueError
    """

    translate: dict = {
        '1': True,
        '2': False,
    }

    if (result := translate.get(choice)) is None:
        raise ValueError("нужно ввести или 1 - если ДА или 2 - НЕТ")

    return result
