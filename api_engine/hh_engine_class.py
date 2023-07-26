import httpx

from api_engine.abstract_engine_class import AbstractAPIEngine
from config import hh_api_config


class HeadHunterApiHandler(AbstractAPIEngine):

    def __init__(self, page: int = 0) -> None:
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "page": page,
            "employer_id": hh_api_config.get('employer_ids'),
            "only_with_salary": hh_api_config.get('only_with_salary'),
            "per_page": hh_api_config.get('vacancies_per_page'),
            "area": hh_api_config.get('area')
        }

    def get_vacancies_data(self) -> list[dict]:
        """Получение данных по вакансии"""
        response = httpx.get(self.url, params=self.params)
        if not response.status_code == 200:
            raise HHApiError(f"Error type: {response.json()['errors'][0]['type']},"
                             f"Status code: {response.status_code}")
        return response.json()['items']

    def get_employer_data(self) -> list[dict]:
        """получение данных по работодателю"""
        return [
            {
                'id': uid,
                'name': httpx.get(f"https://api.hh.ru/employers/{uid}").json().get('name'),
                'url': httpx.get(f"https://api.hh.ru/empliyers/{uid}").json().get('alternate_url')
            }

            for uid in self.params.get('employer_id') if uid is not None
        ]