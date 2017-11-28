# 10: Paging

> 28.11.2017

## Table of contents

_TODO_

## Desired properties when sharing physical memory

- **Protection**:
    - A bug in some process should not affect any other process
    - Do not allow processes to manipulate/observe other process&rsquo; memory
- **Transparency**:
    - Processes should not need to rely on knowing physical memory
    - Processes should be allowed to use big amounts of contiguous memory
- **Resource exhaustion**:
    - Allow the sum of memory allocated by all processes to be greater than actual physical memory

## Memory management unit

Safe and secure protection can only be achieved in hardware.
A hardware device called **memory management unit** (MMU) maps virtual to physical addresses.
Userspace programs only deal with those virtual addresses and never sees real physical ones.

_TODO: insert image from 3/29._

## Paging

A **present bit** in the **page table** indicates whether a virtual page is currently mapped to physical memory.
The MMU reads the page table and translates valid mappings.
If a process issues and instruction that accesses an invalid virtual address, the MMU calls the kernel for handling the situation (**page fault**).

_TODO: insert image from 4/29_

### Page table entry

Except for the **valid bit** and **page frame number**, all of these fields are optional.

- **Valid bit**/**present bit**: whether the page is currently used
- **Page frame number**: base address of the physical memory page
- **Write bit**: whether the page is writable. Writing to a page where this bit is clear will raise a page fault
- **Caching**: what policy this page should be cached with (may be not at all)
- **Accessed bit**: set by the MMU when the page is touched
- **Dirty bit**: set by the MMU when the page is modified

### The operating system and paging

The operating system performs operations that requires semantic knowledge.

_TODO: 9/29_

### Page size trade-offs

_TODO: internal fragmentation 10ff._

- Fragmentation
- Page table size
- I/O

## Page table layouts

### Linear page table

A virtual address consists of the **virtual page number** (VPN), which is an index of the page table mapping it to a **page** (usually around 1Ki) of phyiscal memory, and the **page offset**, which is added to the base address of the page.

```
page_table[0] = 0x0
page_table[1] = 0x1
page_table[2] = 0x2
...

physical_address(virtual_address) =
	((page_table[virtual_address >> 4] << 4) + (virtual_address & 0xffff)
```

_TODO: insert image from 6/29_ 
Not practical, since it uses _a lot_ of space.

_TODO: insert example calculation_

### Hierarchical page table

A mapping for each VPN must be present for each process at all times.
Since most processes only use a tiny slice of their available VPNs, they don&rsquo;t need a complete table.
A method for implementing this is to split up the address space into multiple page tables forming an **hierarchical page table**.

The problem of hierarchical tables is that a lot of lookups are needed per resolved address.

#### Example: two-level page table

On a 32-bit machine using pages of 4 KiB, virtual addresses are divided into:

- Page number (p): 20 bits
- Page offset (d): 12 bits

The page table itself can be paged in order to save memory.
The page number p is subdivided into:

- Index in **page directory** (p1): 10 bits
- Index in **page table entry** (p2): 10 bits

_TODO: 12/29_

#### Example: 32-bit Intel architecture (IA-32)

_TODO: 13ff._

#### Example: four-level page table (x86-64)

Does this even make sense?
Five memory accesses for looking up just a single entry?

_TODO: 16/29_

### Inverted page table

Instead of storing a mapping from VPNs to phyical addresses, store a mapping from physical addresses VPNs.
Thus we avoid having to store lots of entries, as only one table per system is needed (single table serves all processes).

The big advantage over a linear or hierarchical page table is that only a small amount of memory is needed.
The problem is that resolving an address happens in linear time, proportional to the amount of page frames.

_TODO: 17/29_

### Hashed inverted page table

Just like an inverted page table, but the **hash anchor table** limits the search to at most a few PTEs.

_TODO: 18/29_

_TODO: 19/29_

## Translation lookaside buffer

Caches lookups in order to make further lookups fast.
