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
