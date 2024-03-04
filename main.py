import os
from itertools import count

import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


def predict_rub_salary(salary_from=None, salary_to=None):
    if salary_from and salary_to:
        expected_salary = int((salary_from + salary_to) / 2)
    elif salary_from:
        expected_salary = int(salary_from * 1.2)
    elif salary_to:
        expected_salary = int(salary_to * 0.8)
    else:
        expected_salary = None
    return expected_salary


def get_vacancies_hh(language, page=0):
    url = "https://api.hh.ru/vacancies"
    params = {"text": language, "area": 1, "page": page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_hh():
    proffesions = {}
    langs = ['JavaScript'
             'Java', 'Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#']
    for language in langs:
        vacancies_processed = 0
        salaries_by_vacancies = []
        for page in count(0):
            vacancies = get_vacancies_hh(language, page=page)
            if page >= vacancies['pages'] - 1:
                break
            for salary_hh in vacancies['items']:
                salary_money = salary_hh.get('salary')
                if salary_money and salary_money['currency'] == 'RUR':
                    predicted_salary = predict_rub_salary( 
                        salary_hh['salary'].get('from'),
                        salary_hh['salary'].get('to'))
                    if predicted_salary:
                        vacancies_processed += 1
                        salaries_by_vacancies.append(predicted_salary)
        total_vacancies = vacancies["found"]
        average_salary = None
        if salaries_by_vacancies:
            average_salary = int(
                sum(salaries_by_vacancies) / len(salaries_by_vacancies))

        proffesions[language] = {
            "vacancies_found": total_vacancies,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
    return proffesions


def get_vacancies_sj(superjob_secret_key, language, page=0):
    superjob_url = "https://api.superjob.ru/2.0/vacancies/"

    headers = {"X-Api-App-Id": superjob_secret_key}
    params = {"town": "Москва", "keyword": language, "page": 0}
    response = requests.get(superjob_url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_superJob(superjob_secret_key):
    proffesions = {}
    langs = ['JavaScript'
            , 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#']
    for language in langs:
        vacancies_processed = 0
        salaries_by_vacancies = []
        for page in count(0):
            vacancies = get_vacancies_sj(superjob_secret_key, language, page=page)
            if not vacancies['objects']:
                break
            for salary_sj in vacancies['objects']:
                predicted_salary = predict_rub_salary(
                    salary_sj["payment_from"], salary_sj["payment_to"])
                if predicted_salary:
                    vacancies_processed += 1
                    salaries_by_vacancies.append(predicted_salary)
        total_vacancies = vacancies["total"]
        average_salary = None
        if salaries_by_vacancies:
            average_salary = int(
                sum(salaries_by_vacancies) / len(salaries_by_vacancies))

        proffesions[language] = {
            "vacancies_found": total_vacancies,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
    return proffesions


def bring_table(title, proffesions):
    table_template = [[
        'Язык программирования', 'Вакансий найдено', 'Вакансий обработано',
        'Средняя зарплата'
    ]]
    for language, vacancies in proffesions.items():
        table_template.append([
            language, vacancies['vacancies_found'], vacancies['vacancies_processed'],
            vacancies['average_salary']
        ])
    table = AsciiTable(table_template, title)
    return table.table


def main():
    load_dotenv()
    superjob_secret_key = os.environ['SUPERJOB_SECRET_KEY']
    proffesions_hh = predict_rub_salary_hh()
    proffesions_sj = predict_rub_salary_superJob(superjob_secret_key)
    table_hh = bring_table('HeadHunter Moscow', proffesions_hh)
    table_sj = bring_table('SuperJob Moscow', proffesions_sj)
    print(table_hh)
    print(table_sj)


if __name__ == '__main__':
    main()
