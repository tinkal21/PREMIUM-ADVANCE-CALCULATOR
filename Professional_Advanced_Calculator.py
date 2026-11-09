import tkinter as tk
from tkinter import ttk
import math

# ==============================
# PREMIUM ADVANCED CALCULATOR
# ==============================

root = tk.Tk()
root.title("Premium Advanced Calculator")
root.geometry("1000x750")
root.configure(bg="#151922")
root.minsize(850, 650)

BG = "#151922"
DISPLAY_BG = "#202735"
BUTTON_BG = "#293344"
SCI_BG = "#35445C"
ORANGE = "#FF9500"
WHITE = "#FFFFFF"

expression = tk.StringVar(value="")

# Main heading
heading = tk.Label(
    root,
    text="PREMIUM ADVANCED CALCULATOR",
    font=("Arial", 21, "bold"),
    bg=BG,
    fg=ORANGE
)
heading.pack(pady=15)

# Display
display = tk.Entry(
    root,
    textvariable=expression,
    font=("Arial", 27),
    bg=DISPLAY_BG,
    fg=WHITE,
    insertbackground=WHITE,
    justify="right",
    bd=0
)
display.pack(fill="x", padx=20, ipady=18)

# Main frame
main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

# Button click function
def button_click(value):
    expression.set(expression.get() + str(value))

def clear():
    expression.set("")

def backspace():
    expression.set(expression.get()[:-1])

def calculate():
    try:
        result = eval(
            expression.get(),
            {"__builtins__": {}},
            {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "log": math.log10,
                "pi": math.pi,
                "e": math.e,
                "factorial": math.factorial
            }
        )
        with open("history.txt", "a", encoding="utf-8") as file:
            file.write(f"{expression.get()} = {round(result, 4)}\n")
            save_history(expression.get(), round(result, 4))

        expression.set(str(round(result, 10)))

    except Exception:
        expression.set("Error")

# Button design
def create_button(parent, text, command, color=BUTTON_BG):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 15, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=ORANGE,
        activeforeground=WHITE,
        bd=0,
        relief="flat",
        cursor="hand2"
    )

# Keyboard support
def keyboard_input(event):
    key = event.keysym
    char = event.char

    # When the display Entry has focus, let Tkinter handle normal typing
    # and Backspace so characters are not inserted twice.
    if event.widget == display:
        if key == "Return":
            calculate()
            return "break"
        elif key == "Escape":
            clear()
            return "break"
        return

    # Keep keyboard shortcuts available when the calculator window
    # (rather than the display Entry) has focus.
    if char in "0123456789.+-*/()":
        button_click(char)
        return "break"
    elif key == "Return":
        calculate()
        return "break"
    elif key == "BackSpace":
        backspace()
        return "break"
    elif key == "Escape":
        clear()
        return "break"

root.bind("<Key>", keyboard_input)
# ==============================
# SCIENTIFIC CALCULATOR BUTTONS
# ==============================

buttons = [
    ["7", "8", "9", "/", "sin"],
    ["4", "5", "6", "*", "cos"],
    ["1", "2", "3", "-", "tan"],
    ["0", ".", "(", ")", "+"],
    ["√", "log", "π", "e", "x²"],
    ["C", "DEL", "=", "!", "%"]
]

def scientific_click(value):

    if value == "C":
        clear()

    elif value == "DEL":
        backspace()

    elif value == "=":
        calculate()

    elif value == "√":
        button_click("sqrt(")

    elif value == "π":
        button_click("pi")

    elif value == "x²":
        button_click("**2")

    elif value == "!":
        button_click("factorial(")

    elif value == "%":
        button_click("/100")

    elif value in ["sin", "cos", "tan", "log"]:
        button_click(value + "(")

    elif value == "e":
        button_click("e")

    else:
        button_click(value)


