import sys

import xlrd

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        print('python generate_flow.py excel_path')
        print('please specified the excel file path  ')
        sys.exit(-1)
    excel_file = args[1]
    xl = xlrd.open_workbook(excel_file)
    config_sheet = xl.sheet_by_name('config')

    sheet = xl.sheet_by_name('scheduler')
