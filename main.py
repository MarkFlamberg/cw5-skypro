import os
from dotenv import load_dotenv

from db_manage.db_manager import PostgresDBManager
from api_engine.hh_engine_class import HeadHunterApiHandler
from utils import insert_employer_data_to_db, insert_vacancy_data_to_db

if __name__ == '__main__':

    load_dotenv()

    db = PostgresDBManager(
        dbname='coursework',
        user='postgres',
        password=os.environ.get('DB_PASSWORD'),
        host='localhost',
        port='5432'
    )

    db.drop_tables()
    db.create_tables()

    api_handler = HeadHunterApiHandler()
    vacancy_list = api_handler.get_vacancies_data()
    employer_list = api_handler.get_employer_data()

    insert_employer_data_to_db(employer_list, db)
    insert_vacancy_data_to_db(vacancy_list, db)

    print(db.get_companies_and_vacancies_count())  # кол-во вакансий у интересующих компаний
    print(db.get_all_vacancies())  # все вакансии
    print(db.get_avg_salary())  # средняя зп
    print(db.get_vacancies_with_higher_salary())  # вакансии с самыми большими зп
    print(db.get_vacancies_with_keyword('Стажер'))  # вакансии с словом стажер в названии вакансии

    if not db.conn.closed:
        db.conn.close()
