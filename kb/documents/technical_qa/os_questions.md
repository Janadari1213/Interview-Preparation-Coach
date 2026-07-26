## Q: What is the difference between a Process and a Thread?

**Topic:** Operating Systems  
**Role:** Software Engineer  
**Difficulty:** easy  
**Q:** What is the difference between a Process and a Thread?  
**A:** A process is an independent executing program instance with its own isolated memory address space. A thread is an execution unit within a process that shares virtual address space, heap memory, and file handles with sibling threads under lightweight context switching.

## Q: What is a deadlock and what are its four necessary conditions?

**Topic:** Operating Systems  
**Role:** Software Engineer  
**Difficulty:** medium  
**Q:** What is a deadlock and what are its four necessary conditions?  
**A:** A deadlock occurs when concurrent processes are blocked indefinitely, each waiting for a resource held by another. The four necessary conditions are: 1) Mutual Exclusion, 2) Hold and Wait, 3) No Preemption, 4) Circular Wait.

## Q: How do CPU scheduling algorithms like Round Robin and Shortest Job First (SJF) work?

**Topic:** Operating Systems  
**Role:** Software Engineer  
**Difficulty:** hard  
**Q:** How do CPU scheduling algorithms like Round Robin and Shortest Job First (SJF) work?  
**A:** **Shortest Job First (SJF)** selects ready process with smallest estimated CPU burst time, minimizing average waiting time. **Round Robin (RR)** allocates equal CPU time slices (time quanta) cyclically to ready queue processes, preventing process starvation in interactive multitasking systems.
