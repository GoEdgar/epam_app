import requests

url = 'http://127.0.0.1:5000/'


# DEPARTMENT TEST
def dep_test():
    get_dep = requests.get(url + 'department').json()
    print(get_dep)

    id = requests.post(url + 'department',
                             json={'name_department': 'Прогроммист'}).json()['data']['id']
    print(id)
    del_dep = requests.delete(url + 'department/' + str(id)).json()
    print(del_dep)

##################
# EMPLOYEE TEST
def emp_test():
    get_emp = requests.get(url + 'employee').json()
    #print(get_emp)

    post_emp = requests.post(url + 'employee',
                             json={'name_department': 'Повар',
                                   'full_name': 'Edgar Gorobchuk',
                                   'date_of_brith': '2001-05-28',
                                   'salary': 100500}).json()
    print(post_emp)
    print('=====')

    put_emp = requests.put(url + 'employee/' + '40',
                           json={'full_name': 'Me Me'}).json()
    print(put_emp)

    requests.delete(url + 'employee/' + '2')

emp_test()