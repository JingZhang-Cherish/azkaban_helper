# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

import xlrd
import yaml

from Job import Job


def open_excel(filename):
    xl = xlrd.open_workbook(filename)
    for i in range(0, xl.nsheets):
        sheet = xl.sheet_by_index(i)
        print(sheet.name)
        # print(sheet.nrows)
        # print(sheet.ncols)
        sheet = xl.sheet_by_index(0)
        content = sheet.row_values(0)
        with open("G:\\tmp\\myPython\\test.yaml", 'w') as f:
            yaml.dump(content, f)


if __name__ == '__main__':
    fi = "G:\\tmp\\myPython\\test.xlsx"
    open_excel(fi)
    jobs = []
    job1 = Job('job1', 'cc')
    job2 = Job('job2', 'command')
    job2.set_command("echo $dt")
    job1.set_command("echo 123")
    job1.set_depends_on(job2.job_name)

    with open('G:\\tmp\\myPython\\azkaban\\test.flow', 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.Loader)
        print(data)
        f.close()
    with open('G:\\tmp\\myPython\\azkaban\\test1.flow', 'w', encoding='utf8') as f:
        yaml.dump(data, f)
        f.close()
