from utils import make_question, make_skin_question, has_answer

from click import command, option
from jobmatchup.api import Query
from jobmatchup.configs import Config, DBConfig
from jobmatchup.tools import sort_vacancies_by_salary, show_vacancies
from jobmatchup.storage import Repository


# add CLI commands
@command()
@option("--choice", default="", help="где ищем? (1: hh.ru 2: superjob.ru 3: со всех сразу!)")
@option("--query", default="", help="что ищем?")
@option("--amt", default="", help="сколько?")
@option("--async_req", default="", help="использовать асинхронный запрос? работает только если выбрать > 1 сайта!")
@option("--sort", default="", help="отфильтровать по ЗП?")
@option("--save", default="", help="сохранить в файл?")
def main(choice, query, amt, async_req, sort, save) -> None:
    """
    Main func for user interaction.
    """

    # приветствие:
    print('Привет! Выбери что тебе нужно из списка ниже: ')

    # меню
    border, menu = make_skin_question()

    # где ищем?
    if not choice:
        choice = input(f"{border}\nгде ищем?\n  {menu} \n{border}\n")

    # как нужно делать выбор:
    print("Далее необходимо делать выбор так:\n| 1 - ДА |   | 2 - НЕТ |")

    # что ищем?
    if not query:
        query = make_question("что ищем?", border)

    # сколько ищем?
    if not amt:
        amt = make_question("сколько?", border)
    if not amt.isdecimal():
        raise ValueError("! should be integer !")

    # делаем запрос:
    try:
        match choice:
            case '1':
                cfg = Config(without_auth=True)
                result = Query(cfg, query, int(amt)).get_hh()
            case '2':
                cfg = Config(without_auth=False, from_env=True)
                result = Query(cfg, query, int(amt)).get_sj()
            case '3':
                cfg = Config(without_auth=False)
                result = Query(
                    cfg,
                    query,
                    int(amt),
                    async_work=has_answer(async_req, "увеличим скорость?)", border),
                )
    except TypeError:
        print("! Ничего не найдено !")
        return

    # отсортировать?
    if has_answer(sort, "сортируем?", border):
        result = sort_vacancies_by_salary(result)

    # сохранить?
    if has_answer(save, "сохранить в файл?", border):
        db_cfg = DBConfig()
        repo = Repository(db_cfg)

        repo.db.add_vacancy(result)

    # вывод:
    show_vacancies(result)


if __name__ == '__main__':
    main()
