def insert_vacancy_data_to_db(data, db):
    with db.conn.cursor() as cur:
        for vacancy in data:
            cur.execute("""
                INSERT INTO vacancies (id, name, company_id, salary_min, salary_max, url)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                vacancy['id'],
                vacancy['name'],
                vacancy['employer']['id'],
                vacancy['salary']['from'],
                vacancy['salary']['to'],
                vacancy['url']
            )
                        )

            db.conn.commit()


def insert_employer_data_to_db(data, db):
    with db.conn.cursor() as cur:
        for employer in data:
            cur.execute("""
                        INSERT INTO companies (id, name, url)
                        VALUES (%s, %s, %s);
            """, (
                employer['id'],
                employer['name'],
                employer['url']
            )
                        )
            db.conn.commit()
