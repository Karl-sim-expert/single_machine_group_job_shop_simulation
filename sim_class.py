import simpy as sp

#machine class
class Machine:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.resource = sp.Resource(env, capacity=1)


#component(wip) class
class Component:
    def __init__(self, name, job, machine_times, creation_time, duration):
        self.name = name
        self.job = job
        self.machine_times = machine_times
        self.last_machine_in_time = creation_time
        self.due_date= creation_time + duration

#job class: each job can have more than on components. 
class Job:
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        self.components.append(component)


#monitor_queue class
class Monitor_queue:
    def __init__(self, env):
        self.env = env
        self.data = []

    def record(self, resource, machine_name, component, inout):
        self.data.append({
            'time': self.env.now,
            'count': len(resource.queue),
            'users': len(resource.users),
            'machine' : machine_name,
            'component' :component.name,
            'in_out' : inout
        })

#monitor_tat class
class Monitor_tat:
    def __init__(self, env):
        self.env = env
        self.data = []

    def record(self, component, machine_name):
        self.data.append({
            'last_updated_time': self.env.now,
            'component_name': component.name,
            'machine_name' : machine_name,
            'due_date' : component.due_date,
            'creation_time' : component.last_machine_in_time,
            'remaining_time_until_due' : component.due_date - self.env.now,
            'step_tat' : self.env.now - component.last_machine_in_time,
            'job_name' : component.job.name,
            'waiting_count_on_same_job' : len(component.job.components)
           
        })        