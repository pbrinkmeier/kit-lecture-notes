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

The OS interacts directly with compiled programs. The following list is a set of (simplified) assembler instructions you should know.

_Data movement:_  
**mov:** Copy data from second operand to first operand

_Arithmetic commands:_  
**add/sub:** Add, substract, multiply or divide two integer operands storing the result in the first operand  
**inc/dec:** Increment or decrement from register or memory location  
**shl/shr:** Bitshift left/right  
**and/or/xor:** Bitwise and/or/xor of two operands storing the result in the first operand  
**not:** Logical negation  

_Basic jump/branch/call commands:_  
**jmp:** Continue execution at given address  
**je:** "jump equal" (jump if condition is true)  
**jz:** "jump zero" (jump if operand zero)  
**call:** Jump to a function (subrouting) by pushing current code location to stack  
**return:**  Return from subroutine (to return address on the stack)

### x86 Stack

The _stack pointer (SP)_ holds the address of the top of the stack while the stack grows _downwards_. The SP points to the last allocated word ("pre-decremented stack pointer").

_push_ makes room for values on the stack by decrementing the SP and the new element. _pop_ cleans up values from the stack by incrementing the SP (removed data is not overwritten).

![](img/04-stack.png)

## System Calls

## Process API