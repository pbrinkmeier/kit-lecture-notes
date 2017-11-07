[zurück](README.md)

# 06: Dispatching, Scheduling, Scheduling Policies

> 07.11.2017

## Table of Contents

- [Dispatching](#dispatching)
    - [Which Jobs Should Be Assigned to Which CPU(s)?](#which-jobs-should-be-assigned-to-which-cpus)
    - [Voluntary Yielding vs Preemption](#voluntary-yielding-vs-preemption)
    - [CPU Switch from Process to Process](#cpu-switch-from-process-to-process)
- [Scheduling](#scheduling)
    - [Process State](#process-state)
    - [Types of Schedulers](#types-of-schedulers)
    - [Process Scheduling Queues](#process-scheduling-queues)
- [Scheduling Policies](#scheduling-policies)
    - [First-Come, First-Served (FCFS) Scheduling](#first-come-first-served-fcfs-scheduling)
    - [Shortest-Job-First (SJF) Scheduling](#shortest-job-first-sjf-scheduling)
        - [Estimating the Length of Next CPU Burst](#estimating-the-length-of-next-cpu-burst)
        - [CPU vs. I/O Burst Cycles](#cpu-vs-io-burst-cycles)
        - [Process Behavior: Boundedness](#process-behavior-boundedness)
    - [Preemptive Shortest-Job-First (PSJF) Scheduling](#preemptive-shortest-job-first-psjf-scheduling)
    - [Round Robin (RR) Scheduling](#round-robin-rr-scheduling)
    - [Virtual Round Robin (RR) Scheduling](#virtual-round-robin-rr-scheduling)
    - [(Strict) Priority Scheduling](#strict-priority-scheduling)
    - [Multi-Level Feedback Queue (MLFB) Scheduling](#multi-level-feedback-queue-mlfb-scheduling)
    - [Priority Donation](#priority-donation)
    - [Lottery Scheduling](#lottery-scheduling)
    - [Real-Time Scheduling](#real-time-scheduling)

## Dispatching

The machine has `K` jobs ready to run, but only `N` CPUs with `K > N > 1`.

_Scheduling problem:_ Which jobs should be assigned to which CPUs?

### Which Jobs Should Be Assigned to Which CPU(s)?

The CPU _scheduler_ selects the next process to run using a specific _policy_.

The _dispatcher_ performs the actual process switch, including
- saving and restoring process contexts
- switching to user mode

### Voluntary Yielding vs Preemption

The kernel is responsible for performing the CPU switch:

**Voluntary Yielding:**  
Due to the fact that the kernel isn't always running, it cannot dispatch a different process unless it is invoked!  
The kernel can switch at any system call, however using _cooperative multitasking_, the currently running process performs a `yield` system call to ask the kernel to switch to another process.

**Preemption:**  
The kernel often wants to preempt the currently running process to schedule a different process. This requires the kernel to be invoked in certain time intervals. Usually, _timer interrupts_ are used as a trigger to make scheduling decisions after every "time-slice".

### CPU Switch from Process to Process

![](img/06-process-switch.png)

## Scheduling

### Process State

A process can be in different states:
- **new:** has been created but never ran
- **running:** instructions are currently executed
- **waiting:** waiting for some event to occur
- **ready:** waiting to be assigned to a CPU
- **terminated:** finished execution (zombie state)

![](img/06-process-state.png)

### Types of Schedulers

**Short-term scheduler:** (_CPU scheduler_)  
- selects next process to be executed and allocates a CPU
- invoked very frequently (milliseconds), therefore must be fast

**Long-term scheduler:** (_job scheduler_)  
- selects processes to be added into the ready queue
- invoked infrequently (seconds, minutes), there can be slow
- controls the degree of multiprogramming

_The lecture will focus on CPU schedulers (short term)._

### Process Scheduling Queues

**Job queue:** Set of _all_ processes in the system  
**Ready queue:** Processes in _ready_ or _waiting_ state  
**Device queue:** Processes waiting for an I/O device

![](img/06-scheduling-queues.png)

## Scheduling Policies

Some common scheduling policies for different environments. While all policies try to be as _fair_ as possible to processes and _balance_ all system parts, there are different **goals** for every category:
- **Batch Scheduling**
    - still widespread in business applications (payroll, inventory, ...)
    - non-preemptive algorithms are acceptable (-> less switches -> less overhead)
    - **Throughput:** # of processes that complete per time unit
    - **Turnaround Time:** time from submission to completion of a job
    - **CPU Utilization:** keep the CPU(s) as busy as possible
- **Interactive Scheduling**
    - preemption essential to keep processes from hogging CPU time
    - **Waiting Time:** time each process waits in ready queue
    - **Response Time:** Time from request to first response
- **Real-Time Scheduling**
    - garantueed completion of jobs within time constraints
    - preemption is not always needed
    - **Meeting Deadlines:** finish jobs in time
    - **Predictability:** minimize jitter

### First-Come, First-Served (FCFS) Scheduling

Suppose 3 processes arrived in order: P1, P2, P3

![](img/06-fcfs-table-1.png)

_Gantt_ chart:  
![](img/06-fcfs-gantt-1.png)

Turnaround times: `P1 = 24, P2 = 27, P3 = 30`  
Average: `(24 + 27 + 30) / 3 = 27` -> **Can we do better?**

---

Now suppose the 3 processes arrived in order P2, P3, P1

![](img/06-fcfs-table-2.png)

_Gantt_ chart:  
![](img/06-fcfs-gantt-2.png)

Turnaround times: `P1 = 30, P2 = 3, P3 = 6`  
Average: `(30 + 3 + 6) / 3 = 13` -> **Much better than previously!**

Good scheduling can ~~save lives~~ reduce turnaround time!

### Shortest-Job-First (SJF) Scheduling

The FCFS (First-Come First-Served Scheduling) is prone to the _Convoy effect_. All short (_"fast"_) jobs have to wait for long (_"slow"_) jobs that arrived previously.  
**Idea:** Run shortest job first.

SJF has optimal average turnaround, waiting and response times, however the scheduler cannot know job length in advance.  
**Solution:** Predict length of next CPU burst for each process, then schedule the process with the shortest burst next.

#### Estimating the Length of Next CPU Burst

Idea: use exponential averaging based on previous CPU bursts  
`t(n)` = actual length of n-th CPU burst  
`τ(n+1)` = predicted value for the next CPU burst  
Define `τ(n+1) = α*t(n) + (1 - α)*τ(n)` with `0 <= α <= 1`

Example with `α = 0.5`:  
![](img/06-cpu-bursts.png)

#### CPU vs. I/O Burst Cycles

Why do CPU bursts exist? Because the CPU bursts, then waits for I/O.

![](img/06-bursts-io-cpu.png)
![](img/06-bursts-histogram.png)

#### Process Behavior: Boundedness

Processes can be characterized as either:
- **CPU-bound processes:** more time spent doing computations (very long but few CPU bursts)
or
- **I/O-bound processes:** more time spent doing I/O (many short CPU bursts)

### Preemptive Shortest-Job-First (PSJF) Scheduling

SJF (_shortest-job-first_) scheduling optimizes waiting and response time, but what about throughput?  
CPU bound jobs hold the CPU until end of execution of I/O events, that means poor I/O utilization.

**Idea:** use SJF (_shortest-job-first_) scheduling, but periodically preempt to make a new scheduling decision (choose job with shortest remaining time).

![](img/06-psjf-table.png)  
![](img/06-psjf-gantt.png)

### Round Robin (RR) Scheduling

### Virtual Round Robin (RR) Scheduling

### (Strict) Priority Scheduling

### Multi-Level Feedback Queue (MLFB) Scheduling

### Priority Donation

### Lottery Scheduling

### Real-Time Scheduling
