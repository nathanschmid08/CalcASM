#!/usr/bin/env python3
"""
Mathematical Expression Calculator with Assembly Code Generation
GUI Interface using Tkinter with Dark Theme
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
from math_to_assembly import Parser, Compiler, convert_to_assembly

class CalculatorApp:
    def __init__(self, root):
        # Dark theme colors
        self.bg_dark = "#2c2c2c"
        self.fg_light = "#e0e0e0"
        self.button_bg = "#3c3c3c"
        self.button_fg = "#e0e0e0"
        self.entry_bg = "#383838"
        self.entry_fg = "#ffffff"
        self.highlight_color = "#505050"
        self.code_color = "#d580ff"
        
        self.root = root
        self.root.title("CalcASM ")
        self.root.geometry("900x700")
        self.root.configure(bg=self.bg_dark)

        if hasattr(sys, "_MEIPASS"):
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        
        self.root.iconbitmap(icon_path)  # Icon setzen
        
        # Stelle sicher, dass das Fenster nicht zu klein wird
        self.root.minsize(800, 600)
        
        # Hauptframe
        main_frame = tk.Frame(root, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Oberer Bereich: Rechner
        calculator_frame = tk.LabelFrame(main_frame, text="Calculator", bg=self.bg_dark, 
                                       font=("Arial", 12), fg=self.fg_light)
        calculator_frame.pack(fill=tk.BOTH, padx=5, pady=5, ipady=5)
        
        # Anzeige für den mathematischen Ausdruck
        self.display_var = tk.StringVar()
        display_entry = tk.Entry(calculator_frame, textvariable=self.display_var, 
                              font=("Courier", 16), bd=10, relief=tk.RIDGE, justify=tk.RIGHT,
                              bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.fg_light)
        display_entry.pack(fill=tk.X, padx=10, pady=10)
        
        # Tasten-Grid für den Taschenrechner
        buttons_frame = tk.Frame(calculator_frame, bg=self.bg_dark)
        buttons_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Definiere Tasten
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3), ('C', 0, 4),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3), ('(', 1, 4),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3), (')', 2, 4),
            ('0', 3, 0), ('.', 3, 1), ('^', 3, 2), ('+', 3, 3), ('Convert', 3, 4)
        ]
        
        # Erstelle Tasten
        for (text, row, col) in buttons:
            button = tk.Button(buttons_frame, text=text, font=("Arial", 14 if text != "Convert" else 10), 
                           width=5, height=2, bg=self.button_bg, fg=self.button_fg,
                           activebackground=self.highlight_color, activeforeground=self.fg_light,
                           command=lambda t=text: self.button_click(t) if t != "Convert" else self.convert_expression())
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Konfiguriere gleichmässige Grösse für Tasten
        for i in range(5):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.rowconfigure(i, weight=1)
            
        # Konvertierungsoptionen
        convert_frame = tk.Frame(calculator_frame, bg=self.bg_dark)
        convert_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.output_file_var = tk.StringVar(value="output.asm")
        tk.Label(convert_frame, text="Output File:", bg=self.bg_dark, font=("Arial", 10), 
               fg=self.fg_light).pack(side=tk.LEFT, padx=5)
        tk.Entry(convert_frame, textvariable=self.output_file_var, width=20,
              bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.fg_light).pack(side=tk.LEFT, padx=5)
        
        # Unterer Bereich: Assembly-Code-Anzeige
        asm_frame = tk.LabelFrame(main_frame, text="Generated Assembly Code", bg=self.bg_dark, 
                                font=("Arial", 12), fg=self.fg_light)
        asm_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Textfeld für Assembly-Code
        self.asm_display = scrolledtext.ScrolledText(asm_frame, font=("Courier", 12), wrap=tk.WORD, 
                                                  bg=self.entry_bg, fg=self.code_color, 
                                                  insertbackground=self.fg_light)
        self.asm_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Statusleiste
        status_frame = tk.Frame(main_frame, bg=self.bg_dark, relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5)
        
        self.status_var = tk.StringVar(value="Bereit")
        status_label = tk.Label(status_frame, textvariable=self.status_var, bg=self.bg_dark, 
                              fg=self.fg_light, anchor=tk.W)
        status_label.pack(fill=tk.X, padx=5, pady=2)
        
    def button_click(self, text):
        if text == 'C':
            # Clear display
            self.display_var.set("")
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