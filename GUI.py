#!/usr/bin/env python3
"""
Mathematical Expression Calculator with Assembly Code Generation
GUI Interface using Tkinter
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
from math_to_assembly import Parser, Compiler, convert_to_assembly

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mathematischer Ausdruck zu Assembly Konverter")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Stelle sicher, dass das Fenster nicht zu klein wird
        self.root.minsize(800, 600)
        
        # Hauptframe
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Oberer Bereich: Rechner
        calculator_frame = tk.LabelFrame(main_frame, text="Taschenrechner", bg="#f0f0f0", font=("Arial", 12))
        calculator_frame.pack(fill=tk.BOTH, padx=5, pady=5, ipady=5)
        
        # Anzeige für den mathematischen Ausdruck
        self.display_var = tk.StringVar()
        display_entry = tk.Entry(calculator_frame, textvariable=self.display_var, 
                                font=("Courier", 16), bd=10, relief=tk.RIDGE, justify=tk.RIGHT)
        display_entry.pack(fill=tk.X, padx=10, pady=10)
        
        # Tasten-Grid für den Taschenrechner
        buttons_frame = tk.Frame(calculator_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Definiere Tasten
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3), ('C', 0, 4),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3), ('(', 1, 4),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3), (')', 2, 4),
            ('0', 3, 0), ('.', 3, 1), ('^', 3, 2), ('+', 3, 3), ('=', 3, 4)
        ]
        
        # Erstelle Tasten
        for (text, row, col) in buttons:
            button = tk.Button(buttons_frame, text=text, font=("Arial", 14), width=5, height=2,
                            command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Konfiguriere gleichmässige Grösse für Tasten
        for i in range(5):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.rowconfigure(i, weight=1)
            
        # Konvertierungsoptionen
        convert_frame = tk.Frame(calculator_frame, bg="#f0f0f0")
        convert_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.output_file_var = tk.StringVar(value="output.asm")
        tk.Label(convert_frame, text="Ausgabedatei:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Entry(convert_frame, textvariable=self.output_file_var, width=20).pack(side=tk.LEFT, padx=5)
        
        convert_button = tk.Button(convert_frame, text="Konvertieren", font=("Arial", 10), bg="#4CAF50", fg="white",
                                command=self.convert_expression)
        convert_button.pack(side=tk.RIGHT, padx=5)
        
        # Unterer Bereich: Assembly-Code-Anzeige
        asm_frame = tk.LabelFrame(main_frame, text="Generierter Assembly-Code", bg="#f0f0f0", font=("Arial", 12))
        asm_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Textfeld für Assembly-Code
        self.asm_display = scrolledtext.ScrolledText(asm_frame, font=("Courier", 12), wrap=tk.WORD)
        self.asm_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Statusleiste
        status_frame = tk.Frame(main_frame, bg="#f0f0f0", relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5)
        
        self.status_var = tk.StringVar(value="Bereit")
        status_label = tk.Label(status_frame, textvariable=self.status_var, bg="#f0f0f0", anchor=tk.W)
        status_label.pack(fill=tk.X, padx=5, pady=2)
        
    def button_click(self, text):
        if text == 'C':
            # Clear display
            self.display_var.set("")
        elif text == '=':
            # Calculate and convert
            self.convert_expression()
        else:
            # Append character to display
            current = self.display_var.get()
            self.display_var.set(current + text)
            
    def convert_expression(self):
        """Convert the expression to assembly and display the code"""
        expression = self.display_var.get()
        output_file = self.output_file_var.get()
        
        if not expression:
            messagebox.showwarning("Leerer Ausdruck", "Bitte gib einen mathematischen Ausdruck ein.")
            return
        
        try:
            # Parse expression
            parser = Parser(expression)
            ast = parser.parse()
            
            # Generate assembly code
            compiler = Compiler()
            asm_code = compiler.compile(ast)
            
            # Save to file
            try:
                with open(output_file, "w", newline='\n') as f:
                    for line in asm_code:
                        f.write(line + '\n')
                self.status_var.set(f"Assembly-Code wurde in {output_file} gespeichert")
            except Exception as e:
                self.status_var.set(f"Fehler beim Speichern: {str(e)}")
                
            # Display in text area
            self.asm_display.delete(1.0, tk.END)
            self.asm_display.insert(tk.END, "\n".join(asm_code))
            
            # Versuche auch das Ergebnis zu berechnen
            try:
                result = eval(expression)
                self.status_var.set(f"Ergebnis: {result} | Assembly-Code wurde gespeichert in {output_file}")
            except:
                pass
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Konvertierung: {str(e)}")
            self.status_var.set(f"Fehler: {str(e)}")
            self.asm_display.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()