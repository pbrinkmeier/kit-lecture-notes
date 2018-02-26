[zurück](README.md)

# 14: Memory Allocation

> 08.01.2018

## Table of contents

## TL;DR

- **Dynamic memory allocation** means allocating and freeing memory chunks of arbitrary size at runtime
- It is provenly impossible to construct a memory allocator that always performs well (Robson)
- The main problem of dynamic memory allocators is **fragmentation**
- Typical data structures used inside dynamic memory allocators are linked lists and bitmaps
- Simple allocation strategies that perform reasonably well are:
    - **best-fit** (choose the smallest free region the requested chunk fits in)
    - **first-fit** (choose the first free region the requested chunk fits in)
- More advanced memory allocators are the buddy allocator and the SLAB allocator that are used in the Linux kernel to allocate page frames and kernel-internal data structures

## Dynamic memory allocation

**Dynamic memory allocation** makes a system able to allocate and free chunks of memory  of arbitrary size at any time.

Because of its many advantages, almost every program uses dynamic memory allocation, via the **heap**.
Those advantages are:

- Not needing to statically specify complex data structures
- Being able to have a programs data grow as a function of input size

In fact, even the kernel uses dynamic memory allocation for its data structures.

On the other hand, the use of dynamic memory has a huge impact on performance.
It is proven that one can not implement a dynamic memory allocator that always performs well.

> &ldquo;For any possible allocation algorithm, there exists a stream of allocation and deallocation requests that defeat the allocator and force it into severe fragmentation.&rdquo; &mdash; Robson

## What does a dynamic memory allocator do?

The allocator initially has a pool of free memory.
During its lifetime, it accepts **allocation** and **deallocation** requests for that pool.
Thus, the allocator needs to track which parts of its memory are free and which are used.
The allocator has no control over the order or the number of requests it receives.
Once allocated, a used region can not be movement again (within the address space).
That means any bad placement decision taken by the allocator is permanent.
**Fragmentation** is a core problem of allocators.