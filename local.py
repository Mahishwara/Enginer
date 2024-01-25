import csv
import re
import urllib.request
from xml.dom import minidom

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def format_data(data):
    return ' '.join(re.sub(r'<[^>]+>', '', data).split())


def csv_reader():
    with open('vacancies.csv', encoding='utf_8_sig') as file:
        rur_dict = {}
        vacancies = []
        flag = True
        year = ''
        for vacancy in csv.reader(file):
            if flag:
                flag = False
                continue
            result = []
            for i in range(len(vacancy)):
                match i:
                    case 0:
                        result.append(format_data(vacancy[i]))
                    case 1:
                        if '\n' in vacancy[i]:
                            result.append([format_data(desc) for desc in vacancy[i].split('\n')])
                        else:
                            result.append(format_data(vacancy[i]))
                    case 2:
                        result.append(float(vacancy[i]) if vacancy[i] != '' else float(0.0))
                    case 3:
                        if vacancy[i] != '':
                            if result[2] != 0.0:
                                result[2] = (float(vacancy[i]) + result[2]) / 2
                            else:
                                result[2] = float(vacancy[i])
                    case 4:
                        result.append(vacancy[i])
                    case 5:
                        result.append(vacancy[i])
                    case 6:
                        date = vacancy[i]; result.append(date[8:10] + '/' + date[5:7] + '/' + date[:4])
            if result[3] != 'BYR':
                if result[3] != 'RUR' and result[3] != '':
                    if result[5][3:10] in rur_dict.keys():
                        if result[3] != '':
                            result[2] = result[2] * rur_dict[result[5][3:10]][result[3]]
                        else:
                            result = 0.0
                    else:
                        result[2], rur_dict = get_RUR(result[2], result[3], result[5], rur_dict)
                vacancies.append(result)
            if result[5][6:10] != year:
                print(result[5][6:10])
                year = result[5][6:10]
        return vacancies


def get_RUR(salary, salary_currency, date, rur_dict):
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    params = {
        'date_req': '01/' + date[3:10],
    }

    web_file = urllib.request.urlopen(url).read()
    dom = minidom.parseString(web_file)
    dom.normalize()
    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}
    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = float(child.firstChild.data.replace(',', '.'))
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value
    rur_dict = {date[3:10]: currency_dict}
    if salary_currency != '':
        return salary * currency_dict[salary_currency], rur_dict
    return 0.0, rur_dict


def getStatistic(vacancies):
    years = []
    cities = []
    total_count = len(vacancies)
    salary_by_years = {}
    prof_salary_by_years = {}
    count_by_years = {}
    prof_count_by_years = {}
    salary_by_cities = {}
    prof_salary_by_cities = {}
    part_by_cities = {}
    prof_part_by_cities = {}
    top_skills_by_years = {}
    prof_top_skills_by_years = {}
    for vacancy in vacancies:
        city = vacancy[4]
        year = vacancy[5][6:10]
        if city in cities and year in years:
            if vacancy[2] != 0.0 and vacancy[2] <= 10000000:
                if year in salary_by_years.keys():
                    salary_by_years[year].append(vacancy[2])
                else:
                    salary_by_years[year] = [vacancy[2]]
                if city in salary_by_cities.keys():
                    salary_by_cities[city].append(vacancy[2])
                else:
                    salary_by_cities[city] = [vacancy[2]]
            count_by_years[year] += 1
            part_by_cities[city] += (1 / total_count)
            if vacancy[1] != '':
                for skill in vacancy[1]:
                    if skill not in top_skills_by_years[year].keys():
                        top_skills_by_years[year][skill] = 1
                    else:
                        top_skills_by_years[year][skill] += 1
        elif city not in cities:
            cities.append(city)
            if vacancy[2] != 0.0 and vacancy[2] <= 10000000:
                salary_by_cities[city] = [vacancy[2]]
            part_by_cities[city] = 1 / total_count
        if year not in years:
            years.append(year)
            if vacancy[2] != 0.0 and vacancy[2] <= 10000000:
                salary_by_years[year] = [vacancy[2]]
            count_by_years[year] = 1
            top_skills_by_years[year] = {}
            if vacancy[1] != '':
                for skill in vacancy[1]:
                    if skill not in top_skills_by_years[year].keys():
                        top_skills_by_years[year][skill] = 1
        if isProf(vacancy[0]):
            if vacancy[2] != 0.0 and vacancy[2] <= 10000000:
                if year not in prof_salary_by_years.keys():
                    prof_salary_by_years[year] = [vacancy[2]]
                else:
                    prof_salary_by_years[year].append(vacancy[2])
                if city not in prof_salary_by_cities.keys():
                    prof_salary_by_cities[city] = [vacancy[2]]
                else:
                    prof_salary_by_cities[city].append(vacancy[2])
            if year not in prof_count_by_years.keys():
                prof_count_by_years[year] = 1
            else:
                prof_count_by_years[year] += 1
            if city not in prof_part_by_cities.keys():
                prof_part_by_cities[city] = 1
            else:
                prof_part_by_cities[city] += 1
            if year not in prof_top_skills_by_years.keys():
                prof_top_skills_by_years[year] = {}
            else:
                if vacancy[2] != 0.0 and vacancy[2] <= 10000000:
                    for skill in vacancy[1]:
                        if skill not in prof_top_skills_by_years[year].keys():
                            prof_top_skills_by_years[year][skill] = 1
                        else:
                            prof_top_skills_by_years[year][skill] += 1
    salary_by_years = {key: sum(item) / len(item) for key, item in salary_by_years.items()}
    prof_salary_by_years = {key: sum(item) / len(item) for key, item in prof_salary_by_years.items()}
    salary_by_cities = {key: sum(value) / len(value) for key, value in salary_by_cities.items()}
    salary_by_cities = sorted(salary_by_cities.items(), key=lambda kv: kv[1], reverse=True)
    prof_salary_by_cities = {key: sum(value) / len(value) for key, value in prof_salary_by_cities.items()}
    prof_salary_by_cities = sorted(prof_salary_by_cities.items(), key=lambda kv: kv[1], reverse=True)
    part_by_cities = sorted(part_by_cities.items(), key=lambda kv: kv[1], reverse=True)
    prof_part_by_cities = {key: item / sum(prof_count_by_years.values()) for key, item in prof_part_by_cities.items()}
    prof_part_by_cities = sorted(prof_part_by_cities.items(), key=lambda kv: kv[1], reverse=True)
    for key, value in top_skills_by_years.items():
        top_skills_by_years[key] = sorted(value.items(), key=lambda kv: kv[1], reverse=True)
    for key, value in prof_top_skills_by_years.items():
        prof_top_skills_by_years[key] = sorted(value.items(), key=lambda kv: kv[1], reverse=True)
    return (salary_by_years, prof_salary_by_years, count_by_years, prof_count_by_years, salary_by_cities, prof_salary_by_cities,
            part_by_cities, prof_part_by_cities, top_skills_by_years, prof_top_skills_by_years)


