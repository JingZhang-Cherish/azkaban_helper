#!/usr/bin/python
# -*- coding: UTF-8 -*-
import collections
import os
import sys
import shutil
import xlrd

from collections import OrderedDict
import yaml


def ordered_yaml_load(yaml_path, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    with open(yaml_path) as stream:
        return yaml.load(stream, OrderedLoader)


def ordered_yaml_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


'''
 check dependency jobs whether exits in above jobs or not
'''


def check_job(flow, depend_jobs):
    exists_jobs = []
    for job in flow['nodes']:
        exists_jobs.append(job.get('name'))
    return set(depend_jobs).issubset(exists_jobs)


'''
check some cell value whether is null or not
'''


def null(var, desc):
    if len(var.strip()) == 0:
        raise Exception('The value ' + desc + 'is required')


'''
parse jobs and flows from excel 
'''


def parse_flows(sheet_name):
    flow_list = collections.OrderedDict()
    sheet1 = xl.sheet_by_name(sheet_name)
    for i in range(1, sheet1.nrows):
        line = sheet1.row_values(i)
        if len(line) == 0:
            pass
        # get a flow from flow_list
        flow = flow_list.get(line[1], collections.OrderedDict())
        config = parse_flow_config(flow, i, line)
        if config is not None:
            flow['config'] = config

        nodes = flow.get('nodes')
        if nodes is None:
            nodes = []

        job = parse_job(flow, line)
        nodes.append(job)
        flow['nodes'] = nodes

        flow_list[line[1]] = flow
    return flow_list


'''
parse flow config from excel column
'''


def parse_flow_config(flow, i, line):
    config = flow.get('config', collections.OrderedDict())
    if len(config) != 0:
        return config
    if line[3] is not None:
        for conf in line[3].strip().split('|'):
            cp = conf.strip().split('=')
            if cp == '':
                pass
            config[cp[0]] = cp[1]
    else:
        print('location the ' + str(i) + 'th row: flow_configs is null ')
    return config


'''
parse jobs config from excel column
'''


def parse_job(flow, line):
    job_name, job_type = check_null(line)
    job = collections.OrderedDict()
    job['name'] = job_name
    job['type'] = job_type
    depend_jobs = []
    if line[8] is not None and line[8].strip() != '':
        depend_jobs = line[8].strip().split('|')
    if len(depend_jobs) != 0:
        job['dependsOn'] = depend_jobs
        if not check_job(flow, depend_jobs):
            raise Exception(
                'job ' + line[1] + '\'s depends: ' + line[8] + ' On not exist in above jobs')
    job_config = {'command': line[7]}
    job['config'] = job_config
    return job


'''
check null parameter from excel column
'''


def check_null(line):
    job_name = line[4].strip()
    null(job_name, 'job_name')
    job_type = line[6].strip()
    null(job_type, 'job_type')
    return job_name, job_type


def handle_dir(base_dir, sheet_name):
    try:
        shutil.rmtree(base_dir)
    except FileNotFoundError:
        pass
    os.mkdir(base_dir)
    # generate azkaban version describe file
    with open(base_dir + os.sep + sheet_name + '.project', 'w', encoding='utf-8') as version_file:
        version_file.write('azkaban-flow-version: 2.0')
        version_file.close()


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('python generate_flow.py excel_path dir_name')
        print('please specified the excel file path and the base directory to save flow files ')
        sys.exit(-1)
    excel_file = args[1]
    if os.path.exists(excel_file) is None:
        print(excel_file, 'is not exists')
        sys.exit(-2)
    save_dir = args[2]
    if os.path.isdir(save_dir) is None:
        print(save_dir, 'is not exists')
        os.mkdir(save_dir)

    xl = xlrd.open_workbook(excel_file)
    flow_sheets = xl.sheet_names()

    for sheet in flow_sheets:
        # the sheets of list didn't to handle
        exclude_sheets = ['info', 'projects', 'config', 'scheduler']
        if {sheet.strip()}.issubset(exclude_sheets):
            continue
        flows = parse_flows(sheet)
        project_dir = save_dir + os.sep + sheet
        handle_dir(project_dir, sheet)
        for f in flows:
            flow_file = project_dir + os.sep + f + '.flow'
            with open(flow_file, 'w', encoding='utf-8') as output:
                ordered_yaml_dump(flows[f], output)
                output.close()
