from utils import make_question, string_to_bool

from jobmatchup.api import Query
from jobmatchup.configs import Config, DBConfig
from jobmatchup import tools
from jobmatchup import storage


def main():
    # приветствие
    print('Привет! Выбери что тебе нужно из списка ниже: ')

    # меню
    button = '1: hh.ru', '2: superjob.ru', '3: со всех сразу!'
    border = '-' * (max(len(x) for x in button) + 4)
    menu = "  \n  ".join(button)

    # где ищем?
    choice = input(
        f"{border}\nгде ищем?\n  {menu} \n{border}\n"
    )

    # что ищем?
    search_query = make_question("что ищем?", border)

    # сколько ищем?
    if not (amt := make_question("сколько?", border)).isdecimal():
        raise ValueError

    match choice:
        case '1':
            cfg = Config(without_auth=True)
            result = Query(cfg, search_query, int(amt)).get_hh()
        case '2':
            cfg = Config(without_auth=False, from_env=True)
            result = Query(cfg, search_query, int(amt)).get_sj()
        case '3':
            is_async: bool = string_to_bool(input("увеличим скорость?)"))

            cfg = Config(without_auth=False)
            result = Query(cfg, search_query, int(amt), async_work=is_async)

    # отфильтровать по ЗП?
    is_filter = string_to_bool(make_question("отфильтровать по ЗП?", border))
    if is_filter:
        filter_word = input('введи слово для фильтрации')
        result = tools.filter_vacancies(result, filter_word)

    # отсортировать?
    is_sort = string_to_bool(make_question("сортируем?", border))
    if is_sort:
        result = tools.sort_vacancies_by_salary(result)

    # сохранить?
    is_save_to_file = string_to_bool(make_question("сохранить в файл?", border))
    if is_save_to_file:
        db_cfg = DBConfig()
        db = storage.Repository(db_cfg)
        db.db.add_vacancy(result)



if __name__ == '__main__':
    main()
