import os
from argparse import ArgumentParser

from gooey import Gooey, GooeyParser
from generator import *


@Gooey(program_name="Azkaban配置工具 v1.0.2", required_cols=2, optional_cols=3, language='chinese', encoding='utf-8',
       default_size=(810, 530))
def main():
    settings_msg = 'azkaban project配置文件转job和上传工具'
    parser = GooeyParser(description=settings_msg)

    parser.add_argument('config_file', metavar='配置文件路径', widget="FileChooser",
                        default='/Users/jing/PycharmProjects/azkaban_excel_yaml/docs/1zhfd_azkaban.xlsx')  # 文件选择框
    parser.add_argument('output_dir', metavar='输出目录', widget="DirChooser",
                        default='/Users/jing/PycharmProjects/azkaban_excel_yaml/src')  # 目录选择框
    parser.add_argument('url', metavar='web url', widget='TextField', default='https://worker03:18443',
                        help='azkaban web地址')  # 文本
    parser.add_argument('username', metavar='用户名', widget='TextField', default='admin', help='azkaban web用户名')  # 文本
    parser.add_argument('password', metavar='密码', widget='PasswordField', default='admin', help='azkaban web密码')  # 文本
    parser.add_argument("exec_mode", metavar='执行模式', help="请选择执行模式", choices=['仅生成项目', '仅上传项目', '仅调度项目', '全选'],
                        default='全选')

    # parser.add_argument(widget='DropDown',dest='text',action='store')

    args = parser.parse_args()  # 接收界面传递的参数
    file = args.config_file
    mode = args.exec_mode
    username = args.username
    password = args.password
    save_dir = args.output_dir
    url = args.url
    if not url.endswith('/'):
        url = url + '/'
    print('input args:' +
          '\nfile    :' + file +
          '\nmode    :' + mode +
          '\nusername:' + username +
          '\npassword:' + password +
          '\nurl     :' + url +
          '\nsave_dir:' + save_dir)
    ###########################
    requests.packages.urllib3.disable_warnings()
    # handle args

    generate_only, create_only, upload_only, schedule_only = False, True, False, False
    if mode == '仅生成项目':
        generate_only = True
    elif mode == '仅上传项目':
        upload_only = True
    elif mode == '仅调度项目':
        schedule_only = True

    excel = xlrd.open_workbook(file)
    # get valid sheets
    valid_sheets = get_valid_projects(excel)
    if not generate_only and not upload_only and not schedule_only:
        generator(excel, valid_sheets, save_dir)
        print("============generator projects Successfully!============")
        make_zip(valid_sheets, save_dir)
        print("============compress projects Successfully!============")
        # The steps below is needed connection to Azkaban Server
        session = login(url, username, password)
        create_project(excel, url, session)
        pro_map = create_project(excel, url, session)
        run_upload(url, session, valid_sheets, save_dir)
        print("============upload projects Successfully!============")
        schedule(excel, url, session, pro_map)
        print("============schedule flows Successfully!============")
        sys.exit(0)

    if generate_only:
        generator(excel, valid_sheets, save_dir)
        print("============generator projects Successfully!============")
        make_zip(valid_sheets, save_dir)
        print("============compress projects Successfully!============")
        sys.exit()
    if create_only:
        session = login(url, username, password)
        create_project(excel, url, session)
        session.close()
    if upload_only:
        session = login(url, username, password)
        run_upload(url, session, valid_sheets, save_dir)
        session.close()
        sys.exit()
    if schedule_only:
        session = login(url, username, password)
        pro_map = create_project(excel, url, session)
        schedule(excel, url, session, pro_map)
        session.close()
        sys.exit()


if __name__ == '__main__':
    main()
