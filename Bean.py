from typing import Any


class Project:
    name = ''
    desc = ''

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def format(self) -> dict[str, Any]:
        return {'name': self.name, 'desc': self.desc}


class Job:
    name = 'undefined'
    type = 'command'
    command = ''
    config = ''
    dependsOn = []

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def set_command(self, command):
        self.command = command

    def set_depends_on(self, depend):
        self.dependsOn.append(depend)

    def format(self) -> dict[str, Any]:
        return {'name': self.name, 'desc': self.type, 'command': self.command, 'dependsOn': self.dependsOn}


class FlowConfig:
    configs = {}

    def __init__(self):
        pass

    def add_config(self, key, value):
        self.configs = {'%s': '%s'} % (key, value)

    def format(self) -> dict[str, Any]:
        return {'config': self.configs}


'''
节点类
'''


class Nodes:
    jobs = [Job.format()]

    def __init__(self, jobs):
        self.jobs = jobs

    def format(self) -> dict[str, Any]:
        return {'nodes': self.jobs}


class Flow:
    flow_configs = dict[FlowConfig.format()]
    nodes = dict[Nodes.format()]

    def __init__(self, flow_configs, nodes):
        self.flow_configs = flow_configs
        self.nodes = nodes

    def __str__(self) -> dict[str, Any]:
        return {'config': self.flow_configs, 'nodes': self.nodes}
