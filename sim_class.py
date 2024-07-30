import simpy as sp

#machine class
class Machine:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.resource = sp.Resource(env, capacity=1)


#component(wip) class
class Component:
    def __init__(self, name, job, machine_times):
        self.name = name
        self.job = job
        self.machine_times = machine_times #define in the format of dictionary such as machine0 : 30

#job class: each job can have more than on components. 
class Job:
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        self.components.append(component)


#monitor class
class Monitor:
    def __init__(self, env):
        self.env = env
        self.data = []

    def record(self, resource, machine_name, inout):
        self.data.append({
            'time': self.env.now,
            'count': len(resource.queue),
            'users': len(resource.users),
            'machine' : machine_name,
            'in_out' : inout
        })