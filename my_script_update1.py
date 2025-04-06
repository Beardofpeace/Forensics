import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os


class ForensicToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Forensic Tools Launcher")
        self.root.geometry("500x650")  # Increased height to accommodate new elements

        # Variables to store paths
        self.mft_input = tk.StringVar()
        self.mft_output = tk.StringVar()
        self.pe_input = tk.StringVar()
        self.pe_output = tk.StringVar()
        self.jl_input = tk.StringVar()
        self.jl_output = tk.StringVar()

        # Labels for success messages
        self.mft_success_label = None
        self.pe_success_label = None
        self.jl_success_label = None

        # Create GUI sections for each tool
        self.create_mft_section()
        self.create_pe_section()
        self.create_jl_section()

    def create_mft_section(self):
        mft_frame = tk.LabelFrame(self.root, text="MFTECmd", padx=10, pady=10)
        mft_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(mft_frame, text="Input File:").grid(row=0, column=0, sticky="w")
        tk.Entry(mft_frame, textvariable=self.mft_input, width=40).grid(row=0, column=1, padx=5)
        tk.Button(mft_frame, text="Browse", command=self.browse_mft_input).grid(row=0, column=2)

        tk.Label(mft_frame, text="Output Dir:").grid(row=1, column=0, sticky="w")
        tk.Entry(mft_frame, textvariable=self.mft_output, width=40).grid(row=1, column=1, padx=5)
        tk.Button(mft_frame, text="Browse", command=self.browse_mft_output).grid(row=1, column=2)

        tk.Button(mft_frame, text="Run MFTECmd", command=self.run_mft).grid(row=2, column=1, pady=5)

        # Success label (initially empty)
        self.mft_success_label = tk.Label(mft_frame, text="", fg="green")
        self.mft_success_label.grid(row=3, column=1, pady=5)

        # Open output folder button
        tk.Button(mft_frame, text="Open Output Folder", command=self.open_mft_output).grid(row=4, column=1, pady=5)

    def create_pe_section(self):
        pe_frame = tk.LabelFrame(self.root, text="PECmd", padx=10, pady=10)
        pe_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(pe_frame, text="Input File:").grid(row=0, column=0, sticky="w")
        tk.Entry(pe_frame, textvariable=self.pe_input, width=40).grid(row=0, column=1, padx=5)
        tk.Button(pe_frame, text="Browse", command=self.browse_pe_input).grid(row=0, column=2)

        tk.Label(pe_frame, text="Output Dir:").grid(row=1, column=0, sticky="w")
        tk.Entry(pe_frame, textvariable=self.pe_output, width=40).grid(row=1, column=1, padx=5)
        tk.Button(pe_frame, text="Browse", command=self.browse_pe_output).grid(row=1, column=2)

        tk.Button(pe_frame, text="Run PECmd", command=self.run_pe).grid(row=2, column=1, pady=5)

        # Success label (initially empty)
        self.pe_success_label = tk.Label(pe_frame, text="", fg="green")
        self.pe_success_label.grid(row=3, column=1, pady=5)

        # Open output folder button
        tk.Button(pe_frame, text="Open Output Folder", command=self.open_pe_output).grid(row=4, column=1, pady=5)

    def create_jl_section(self):
        jl_frame = tk.LabelFrame(self.root, text="JLECmd", padx=10, pady=10)
        jl_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(jl_frame, text="Input File:").grid(row=0, column=0, sticky="w")
        tk.Entry(jl_frame, textvariable=self.jl_input, width=40).grid(row=1, column=1, padx=5)
        tk.Button(jl_frame, text="Browse", command=self.browse_jl_input).grid(row=1, column=2)

        tk.Label(jl_frame, text="Output Dir:").grid(row=2, column=0, sticky="w")
        tk.Entry(jl_frame, textvariable=self.jl_output, width=40).grid(row=2, column=1, padx=5)
        tk.Button(jl_frame, text="Browse", command=self.browse_jl_output).grid(row=2, column=2)

        tk.Button(jl_frame, text="Run JLECmd", command=self.run_jl).grid(row=3, column=1, pady=5)

        # Success label (initially empty)
        self.jl_success_label = tk.Label(jl_frame, text="", fg="green")
        self.jl_success_label.grid(row=4, column=1, pady=5)

        # Open output folder button
        tk.Button(jl_frame, text="Open Output Folder", command=self.open_jl_output).grid(row=5, column=1, pady=5)

    # Browse functions (unchanged)
    def browse_mft_input(self):
        filename = filedialog.askopenfilename(title="Select MFT File")
        if filename:
            self.mft_input.set(filename)

    def browse_mft_output(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.mft_output.set(directory)

    def browse_pe_input(self):
        filename = filedialog.askopenfilename(title="Select Prefetch File")
        if filename:
            self.pe_input.set(filename)

    def browse_pe_output(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.pe_output.set(directory)

    def browse_jl_input(self):
        filename = filedialog.askopenfilename(title="Select JumpList File")
        if filename:
            self.jl_input.set(filename)

    def browse_jl_output(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.jl_output.set(directory)

    # Run commands (modified to update success labels)
    def run_mft(self):
        if not self.mft_input.get() or not self.mft_output.get():
            messagebox.showerror("Error", "Please select both input file and output directory for MFTECmd")
            return

        cmd = f'MFTECmd.exe -f "{self.mft_input.get()}" --csv "{self.mft_output.get()}"'
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.mft_success_label.config(text="Success")  # Update label to "Success" in green
            messagebox.showinfo("Success", "MFTECmd completed successfully")
        except subprocess.CalledProcessError as e:
            self.mft_success_label.config(text="")  # Clear label on failure
            messagebox.showerror("Error", f"MFTECmd failed: {e}")

    def run_pe(self):
        if not self.pe_input.get() or not self.pe_output.get():
            messagebox.showerror("Error", "Please select both input file and output directory for PECmd")
            return

        cmd = f'PECmd.exe -f "{self.pe_input.get()}" --csv "{self.pe_output.get()}"'
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.pe_success_label.config(text="Success")  # Update label to "Success" in green
            messagebox.showinfo("Success", "PECmd completed successfully")
        except subprocess.CalledProcessError as e:
            self.pe_success_label.config(text="")  # Clear label on failure
            messagebox.showerror("Error", f"PECmd failed: {e}")

    def run_jl(self):
        if not self.jl_input.get() or not self.jl_output.get():
            messagebox.showerror("Error", "Please select both input file and output directory for JLECmd")
            return

        cmd = f'JLECmd.exe -f "{self.jl_input.get()}" --csv "{self.jl_output.get()}"'
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.jl_success_label.config(text="Success")  # Update label to "Success" in green
            messagebox.showinfo("Success", "JLECmd completed successfully")
        except subprocess.CalledProcessError as e:
            self.jl_success_label.config(text="")  # Clear label on failure
            messagebox.showerror("Error", f"JLECmd failed: {e}")

    # New methods to open output folders
    def open_mft_output(self):
        if self.mft_output.get():
            os.startfile(self.mft_output.get())
        else:
            messagebox.showwarning("Warning", "No output directory selected for MFTECmd")

    def open_pe_output(self):
        if self.pe_output.get():
            os.startfile(self.pe_output.get())
        else:
            messagebox.showwarning("Warning", "No output directory selected for PECmd")

    def open_jl_output(self):
        if self.jl_output.get():
            os.startfile(self.jl_output.get())
        else:
            messagebox.showwarning("Warning", "No output directory selected for JLECmd")


def main():
    root = tk.Tk()
    app = ForensicToolsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()