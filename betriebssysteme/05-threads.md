[zurück](README.md)

# 05: Threads

> 30.10.2017, 06.11.2017

## Table of Contents

*TODO*

## What is a thread?

Traditionally, each process has it’s own address space, it’s own set of allocated resources and exactly one thread of execution.
Modern operating systems provide the option of having *multiple* **threads** per process.

**Note**: This does not always apply.
    Sometimes threads don’t share address spaces, and e.g. in Linux threads are regular processes with shared resources and address space.

Some data is **thread local**, some is **thread global** (but still **process local**).

### Why threads?

While processes share data explicity, threads usually work with common memory.
Hence, if activities share a lot of data, it’s often better to use a thread instead of a process.

#### Example: word processor

Activities may be:

- Accepting input
- Applying a lot of formatting
- Rendering output
- Reading and writing files

Those activities all operate on the same set of data.

## Pthreads

A **thread library** provides an API for creating and managing threads. **Pthreads** is a POSIX thread library (IEEE 1003.1c) common in UNIX systems.
The API defines more than 60 functions for dealing with threads.
Internals depend on the specific implementation.

### Pthread API basics

Each `Pthread` has

- a **thread identifier** (TID)
- a set of registers (at least IP and SP)
- a stack containing it's call history and thread local variables

Some basic Pthread functions are:

- **Pthread_create**: creates a new thread
- **Pthread_exit**: terminates the calling thread
- **Pthread_join**: waits for a specific thread to exit
- **Pthread_yield**: invoke thread library to choose another process
```

### Mulithreaded programming is hard

Brace yourself.
It doesn’t matter whether you’re using multiple processes, mulitple threads or both; you will need to take care of a lot more things compared to singlethreaded programming:

- Distributing and balancing activities
- Distributung data
- Synchronizing access to shared state

A rule of thumb: processes share less data than threads, so there is less that can go wrong.

## Data structures

## Thread models