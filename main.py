from flask import Flask, render_template, request
from werkzeug.utils import redirect

app = Flask(__name__)

# TODO: Сейчас у фанфиков есть только текст. Придумай для каждого название и укажи сколько у него лайков по своему усмотрению (получится список словарей).

categories = [
    {
        "name": "Лунтик",
        "fanfics": [
            {'likes': 15, 'name': 'Первый фанфик', 'text': '0.txt'},
            {'likes': 50, 'name': 'Второй фанфик', 'text': '1.txt'},
            {'likes': 75, 'name': 'Третий фанфик', 'text': '2.txt'},
            {'likes': 105, 'name': 'Четвертый фанфик', 'text': '3.txt'}
        ]

    },

    {
        "name": 'Вупсень',
        'fanfics': [
            {'likes': 10000, 'name': 'Пятый фанфик', 'text': '4.txt'},
            {'likes': 10, 'name': 'Шестой фанфик', 'text': '5.txt'},

        ]
    }
]

titles = [i['name'] for i in categories]


@app.route('/')
def i():
    return redirect('/0')

@app.route('/<number>')
def index(number):
    global categories
    number = int(number)
    texts = []
    categories[number]['fanfics'] = sorted(categories[number]['fanfics'], key=lambda x: x['likes'], reverse=True)
    for i in categories[number]['fanfics']:
        with open(f'static/text/{i["text"]}') as file:
            texts.append(file.read())


    return render_template('index.html', arr=categories[number]['fanfics'], texts=texts, title=categories[number]["name"],
                           titles=titles, index=number)

@app.route('/category/<int:category_id>/fanfic/<fanfic_id>/like')
def add_like(category_id, fanfic_id):
    global categories
    categories[int(category_id)]['fanfics'][int(fanfic_id)]['likes'] += 1
    return redirect(f'/{category_id}')


@app.route('/add_category_form')
def add_category_form():
    return render_template('category_add_form.html')

@app.route('/add_category', methods=['post', 'get'])
def add_category():
    global categories, titles

    categories.append({'name': request.form.get('category_name'), 'fanfics': []})

    titles = [i['name'] for i in categories]

    print(categories)

    return redirect('/')

@app.route('/delete/<category_id>/<fanfic_id>')
def delete(category_id, fanfic_id):
    global categories
    categories[int(category_id)]['fanfics'].pop(int(fanfic_id))
    return redirect(f'/{category_id}')

app.run(debug=True)
