#!/usr/bin/env python3
"""
Math Expression to x86-64 NASM Assembly Converter for Windows

This program converts a mathematical expression into x86-64 NASM assembly code
that can be compiled and run on Windows.
"""

import re
import sys
import os


class Parser:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = self._tokenize(expression)
        self.pos = 0
        self.current_token = None
        self.next_token()

    def _tokenize(self, expression):
        token_pattern = r'(\d+\.\d+|\d+|[+\-*/()^])'
        return re.findall(token_pattern, expression)

    def next_token(self):
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None
        return self.current_token

    def parse(self):
        return self.expr()

    def expr(self):
        """Parse expression (lowest precedence: addition, subtraction)"""
        node = self.term()
        while self.current_token in ('+', '-'):
            op = self.current_token
            self.next_token()
            right = self.term()
            node = {'type': 'binary', 'op': op, 'left': node, 'right': right}
        return node

    def term(self):
        """Parse term (medium precedence: multiplication, division)"""
        node = self.factor()
        while self.current_token in ('*', '/'):
            op = self.current_token
            self.next_token()
            right = self.factor()
            node = {'type': 'binary', 'op': op, 'left': node, 'right': right}
        return node

    def factor(self):
        """Parse factor (highest precedence: power)"""
        node = self.primary()
        if self.current_token == '^':
            op = self.current_token
            self.next_token()
            right = self.factor()  # Right-associative
            node = {'type': 'binary', 'op': op, 'left': node, 'right': right}
        return node

    def primary(self):
        """Parse primary (numbers, parenthesized expressions)"""
        token = self.current_token
        if token is None:
            raise SyntaxError("Unexpected end of expression")
        
        if token.replace('.', '', 1).isdigit():  # Number (integer or float)
            self.next_token()
            if '.' in token:
                return {'type': 'number', 'value': float(token)}
            else:
                return {'type': 'number', 'value': int(token)}
        elif token == '(':
            self.next_token()
            node = self.expr()
            if self.current_token != ')':
                raise SyntaxError("Expected closing parenthesis")
            self.next_token()
            return node
        else:
            raise SyntaxError(f"Unexpected token: {token}")


class Compiler:
    def __init__(self):
        self.asm_code = []
        self.temp_counter = 0

    def generate_code(self, node):
        if node['type'] == 'number':
            # Push number onto stack
            return [f"    push {int(node['value'])}"]
        
        elif node['type'] == 'binary':
            op = node['op']
            # Generate code for operands
            left_code = self.compile_expr(node['left'])
            right_code = self.compile_expr(node['right'])
            
            # Generate operation code
            if op == '+':
                return self._generate_binary_op(left_code, right_code, "add")
            elif op == '-':
                return self._generate_binary_op(left_code, right_code, "sub")
            elif op == '*':
                return self._generate_binary_op(left_code, right_code, "imul")
            elif op == '/':
                return self._generate_division(left_code, right_code)
            elif op == '^':
                return self._generate_power(left_code, right_code)
        
        raise ValueError(f"Unknown node type: {node['type']}")

    def _generate_binary_op(self, left_code, right_code, asm_op):
        code = []
        # Right operand first (will end up second on the stack)
        code.extend(right_code)
        # Left operand
        code.extend(left_code)
        # Perform operation
        code.append("    pop rax    ; Get right operand")
        code.append("    pop rbx    ; Get left operand")
        code.append(f"    {asm_op} rbx, rax  ; {asm_op} left, right")
        code.append("    push rbx   ; Push result")
        return code

    def _generate_division(self, left_code, right_code):
        code = []
        # Right operand first (will end up second on the stack)
        code.extend(right_code)
        # Left operand
        code.extend(left_code)
        # Perform division
        code.append("    pop rbx    ; Get divisor (right operand)")
        code.append("    pop rax    ; Get dividend (left operand)")
        code.append("    xor rdx, rdx  ; Clear rdx for division")
        code.append("    idiv rbx      ; rax = rax / rbx, rdx = remainder")
        code.append("    push rax   ; Push result")
        return code

    def _generate_power(self, left_code, right_code):
        code = []
        # Simple approach: only support integer exponents
        # Right operand first (will end up second on the stack)
        code.extend(right_code)
        # Left operand
        code.extend(left_code)
        
        # Generate a loop to calculate power
        code.append("    pop rcx    ; Get exponent (right operand)")
        code.append("    pop rax    ; Get base (left operand)")
        code.append("    mov rbx, 1  ; Initialize result to 1")
        
        # Check if exponent is 0
        temp_label = f"power_loop_{self.temp_counter}"
        end_label = f"power_end_{self.temp_counter}"
        self.temp_counter += 1
        
        code.append("    cmp rcx, 0")
        code.append(f"    je {end_label}")
        
        # Loop to calculate power
        code.append(f"{temp_label}:")
        code.append("    imul rbx, rax  ; result *= base")
        code.append("    dec rcx        ; exponent--")
        code.append("    jnz " + temp_label)
        code.append(f"{end_label}:")
        code.append("    push rbx   ; Push result")
        
        return code

    def compile_expr(self, node):
        return self.generate_code(node)

    def compile(self, ast):
        # Start with NASM header and setup
        asm_header = [
            "; Generated NASM Assembly Code for Windows x64",
            "global main",
            "extern ExitProcess",
            "extern printf",
            "",
            "section .data",
            '    format db "%d", 10, 0  ; Format string for printf',
            "",
            "section .text",
            "main:",
            "    ; Initialize stack frame",
            "    push rbp",
            "    mov rbp, rsp",
            "    sub rsp, 32  ; Shadow space for Win64 calling convention",
            ""
        ]
        
        # Add the expression computation
        expr_code = self.compile_expr(ast)
        
        # Add the printf and exit code
        asm_footer = [
            "    ; Prepare for printf (Windows x64 calling convention)",
            "    pop rcx      ; First argument - the value to print",
            "    lea rdx, [format]  ; Second argument - format string",
            "    xor r8, r8   ; Clear other arguments",
            "    xor r9, r9",
            "    call printf",
            "",
            "    ; Exit program",
            "    xor rcx, rcx  ; Exit code 0",
            "    call ExitProcess",
        ]
        
        # Combine all parts
        self.asm_code = asm_header + expr_code + asm_footer
        return self.asm_code


def convert_to_assembly(expression, output_file="output.asm"):
    try:
        parser = Parser(expression)
        ast = parser.parse()
        
        compiler = Compiler()
        asm_code = compiler.compile(ast)
        
        # Write to file - explicitly use newlines to ensure proper formatting
        with open(output_file, "w", newline='\n') as f:
            for line in asm_code:
                f.write(line + '\n')
        
        print(f"Assembly code has been written to {output_file}")
        print("\nCompilation instructions:")
        print("1. Make sure you have NASM installed and in your PATH")
        print("2. Compile with: nasm -f win64 output.asm -o output.obj")
        print("3. Link with: link output.obj /subsystem:console /entry:main /LARGEADDRESSAWARE:NO")
        print("4. Run with: output.exe")
        
        return asm_code
        
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        expression = sys.argv[1]
    else:
        expression = input("Enter a mathematical expression: ")
    
    output_file = "output.asm"
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    convert_to_assembly(expression, output_file)