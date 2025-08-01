import tkinter as tk
from tkinter import filedialog, messagebox
import re
import subprocess
import os

OPCODES = {
    'NOP': 0x0, 'HLT': 0x1, 'ADD': 0x2, 'SUB': 0x3, 'AND': 0x4, 'OR':  0x5,
    'XOR': 0x6, 'NOR': 0x7, 'JMP': 0x8, 'RSH': 0x9, 'LSH': 0xA, 'LDI': 0xB,
    'ADI': 0xC, 'BRZ': 0xD, 'PLT': 0xE, 'SEG': 0xF
}

def print_list_hex(lst):
    for item in lst:
        print(hex(item))

def reg_num(r):
    return int(r.strip().replace("R", ""))

def assemble(asm):
    lines = []
    for raw_line in asm.splitlines():
        line = raw_line.split(";", 1)[0].strip()
        lines.append(line.upper())

    labels = {}
    pc = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        if ":" in line:
            label, rest = line.split(":", 1)
            labels[label.strip()] = pc
            line = rest.strip()
            if not line:
                continue
        pc += 2

    rom = [0x00, 0x00]
    for lineno, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        if ":" in line:
            _, line = line.split(":", 1)
            line = line.strip()
            if not line:
                continue

        parts = line.split()
        if not parts:
            continue

        instr = parts[0]
        opcode = OPCODES.get(instr)
        if opcode is None:
            raise ValueError(f"Line {lineno}: Unknown instruction: {instr}")

        try:
            operands_str = line[len(instr):].strip()
            operands = [op.strip() for op in operands_str.split(",")]

            if instr in ('ADD', 'SUB', 'AND', 'OR', 'XOR', 'NOR'):
                a, b, c = map(reg_num, operands)
                opval = (a << 8) | (b << 4) | c
            elif instr in ('RSH', 'LSH'):
                a = reg_num(operands[0])
                c = reg_num(operands[2])
                opval = (a << 8) | c
            elif instr in ('LDI', 'ADI'):
                r = reg_num(operands[0])
                val = int(operands[1], 0)
                opval = (r << 8) | (val & 0xFF)
            elif instr == 'SEG':
                r = reg_num(operands[0])
                opval = (r << 8)
            elif instr in ('JMP', 'BRZ'):
                arg = operands[0]
                addr = labels[arg] if arg in labels else int(arg, 0)
                opval = addr & 0xFF
            elif instr == 'PLT':
                x, y = map(reg_num, operands)
                opval = (x << 4) | y
            elif instr in ('NOP', 'HLT'):
                opval = 0
            else:
                raise ValueError(f"Line {lineno}: Invalid syntax")

            byte1 = (opcode << 4) | ((opval >> 8) & 0xF)
            byte2 = opval & 0xFF
            rom.append(byte1)
            rom.append(byte2)

        except Exception as e:
            raise ValueError(f"Line {lineno}: {e}")

    return rom

def convert_to_original_syntax():
    answer = messagebox.askyesno("Warning", "The converted code will no longer be executable in this IDE.\nDo you want to continue?")
    if not answer:
        return

    asm = editor.get("1.0", tk.END)
    lines = asm.splitlines()
    label_to_line = {}
    clean_lines = []
    current_line_num = 0
    for line in lines:
        line_no_comment = line.split(";", 1)[0].strip()
        if not line_no_comment:
            continue
        if ":" in line_no_comment:
            label, rest = line_no_comment.split(":", 1)
            label = label.strip().upper()
            rest = rest.strip()
            label_to_line[label] = current_line_num + 1
            if rest:
                clean_lines.append(rest)
                current_line_num += 1
        else:
            clean_lines.append(line_no_comment)
            current_line_num += 1

    jump_instrs = {'JMP', 'BRZ'}
    hex_pattern = re.compile(r'0x[0-9A-Fa-f]+')
    converted_lines = []

    for line in clean_lines:
        if not line.strip():
            continue
        parts = line.split()
        if not parts:
            continue
        instr = parts[0].upper()
        operands_str = line[len(parts[0]):].strip()
        operands = [op.strip() for op in operands_str.replace(',', ' ').split() if op]

        if instr in jump_instrs and len(operands) == 1:
            target = operands[0].upper()
            if target in label_to_line:
                operands[0] = str(label_to_line[target])
            else:
                try:
                    if target.startswith("0X"):
                        operands[0] = str(int(target, 16))
                    else:
                        int(target)
                except Exception:
                    pass

        for i, op in enumerate(operands):
            if hex_pattern.fullmatch(op):
                operands[i] = str(int(op, 16))

        new_line = instr + " " + " ".join(operands) if operands else instr
        converted_lines.append(new_line.lower())

    editor.delete("1.0", tk.END)
    editor.insert(tk.END, "\n".join(converted_lines))

