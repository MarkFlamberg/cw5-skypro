from abc import ABC, abstractmethod


class AbstractAPIEngine(ABC):

    @abstractmethod
    def get_vacancies_data(self):
        pass

    @abstractmethod
    def get_employer_data(self):
        pass