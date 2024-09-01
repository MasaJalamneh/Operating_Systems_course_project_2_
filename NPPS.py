# Name: Masa Jalamneh
# ID: 1212145
# Section: 1

# Non preemptive priority scheduling code 
import matplotlib.pyplot as plt

TotalTime = 300

class Process:
    def __init__(self, name, arrival_time, burst_time, IO_burst_time, priority):
        # main specifications of the process
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.IO_burst_time = IO_burst_time
        self.priority = priority
        # additional features
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.end = 0
        self.last_exec_time = -1
        self.flag = False

def NonPreemptivePriorityScheduling(processes, n, start):
    t = start    # to track the time 
    quantum = 2  # for round robin

    # initialize waiting time and turnaround time
    for process in processes:
        process.waiting_time = 0
        process.turnaround_time = 0
        process.remaining_time = process.burst_time
        process.end = 0
        process.last_exec_time = -1
        process.flag = False

    print("Non-Preemptive Priority Scheduling with Round Robin (q = 2) for Same Priority Level:")
    print("Gantt Chart:")
    
    # create a figure and axis and set the title for the plot
    fig, ax = plt.subplots(figsize=(10, 5))  
    ax.set_title('Gantt Chart - Non Preemptive Priority Scheduling')  

    y_ticks = []           # a list to store process names for y-axis 
    start_times = []       # a list to store start times for plotting
    durations = []         # a list to store durations for plotting
    colors = []            # a list to store colors for each process

    # a color map for processes (to give each process different color)
    color_map = {
        1: 'skyblue',
        2: 'red',
        3: 'lightgreen',
        4: 'orchid',
        5: 'lightcoral',
        6: 'gold',
        7: 'lightseagreen'
    }

    last_rr_time = {p.name: -1 for p in processes}  # to track last execution time for round robin processes
    rr_queue = []  # round robin queue for same priority processes

    while t <= TotalTime: # track the time (the limit is 300)
        ready_queue = [process for process in processes if process.arrival_time <= t and process.remaining_time > 0]

        if not ready_queue:
            t += 1
            continue

        highest_priority = min(p.priority for p in ready_queue)  # find the processes with the highest priority 
        same_priority_processes = [p for p in ready_queue if p.priority == highest_priority]

        if len(same_priority_processes) > 1:   # processes with the same priority -> round robin queue
            rr_queue = [p for p in rr_queue if p in same_priority_processes] + \
                       [p for p in same_priority_processes if p not in rr_queue]

            # find the next process in round robin
            rr_queue.sort(key=lambda p: last_rr_time[p.name])
            current_process = rr_queue[0]
            execute_time = min(current_process.remaining_time, quantum)
        else:
            current_process = same_priority_processes[0]
            execute_time = current_process.remaining_time

        start_time = t
        t += execute_time
        current_process.remaining_time -= execute_time
        last_rr_time[current_process.name] = t

        # plot the segment of Gantt chart
        y_ticks.append(f'P{current_process.name}')      #  process name will be added to y-axis 
        start_times.append(start_time)                  #  start time for plotting
        durations.append(execute_time)                  #  duration for plotting
        colors.append(color_map[current_process.name])  #  assign color based on process name

        # update process times if finished (so the scheduling will repeat forever)
        if current_process.remaining_time == 0:
            current_process.turnaround_time = t - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            current_process.end = t
            current_process.arrival_time = t + current_process.IO_burst_time
            current_process.remaining_time = current_process.burst_time  # reset remaining time
            current_process.last_exec_time = -1  # reset last execution time
            current_process.flag = False  # reset flag

    # plot the Gantt chart using matplotlib
    ax.barh(y_ticks, durations, left=start_times, color=colors, edgecolor='black')
    ax.set_xlabel('Time')
    ax.set_yticks(y_ticks)

    plt.show()  # display the plot

    # calculate average waiting time and turnaround time
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes) 

    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n

    print(f"Average Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")

if __name__ == "__main__":
    processes = [
        Process(1, 0, 15, 5, 3),
        Process(2, 1, 23, 14, 2),
        Process(3, 3, 14, 6, 3),
        Process(4, 4, 16, 15, 1),
        Process(5, 6, 10, 13, 0),
        Process(6, 7, 22, 4, 1),
        Process(7, 8, 28, 10, 2)
    ]
    n = len(processes)

    NonPreemptivePriorityScheduling(processes, n, 0)
