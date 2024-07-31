import simhelper as sh
import random 
import inspect
from collections import deque


def call_dispatch_function(func, *args, **kwargs):
    sig = inspect.signature(func)
    num_args = len(sig.parameters)
    
    # 필요한 인자만 전달
    return func(*args[:num_args])

#FIFO policy
def FIFO(component_queue):
    return component_queue.get()

#SPT policy
def SPT(component_queue, machine_index):
    component_queue.items.sort(key=lambda x: x.machine_times[machine_index])
    return component_queue.get()

#EDD policy 
def EDD(component_queue):
    component_queue.items.sort(key=lambda x:x.due_date)
    return component_queue.get()

#CR policy 
def CR(component_queue, machine_index, a_now) :
    component_queue.items.sort(key=lambda x: (x.due_date -  a_now) / x.machine_times[machine_index]  )
    return component_queue.get()

#SLACk policy 
def SLACK(component_queue, machine_index, a_now) :
    component_queue.items.sort(key=lambda x: (x.due_date -  a_now) - x.machine_times[machine_index]  )
    return component_queue.get()

#main dispatching function
def dispatcher(env, machine_obj, component_queue, monitor_queue, monitor_tat,  dis_rule):
    while True:

         #store queue 에서 고를 랏이 들어갈 장비 선정
        machine_queue_len_list = [len(b.resource.queue) for a,b in machine_obj.items()]
        machine_index = random.choice([i for i,value in enumerate(machine_queue_len_list) if value == min(machine_queue_len_list)])

        #store queue에서 작업 고름 
        component = yield call_dispatch_function(dispatch_set[dis_rule], component_queue, machine_index, env.now) 
    
        
        #작업 맡김
        env.process(sh.component_process(env, component, machine_obj[list(machine_obj.keys())[machine_index]], monitor_queue, monitor_tat,  machine_index))


#dictionary_set
dispatch_set = {'FIFO': FIFO, 'SPT': SPT, 'EDD' : EDD, 'CR': CR, 'SLACK': SLACK}