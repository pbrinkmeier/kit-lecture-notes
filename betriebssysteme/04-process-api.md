[zurück](README.md)

# 04: Process API

> 24.10.2017

## Table of Contents

- [Execution Model](#execution-model)
    - [Assembler (x86 Intel style)](#assembler-x86-intel-style)
    - [x86 Stack](#x86-stack)
- [System Calls](#system-calls)
- [Process API](#process-api)

## Execution Model

### Assembler (x86 Intel style)

The OS interacts directly with compiled programs.
The following list is a set of (simplified) assembler instructions you should know.

- **mov**: Copy data from second operand to first operand

#### Arithmetic instructions

- **add, sub, mul, div**: add, subtract, multiply or divide two integer operands storing the result in the first operand  
- **inc, dec**: increment or decrement from register or memory location  
- **shl, shr**: bitshift left/right  
- **and, or, xor**: bitwise and/or/xor of two operands storing the result in the first operand  
- **not**: logical negation  

#### Control flow

- **jmp**: continue execution at given address  
- **je**: &ldquo;jump equal&rdquo; (jump if condition is true)  
- **jz**: &ldquo;jump zero&rdquo; (jump if operand is zero)  
- **call**: jump to a function (subroutine) by pushing current code location to stack  
- **return**:  return from subroutine (to return address on the stack)

#### Stack

The **stack pointer** (SP) holds the address of the top of the stack while the stack grows _downwards_.
The SP points to the last allocated word (&ldquo;pre&ndash;decremented stack pointer&rdquo;).

- **push**: makes room for values on the stack by decrementing the SP and the inserting new element
- **pop**: cleans up values from the stack by incrementing the SP (removed data is not overwritten)

![Stack layout](img/04-stack.png)

A **base pointer** (BP), also known as **frame pointer** (FP), can be used to organize larger chunks of the stack called **stack frames**.

## Application Binary Interface

The **Application Binary Interface** (ABI) standardizes communication between applications and the OS.
It may specify executable/object file layout, calling conventions, stack alignment rules etc.
The **calling conventions** define the way function calls are implemented in order to achieve interoperatibility across compilers.
In C, these conventions are (historically) called **cdecl**.

**Example**: SystemV AMD64 ABI (used in Linux, BSD and OS X)

### x86 calling conventions

When a function is called, the calling function

1. saves the state of the local scope
2. sets up parameters where the called function can find them
3. jumps to (*calls*) the called function

The called function then

1. sets up a new local scope
2. runs its body (which may include calling other functions)
3. puts the return value where the calling function can find them
4. jumps back (*returns*) to the calling function

## Parameter passing and return codes

The system call number must be passed to the system along with the other arguments of the system call. The ABI specifies how to do that. Arguments can be transferred in different places:

- CPU registers (limit depends on how many registers there are)
- Main memory (heap or stack) for strings or if the registers are not enough

Arguments may also just all be transferred via main memory.

A **return code** needs to be returned to the application.
Usually, negative numbers denote an error condition, positive numbers and zero denote success.
Return codes are usually stored in the A and D registers.

### System call handler

When an application &ldquo;traps&rdquo; into the Kernel, the System call handler

1. saves registers that it will use
2. reads passed parameters
3. **sanitizes and checks those parameters**
4. checks if the calling process has permission to perform the requested action
5. performs the requested action on behalf of the process
6. writes return value
7. returns to the process

## Process API

Processes are started in a variety of ways, for example:

- Initialisation (&ldquo;boot process&rdquo;)
- By another process via a system call
- User requests a new process (e.g. opening files on the Desktop)
- Initiation of a batch job

But in the end all of those ways boil down to two mechanisms:

- The Kernel spawns an initial (user space) process on boot
    - Linux: **init**
- A process starts another process
    - POSIX: `fork`
    - Windows: `CreateProcess`

### POSIX process creation using `fork`

Every process has an unique **process identifier** (PID).

- `pid = fork()` copies the calling process
    - `pid` is 0 for the new child and the childs PID for the parent
- `exec(name)` replaces the calling process&rsquo; memory with the executable file `name`
- `exit(status)` terminates the calling process and returns an **exit status**
- `pid = waitpid(pid, &status)` waits for the termination of child process with identified by `pid`
    - `status` is a data structure that process exit information will be written to (e.g. the exit status)
    - On success, the argument `pid` is returned, -1 signifies failure

![Process states](img/04-posix-process-api.png)

### Process environment

Each process has **environment variables** that can be passed at creation.
The environment is typically defined by your shell (type `env` in a Linux shell).
In order to pass **e**nvironment variables, use execv**e** instead of  exec.

### Command line arguments

Each process is started with a vector of command line arguments
The first argument always is the name of the executable.
Other arguments may be passed when running a program on the command line.

```
$ my_app arg1 arg2 arg3
```

### Passing the argument vector

All C programs need to include a function `main` of the following signature.

```int main(int argc, char argv**, char envp**);```

You may omit `envp` or `argc`, `argv` and `envp` together.

- `argc` contains the number of arguments
- `argv` is the command line argument vector
- `envp` is the environment variable vector

The function `main` is just handled like any other function in C.
On process creation, the OS:

- writes the argument strings somewhere in main memory
- creates the stack for the process, pushing the `argv` and `envp` pointers to those strings
- jumps to the function `main`

## POSIX process hierarchy

**Parent process** creates **child process**, which can become a parent process too, forming a **process tree**.
Parent and children share resources (part of the address space) and execute concurrently.
Parents can wait for the children to terminate using `waitpid` (see above).

![Process hierarchy](img/04-posix-hierarchy.png)

### Daemons

Some processes are designed to run in the background, for example web servers.
Those processes are called **daemons**.
After creation, a daemon detaches from its parent process and reattaches to the root of the process tree, the init process.
Thus, the daemon keeps running even if its initial parent process terminates.

- In C, you can do this by creating a new session (using `setsid`)
- In Bash, you can use `disown`
- In a Linux shell, run `pstree -a` to show the process tree

### Process states

Sometimes, processes wait for events (for example arrival of a network packet) or other processes.
Waiting processes are called **blocking**.
Processes usually block on system calls.
The OS should not run the process until the event occurs.

![Process states model](img/04-process-states.png)

1. Process blocks for event
2. Scheduler activates another process
3. Scheduler activates this process
4. Event has occurred

## Process Termination

### Voluntary exit

- Normal exit: `return 0;` in `main` or `exit(0);`
- Error exit: `return x;` in `main`, `abort();` or `exit(x);` where x &ne; 0

### Involuntary exit

- OS kills process (**fatal error**), e.g.:
    - After CPU exception
    - Process exceeds alloted resources
- Another process sends a signal to kill the process
    - Only possible with sufficient privileges (parent process or running as root)

### Exit Status

If a process terminated voluntarily, it returns an **exit status** in the form of an integer.
In Linux, regardless of this integers size, only the lowest 8 bits are significant.

A process&rsquo; resources cannot be completely freed after it terminates.
A so&ndash;called **Zombie process** or **process stub**  remains until the exit status is collected (via `waitpid`).
Only then can the PID and the allocated resources be freed.

### Orphans

Children that keep running after their parent process dies are called **orphans**.
Generally, the init process &ldquo;adopts&rdquo; orphans &mdash; they keep running.
Some operating systems perform a **cascading termination**, i.e. when a process terminates, all of its children terminate as well.
