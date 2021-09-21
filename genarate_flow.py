#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

import xlrd

from Bean import Project


def parse_project():
    project_list = []
    sheet = xl.sheet_by_name('projects')
    for i in range(1, sheet.nrows):
        project_list.append(Project(sheet.cell(i, 0).value, sheet.cell(i, 1).value))
    print(project_list[0].format())
    return project_list


def parse_flows():
    flow_list = []
    xl.sheet_by_name('flows')

    return flow_list

def parse_jobs():
    sheet=xl.sheet_by_name('jobs')
    for i in range(1,sheet.nrows):
        print(i)




if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        print('pleas specified the execl file path')
        sys.exit(-1)

    xl = xlrd.open_workbook(args[1])

    projects = parse_project()
    flows = parse_flows()
