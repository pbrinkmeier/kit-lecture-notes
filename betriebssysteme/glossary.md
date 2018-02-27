[zurück](README.md)

# Glossary

## Chapter 01: Orga and overview

**CPU**: Central processing unit

**RAM**: Random-access memory
 
**APIC**: Advanced Programmable Interrupt Controller _(handles interrupts)_

**PMIO**: Port-mapped I/O

**MMIO**: Memory-mapped I/O

## Chapter 02: OS concepts

**API**: Application programming interface

**NIC**: Network interface card

**MMU**: Memory management unit _(built-in CPU hardware that translates virtual to physical addresses)_

**PCB**: Process control block _(contains information about allocated resources)_

**AS**: Address space _(all virtual memory locations a program can name, consists of sections like stack, data and text)_

**IP**: Instruction pointer _(stores currently executed instruction)_

**SP**: Stack pointer _(stores address of stack top)_

**PSW**: Program status word _(contains flags about execution history)_

## Chapter 03: Processes, Address Spaces and Compiling, Linking, Loading

**BSS**: Block started by symbol _(address space segment for statically allocated/non-initialized variables)_

**RO-Data**: Read-only data _(address space segment for constant numbers and strings)_

**BRK/SBRK**: Break pointer (heap) _(highest address of heap and address space)_

## Chapter 04: Process API

**BP/FP**: Base pointer/frame pointer _(used to organize stack frames)_

**ABI**: Application binary interface _(standardized interface between programs, modules and OS)_

**PID**: Process identifier

## Chapter 05: Threads

**TID**: Thread identifier

**PCB**: Process control block _(contains information about allocated resources, known to OS)_

**TCB**: Thread control block _(per thread data, OS knowledge depends on thread model)_

**ULT**: User level threads

**KLT**: Kernel level threads

## Chapter 06: Dispatching, Scheduling, Scheduling Policies

**FCFS**: First come first served

**(P)SJF**: (Preemptive) Shortest job first

**(V)RR**: (Virtual) Round robin

**MLFQ**: Multi-level feedback queue

## Chapter 07: Inter Process Communication

## Chapter 08: Synchronization and Deadlocks

## Chapter 09: Memory Management Hardware

## Chapter 10: Paging

## Chapter 11: Caching

## Chapter 12: Page Faults

## Chapter 13: Page Replacement Policies

## Chapter 14: Memory Allocation

## Chapter 15: Secondary Storage Structure

## Chapter 16: File Systems

## Chapter 17: Implementing File Systems

## Chapter 18: I/O System

## Chapter 19: I/O Virtualization (IOMMU)

## Chapter 20: Operating System Structures

