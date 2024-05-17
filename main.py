class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.finish_time = None
        self.waiting_time = None

    def execute(self, time_quantum):
        if self.remaining_time <= time_quantum:
            executed_time = self.remaining_time
        else:
            executed_time = time_quantum
        self.remaining_time -= executed_time
        return executed_time

    def is_finished(self):
        return self.remaining_time == 0


def calculate_average_waiting_time(processes):
    total_waiting_time = sum(process.waiting_time for process in processes)
    return total_waiting_time / len(processes)


def calculate_average_turnaround_time(processes):
    total_turnaround_time = sum(process.finish_time - process.arrival_time for process in processes)
    return total_turnaround_time / len(processes)


def calculate_cpu_utilization(processes):
    total_cpu_time = sum(process.burst_time for process in processes)
    total_execution_time = max(process.finish_time for process in processes)
    return (total_cpu_time / total_execution_time) * 100



def simulate_fcfs(processes, cs_time):
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        process.waiting_time = current_time - process.arrival_time
        current_time += process.burst_time + cs_time
        process.finish_time = current_time


def simulate_sjf(processes, cs_time):
    current_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        remaining_processes.sort(key=lambda p: p.burst_time)
        process = remaining_processes.pop(0)
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        process.waiting_time = current_time - process.arrival_time
        current_time += process.burst_time + cs_time
        process.finish_time = current_time


def simulate_rr(processes, time_quantum, cs_time):
    current_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        process = remaining_processes[0]
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        executed_time = process.execute(time_quantum)
        current_time += executed_time + cs_time
        if process.is_finished():
            process.finish_time = current_time
            process.waiting_time = process.finish_time - process.arrival_time - process.burst_time
            remaining_processes.pop(0)
        else:
            remaining_processes.append(remaining_processes.pop(0))



def print_gantt_chart(processes):
    gantt_chart = "|"
    for process in processes:
        gantt_chart += f" P{process.process_id} |"
    print(gantt_chart)


def print_results(processes):
    print("\nProcess\tFinish Time\tWaiting Time\tTurnaround Time")
    total_waiting_time = 0
    total_turnaround_time = 0
    for process in processes:
        turnaround_time = process.finish_time - process.arrival_time
        total_waiting_time += process.waiting_time
        total_turnaround_time += turnaround_time
        print(
            f"P{process.process_id}\t{process.finish_time}\t\t{process.waiting_time}\t\t{turnaround_time}"
        )
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)
    print(
        f"\nAverage Waiting Time: {avg_waiting_time}"
    )
    print(
        f"Average Turnaround Time: {avg_turnaround_time}"
    )
    cpu_utilization = calculate_cpu_utilization(processes)
    print(f"CPU Utilization: {cpu_utilization}%")


processes = [
    Process(1, 0, 10),
    Process(2, 3, 5),
    Process(3, 5, 8),
]

def read_process_data(file):
    processes = []
    with open(file, 'r') as file:
        for line in file:
            data = line.strip().split()
            process_id = int(data[0])
            arrival_time = int(data[1])
            burst_time = int(data[2])
            process = Process(process_id, arrival_time, burst_time)
            processes.append(process)
    return processes
processes = read_process_data('process_data.txt')

print(
    '''
===============									  									  
|simulate fcfs| 																		  
===============
'''
)

simulate_fcfs(processes, cs_time=1)
print_gantt_chart(processes)
print_results(processes)

# Simulate SJF scheduling
print(
    '''
===============									  									  
|simulate SJF| 																		  
===============
'''
)
processes_sjf = [
    Process(1, 0, 10),
    Process(2, 3, 5),
    Process(3, 5, 8),
]
simulate_sjf(processes_sjf, cs_time=1)
print_gantt_chart(processes_sjf)
print_results(processes_sjf)

# Simulate RR scheduling
print(
    '''
===============									  									  
|simulate RR| 																		  
===============
'''
)
processes_rr = [
    Process(1, 0, 10),
    Process(2, 3, 5),
    Process(3, 5, 8),
]
time_quantum = 2
simulate_rr(processes_rr, time_quantum, cs_time=1)
print_gantt_chart(processes_rr)
print_results(processes_rr)
