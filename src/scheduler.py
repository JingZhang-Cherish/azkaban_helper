#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

import requests

HEADERS = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}


def login(excel):
    config_sheet = excel.sheet_by_name('config')
    url = config_sheet.cell_value(1, 0).strip()
    if not url.endswith(os.sep):
        url.append(os.sep)
    username = config_sheet.cell_value(1, 1).strip()
    password = config_sheet.cell_value(1, 2).strip()
    base_dir = config_sheet.cell_value(1, 3).strip()
    if base_dir == '':
        base_dir = os.getcwd()
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
        return url, session, base_dir


def create_project(excel, url, session):
    ps = excel.sheet_by_name('projects')
    for r in range(1, ps.nrows):
        p_name = ps.cell_value(r, 0)
        if p_name == '':
            continue
        p_desc = ps.cell_value(r, 1)
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


def schedule_flow(url, session, p_name, f_name, cron):
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

    response = session.post(url + 'schedule', headers=headers, data=data, verify=False)
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


def upload_project(url, session, base_dir, project):
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    zip_file_name = project + '.zip'
    zip_path = base_dir + zip_file_name

    upload_data = MultipartEncoder(
        fields={
            'ajax': 'upload',
            'project': project,
            'file': (zip_file_name, open(zip_path, 'rb'), 'application/zip')
        }
    )

    response = session.post(url + 'manager', data=upload_data, headers={'Content-Type': upload_data.content_type})
    if response.raise_for_status():
        raise Exception("request failed")
    else:
        print('upload project: %s successfully! success info: %s' % (project, response.json()))


def schedule(excel, url, session):
    schedule_sheet = excel.sheet_by_name('scheduler')
    for row in range(1, schedule_sheet.nrows):
        if len(schedule_sheet.row_values(row)) == 0:
            continue
        project_name = schedule_sheet.cell_value(row, 0).strip()
        flow_name = schedule_sheet.cell_value(row, 1).strip()
        cron = schedule_sheet.cell_value(row, 2).strip()
        if project_name == '' or flow_name == '':
            continue
        if project_name != '' and flow_name != '':
            if cron != '':
                schedule_flow(url, session, project_name, flow_name, cron)
            else:
                sche_id = schedule_flow(url, session, project_name, flow_name, '0 0 0 1 12 ? 2100')
                remove_schedule(url, session, sche_id)


'''
the sheets that exits in projects list. 
In other words ,the project has configure at a single sheet
'''


def valid_project(xl):
    valid_projects = []
    for project in xl.sheet_names():
        # the sheets of list didn't to handle
        exclude_sheets = ['info', 'projects', 'config', 'scheduler']
        if not {project.strip()}.issubset(exclude_sheets):
            valid_projects.append(project.strip())
    return valid_projects


def run(xl):
    requests.packages.urllib3.disable_warnings()
    azkaban_url, s, b_dir = login(xl)
    create_project(xl, azkaban_url, s)
    configured_projects = valid_project(xl)
    for p in configured_projects:
        upload_project(azkaban_url, s, b_dir, p)
    schedule(xl, azkaban_url, s)
    s.close()
