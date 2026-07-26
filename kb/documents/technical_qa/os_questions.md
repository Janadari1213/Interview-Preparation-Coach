## Q: What is the difference between a process and a thread?
**Topic:** Operating Systems
**Difficulty:** easy
**A:** A process is an independent program in execution with its own dedicated memory space, file handles, and system resources. A thread is a lightweight unit of execution within a process that shares the parent process's memory space and resources with sibling threads. Consequently, context switching between threads is faster than between processes, though thread errors can crash the entire host process.

## Q: What is a deadlock and what are its four necessary conditions?
**Topic:** Operating Systems
**Difficulty:** medium
**A:** A deadlock occurs when a set of concurrent processes are blocked indefinitely, each waiting for a resource held by another process in the set. The four necessary conditions for a deadlock to exist are Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. Deadlocks can be handled through prevention, avoidance (e.g., Banker's Algorithm), detection, or recovery mechanisms.

## Q: How does CPU scheduling work and what are common scheduling algorithms?
**Topic:** Operating Systems
**Difficulty:** hard
**A:** CPU scheduling is the OS task of deciding which process in the ready queue receives processor execution time when the current process pauses or yields. Preemptive scheduling can interrupt running processes, whereas non-preemptive scheduling runs processes to completion or I/O blockage. Common algorithms include First-Come First-Served (FCFS), Shortest Job First (SJF), Round Robin (RR), and Priority Scheduling.