def run_emulator(rom_bytes, speed, debug):
    import sys
    sys.path.insert(0, os.path.abspath(os.getcwd()))
    temp_dir = os.path.dirname(os.path.abspath(__file__))
    tempname = os.path.join(temp_dir, "_temp_emulator_runner.py")
    with open(tempname, "w") as f:
        emulator_path = os.path.abspath("RBC_V3.py")
        rom_data = "RBC_V3.ROM = [" + ", ".join(str(b) for b in rom_bytes) + "]"
        f.write(f"import RBC_V3\n{rom_data}\nRBC_V3.main({speed}, debug={debug})")
    python_exe = "python" if sys.platform.startswith("win") else "python3"
    subprocess.Popen([python_exe, tempname])
    print_list_hex(rom_bytes)

def on_assemble():
    try:
        asm = editor.get("1.0", tk.END)
        rom = assemble(asm)
        speed = float(speed_entry.get())
        run_emulator(rom, speed, debug_var.get())
    except Exception as e:
        messagebox.showerror("Assembly Error", str(e))

def on_open():
    path = filedialog.askopenfilename(filetypes=[("RBC Assembly", "*.RASM"), ("All files", "*")])
    if path:
        with open(path) as f:
            editor.delete("1.0", tk.END)
            editor.insert(tk.END, f.read())

def on_save():
    path = filedialog.asksaveasfilename(defaultextension=".RASM", filetypes=[("RBC Assembly", "*.RASM"), ("All files", "*")])
    if path:
        with open(path, "w") as f:
            f.write(editor.get("1.0", tk.END))

def update_line_numbers(event=None):
    editor_lines = editor.get("1.0", tk.END).splitlines()
    line_content = "\n".join(str(i + 1) for i in range(len(editor_lines)))
    line_numbers.config(state='normal')
    line_numbers.delete("1.0", tk.END)
    line_numbers.insert("1.0", line_content)
    line_numbers.config(state='disabled')

root = tk.Tk()
root.title("RBC v3 IDE")

line_numbers = tk.Text(root, width=4, padx=5, takefocus=0, border=0, background='lightgray', state='disabled')
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

editor = tk.Text(root, wrap=tk.NONE, font=("Courier", 12), yscrollcommand=scrollbar.set)
editor.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=editor.yview)

editor.bind("<KeyRelease>", update_line_numbers)
editor.bind("<MouseWheel>", update_line_numbers)
update_line_numbers()

toolbar = tk.Frame(root)
toolbar.pack()

tk.Button(toolbar, text="Assemble & Run", command=on_assemble).pack(side=tk.LEFT)
tk.Button(toolbar, text="Open", command=on_open).pack(side=tk.LEFT)
tk.Button(toolbar, text="Save", command=on_save).pack(side=tk.LEFT)

speed_label = tk.Label(toolbar, text="Speed (Hz):")
speed_label.pack(side=tk.LEFT)
speed_entry = tk.Entry(toolbar, width=6)
speed_entry.insert(0, "60.0")
speed_entry.pack(side=tk.LEFT)

debug_var = tk.BooleanVar()
debug_check = tk.Checkbutton(toolbar, text="Debug Mode", variable=debug_var)
debug_check.pack(side=tk.LEFT)

root.mainloop()
