import tkinter as tk


window = tk.Tk()
window.title("Two Pass Assembler")
window.geometry('600x400')

tk.Label(window, text="Enter Assembly Code Below:", font=("Helvetica", 14)).pack()
code_input = tk.Text(window, height=10, width=60)
code_input.pack()

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

symbol_table = {}


def update_output(text):
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state=tk.DISABLED)

def pass_one():
    global symbol_table
    symbol_table = {}
    code = code_input.get("1.0", "end-1c").splitlines()  # Get the input assembly code and split by lines
    location_counter = 0

  
    for line in code:
        line = line.strip()
        if line:  # Ignore empty lines
            parts = line.split()

            if parts[0] == "START":
                location_counter = int(parts[1])
                continue

          
            if len(parts) > 1 and parts[1] == "DATA":
                label = parts[0]
                symbol_table[label] = location_counter
                location_counter += 1
            elif parts[0] == "LOAD" or parts[0] == "STORE":
                location_counter += 1  # Instruction, move location counter
            else:
                # Label followed by instruction (e.g., 'LABEL: LOAD ALPHA')
                if ":" in parts[0]:
                    label = parts[0].replace(":", "")
                    symbol_table[label] = location_counter
                location_counter += 1

    output = "Pass One Complete: Processed symbol table:\n" + str(symbol_table)
    update_output(output)


def pass_two():
    if not symbol_table:
        update_output("Error: Run Pass One first!")
        return
    
    code = code_input.get("1.0", "end-1c").splitlines()
    machine_code = []

    for line in code:
        line = line.strip()
        if line:
            parts = line.split()

            if parts[0] == "START" or (len(parts) > 1 and parts[1] == "DATA"):
                continue

            
            if parts[0] == "LOAD":
                operand = parts[1]
                if operand in symbol_table:
                    machine_code.append(f"LOAD {symbol_table[operand]}")
                else:
                    machine_code.append("LOAD Unknown")
            elif parts[0] == "STORE":
                operand = parts[1]
                if operand in symbol_table:
                    machine_code.append(f"STORE {symbol_table[operand]}")
                else:
                    machine_code.append("STORE Unknown")
            else:
                machine_code.append("NOP") 

    output = "Pass Two Complete: Machine code:\n" + "\n".join(machine_code)
    update_output(output)

tk.Button(button_frame, text="Run Pass One", command=pass_one, bg="black", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Run Pass Two", command=pass_two, bg="black", fg="white", width=15).grid(row=0, column=1, padx=10)


output_box = tk.Text(window, height=5, width=60, state=tk.DISABLED)
output_box.pack(pady=10)


window.mainloop()
