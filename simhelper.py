import random
import sim_class as sc
import queue
#define a function that filters out the tokens that are not number
def non_num_remover(tokens):
    numbers = []
    for token in tokens: 
        if token.isdigit():
            numbers.append(token)
        else:
            pass
    return numbers

#function that performs the processing of component
def component_process(env, component, machine_obj, monitor_queue,monitor_tat,  machine_index):
    machine_name  = machine_obj.name
    process_time = component.machine_times[machine_index]
    
    machine = machine_obj


    with machine.resource.request() as request:
        yield request
        monitor_queue.record(machine.resource, machine_name, component, "machine_in") #data acquisition via monitor

        print(f"{env.now}: {component.name} of {component.job.name} starting on {machine.name}")
        yield env.timeout(process_time)
        monitor_queue.record(machine.resource, machine_name, component, "machine_out") #data acquisition via monitor
        monitor_tat.record(component, machine_name)
        component.job.components.remove(component)#remove the component from job class
        machine.resource.release(request) #release after timeout


        print(f"{env.now}: {component.name} of {component.job.name} finished on {machine.name}")
            


#function that dynamically generates components + loads to queue
def dynamic_component_creator(env, job, component_queue, job_machine_times, min_time, max_time, duration):
    while True:
        yield env.timeout(random.randint(min_time, max_time))  # Generate component bteween 5 ~ 15 seconds
        new_component = sc.Component(f"{job.name}_{env.now}", job, job_machine_times[job.name], env.now, duration)
        job.add_component(new_component)
        component_queue.put(new_component)
        print(f"{env.now}: New component {new_component.name} added for {job.name}")

#function that transpose the structure of time matrix
def transposer_for_time_matrix(ori_matrix, job_size):
    result = {f"job{j}": {} for j in range(job_size)}
    for k in range(job_size):
        temp = []
        for machine, job_times in ori_matrix.items():
            temp.append(job_times[k])
        result['job'+str(k)] = temp
    return result

#function that transform from list to queue
def list_to_queue(lst):
    q = queue.Queue()
    for item in lst:
        q.put(item)
    return q

#function that transform from queue to list
def queue_to_list(q):
    lst = []
    while not q.empty():
        lst.append(q.get())
    return lst

#function that specifies an equipment on each component 
# def allocator (store, machine_objs, a_now):
#     while True:
#         # store에서 작업을 가져옴
#         job_obj = yield store.get()
        
#         # 각 머신의 큐에서 우선 작업을 선택
#         machine_queue_len_list = [len(b.resource.queue) for a,b in machine_objs.items()]
#         machine_index = random.choice([i for i,value in enumerate(machine_queue_len_list) if value == min(machine_queue_len_list)])
#         machine_objs[machine_index].queue.put(job_obj)
#         print(f"time {2}: {0} is allocated to machine{1}", job_obj.name, machine_index, a_now)
  