def isProf(title):
    prof = ['engineer', 'инженер программист', 'інженер', 'it инженер', 'инженер разработчик']
    for i in prof:
        if i in title:
            return True
    return False


def generate_first_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                {% for item in my_array %}
                <tr>
                <td>{{item[0]}}</td>
                <td>{{item[1]}}</td>
                {% endfor %}
                </tr>
                </table>""")
    my_array = [(key, round(value, 2)) for key, value in data.items()]
    with open('First graphic.txt', 'w') as file:
        file.writelines(template.render(my_array=my_array))


def generate_second_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                {% for item in my_array %}
                <tr>
                <td>{{item[0]}}</td>
                <td>{{item[1]}}</td>
                {% endfor %}
                </tr>
                </table>""")
    my_array = [(key, round(value, 2)) for key, value in data.items()]
    with open('Second graphic.txt', 'w') as file:
        file.writelines(template.render(my_array=my_array))

def generate_third_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                {% for item in my_array %}
                <tr>
                <td>{{item[0]}}</td>
                <td>{{item[1]}}</td>
                {% endfor %}
                </tr>
                </table>""")
    my_array = [(key, round(value, 2)) for key, value in data.items()]
    with open('Third graphic.txt', 'w') as file:
        file.writelines(template.render(my_array=my_array))

def generate_fourth_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                {% for item in my_array %}
                <tr>
                <td>{{item[0]}}</td>
                <td>{{item[1]}}</td>
                {% endfor %}
                </tr>
                </table>""")
    my_array = [(key, round(value, 2)) for key, value in data.items()]
    with open('Fourth graphic.txt', 'w') as file:
        file.writelines(template.render(my_array=my_array))


def generate_fifth_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                {% for item in my_array %}
                <tr>
                <td>{{item[0]}}</td>
                <td>{{item[1]}}</td>
                {% endfor %}
                </tr>
                </table>""")
    with open('Fifth graphic.txt', 'w') as file:
        file.writelines(template.render(my_array=data[:30]))


def generate_sixth_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                {% for item in my_array %}
                <tr>
                <td>{{item[0]}}</td>
                <td>{{item[1]}}</td>
                {% endfor %}
                </tr>
                </table>""")
    with open('Sixth graphic.txt', 'w') as file:
        file.writelines(template.render(my_array=data[:30]))

def generate_seventh_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                {% for item in my_array %}
                <tr>
                <td>{{item[0]}}</td>
                <td>{{item[1]}}</td>
                {% endfor %}
                </tr>
                </table>""")
    with open('Seventh graphic.txt', 'w') as file:
        file.writelines(template.render(my_array=data[:30]))

def generate_eighth_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                {% for item in my_array %}
                <tr>
                <td>{{item[0]}}</td>
                <td>{{item[1]}}</td>
                {% endfor %}
                </tr>
                </table>""")
    with open('Eighth graphic.txt', 'w') as file:
        file.writelines(template.render(my_array=data[:30]))




def generate_tenth_table(data):
    from jinja2 import Template
    template = Template("""
                <table style="border:2px black solid">
                <tr>
                {% for i in my_keys %}
                <td>{{i}}</td>
                {% endfor %}
                </tr>
                {% for item in my_array %}
                <tr>
                {% for i in item %}
                <td>{{i}}</td>
                {% endfor %}
                {% endfor %}
                </tr>
                </table>""")
    my_array = []
    new_array = []
    for item in data.values():
        row = []
        for key, value in item:
            row.append(f'{key}: {value}')
        new_array.append(row)
    tr_array = [[0 for i in range(len(new_array))] for j in range(len(new_array[0]))]
    for i in range(len(new_array)):
        for j in range(len(new_array[0])):
            tr_array[j][i] = new_array[i][j]
    my_array.append(tr_array)
    with open('Eighth graphic.txt', 'w') as file:
        file.writelines(template.render(my_keys=data.keys(), my_array=my_array))




stat = getStatistic(csv_reader())
print(stat[8], stat[9], sep='\n')
generate_first_table(stat[0])
generate_second_table(stat[1])
generate_third_table(stat[2])
generate_fourth_table(stat[3])
generate_fifth_table(stat[4])
generate_sixth_table(stat[5])
generate_seventh_table(stat[6])
generate_eighth_table(stat[7])
generate_tenth_table({key: value[:20] for key, value in stat[9].items() if value})
