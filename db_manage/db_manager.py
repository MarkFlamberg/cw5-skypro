import psycopg2

from db_manage.abstact_db_manager import AbstractDBManager


class PostgresDBManager(AbstractDBManager):
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(database=dbname,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port)

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id INT PRIMARY KEY,
                    name TEXT NOT NULL,
                    url VARCHAR(100)
                );                
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id INT PRIMARY KEY,
                    name TEXT NOT NULL,
                    company_id INT REFERENCES companies(id) ON DELETE CASCADE,
                    salary_min INT,
                    salary_max INT,
                    url VARCHAR(100) NOT NULL
                );
            """)
            self.conn.commit()

    def drop_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS vacancies;")
            cur.execute("DROP TABLE IF EXISTS companies;")
            self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, COUNT(vacancies.id)
                FROM companies
                JOIN vacancies ON companies.id = vacancies.company_id
                GROUP BY companies.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(salary_min + salary_max) / 2
                FROM vacancies;
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """ получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies 
                JOIN companies ON vacancies.company_id = companies.id
                WHERE ((vacancies.salary_min + vacancies.salary_max) / 2) > {self.get_avg_salary()};
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова 'Стажер' """
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = company_id
                WHERE vacancies.name ILIKE '%{keyword}%' OR companies.name ILIKE '%{keyword}%';
            """)
            return cur.fetchall()

