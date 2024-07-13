from flask import Flask, render_template, request
from parser import HeadHunter
from time import sleep

app = Flask(__name__)

skills = [
    {'name': 'Python', 'count': 983, 'percent': '65,3%'},
    {'name': 'SQL', 'count': 666, 'percent': '43,0%'},
    {'name': 'PostgreSQL', 'count': 540, 'percent': '39,8%'},
    {'name': 'DockerFiles', 'count': 304, 'percent': '19,2%'},
    {'name': 'Сексуальность', 'count': 221, 'percent': '18,0%'},
    {'name': 'ЗКДШНОСТЬ', 'count': 1, 'percent': '1%'}
]

def is_form_valid(form):
    """ Index Form valid checker """
    query = form.get('query')
    vacancy_count = form.get('vacancy_count')

    if query is None or vacancy_count is None:
        return False

    if len(query) > 40:
        return False

    if vacancy_count not in (str(i) for i in range(5)):
        return False

    return True


@app.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('result.html', title='TEST', skills=[])
    # Проверить длину запроса
    if request.method == 'POST':
        if is_form_valid(request.form):
            query = request.form.get('query')
            vacancy_count_index = request.form.get('vacancy_count')
            is_ignore = request.form.get('is_ignore')

            if len(query) == 0:
                return render_template('index.html', is_warning_message=True)

            page_count = [1, 5, 10, 15, 20][int(vacancy_count_index)]
            HH = HeadHunter(query, page_count, is_ignore)
            vacancy_count, skills = HH.get_skills_statistics()

            skills = sorted(skills.items(), key=lambda item: item[1], reverse=True)
            skills = skills[:15]

            result = []
            for name, count in skills:
                percent = str(round(count / vacancy_count * 100, 1)).replace('.', ',') + '%'
                result.append({'name': name, 'count': count, 'percent': percent})

            return render_template('result.html', query=query, skills=result)

        else:
            return '404404 FATALITY ERROR!!!'


    return render_template('index.html')

if __name__ == "__main__":
    app.run('127.0.0.1', 8080, debug=True)
