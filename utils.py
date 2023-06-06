from atexit import register as atexit_reg


def make_question(q: str, border: str) -> str:
    """
    Formation of a request.
    :param q: question
    :param border: visual design
    :return: user answer
    """
    result: str = input(f"{border}\n{q}?\n{border}\n")
    return result


def string_to_bool(choice: str) -> bool:
    """
    Translate from string to bool.
    :param choice: string value
    :return: bool value or raise ValueError
    """
    translate: dict = {
        "1": True,
        "2": False,
    }

    if (result := translate.get(choice)) is None:
        raise ValueError("нужно ввести или 1 - если ДА или 2 - НЕТ")

    return result


def make_skin_question() -> tuple[str, str]:
    """
    Make 'menu'.
    :return: strings for design
    """
    button = "1: hh.ru", "2: superjob.ru", "3: со всех сразу!"
    border = "-" * (max(len(x) for x in button) + 4)
    menu = "  \n  ".join(button)
    return border, menu


def has_answer(param: str, msg, border) -> bool:
    """
    DRY!
    :return: bool or ValueError
    """
    if not param:
        return string_to_bool(make_question(msg, border))
    return string_to_bool(param)


@atexit_reg
def bye():
    print("! Завершение программы !")
