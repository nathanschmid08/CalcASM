<h1 align="center">
  <img src="icon.ico" alt="CalcASM Icon" height="50"> 
  <br>CalcASM
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Stable-green" alt="Status">
  <img src="https://img.shields.io/badge/Version-1.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
</p>

<div align="center">
  <h3>
    <strong>Convert Mathematical Expressions to Assembly Code in Seconds</strong>
  </h3>
  <h3>🔢 → 🔍 → 📝 → 💻</h3>
  <p><em>From Expression to Assembly in One Click</em></p>
</div>

<p align="center">
  <a href="#-overview"><b>📋 Overview</b></a> ·
  <a href="#-key-features"><b>🌟 Key Features</b></a> ·
  <a href="#-quick-start"><b>🚀 Quick Start</b></a> ·
  <a href="#-showcase"><b>✨ Showcase</b></a> ·
  <a href="#-behind-the-scenes"><b>🔬 Behind the Scenes</b></a>
</p>

<hr>

<img align="right" src="icon.ico" width="150">

## 📋 Overview
**CalcASM** is a sleek, dark-themed calculator application that not only evaluates mathematical expressions but also generates corresponding x86-64 NASM assembly code for Windows. Perfect for students, programmers, and assembly enthusiasts who want to understand the low-level implementation of mathematical operations.

<hr>

## 🌟 Key Features

<table>
  <tr>
    <td width="80" align="center">
      <h1>🌒</h1>
    </td>
    <td>
      <h3>Elegant Dark UI</h3>
      <p>Sleek dark-themed calculator with high-contrast elements designed for long coding sessions</p>
    </td>
  </tr>
  <tr>
    <td width="80" align="center">
      <h1>⚡</h1>
    </td>
    <td>
      <h3>Real-Time Conversion</h3>
      <p>Instantly transform any valid expression into optimized x86-64 NASM assembly code</p>
    </td>
  </tr>
  <tr>
    <td width="80" align="center">
      <h1>🧠</h1>
    </td>
    <td>
      <h3>Educational Insights</h3>
      <p>See exactly how the CPU would execute your calculations with detailed assembly instructions</p>
    </td>
  </tr>
  <tr>
    <td width="80" align="center">
      <h1>🔌</h1>
    </td>
    <td>
      <h3>Ready to Run</h3>
      <p>Generated code is fully executable - no additional modifications needed</p>
    </td>
  </tr>
</table>

<hr>

## 🚀 Quick Start

> **Note:** CalcASM is ready to use out of the box - no installation or compilation required!

### In Just 3 Steps:

<div align="center">
  <table>
    <tr>
      <td align="center" width="33%">
        <h2>1️⃣</h2>
        <p>Download the repository and find <code>CalcASM.exe</code> in the <code>dist</code> folder</p>
      </td>
      <td align="center" width="33%">
        <h2>2️⃣</h2>
        <p>Enter your mathematical expression using the calculator or type directly</p>
      </td>
      <td align="center" width="33%">
        <h2>3️⃣</h2>
        <p>Click "Convert" to generate and save your assembly code</p>
      </td>
    </tr>
  </table>
</div>

<hr>

## ✨ Showcase

### Examples of What You Can Do:

<table>
  <tr>
    <th width="40%">Expression</th>
    <th width="60%">Key Assembly Concepts Demonstrated</th>
  </tr>
  <tr>
    <td><code>5 + 3 * 2</code></td>
    <td>Order of operations, stack manipulation, basic arithmetic</td>
  </tr>
  <tr>
    <td><code>(7 - 2) / 5</code></td>
    <td>Register usage, division operations, parentheses handling</td>
  </tr>
  <tr>
    <td><code>2^8 - 1</code></td>
    <td>Looping constructs, exponentiation, power implementation</td>
  </tr>
  <tr>
    <td><code>3 * (4 + 2^3) / 2</code></td>
    <td>Complex expression parsing, nested operations, efficient code generation</td>
  </tr>
</table>

### Sample Assembly Output:

```nasm
; Generated NASM Assembly Code for Windows x64
global main
extern ExitProcess
extern printf

section .data
    format db "%d", 10, 0  ; Format string for printf

section .text
main:
    ; Initialize stack frame
    push rbp
    mov rbp, rsp
    sub rsp, 32  ; Shadow space for Win64 calling convention

    push 2       ; Push base (2)
    push 4       ; Push exponent (4)
    
    ; Calculate power
    pop rcx      ; Get exponent
    pop rax      ; Get base
    mov rbx, 1   ; Initialize result to 1
    cmp rcx, 0
    je power_end_0
power_loop_0:
    imul rbx, rax  ; Result *= base
    dec rcx        ; Exponent--
    jnz power_loop_0
power_end_0:
    push rbx     ; Push result (16)
    
    push 3       ; Push second operand (3)
    pop rax      ; Get right operand
    pop rbx      ; Get left operand
    add rbx, rax ; Add left and right
    push rbx     ; Push final result (19)
    
    ; Display result
    pop rcx      ; First argument - value to print
    lea rdx, [format]
    xor r8, r8
    xor r9, r9
    call printf
    
    ; Exit program
    xor rcx, rcx
    call ExitProcess
```

<hr>

## 🔬 Behind the Scenes

### Supported Mathematical Operations:

```
+  Addition        →  add instruction
-  Subtraction     →  sub instruction
*  Multiplication  →  imul instruction
/  Division        →  idiv instruction
^  Exponentiation  →  Custom loop implementation
() Parentheses     →  Expression grouping
```

<hr>

<div align="center">
  <h3>💻 Made for Assembly Enthusiasts, by an Assembly Enthusiast 💻</h3>
  <p><em>"Understanding assembly is understanding the machine."</em></p>
</div>
