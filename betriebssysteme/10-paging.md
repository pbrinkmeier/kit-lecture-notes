# 10: Paging

> 28.11.2017, 04.12.2017

## Table of contents

_TODO_

## Desired properties when sharing physical memory

- **Protection**: processes should not be allowed to manipulate/observe other process&rsquo; memory
- **Transparency**: processes should not need to rely on knowing physical memory
- **Resource exhaustion**: allow the sum of memory allocated by all processes to be greater than actual physical memory

See chapter 9 for more information.

## Memory management unit

Safe and secure memory protection can only be achieved in hardware.
A hardware device called **memory management unit** (MMU) maps virtual to physical addresses.
Userspace programs only deal with those virtual addresses and never see real physical ones.

![Memory management unit schema](img/09-mmu.png)

## Paging

**Paging** describes dividing physical memory into chunks of fixed size called **page frames**.
Typical frame sizes are between 1KiB and 4MiB.

The operating system maintains a **page table** that represents a mapping from **virtual page numbers** (VPNs) to **page frame numbers** (PFNs).
A **present bit** in this table indicates whether a virtual page is currently mapped to physical memory.
The MMU accesses the page table and translates virtual addresses into physical addresses.
If a process issues an instruction that accesses an invalid virtual address, the MMU calls the kernel for handling the situation (**page fault**).

![Paging](img/10-paging.png)

### Page table entry

The following is a list of fields a page table entry may have.
Which fields the entry actually has depends on the system used.
Except for the **valid bit** and the **page frame number, all of these are optional.

