#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

import xlrd

'''
project_name	flow_name	flow_desc	flow_configs	job_name	job_comment	type	command	dependOn
ods	ODS_USER_INFO	用户信息	base_dir=/home/pg/ods;yxj=100;retries=3	jobA	作业A	command	sh ${base_dir}/user_info.sh	
ods	ODS_USER_INFO	用户信息	base_dir=/home/pg/ods;yxj=100;retries=4	jobB	作业B	command	sh ${base_dir}/step2.sh	jobA
ods	ODS_USER_INFO	用户信息	base_dir=/home/pg/ods;yxj=100;retries=5	jobC	作业C	command	sh ${base_dir}/step2.sh	jobB,JobA
'''


def parse_flows():
    flow_list = {}
    sheet = xl.sheet_by_name('flows')
    for i in range(1, sheet.nrows):
        line = sheet.row_values(i)
        if len(line) == 0:
            pass
        flow = flow_list.get(line[1])
        # 从flow_list中取出flow
        if flow is None:
            flow = {}
        config = flow.get('config')
        if config is None:
            config = {}
        if line[3] is not None:
            for conf in line[3].strip().split(','):
                print(conf)
                cp = conf.strip().split('=')
                if cp == '':
                    pass
                config[cp[0]] = cp[1]
        if config is not None:
            flow['config'] = config

        nodes = flow.get('nodes')
        if nodes is None:
            nodes = []
        job_name = line[4].strip()
        job_type = line[6].strip()
        job_config = {'command': line[7].strip()}
        job = {'name': job_name, 'type': job_type, 'config': job_config}
        nodes.append(job)
        flow['nodes'] = nodes

        flow_list[line[1]] = flow
    return flow_list


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        print('please specified the execl file path')
        sys.exit(-1)

    xl = xlrd.open_workbook(args[1])
    flows = parse_flows()
    print(flows)
