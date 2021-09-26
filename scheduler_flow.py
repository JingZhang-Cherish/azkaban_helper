#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys

import requests
import xlrd
from urllib3.exceptions import InsecureRequestWarning

HEADERS = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}


def login():
    config_sheet = xl.sheet_by_name('config')
    url = config_sheet.cell_value(1, 0).strip()
    if not url.endswith('/'):
        url.append('/')
    username = config_sheet.cell_value(1, 1).strip()
    password = config_sheet.cell_value(1, 2).strip()
    print('Read Azkaban Connection Info From "config" sheet: url="%s", username=%s,password=%s' % (
        url, username, password))
    session = requests.Session()
    data = {
        'action': 'login',
        'username': username,
        'password': password
    }
    response = session.post(url, data=data, verify=False, headers=HEADERS)
    if response.raise_for_status():
        raise Exception("login azkaban failed,please check the config sheet's content")
    else:
        return url, session


def create_project(url, session):
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
            'name': p_name,
            'description': p_desc
        }
        response = session.post(url + 'manager', data=data, params=params, verify=False, headers=HEADERS)
        if response.raise_for_status():
            raise Exception("request failed")
        else:
            print("create project %s %s response: %s" % (p_name, p_desc, response.json()))
            status = response.json().get('status')
            if status is None:
                raise Exception(response.json().get('error'))


def schedule_flow(url, p_name, f_name, cron):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'project': p_name,
        'ajax': 'scheduleCronFlow',
        'flow': f_name,
        'disabled': '[]',
        'failureEmailsOverride': 'false',
        'successEmailsOverride': 'false',
        'failureAction': 'finishCurrent',
        'failureEmails': '',
        'successEmails': '',
        'notifyFailureFirst': 'false',
        'notifyFailureLast': 'false',
        'concurrentOption': 'skip',
        'projectName': p_name,
        'cronExpression': cron
    }

    response = s.post(url + 'schedule', headers=headers, data=data, verify=False)
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print(response.json())
        return response.json()['scheduleId']


def remove_schedule(url, session, schedule_id):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'action': 'removeSched',
        'scheduleId': schedule_id
    }
    response = session.post(url + 'schedule', headers=headers, data=data, verify=False)
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print(response.json())


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        print('python generate_flow.py excel_path')
        print('please specified the excel file path  ')
        sys.exit(-1)
    excel_file = args[1]
    xl = xlrd.open_workbook(excel_file)
    requests.packages.urllib3.disable_warnings()

    azkaban_url, s = login()

    create_project(azkaban_url, s)
    schedule_sheet = xl.sheet_by_name('scheduler')
    for row in range(1, schedule_sheet.nrows):
        if len(schedule_sheet.row_values()) == 0:
            continue
        project_name = schedule_sheet.cell_value(row, 0).strip()
        flow_name = schedule_sheet.cell_value(row, 1).strip()
        cron = schedule_sheet.cell_value(row, 2).strip()
        if project_name == '' or flow_name == '':
            continue
        if project_name != '' and flow_name != '':
            if cron != '':
                schedule_flow(azkaban_url, project_name, flow_name, cron)
            else:
                sche_id = schedule_flow(azkaban_url, project_name, flow_name, '0 0 0 1 12 ? 2100')
                remove_schedule(azkaban_url, s, sche_id)
