import simhelper as sh
import random 
import inspect
from collections import deque


def call_dispatch_function(func, *args, **kwargs):
    sig = inspect.signature(func)
    num_args = len(sig.parameters)
    
    # 필요한 인자만 전달
    return func(*args[:num_args])

#dispatcher class - FIFO
def FIFO(component_queue):
    return component_queue.get()
   


def dispatcher(env, machine_obj, component_queue, monitor, dis_rule):
    while True:
        
        component = yield call_dispatch_function(dispatch_set[dis_rule], component_queue  ) 
        
        #store queue 에서 고를 랏이 들어갈 장비 선정
        machine_queue_len_list = [len(b.resource.queue) for a,b in machine_obj.items()]
        machine_index = random.choice([i for i,value in enumerate(machine_queue_len_list) if value == min(machine_queue_len_list)])
        
        #작업 맡김
        env.process(sh.component_process(env, component, machine_obj[list(machine_obj.keys())[machine_index]], monitor, machine_index))


#dictionary_set
dispatch_set = {'FIFO': FIFO}