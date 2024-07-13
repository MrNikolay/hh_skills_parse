from flask import Flask, render_template, request
from parser import HeadHunter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    skills = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        hh = HeadHunter(keyword, page_count=1)
        skills = hh.get_skills_statistics()

    return render_template('index.html', skills=skills)


if __name__ == "__main__":
    app.run('127.0.0.1', 8080, debug=True)
