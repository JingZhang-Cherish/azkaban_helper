import os

from gooey import Gooey, GooeyParser
from generator import *


@Gooey(program_name="Azkaban配置工具 v1.0.2", required_cols=2, optional_cols=2, language='chinese')
def main():
    settings_msg = 'azkaban project配置文件转job和上传工具'
    parser = GooeyParser(description=settings_msg)
    parser.add_argument('config_file', metavar='配置文件路径', widget="FileChooser")  # 文件选择框
    parser.add_argument('output_dir', metavar='输出目录', widget="DirChooser")  # 文件选择框
    parser.add_argument("exec_mode", metavar='执行模式', help="请选择执行模式",
                        choices=['仅生成项目', '仅上传项目', '仅调度项目', '所有'], default='所有')

    args = parser.parse_args()  # 接收界面传递的参数
    file = args.config_file
    mode = args.exec_mode
    output_dir = args.output_dir

    ###########################
    requests.packages.urllib3.disable_warnings()
    # handle args

    generate_only, create_only, upload_only, schedule_only = False, False, False, False
    if mode == '仅生成项目':
        generate_only = True
    elif mode == '仅上传项目':
        upload_only = True
    elif mode == '仅调度项目':
        schedule_only = True

    excel = xlrd.open_workbook(file)
    # get valid sheets
    valid_sheets = get_valid_projects(excel)
    web_configs = get_urls_info(excel)
    for w in web_configs:
        url, username, password, save_dir = w[0], w[1], w[2], w[3]
        if output_dir:
            save_dir = output_dir
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
            sys.exit()
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
        generator(excel, valid_sheets, save_dir)
        print("============generator projects Successfully!============")
        make_zip(valid_sheets, save_dir)
        print("============compress projects Successfully!============")
        # The steps below is needed connection to Azkaban Server
        session = login(url, username, password)
        pro_map = create_project(excel, url, session)
        run_upload(url, session, valid_sheets, save_dir)
        print("============upload projects Successfully!============")
        schedule(excel, url, session, pro_map)
        print("============schedule flows Successfully!============")
        session.close()


if __name__ == '__main__':
    main()