- **Valid bit**/**present bit**: whether the page is currently used
- **Page frame number**: base address of the physical memory page
- **Write bit**: whether the page is writable. Writing to a page where this bit is clear will raise a page fault
- **Caching**: what policy this page should be cached with (may be not at all)
- **Accessed bit**: set by the MMU when the page is touched
- **Dirty bit**: set by the MMU when the page is modified

### The operating system and paging

The operating system performs operations that require semantic knowledge:

- Page allocation (finding a free page frame in the page table)
- Page replacement (some pages are replaceable, e.g. heap segments that can be swapped to a **pagefile** or **swap area**)
- Context switches (OS sets the MMU&rsquo;s base register (e.g. `%CR3` on x86) to point to the page hierarchy of the another process&rsquo; address space

### Page size trade-offs

Paging eliminates external fragmentation due to its fixed size blocks.
However, **internal fragmentation** becomes a problem:
If a the memory allocated by a process is not exact multiple of the page size (which is mostly isn&rsquo;t), some of the allocated memory is not used.

![Internal fragmentation visualized](img/10-internal-fragmentation.png)

- Fragmentation:
    - Large pages ⇒ more memory is wasted due to internal fragmentation
    - Small pages ⇒ less internal fragmentation
- Page table size:
    - Large pages ⇒ less pages ⇒ fewer bits for page frame numbers, fewer page table entries
    - Small pages ⇒ more pages ⇒ more bits for page frame numbers, more page table entries
    - Note: some page table layouts support multiple page sizes (e.g. x86-64)
- I/O:
    - Small pages ⇒ more page faults when loading big chunks of data ⇒ more overhead

## Page table layouts

### Linear page table

In this layout, a virtual address consists of a **virtual page number** (VPN) and a **page offset**.
The virtual address is an index in an array of base addresses.
The physical address is the sum of the base address and the page offset.

![Translation of virtual address 0x10123 using a linear page table](img/10-paging-translation-scheme.png)

Linear page tables are not used in practice, because the use a _lot_ of space.

### Hierarchical page table

Each process needs to have a mapping for all VPNs at all times; however, most processes only use a small slice of their available VPNs.
This means that most processes do not need to have access to the whole page table.
An **hierarchical page table** splits up the address space into multiple smaller page tables.

The problem of hierarchical tables usually is that a lot of lookups (slow main memory accesses) are needed per resolved address.

### Linear inverted page table

An **inverted page table** stores mapping _from_ physical addresses to VPNs.
Only one table per system is needed, because one table can serve all processes.
This way, it uses only a fraction of the memory a linear or hierarchical page table would.

![Linear inverted page table schema](img/10-linear-inverted-page-table.png)

The problem is that resolving an address happens in linear time, proportional to the amount of page frames.

### Hashed inverted page table

Just like an inverted page table, but a **hash anchor table**, indexed by hashed virtual page numbers, limits the search to at most a few page table entries.

![Hashed inverted page table schema](img/10-hashed-inverted-page-table.png)

#### Typical lookup in an hashed inverted page table

1. Hash virtual page number part of virtual address
2. Lookup the page table entry using this hash
3. If the virtual page number of the entry does not match the one of the virtual address, look at the next one and repeat this step
4. Use the page table entry to make the physical address

![Lookup schema for hashed inverted page table](img/10-hashed-inverted-lookup.png)

## Translation lookaside buffer

### Naïve paging is slow

Using page tables, especially the most commonly used hierarchical ones, means that every load and store operation requires multiple memory accesses.
In a four level hierarchy, every load and store operation performs five memory accesses; four accesses to page directories and tables and the actual operation.

Memory lookups often happen sequentially (e.g. array accesses, reading instructions) and thus only a few pages are used most of the time.
The **translation lookaside buffer** (TLB) caches results of page table lookups.
It maps virtual page numbers to page frame numbers and their flags.

Typically, a TLB has somewhere around 64 and 2 thousand entries and a hit rate of at least 95%.

### TLB operation

Many TLB entries can be compared at the same time in hardware.
That&rsquo;s what makes the TLB fast.
On every memory load and store operation, check if result is already cached, if not, look it up in the page table and insert it into the cache.

![Translation lookaside buffer schema](img/10-translation-lookaside-buffer.png)

### TLB misses

When the TLB does not contain an entry for a virtual page number, a new entry is inserted and an older one will be overwritten.
This can be handled either in software or in hardware.

#### Software-managed TLB

On a TLB miss, the CPU issues a TLB miss exception.
The OS receives the exception and decides what entry to evict from the TLB in order to make space.
It then walks the page table hierarchy to insert the new entry.

For example, the MIPS architecture uses a software-managed TLB.

#### Hardware-managed TLB

On a TLB miss, an entry gets evicted from the TLB by some policy encoded in hardware.
The hardware then walks the page table hierarchy to insert the new entry.

For example, x86-64 and ARM use a hardware-managed TLB.

### Address space identifiers

Using multiple address spaces, one and the same virtual page number may refer to different page frames.
This may lead to entries being evicted from the TLB on address space switches.

This issue can be avoided by resolving the ambiguity of VPNs in the TLB by adding additional identfiers to TLB entries.
These identifiers are called **address space identifier**s (ASID).

The TLB now maps a combination of ASID and VPN to page frame numbers.
TLB flushing resulting from context switches are now eliminated.

### TLB reach

**TLB reach** (also known as **TLB coverage**) describes the amount of memory accessible with TLB hits.
The formula is:

```
TLB_reach = TLB_size * page_size
```

Ideally, the working set of each process can be and is stored in the TLB.

In order to increase the TLB reach, we can either increase the TLB size or the page size.
Increasing TLB size is very expensive; increasing page size increases internal fragmentation.

A good approach is to provide different page sizes.
This allow processes to allocate larger memory areas without filling the TLB too much and increasing internal fragmentation.

### Effective access time

A TLB lookup takes `t` time units, e.g. `t = 1`.
A memory cycle takes `m` time units, e.g. `m = 100`.
TLB has a hit rate (cached accesses per memory accesses) of `a`, e.g. `a = 0.99`.
The **effective access time** (EAT) for a linear page table without additional cache is defined as:

```
EAT =
  // one TLB lookup and one memory access per cache hit
  (t + m) * a
  // one TLB lookup and 2 memory accesses per cache miss
+ (t + 2 * m) * (1 - a)

= t + 2 * m - m * a
```

### Influence on program structure

Goal: fill a 128&times;128 matrix with zeroes.
We assume that each row is stored in one page and that in the beginning, none of the pages is cached in the TLB.

Naïve approach:

```c
int data[128][128];

for (int j = 0; j < 128; j++) {
	for (int i = 0; i < 128; i++) {
		data[i][j] = 0;
	}
}
```

This yields 16,384 (128 &times; 128) TLB misses because it sets the first cell of the first page, then the first of the second page, then the first of the third page and so on.
The better approach is to iterate over a row before jumping to the next row:

```
int data[128][128];

for (int j = 0; j < 128; j++) {
	for (int i = 0; i < 128; i++) {
		data[j][i] = 0; // indices swapped
	}
}
```

This only causes one TLB miss for each row, i.e. 128.

## Page tables and virtualization

So far we only concerned ourselves with traditional system architectures.
But what about hardware virtualization?
In a traditional system, we only have a kernel address space and a seperate address space for each process.
But now we have a whole other operating system running in a virtual machine.
We can either just let the hypervisor manage the guest resources (**hosted virtualization**) or take care of that in the hosting OS (**bare-metal virtualization**).

This way, we have two levels of memory virtualization.
At the hosts level, there is a mapping between phyiscal memory and virtual addresses.
The hosts virtual addresses are perceived to be phyiscal addresses by the guest (**guest-physical addresses**).
Within the virtual machine, those are mapped to **guest-virtual addresses**.

![Bare-metal (left) vs. hosted (right)](img/10-baremetal-vs-hosted.png)

### Two levels of page tables

Host OS translates between physical and virtual (physical for the guest) addresses.
Hypervisor translates between virtual and guest-virtual addresses.

But is there a faster way?

### Shadow page tables

Software-based virtualization of page tables.
The hypervisor maintains **shadow page tables** not visible to the guest and keeps them synchronized with the guests page tables.

![Shadow page tables](img/10-shadow-page-tables.png)

Due to a lot of trapping to the hypervisor necessary because of page table synchronization, this adds too much overhead.

### Hardware based virtualization

Capacities for nested page tables may be implemented in hardware (e.g. **NPT** by AMD, **EPT** by Intel).

![](img/10-nested-pt.png)

![](img/10-amd-npt-guest-tables.png)

### Pros and cons of hardware-based virtualization of address translation

Advantages include:

- The guest can manage its page tables without trapping to the hypervisor
- No need for the hypervisor to keep a copy of the guests page table
- Additional performance optimizations can be implemented in memory, e.g. nested TLBs, TLB partioning, page-walk cachec, &hellip;

Disadvantages include:

- `n`th level guest on `m`th level host page table lookup needs `(n + 1) * m` memory accesses, leading to a higher cost of TLB misses

## Examples

### Example: two-level page table

On a 32-bit machine using pages of 4 KiB, virtual addresses are divided into:

- Page number (p): 20 bits
- Page offset (d): 12 bits

The page table itself can be paged in order to save memory.
The page number p is subdivided into:

- Index in **page directory** (p1): 10 bits
- Index in **page table entry** (p2): 10 bits

![A simple example of an hierarchical page table](10-hierarchical-page-table.png)

### Example: 32-bit Intel architecture (IA-32)

IA-32 divides a virtual address into a 10-bit directory pointer, a 10-bit table pointer and a 12-bit offset.

![IA-32 page table hierarchy overview](10-ia32-page-hierarchy.png)

The **page directory** contains pointers to a page tables.
The directory pointer points to such an entry.

![IA-32 page directory](10-ia32-page-directory.png)

The **page table**s contain pointers to actual pages.
The offset is added to such a pointer to get the physical address.

![IA-32 page table](10-ia32-page-table.png)

### Example: Intel/AMD x86 64-bit

- x86-64 **long mode**: 4-level hierarchical page table
- **Page directory base register** (control register 3, `%CR3`) stores the starting physical address of the first level page table
- For every address space, the page table hierarchy goes as follows
    - Page map level 4 (PML4)
    - Page directory pointers table (PDPT)
    - Page directory (PD)
    - Page table entry (PTE)
- At each level, the respective table can either point to a directory in the next hierarchy level, or to an entry containing actual mapping data
- Depending on the depth of the entry, the mapping has different sizes:
    - PDPTE: 1 GiB page
    - PDE: 2 MiB page
    - PTE: 4 KiB page

![x86-64 page table hierarchy](img/10-x86-64-page-table-hierarchy.png)

- Intel 4-level paging supports a maximum of 256 TiB virtual address space
    - 48 bit linear addresses
    - with 4 KiB page: 9 bit index into PML4, PDPT, PD, PT; 12 bit page offset
- Processors use 46 bit physical addresses (max. 64 TiB physical memory)
- Intel 5-level pages: extension for larger address space
    - add 9 bits for 5th level of hierarchy ⇒ 128 PiB virtual memory
    - physical address width extended up to 52 bit ⇒ 4 PiB virtual memory

### Example: ARM 32-bit

- 1 MiB pages with a 1 level page table: 12/20
- 64 KiB pages with a 2 level page table: 12/4/16
- 4 KiB pages with a 2 level page table: 12/8/12

In newer architectures, the subpages shown below are deprecated.

![ARM 32-bit page table hierarchy](10-arm32-page-table.png)

### Example: ARM 64-bit

- 512 MiB pages with a 2 level page table: 1/13/29

![ARM 64-bit large pages](10-arm64-512m.png)

- 64 KiB with a 3 level page table: 1/13/13/16

![ARM 64-bit small pages](10-arm64-64k.png)

- Additional level using bits 47 to 42 supported

### Example: PowerPC 32-bit

- Combination of segmentation and inverted page table
- Segementation yields virtual base, hash indicates entry in page table bucket
- CPU searches page table bucket, calls OS if no matching entry exists

![PowerPC 32-bit page table hierarchy](10-powerpc32-page-table.png)
