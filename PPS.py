# Name: Masa Jalamneh
# ID: 1212145
# Section: 1

# Preemptive priority scheduling code 
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
        self.updatedP = priority
        self.agingT = 0

def PreemptivePriorityScheduling(processes, n, start):
    t = start       # to track the time 
    prev = -1
    
    # for round robin
    quantum = 2     
    rr_remaining_quantum = 0
    current_rr_process = None

    # initialize waiting time and turnaround time
    for i in range(n):
        processes[i].waiting_time = 0
        processes[i].turnaround_time = 0
        processes[i].remaining_time = processes[i].burst_time
        processes[i].end = 0
        processes[i].last_exec_time = -1
        processes[i].flag = False
        processes[i].updatedP = processes[i].priority
        processes[i].agingT = 0

    print("Preemptive Priority Scheduling with Aging and Round Robin (q = 2) for Same Priority Level:")
    print("Gantt Chart:")

    # create a figure and axis and set the title for the plot
    fig, ax = plt.subplots(figsize=(15, 5))  
    ax.set_title('Gantt Chart - Preemptive Priority Scheduling') 

    start_times = {p.name: [] for p in processes}   # store start times for plotting
    durations = {p.name: [] for p in processes}     # store durations for plotting
    colors = []                                     # list to store colors for each process

    # color map for processes
    color_map = {
        1: 'skyblue',
        2: 'red',
        3: 'lightgreen',
        4: 'orchid',
        5: 'lightcoral',
        6: 'gold',
        7: 'lightseagreen'
    }

    while t <= TotalTime:   # track the time (the limit is 300)
        round_robin = False
        pos = -1

        # find the highest priority process or round robin (processes with the same priority)
        for i in range(n):
            if processes[i].arrival_time <= t and processes[i].remaining_time > 0:
                if pos == -1 or processes[i].updatedP < processes[pos].updatedP:
                    pos = i
                    round_robin = False  # priorities are not the same 
                elif processes[i].updatedP == processes[pos].updatedP:
                    round_robin = True   # same priority

        # round robin for processes with same priority
        if round_robin and rr_remaining_quantum == 0:
            highest_priority = processes[pos].updatedP
            rr_pos = -1
            for i in range(n):
                if processes[i].arrival_time <= t and processes[i].remaining_time > 0 and processes[i].updatedP == highest_priority:
                    if rr_pos == -1 or processes[i].last_exec_time < processes[rr_pos].last_exec_time:
                        rr_pos = i
            pos = rr_pos
            current_rr_process = processes[pos]
            rr_remaining_quantum = quantum

        if pos != -1:
            processes[pos].agingT = 0
            processes[pos].waiting_time += t - processes[pos].arrival_time
            end = t + 1
            processes[pos].turnaround_time += end - processes[pos].end
            processes[pos].remaining_time -= 1
            processes[pos].last_exec_time = t

            # plot the segment of Gantt chart
            start_times[processes[pos].name].append(t)      #  start time for plotting
            durations[processes[pos].name].append(1)        #  duration for plotting
            colors.append(color_map[processes[pos].name])   # Assign color based on process name

            t = end
            processes[pos].end = end
            processes[pos].arrival_time = end

            if processes[pos].remaining_time == 0:
                processes[pos].remaining_time = processes[pos].burst_time
                processes[pos].arrival_time = end + processes[pos].IO_burst_time
                processes[pos].updatedP = processes[pos].priority
                current_rr_process = None
                rr_remaining_quantum = 0
            else:
                rr_remaining_quantum -= 1

            # aging to other processes
            for i in range(n):
                if i != pos and processes[i].arrival_time <= t and processes[i].remaining_time > 0:
                    processes[i].agingT += 1
                    if processes[i].agingT >= 5:  # for process remains in the ready queue for 5 time units
                        if processes[i].updatedP > 0:
                            processes[i].updatedP -= 1
                        processes[i].agingT = 0

            prev = pos
        else:
            t += 1

    # Calculate average waiting time and turnaround time
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)

    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n

    print(f"\nAverage Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")

    # Plot the Gantt chart using matplotlib
    y_ticks = [f'P{p.name}' for p in processes]
    for process in processes:
        y_label = f'P{process.name}'
        ax.barh(y_label, durations[process.name], left=start_times[process.name], color=color_map[process.name], edgecolor='black')

    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks) 

    plt.show()  # Display the plot

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

    PreemptivePriorityScheduling(processes, n, 0)
