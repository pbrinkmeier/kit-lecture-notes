[zurück](README.md)

# 07: Inter Process Communication

> 14.11.2017

## Table of Contents

- [Inter Process Communication (IPC)](#inter-process-communication-ipc)
    - [Message passing](#message-passing)
        - [Direct vs. indirect messages](#direct-vs-indirect-messages)
        - [Sender/receiver synchronization](#senderreceiver-synchronization)
        - [Buffering](#buffering)
        - [Example: message boxes in mach (e.g. Max OS X)](#example-message-boxes-in-mach-eg-max-os-x)
        - [Example: POSIX message queues](#example-posix-message-queues)
    - [Shared memory](#shared-memory)
        - [Example: POSIX shared memory](#example-posix-shared-memory)
        - [Sequential memory consistency](#sequential-memory-consistency)
        - [Memory consistency model](#memory-consistency-model)
        - [x86 memory consistency](#x86-memory-consistency)

## Inter Process Communication (IPC)

Processes and threads need to communicate with one another, reasons for that are e.g. information sharing, computation speed-up and modularity.

The **Interprocess Communication** (IPC) allows exchanging data using two different methods:
- **Message passing** using system calls to explicitly send and receive information (e.g. pipes, sockets)
- **Shared memory** establishes a physical memory region that multiple processes/threads can read and write to (e.g. shared memory-mapped files)

![](img/07-message-passing-shared-memory.png)

### Message passing

Message passing is a mechanism for processes to communicate and synchronize their actions using `send` and `receive` operations.

An implementation of this communication link is based on the hardware bus, shared memory, kernel memory and the network interface card (NIC).

#### Direct vs. indirect messages

In **direct messages**, processes name each other explicitly, e.g.
- `send(P, message)` sends a message to process `P`
- `receive(Q, message)` receives a message from process `Q`

**Indirect messages** use a _mailbox_ system instead. Each mailbox has a unique id, a mailbox is automaticly created together with the first communicating process and destroyed with the last one. However this model requires a shared mailbox between the communicating processes.

Problems using mailboxes:  
Assume `P1`, `P2` and `P3` share a mailbox and `P1` sends a message which is received by `P2` and `P3`.
- Who gets the message?
- Allow a link to be associated with at most two processes?
- Allow only one process at a time to execute a receive operation?
- Allow the system to arbitrarily select the receiver?

#### Sender/receiver synchronization

Message passing may be either **blocking** or **non-blocking**.

**Blocking** is considered _synchronous_:
- Blocking `send` blocks the sender until message was received
- Blocking `receive` blocks the receiver until a message is available

**Non-blocking** is considered _asynchronous_:
- Non-blocking `send` sends the message and continues
- Non-blocking `receive` will receive a valid message or `null`

The question whether non-blocking senders can communicate with non-blocking receivers depends on the **buffering scheme**.

#### Buffering

Messages are _queued_ using different capacities:
- Zero capacity - no queuing
    - Sender must wait for receiver (_rendezvous_)
    - Message is tranferred a soon as receiver becomes available
- Bounded capacity - finite number and length of messages
    - Sender can send before receiver expects a message
    - Sender can send while receiver still busy (e.g. with previous message)
    - Sender must wait if link full
- Unbounded capacity
    - Sender never waits
    - Potential memory overflow
    - Possibly large latency between `send` and `receive`

#### Example: message boxes in mach (e.g. Max OS X)

All communication is based on messages (even system calls). Every task gets two initial mailboxes (_ports_) on creation: _Kernel_ and _Notify_, further mailboxes can be allocated for process-to-process communication using `port_allocate()`.

`msg_send`, `msg_receive` and `msg_rpc` are used for messaging while _blocking_, _time-out_ and _non-blocking_ synchronizations with a max buffer capacity of 65536 messages are available.

Every port is owned by a single process which is allowed to receive messages, _Mailbox-Sets_ allow receiving messages from multiple mailboxes.

#### Example: POSIX message queues

- Creation or opening of an existing message queue:  
`mqd_t mq_open(const char *name, int oflag);`
- Send a message to the queue:  
`int mq_send(mqd_t md, const char *msg, size_t len, unsiged priority);`
- Receive message with the hightest priority:  
`int mq_receive(mqd_t md, char *msg, size_t len, unsiged *priority);`
- Register a callback handler on message queue to avoid polling:  
`int mq_notify(mqd_t md, const struct sigevent *sevp);`
- Remove message queue:  
`int mq_unlink(const char *name);`

### Shared memory

Interprocess communication using shared memory works by creating a region in memory that can be access by multiple processes. Every write operation is visible to the other processes, the hardware guarantees that read operations will always return the most recent write.

Using shared memory in a safe way (and high performace) is tricky due to the _cache coherency protcol_ if many processes and many CPUs are involved and _race conditions_ if there are multiple writers.

#### Example: POSIX shared memory

- Open or create a new POSIX shared memory object (returns handle):  
`int shm_open(const char *name, int oflag, mode_t mode);`
- Set size of shared memory region:  
`ftruncate(smd, size_t len);`
- Map shared memory object to address space:  
`void * mmap(void *addr, size_t len, [...], smd, [...]);`
- Unmap shared memory object from address space:  
`int munmap(void *addr, size_t len);`
- Destroy shared memory object:  
`int shm_unlink(const char *name);`

#### Sequential memory consistency

**Sequential consistency (SC)**:
> The result of execution is as if all operations were executed in some sequential order, and the operations of each processor occured in the order specified by the program. (Lamport)

When communicating via shared memory, we tend to assume sequential consistency. However in reality, the compiler and the CPU re-order instructions to _execution order_ for more efficiency. Without sequential consistency, multiple processes on multiple cores behave worse than preemptive threads on a single core.

#### Memory consistency model

CPUs a generally **not** sequentially consistent because it would..
- ..complicate write buffers
- ..complicate non-blocking reads
- ..make cache coherence more expensive

Compilers also do not generate code in program order because they e.g. re-arrange loops for better performance and perform common subexpression elimination.

As long as a single thread accesses a memory location at a time, this is not a problem. But **don't try to access the same memory location with multiple threads at the same time without proper synchronization!**

#### x86 memory consistency

x86 includes multiple consistency and caching models, including _memory type range registers (MTRR)_ for specifying consistent ranges of physical memory and _page attribute table (PAT)_ for control on 4k page granularity.

The caching model and memory consistency are strongly tied together, e.g. certain store instructions such as `movnt` bypass the cache and can be re-ordered with other writes that go through the cache.

A `lock` prefix makes memory instructions _atomic_, meaning that they are totally ordered and cannot be re-ordered with non-locked instructions. (The `xchg` instruction is always locked, although it doesn't wear the prefix.)  
Special `fence` instructions prevent re-ordering:
- `lfence` can't be re-ordered with reads
- `sfence` can't be re-ordered with writes
- `mfence` can't be re-ordered with reads or writes
