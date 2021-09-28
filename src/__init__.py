import os
import sys

import requests
import xlrd

import generator as gen
import scheduler as sc


def start():
    excel_file = args[0]
    if os.path.exists(excel_file) is None:
        print(excel_file, 'is not exists')
        sys.exit(-2)
    requests.packages.urllib3.disable_warnings()
    xl = xlrd.open_workbook(excel_file)
    flow_sheets = xl.sheet_names()
    azkaban_url, s, save_dir = gen.login(xl)
    if save_dir.endswith(os.sep):
        save_dir = save_dir[:-1]
    if os.path.isdir(save_dir) is None:
        print(save_dir, 'is not exists')
        os.mkdir(save_dir)

    # gen.generator(xl, flow_sheets, save_dir)
    # gen.run_upload(xl)
    gen.schedule(xl, azkaban_url, s)
    s.close()


if __name__ == '__main__':
    global args
    args = sys.argv
    if len(args) < 1:
        print('python generator.py excel_path')
        sys.exit(-1)
    start()