# Create scientific button grid
for r, row in enumerate(buttons):
    for c, value in enumerate(row):

        color = ORANGE if value in ["=", "+", "-", "*", "/"] else (
            SCI_BG if value in ["sin", "cos", "tan", "log", "√", "π", "e", "x²", "!"] else BUTTON_BG
        )

        btn = create_button(
            main_frame,
            value,
            lambda v=value: scientific_click(v),
            color
        )

        btn.grid(
            row=r,
            column=c,
            padx=5,
            pady=5,
            sticky="nsew",
            ipadx=5,
            ipady=15
        )

for i in range(5):
    main_frame.grid_columnconfigure(i, weight=1)

for i in range(6):
    main_frame.grid_rowconfigure(i, weight=1)


# ==============================
# START APPLICATION
# ==============================

# ==================================
# FINANCE CALCULATOR - EMI AND LOAN
# ==================================

def open_finance():

    finance = tk.Toplevel(root)
    finance.title("Premium Finance Calculator")
    finance.geometry("550x600")
    finance.configure(bg=BG)

    title = tk.Label(
        finance,
        text="FINANCE CALCULATOR",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=ORANGE
    )
    title.pack(pady=15)

    notebook = ttk.Notebook(finance)
    notebook.pack(fill="both", expand=True, padx=15, pady=15)

    # EMI TAB
    emi_tab = tk.Frame(notebook, bg=BG)
    notebook.add(emi_tab, text="EMI Calculator")

    # LOAN TAB
    loan_tab = tk.Frame(notebook, bg=BG)
    notebook.add(loan_tab, text="Loan Calculator")

    def make_field(parent, label):
        tk.Label(
            parent,
            text=label,
            font=("Arial", 12, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(pady=(12, 3))

        entry = tk.Entry(
            parent,
            font=("Arial", 14),
            justify="center",
            bg=DISPLAY_BG,
            fg=WHITE,
            insertbackground=WHITE
        )
        entry.pack(ipady=7, padx=40, fill="x")
        return entry

    # EMI INPUTS
    tk.Label(
        emi_tab, text="Calculate Your Monthly EMI",
        font=("Arial", 15, "bold"),
        bg=BG, fg=ORANGE
    ).pack(pady=10)

    emi_amount = make_field(emi_tab, "Loan Amount (₹)")
    emi_rate = make_field(emi_tab, "Annual Interest Rate (%)")
    emi_years = make_field(emi_tab, "Loan Tenure (Years)")

    emi_result = tk.Label(
        emi_tab, text="Monthly EMI: ₹0",
        font=("Arial", 15, "bold"),
        bg=BG, fg=ORANGE
    )
    emi_result.pack(pady=15)

    emi_details = tk.Label(
        emi_tab, text="Total Interest: ₹0\nTotal Payment: ₹0",
        font=("Arial", 12),
        bg=BG, fg=WHITE
    )
    emi_details.pack(pady=5)

    def calculate_emi():
        try:
            p = float(emi_amount.get())
            annual_rate = float(emi_rate.get())
            years = float(emi_years.get())

            if p <= 0 or annual_rate < 0 or years <= 0:
                raise ValueError

            r = annual_rate / 1200
            n = years * 12

            if r == 0:
                emi = p / n
            else:
                emi = p * r * (1+r)**n / ((1+r)**n - 1)

            total = emi * n
            interest = total - p

            emi_result.config(
                text=f"Monthly EMI: ₹{emi:,.2f}"
            )

            emi_details.config(
                text=f"Total Interest: ₹{interest:,.2f}\n"
                     f"Total Payment: ₹{total:,.2f}"
            )

        except ValueError:
            emi_result.config(text="Please enter valid values")
            emi_details.config(text="")

    tk.Button(
        emi_tab,
        text="CALCULATE EMI",
        command=calculate_emi,
        bg=ORANGE,
        fg=WHITE,
        font=("Arial", 13, "bold"),
        bd=0
    ).pack(pady=12, ipadx=25, ipady=8)

    # LOAN TAB
    tk.Label(
        loan_tab, text="Loan Calculator",
        font=("Arial", 15, "bold"),
        bg=BG, fg=ORANGE
    ).pack(pady=10)

    loan_amount = make_field(loan_tab, "Loan Amount (₹)")
    loan_rate = make_field(loan_tab, "Interest Rate (%)")
    loan_years = make_field(loan_tab, "Loan Period (Years)")

    loan_result = tk.Label(
        loan_tab,
        text="Enter loan details",
        font=("Arial", 13, "bold"),
        bg=BG, fg=ORANGE
    )
    loan_result.pack(pady=15)

    def calculate_loan():
        try:
            p = float(loan_amount.get())
            rate = float(loan_rate.get())
            years = float(loan_years.get())

            if p <= 0 or rate < 0 or years <= 0:
                raise ValueError

            monthly_rate = rate / 1200
            months = years * 12

            if monthly_rate == 0:
                emi = p / months
            else:
                emi = (
                    p * monthly_rate *
                    (1 + monthly_rate)**months
                    / ((1 + monthly_rate)**months - 1)
                )

            total = emi * months
            interest = total - p

            loan_result.config(
                text=f"Monthly EMI: ₹{emi:,.2f}\n\n"
                     f"Principal: ₹{p:,.2f}\n"
                     f"Interest: ₹{interest:,.2f}\n"
                     f"Total Repayment: ₹{total:,.2f}"
            )

        except ValueError:
            loan_result.config(text="Please enter valid values")

    tk.Button(
        loan_tab,
        text="CALCULATE LOAN",
        command=calculate_loan,
        bg=ORANGE,
        fg=WHITE,
        font=("Arial", 13, "bold"),
        bd=0
    ).pack(pady=12, ipadx=25, ipady=8)


# FINANCE BUTTON
finance_button = create_button(
    main_frame,
    "FINANCE CALCULATOR  |  EMI & LOAN",
    open_finance,
    ORANGE
)

finance_button.grid(
    row=6,
    column=0,
    columnspan=5,
    padx=5,
    pady=10,
    sticky="nsew",
    ipady=10
)

# START APPLICATION
# ==================================
# PART 4 - GST CALCULATOR
# ==================================

def open_gst():

    gst_window = tk.Toplevel(root)
    gst_window.title("Premium GST Calculator")
    gst_window.geometry("500x600")
    gst_window.configure(bg=BG)

    tk.Label(
        gst_window,
        text="GST CALCULATOR",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=ORANGE
    ).pack(pady=20)

    # Amount
    tk.Label(
        gst_window,
        text="₹ ENTER AMOUNT",
        font=("Arial", 13, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(pady=5)

    amount_entry = tk.Entry(
        gst_window,
        font=("Arial", 16),
        justify="center",
        bg=DISPLAY_BG,
        fg=WHITE,
        insertbackground=WHITE
    )
    amount_entry.pack(ipady=8, padx=50, fill="x")

    # GST Rate
    tk.Label(
        gst_window,
        text="Select GST Rate",
        font=("Arial", 13, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(pady=12)

    gst_rate = tk.StringVar(value="18")

    rate_box = ttk.Combobox(
        gst_window,
        textvariable=gst_rate,
        values=["5", "12", "18", "28"],
        font=("Arial", 14),
        state="readonly"
    )
    rate_box.pack(ipady=5)

    # GST Type
    gst_type = tk.StringVar(value="Exclusive")

    tk.Label(
        gst_window,
        text="GST Type",
        font=("Arial", 13, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(pady=12)

    tk.Radiobutton(
        gst_window,
        text="Exclusive (Add GST)",
        variable=gst_type,
        value="Exclusive",
        bg=BG,
        fg=WHITE,
        selectcolor=DISPLAY_BG
    ).pack()

    tk.Radiobutton(
        gst_window,
        text="Inclusive (GST Already Included)",
        variable=gst_type,
        value="Inclusive",
        bg=BG,
        fg=WHITE,
        selectcolor=DISPLAY_BG
    ).pack()

    # Result
    result_label = tk.Label(
        gst_window,
        text="GST Result Will Appear Here",
        font=("Arial", 13, "bold"),
        bg=BG,
        fg=ORANGE,
        justify="left"
    )
    result_label.pack(pady=25)

    def calculate_gst():
        try:
            amount = float(amount_entry.get())
            rate = float(gst_rate.get())

            if amount < 0:
                raise ValueError

            if gst_type.get() == "Exclusive":
                gst = amount * rate / 100
                total = amount + gst
                base = amount
            else:
                base = amount / (1 + rate / 100)
                gst = amount - base
                total = amount

            result_label.config(
                text=(
                    f"Original Amount: ₹{base:,.2f}\n"
                    f"GST Amount: ₹{gst:,.2f}\n"
                    f"Total Amount: ₹{total:,.2f}"
                )
            )

        except ValueError:
            result_label.config(
                text="Please enter a valid amount!"
            )

    tk.Button(
        gst_window,
        text="CALCULATE GST",
        command=calculate_gst,
        bg=ORANGE,
        fg=WHITE,
        font=("Arial", 14, "bold"),
        bd=0,
        cursor="hand2"
    ).pack(pady=15, ipadx=25, ipady=10)


# GST BUTTON
gst_button = create_button(
    main_frame,
    "GST CALCULATOR",
    open_gst,
    ORANGE
)

gst_button.grid(
    row=7,
    column=0,
    columnspan=5,
    padx=5,
    pady=10,
    sticky="nsew",
    ipady=10
)

# START APPLICATION
# ==================================
# PART 5 - INTEREST & CGST/SGST
# ==================================

def open_interest():

    win = tk.Toplevel(root)
    win.title("Interest Calculator")
    win.geometry("550x650")
    win.configure(bg=BG)

    tk.Label(
        win,
        text="INTEREST CALCULATOR",
        font=("Arial", 20, "bold"),
        bg=BG, fg=ORANGE
    ).pack(pady=15)

    tabs = ttk.Notebook(win)
    tabs.pack(fill="both", expand=True, padx=12, pady=12)

    simple_tab = tk.Frame(tabs, bg=BG)
    compound_tab = tk.Frame(tabs, bg=BG)
    gst_tab = tk.Frame(tabs, bg=BG)

    tabs.add(simple_tab, text="Simple Interest")
    tabs.add(compound_tab, text="Compound Interest")
    tabs.add(gst_tab, text="CGST + SGST")

    def make_input(parent, label):
        tk.Label(
            parent, text=label,
            font=("Arial", 12, "bold"),
            bg=BG, fg=WHITE
        ).pack(pady=(12, 3))

        entry = tk.Entry(
            parent, font=("Arial", 14),
            justify="center",
            bg=DISPLAY_BG, fg=WHITE,
            insertbackground=WHITE
        )
        entry.pack(ipady=7, padx=35, fill="x")
        return entry

    # SIMPLE INTEREST

    p1 = make_input(simple_tab, "Principal Amount (₹)")
    r1 = make_input(simple_tab, "Annual Interest Rate (%)")
    t1 = make_input(simple_tab, "Time (Years)")

    result1 = tk.Label(
        simple_tab, text="Result will appear here",
        bg=BG, fg=ORANGE,
        font=("Arial", 13, "bold")
    )
    result1.pack(pady=15)

    def simple_interest():
        try:
            p = float(p1.get())
            r = float(r1.get())
            t = float(t1.get())

            if p < 0 or r < 0 or t < 0:
                raise ValueError

            interest = (p * r * t) / 100
            total = p + interest

            result1.config(
                text=f"Interest: ₹{interest:,.2f}\n"
                     f"Total Amount: ₹{total:,.2f}"
            )
        except ValueError:
            result1.config(text="Enter valid values!")

    tk.Button(
        simple_tab, text="CALCULATE SIMPLE INTEREST",
        command=simple_interest,
        bg=ORANGE, fg=WHITE,
        font=("Arial", 12, "bold"), bd=0
    ).pack(pady=10, ipadx=12, ipady=8)

    # COMPOUND INTEREST

    p2 = make_input(compound_tab, "Principal Amount (₹)")
    r2 = make_input(compound_tab, "Annual Interest Rate (%)")
    t2 = make_input(compound_tab, "Time (Years)")

    result2 = tk.Label(
        compound_tab, text="Result will appear here",
        bg=BG, fg=ORANGE,
        font=("Arial", 13, "bold")
    )
    result2.pack(pady=15)

    def compound_interest():
        try:
            p = float(p2.get())
            r = float(r2.get())
            t = float(t2.get())

            if p < 0 or r < 0 or t < 0:
                raise ValueError

            total = p * (1 + r / 100) ** t
            interest = total - p

            result2.config(
                text=f"Compound Interest: ₹{interest:,.2f}\n"
                     f"Total Amount: ₹{total:,.2f}"
            )
        except ValueError:
            result2.config(text="Enter valid values!")

    tk.Button(
        compound_tab, text="CALCULATE COMPOUND INTEREST",
        command=compound_interest,
        bg=ORANGE, fg=WHITE,
        font=("Arial", 12, "bold"), bd=0
    ).pack(pady=10, ipadx=12, ipady=8)

    # CGST AND SGST

    amount = make_input(gst_tab, "Original Amount (₹)")
    rate = make_input(gst_tab, "Total GST Rate (%)")

    result3 = tk.Label(
        gst_tab, text="CGST and SGST will appear here",
        bg=BG, fg=ORANGE,
        font=("Arial", 13, "bold")
    )
    result3.pack(pady=20)

    def calculate_split_gst():
        try:
            p = float(amount.get())
            r = float(rate.get())

            if p < 0 or r < 0:
                raise ValueError

            cgst = p * r / 200
            sgst = p * r / 200
            total = p + cgst + sgst

            result3.config(
                text=f"CGST: ₹{cgst:,.2f}\n"
                     f"SGST: ₹{sgst:,.2f}\n"
                     f"Total GST: ₹{cgst+sgst:,.2f}\n"
                     f"Final Amount: ₹{total:,.2f}"
            )
        except ValueError:
            result3.config(text="Enter valid values!")

    tk.Button(
        gst_tab, text="CALCULATE CGST + SGST",
        command=calculate_split_gst,
        bg=ORANGE, fg=WHITE,
        font=("Arial", 12, "bold"), bd=0
    ).pack(pady=10, ipadx=12, ipady=8)


# INTEREST BUTTON
interest_button = create_button(
    main_frame,
    "INTEREST & CGST / SGST",
    open_interest,
    ORANGE
)

interest_button.grid(
    row=8,
    column=0,
    columnspan=5,
    padx=5,
    pady=10,
    sticky="nsew",
    ipady=10
)

# START APPLICATION
# ==============================
# PART 6 - CALCULATION HISTORY
# ==============================

calculation_history = []

def save_history(expression, result):
    calculation_history.append(f"{expression} = {result}")

def open_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_window.geometry("450x500")
    history_window.configure(bg="#151922")

    tk.Label(
        history_window,
        text="CALCULATION HISTORY",
        font=("Arial", 18, "bold"),
        bg="#151922",
        fg="#FF9500"
    ).pack(pady=15)

    history_list = tk.Listbox(
        history_window,
        font=("Arial", 12),
        bg="#202735",
        fg="white",
        selectbackground="#FF9500",
        width=45,
        height=15
    )
    history_list.pack(padx=15, pady=10, fill="both", expand=True)

    for item in calculation_history:
        history_list.insert(tk.END, item)

    def clear_history():
        calculation_history.clear()
        history_list.delete(0, tk.END)

    tk.Button(
        history_window,
        text="CLEAR HISTORY",
        command=clear_history,
        bg="#FF9500",
        fg="white",
        font=("Arial", 11, "bold")
    ).pack(pady=15)

# HISTORY BUTTON
history_button = tk.Button(
    main_frame,
    text="CALCULATION HISTORY",
    command=open_history,
    bg="#FF9500",
    fg="white",
    font=("Arial", 11, "bold"),
    cursor="hand2"
)
history_button.grid(row=9, column=0, columnspan=5, sticky="ew", padx=5, pady=8)

root.mainloop() 