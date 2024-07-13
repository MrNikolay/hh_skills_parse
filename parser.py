import requests
import json
from pprint import pprint


class HeadHunter:
    __api_url = "https://api.hh.ru/vacancies"

    def __init__(self, keyword: str, page_count: int = 20):
        self.keyword = keyword
        self.page_count = page_count
        self.all_vacancies = self.get_all_vacancies()

    def get_all_vacancies(self):
        all_vacancies = []
        for page in range(self.page_count):
            print(f"Страница №{page+1}:", end=' ')
            all_vacancies.extend(
                self.get_vacancies_page(self.keyword, page)
            )
            print('OK!')

        print('-- ПОЛУЧИЛИ ВСЕ ВАКАНСИИ --')

        return all_vacancies

    def get_vacancies_page(self, keyword, page) -> list:
        request_params = {
            "text": keyword,
            "per_page": 100,
            "page": page
        }

        headers = {
            "User-Agent": "Your User Agent"
        }

        response = requests.get(HeadHunter.__api_url, params=request_params, headers=headers)
        vacancies_ids = []

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items", [])
            for vacancy in vacancies:
                vacancies_ids.append(vacancy.get('id'))
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

        return vacancies_ids


    def get_vacancy_skills(self, vacancy_id) -> list:
        url = f"{self.__api_url}/{vacancy_id}"
        headers = {"User-Agent": "Your User Agent"}
        response_json = requests.get(url, headers=headers).text
        key_skills = json.loads(response_json).get('key_skills')  # Возможно, ключевых навыков не будет. Тогда должен быть KeyError! (а может и нет)
        if key_skills is not None:
            return [key_skill['name'] for key_skill in key_skills]


    def get_skills_statistics(self):
        print('-- СОБИРАЕМ СТАТИСТИКУ ПО НАВЫКАМ --')
        skills = {}
        for v_id in self.all_vacancies:
            print(f'Вакансия (id={v_id}):', end=' ')
            vacancy_skills = self.get_vacancy_skills(v_id)
            if vacancy_skills:
                for skill in vacancy_skills:
                    if skill in skills:
                        skills[skill] += 1
                    else:
                        skills[skill] = 1
            print('OK!')

        return skills


def test():
    url = "https://api.hh.ru/vacancies/102832646"
    headers = {"User-Agent": "Your User Agent"}
    response_json = requests.get(url, headers=headers).text
    key_skills = json.loads(response_json).get(
        'key_skills')  # Возможно, ключевых навыков не будет. Тогда должен быть KeyError! (а может и нет)
    if key_skills is not None:
        pprint([key_skill['name'] for key_skill in key_skills])
    else:
        print('Ошибка: key_skills is None навыков нет!')


# for tests
if __name__ == '__main__':
    test()