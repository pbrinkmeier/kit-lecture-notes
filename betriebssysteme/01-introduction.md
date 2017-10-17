# Overview

> 2017-10-16

## The lecture

Professor: Dr. Hans Reiser <hans.reiser@kit.edu>

Assistants: gottschlag@kit.edu, rittinghaus@kit.edu

Password for the ILIAS page: **BS17**

### Tutoria

Sign-up for Tutoria: https://wiwi.link/os2017

Each week there will be two worksheets: so-called **"Tutoriumsblätter"** and **"Übungsblätter"**.
Only the Übungsblatter will be turned in and graded but it is highly recommended to do both sheets.

### Exams

- Hauptklausur: **2018-03-02**, 14:00, 2 hours
- Übungsscheinklausur: **2018-03-22**, 11:00, 2 hours

**Only the Hauptklausur is graded as usual**, the Übungsscheinklausur only gets you extra points for the Hauptklausur.
However, **attendance to the Übungsscheinklausur is mandatory.**

In the week before the Hauptklausur there will be **additional Tutoria** ("Zusatztutorien") which will be announced in the lecture.

### Contents of the lecture

- Processes and threads
- Scheduling
- Synchronization
- Memory management
- Secondary memory
- File systems
- Input/Output systems

### Recommended literature

**TBD**

## Introduction

### What is an operating system?

- There is no commonly accepted definition.
- Definitions (not mutually exclusive)
    - **"Everything a vendor ships when you order an operating system"**, which basically covers everything from Windows to some embedded system running Lua on an 40MHz MCU.
    - **Resource mananger**: distributes resources across processes and especially prevents two processes from using the same memory.
    - **Control program**: watches programs and assures that they execute correctly.

### History

- **1st generation (1945-55)**: plugboard computers made of a whole lotta vacuum  tubes. Example: ENIAC
- **2nd generation (1955-65)**: big machines operated by inputting punchcards. Example: IBM 7094
- **3rd generation (1965-80)**: Integrated circuits. Example: DEC PDP-7 
    - First parallel systems.
- **4th generation (1980-90)**: Personal computers hit the mass market. Everybody can own a computer. Example: Commodore 64
- **5th generation (1990-?)**: Mobile computers. Example: Smartphones, Smartwatches, etc.

### Hardware

- Examples of omponents (some of which can be present a lot of times):
    - CPU
    - Memory
    - Video device
    - Keyboard device
    - USB device
    - Hard drive
- All of those operate **concurrently**.

#### CPU

- Fetches instructions from main memory and executes them.
- A CPU usually has some number of **registers**:
    - General purpose registers
    - Floating point registers
    - Instruction pointer
    - Stack pointer
    - Program Status Word (PSW)
- **Modes of execution** ("Rings"):
    - **User Mode** (Ring 3 in x86):
        - Only non-privileged instructions are executable
        - For example, direct control of hardware is forbidden in User Mode.
    - **Kernel Mode** (Ring 0 in x86):
        - All instructions are executable.
    - Today, only Ring 0 and Ring 3 are commonly used.

#### RAM

- Contains data (which program instructions are a part of).
- CPUs come with a memory controller.
- Usually, loading fetching instructions from RAM is much slower than their execution on the CPU.
    - Effective caching can be used because instructions are in a sequence most of the time (**TBD**: spatial blabla).

**TBD**: access times images

#### CPU cache organization

- CPU caches are hardware.
- They contain **chunks of main memory copied for faster access**.
- There usually are **multiple levels of caches**; on an Haswell chip, there are the caches L1 through L3 (lower number is closer to the processor).
    - The closer to the processor, the lower is the access time.
    - The closer to the processor, the smaller is the cache.
    - The highest level of cache before the memory is also called **LLC (last-level cache)**.
- Typically, caches are managed in so-called **"cache-lines" of 64 Bytes**.
- **"Cache hit"**: Requested data is stored in cache (e.g. "L2 cache hit").
- **"Cache miss"**: Requested data is not stored in cache (e.g. "L1 cache miss").

#### Interplay of CPU and devices

- CPU sends data to device controller.
- After it is done, the device notifies APIC (**TBD**: what is this).
- APIC interrupts the CPU.
- Transfer of data from the CPU to the devices:
    - **PMIO** (**P**ort-**M**apped **IO**): data to be transferred is stored in some **registers** on the CPU itself.
    - **MMIO** (**M**emory-**M**apped **IO**): data to be transferred is stored in **main memory**.
