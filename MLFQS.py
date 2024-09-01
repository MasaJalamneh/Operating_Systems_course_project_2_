# Name: Masa Jalamneh
# ID: 1212145
# Section: 1

# Multi Level Feedback Queue scheduling code 
import matplotlib.pyplot as plt
from collections import deque

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
        self.start = -1
        self.queue_level = 0

print("Multi Level Feedback Queue Scheduling:")

def MultilevelFeedbackQueueScheduling(processes, n):
    t = 0    # to track the time 

    # levels queues
    top_level_queue = deque()
    middle_level_queue = deque()
    bottom_level_queue = deque()
    io_waiting_processes = []  # a list to track processes waiting for I/O

    queues = [top_level_queue, middle_level_queue, bottom_level_queue]
    quantum = [8, 16, float('inf')] # top level q = 8  // middle level q = 16  // bottom level does not use RR 
    gantt_chart = []

    # enqueue all processes to the top level queue initially (all procoesses initially enter top level)
    for process in processes:
        top_level_queue.append(process)

    while t < TotalTime:     # track the time (the limit is 300)
        for level in range(3):
            queue = queues[level]
            time_slice = quantum[level]
            
            if queue:
                process = queue.popleft()
                if process.start == -1:
                    process.start = t
                execution_time = min(time_slice, process.remaining_time, TotalTime - t)
                
                gantt_chart.append((process.name, t, t + execution_time, level))
                
                t += execution_time
                process.remaining_time -= execution_time
                
                if process.remaining_time > 0:
                    if level < 2:
                        queues[level + 1].append(process)
                    else:
                        queue.append(process)
                else:
                    process.end = t
                    process.turnaround_time = process.end - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    io_waiting_processes.append(process)  # add to I/O waiting list
                break
        else:
            t += 1         # if no processes in any queue -> increment time



        #  to check if any processes in I/O waiting list can re-enter the top level queue
        for process in io_waiting_processes[:]:
            if t >= process.end + process.IO_burst_time:
                process.remaining_time = process.burst_time  # reset remaining time
                process.start = -1                           # reset start time
                top_level_queue.append(process)              # re-enter top-level queue after I/O burst
                io_waiting_processes.remove(process)         # remove from I/O waiting list

        if t >= TotalTime and not any(queue for queue in queues if queue or io_waiting_processes):
            break  # exit loop if no more work and time reached total time (300)

    print("\nGantt Chart:")

    # create a figure and axis and set the title for the plot
    fig, ax = plt.subplots(figsize=(15, 5))  
    ax.set_title('Gantt Chart - Multi Level Feddback Queue') 

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

    start_times = {p.name: [] for p in processes}   # store start times for plotting
    durations = {p.name: [] for p in processes}     # store durations for plotting

    # Gantt chart data
    for entry in gantt_chart:
        process_name, start, end, level = entry
        start_times[process_name].append(start)
        durations[process_name].append(end - start)
        colors = color_map[process_name]
        ax.barh(f'P{process_name}', end - start, left=start, color=colors, edgecolor='black')

    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_xlim(0, TotalTime)
    ax.set_yticks([f'P{p.name}' for p in processes])
    ax.set_yticklabels([f'P{p.name}' for p in processes])

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

    MultilevelFeedbackQueueScheduling(processes, n)
