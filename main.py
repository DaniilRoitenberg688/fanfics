from flask import Flask, render_template, request
from werkzeug.utils import redirect
import json

import os

app = Flask(__name__)

# TODO: Сейчас у фанфиков есть только текст. Придумай для каждого название и укажи сколько у него лайков по своему усмотрению (получится список словарей).

with open('data/categories.json', 'r', encoding='utf-8') as file:
    categories = json.loads(file.read())


def find_maximum_file_name():
    global categories
    file_names = []
    for i in categories:
        [file_names.append(int(j['text'][:j['text'].index('.txt')])) for j in i['fanfics']]

    file_names.sort()
    res = file_names[-1]
    return int(res)


current_count = find_maximum_file_name()

titles = [i['name'] for i in categories]


def safe():
    with open('data/categories.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(categories))


def sort(number):
    global categories
    categories[number]['fanfics'] = sorted(categories[number]['fanfics'], key=lambda x: x['likes'], reverse=True)


@app.route('/')
def i():
    return redirect('/categories/0')


@app.route('/categories/<int:number>')
def index(number):
    global categories
    number = int(number)
    texts = []

    for i in categories[number]['fanfics']:
        with open(f'static/text/{i["text"]}') as file:
            texts.append(file.read())

    return render_template('index.html', arr=categories[number]['fanfics'], texts=texts,
                           title=categories[number]["name"],
                           titles=titles, index=number)


@app.route('/category/<int:category_id>/fanfic/<fanfic_id>/like')
def add_like(category_id, fanfic_id):
    global categories
    categories[int(category_id)]['fanfics'][int(fanfic_id)]['likes'] += 1
    sort(category_id)
    safe()
    return redirect(f'/categories/{category_id}')


@app.route('/add_category_form')
def add_category_form():
    return render_template('category_add_form.html')


@app.route('/add_category', methods=['post', 'get'])
def add_category():
    global categories, titles

    categories.append({'name': request.form.get('category_name'), 'fanfics': []})

    titles = [i['name'] for i in categories]

    safe()

    return redirect('/')


@app.route('/delete_fanfic/<int:category_id>/<int:fanfic_id>')
def delete_fanfic(category_id, fanfic_id):
    global categories, current_count
    os.remove(f'static/text/{categories[category_id]["fanfics"][fanfic_id]["text"]}')
    categories[int(category_id)]['fanfics'].pop(int(fanfic_id))
    sort(category_id)
    current_count = find_maximum_file_name()
    safe()
    return redirect(f'/categories/{category_id}')


@app.route('/add_fanfic_form/<int:category_id>')
def add_fanfic_form(category_id):
    return render_template('add_fanfic_form.html', category=category_id,
                           name=categories[category_id]['name'])


@app.route('/add_fanfic/<int:category_id>', methods=['post', 'get'])
def add_fanfic(category_id):
    global categories, current_count

    name = request.form.get('name')
    text = request.form.get('text')

    if not name:
        return render_template('add_fanfic_form.html', category=category_id,
                               name=categories[category_id]['name'], message='Введите название')

    if not text:
        return render_template('add_fanfic_form.html', category=category_id,
                               name=categories[category_id]['name'], message='Введите текст')

    current_count += 1
    with open(f'static/text/{current_count}.txt', 'w') as file:
        file.write(text)
    categories[category_id]['fanfics'].append({'name': name, 'text': f'{current_count}.txt', 'likes': 0})

    sort(category_id)
    safe()

    return redirect(f'/categories/{category_id}')


@app.route('/edit_fanfic_form/<int:category_id>/<int:fanfic_id>')
def edit_fanfic_form(category_id, fanfic_id):
    return render_template('edit_fanfic_form.html', category=category_id,
                           name=categories[category_id]['fanfics'][fanfic_id]['name'], fanfic=fanfic_id)


@app.route('/edit_fanfic/<int:category_id>/<int:fanfic_id>', methods=['post', 'get'])
def edit_fanfic(category_id, fanfic_id):
    global categories, current_count

    name = request.form.get('name')
    text = request.form.get('text')

    current_fanfic = categories[category_id]['fanfics'][fanfic_id]

    if name:
        current_fanfic['name'] = name

    if text:
        with open(f'static/text/{current_fanfic["text"]}', 'w') as file:
            file.write(text)

    sort(category_id)
    safe()

    return redirect(f'/categories/{category_id}')


@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    global categories, current_count, titles

    category = categories[category_id]

    for i in category['fanfics']:
        os.remove(f'static/text/{i["text"]}')

    categories.pop(category_id)

    current_count = find_maximum_file_name()
    titles = [i['name'] for i in categories]
    safe()
    return redirect(f'/categories/{category_id - 1}')


@app.route('/edit_category_form/<int:category_id>')
def edit_category_form(category_id):
    return render_template('edit_category_form.html', name=categories[category_id]['name'],
                           category=category_id)


@app.route('/edit_category/<int:category_id>', methods=['post', 'get'])
def edit_category(category_id):
    global categories, titles

    categories[category_id]['name'] = request.form.get('name')

    titles = [i['name'] for i in categories]

    safe()

    return redirect('/')


app.run(debug=True)
