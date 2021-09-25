#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

import requests
import xlrd

HEADERS = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}


def login():
    config_sheet = xl.sheet_by_name('config')
    azkaban_url = config_sheet.cell_value(1, 0).strip()
    if not azkaban_url.endswith('/'):
        azkaban_url = azkaban_url + '/'
    username = config_sheet.cell_value(1, 1).strip()
    password = config_sheet.cell_value(1, 2).strip()
    data = {
        'action': 'login',
        'username': username,
        'password': password
    }
    response = requests.post(azkaban_url, data=data, verify=False, headers=HEADERS)
    if response.raise_for_status():
        raise Exception("login azkaban failed,please check the config sheet's content")
    else:
        sid = response.json().get('session.id')
        if sid is None:
            raise Exception(response.json().get('error'))
        return azkaban_url, sid


def create_project(azkaban_url, sid):
    ps = xl.sheet_by_name('projects')
    for row in range(1, ps.nrows):
        if len(ps.row_values(row)) == 0:
            continue
        p_name = ps.cell_value(row, 0)
        p_desc = ps.cell_value(row, 1)
        if p_desc == '':
            p_desc = p_name
        params = (
            ('action', 'create'),
        )
        data = {
            'session.id': sid,
            'name': p_name,
            'description': p_desc
        }
        response = requests.post(azkaban_url + 'manager', data=data, params=params, verify=False, headers=HEADERS)
        print("response.json()", response.json())
        if response.raise_for_status():
            raise Exception("request failed")
        else:
            status = response.json().get('status')
            if status is None:
                raise Exception(response.json().get('error'))


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        print('python generate_flow.py excel_path')
        print('please specified the excel file path  ')
        sys.exit(-1)
    excel_file = args[1]
    xl = xlrd.open_workbook(excel_file)

    url, session_id = login()
    create_project(url, session_id)

    # curl -k -X POST --data "session.id=9089beb2-576d-47e3-b040-86dbdc7f523e&name=aaaa&description=11" https://localhost:8443/manager?action=create
