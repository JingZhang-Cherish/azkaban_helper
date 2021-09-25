#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests


def login():
    global headers, response, res
    s = requests.Session()
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}
    data = {
        'action': 'login',
        'username': 'admin',
        'password': 'admin'
    }
    response = s.post('https://192.168.200.100:8443', data=data, verify=False, headers=headers)
    res = response.json()
    return s, res.get('session.id')


if __name__ == '__main__':
    # make_zip('G:\\tmp\\azkaban\\ora2pg','G:\\tmp\\azkaban\\ora2pg\\ora2pg.zip')

    s, session_id = login()
    print(session_id)
    #
    # params = (
    #     ('action', 'create'),
    # )
    # data2 = {
    #     'session.id': session_id,
    #     'name': 'ods',
    #     'description': 'ods层贴源数据'
    # }
    # response = requests.post('https://192.168.200.100:8443/manager', params=params,data=data2, verify=False, headers=headers)
    # print(response.json())

    file_path = "G:\\tmp\\azkaban\\ora2pg.zip"
    headers = {'Content-Type': 'type=application/zip', 'X-Requested-With': 'XMLHttpRequest'}
    params = (
        ('project', 'ora2pg'),
    )
    data3 = {
        'session.id': session_id,
        'type': 'application/zip',
        'file': file_path,
        'project': 'ora2pg',
        'ajax': 'upload'
    }
    files = {'file': open(file_path, 'rb')}
    print('upload file to azkaban')
    response = s.post(url='https://192.168.200.100:8443/manager?ajax=upload', params=params, data=data3,
                      verify=False, headers=headers, files=files)
    print(response.status_code)
    print(response.text)

