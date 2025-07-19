import tkinter as tk

# Install required packages if not already installed

# Windows is below:
# pip install tk
# pip install ttk
# pip install math

#Linux (Debian)
# sudo apt-get install python3-tk
from tkinter import ttk, messagebox
import math

class FinancialCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Singapore Financial Calculator")
        self.geometry("900x700")
        self.configure(bg="#f0f9ff")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create tabs
        self.loan_tab = LoanCalculator(self.notebook)
        self.investment_tab = InvestmentCalculator(self.notebook)
        self.retirement_tab = RetirementCalculator(self.notebook)
        self.cpf_tab = CPFCalculator(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.loan_tab, text="Loan Calculator")
        self.notebook.add(self.investment_tab, text="Investment Growth")
        self.notebook.add(self.retirement_tab, text="Retirement Planning")
        self.notebook.add(self.cpf_tab, text="CPF Calculator")
        
        # Add disclaimer
        disclaimer = tk.Label(self, text="Disclaimer: This calculator provides estimates only. Actual results may vary. "
                                "Consult with licensed financial advisors for personalized advice.", 
                             bg="#f0f9ff", fg="#555555", wraplength=800, font=("Arial", 9))
        disclaimer.pack(side="bottom", pady=10)

    @staticmethod
    def format_currency(amount):
        """Format number as SGD currency"""
        if amount >= 0:
            return f"S${abs(amount):,.0f}"
        return f"-S${abs(amount):,.0f}"


class CalculatorTab(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.configure(bg="white")
        self.title = title
        
        # Title
        title_frame = tk.Frame(self, bg="white")
        title_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(title_frame, text=title, font=("Arial", 14, "bold"), 
                bg="white", fg="#0d47a1").pack(side="left")
        
        # Content container
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True, padx=20, pady=10)


class LoanCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent, "Loan Payment Calculator")
        self.create_widgets()
        
    def create_widgets(self):
        # Left panel - Inputs
        input_frame = tk.LabelFrame(self.container, text="Loan Details", bg="white", 
                                  font=("Arial", 10, "bold"), padx=10, pady=10)
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Loan type
        tk.Label(input_frame, text="Loan Type:", bg="white", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.loan_type = ttk.Combobox(input_frame, values=[
            "HDB Loan (2.6%)", "Bank Loan (Variable)", "Car Loan", "Personal Loan"
        ])
        self.loan_type.set("HDB Loan (2.6%)")
        self.loan_type.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Loan amount
        tk.Label(input_frame, text="Loan Amount (SGD):", bg="white", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.loan_amount = tk.Entry(input_frame)
        self.loan_amount.insert(0, "500000")
        self.loan_amount.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Interest rate
        tk.Label(input_frame, text="Interest Rate (%):", bg="white", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.loan_rate = tk.Entry(input_frame)
        self.loan_rate.insert(0, "3.5")
        self.loan_rate.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Loan term
        tk.Label(input_frame, text="Loan Term (Years):", bg="white", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.loan_term = tk.Entry(input_frame)
        self.loan_term.insert(0, "25")
        self.loan_term.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate", command=self.calculate).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Right panel - Results
        result_frame = tk.LabelFrame(self.container, text="Payment Summary", bg="white", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        result_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Results labels
        self.monthly_payment = tk.Label(result_frame, text="Monthly Payment: S$0", 
                                       bg="white", font=("Arial", 12))
        self.monthly_payment.pack(anchor="w", pady=10)
        
        self.total_payment = tk.Label(result_frame, text="Total Payment: S$0", bg="white")
        self.total_payment.pack(anchor="w", pady=10)
        
        self.total_interest = tk.Label(result_frame, text="Total Interest: S$0", 
                                     bg="white", fg="#d32f2f")
        self.total_interest.pack(anchor="w", pady=10)
    
    def calculate(self):
        try:
            principal = float(self.loan_amount.get())
            annual_rate = float(self.loan_rate.get())
            term = float(self.loan_term.get())
            
            monthly_rate = annual_rate / 100 / 12
            num_payments = term * 12
            
            if monthly_rate == 0:
                monthly_payment = principal / num_payments
            else:
                monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
                                ((1 + monthly_rate) ** num_payments - 1)
            
            total_payment = monthly_payment * num_payments
            total_interest = total_payment - principal
            
            self.monthly_payment.config(text=f"Monthly Payment: {FinancialCalculator.format_currency(monthly_payment)}")
            self.total_payment.config(text=f"Total Payment: {FinancialCalculator.format_currency(total_payment)}")
            self.total_interest.config(text=f"Total Interest: {FinancialCalculator.format_currency(total_interest)}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields")


class InvestmentCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent, "Investment Growth Calculator")
        self.create_widgets()
        
    def create_widgets(self):
        # Left panel - Inputs
        input_frame = tk.LabelFrame(self.container, text="Investment Details", bg="white", 
                                  font=("Arial", 10, "bold"), padx=10, pady=10)
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Initial investment
        tk.Label(input_frame, text="Initial Investment (SGD):", bg="white", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.initial_investment = tk.Entry(input_frame)
        self.initial_investment.insert(0, "10000")
        self.initial_investment.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Monthly contribution
        tk.Label(input_frame, text="Monthly Contribution (SGD):", bg="white", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.monthly_contribution = tk.Entry(input_frame)
        self.monthly_contribution.insert(0, "1000")
        self.monthly_contribution.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Expected return
        tk.Label(input_frame, text="Expected Annual Return (%):", bg="white", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.investment_rate = tk.Entry(input_frame)
        self.investment_rate.insert(0, "7")
        self.investment_rate.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Investment period
        tk.Label(input_frame, text="Investment Period (Years):", bg="white", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.investment_years = tk.Entry(input_frame)
        self.investment_years.insert(0, "20")
        self.investment_years.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate", command=self.calculate).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Right panel - Results
        result_frame = tk.LabelFrame(self.container, text="Investment Projection", bg="white", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        result_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Results labels
        self.final_value = tk.Label(result_frame, text="Final Value: S$0", 
                                   bg="white", font=("Arial", 12))
        self.final_value.pack(anchor="w", pady=10)
        
        self.total_contributions = tk.Label(result_frame, text="Total Contributions: S$0", bg="white")
        self.total_contributions.pack(anchor="w", pady=10)
        
        self.total_gains = tk.Label(result_frame, text="Total Gains: S$0", 
                                  bg="white", fg="#388e3c")
        self.total_gains.pack(anchor="w", pady=10)
    
    def calculate(self):
        try:
            initial = float(self.initial_investment.get())
            monthly = float(self.monthly_contribution.get())
            annual_rate = float(self.investment_rate.get())
            years = float(self.investment_years.get())
            
            monthly_rate = annual_rate / 100 / 12
            months = years * 12
            
            # Future value of initial investment
            future_initial = initial * (1 + monthly_rate) ** months
            
            # Future value of monthly contributions
            if monthly_rate == 0:
                future_monthly = monthly * months
            else:
                future_monthly = monthly * ((1 + monthly_rate) ** months - 1) / monthly_rate
            
            total_value = future_initial + future_monthly
            total_contributions = initial + (monthly * months)
            total_gains = total_value - total_contributions
            
            self.final_value.config(text=f"Final Value: {FinancialCalculator.format_currency(total_value)}")
            self.total_contributions.config(text=f"Total Contributions: {FinancialCalculator.format_currency(total_contributions)}")
            self.total_gains.config(text=f"Total Gains: {FinancialCalculator.format_currency(total_gains)}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields")


class RetirementCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent, "Retirement Planning Calculator")
        self.create_widgets()
        
    def create_widgets(self):
        # Left panel - Inputs
        input_frame = tk.LabelFrame(self.container, text="Retirement Details", bg="white", 
                                  font=("Arial", 10, "bold"), padx=10, pady=10)
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Age fields
        tk.Label(input_frame, text="Current Age:", bg="white", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.current_age = tk.Entry(input_frame)
        self.current_age.insert(0, "30")
        self.current_age.grid(row=0, column=1, sticky="ew", pady=5)
        
        tk.Label(input_frame, text="Retirement Age:", bg="white", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.retirement_age = tk.Entry(input_frame)
        self.retirement_age.insert(0, "65")
        self.retirement_age.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Current savings
        tk.Label(input_frame, text="Current Savings (SGD):", bg="white", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.current_savings = tk.Entry(input_frame)
        self.current_savings.insert(0, "50000")
        self.current_savings.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Monthly savings
        tk.Label(input_frame, text="Monthly Savings (SGD):", bg="white", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.monthly_savings = tk.Entry(input_frame)
        self.monthly_savings.insert(0, "2000")
        self.monthly_savings.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Expected return
        tk.Label(input_frame, text="Expected Return (%):", bg="white", anchor="w").grid(row=4, column=0, sticky="w", pady=5)
        self.expected_return = tk.Entry(input_frame)
        self.expected_return.insert(0, "6")
        self.expected_return.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Retirement income
        tk.Label(input_frame, text="Desired Monthly Income (SGD):", bg="white", anchor="w").grid(row=5, column=0, sticky="w", pady=5)
        self.retirement_income = tk.Entry(input_frame)
        self.retirement_income.insert(0, "4000")
        self.retirement_income.grid(row=5, column=1, sticky="ew", pady=5)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate", command=self.calculate).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Right panel - Results
        result_frame = tk.LabelFrame(self.container, text="Retirement Projection", bg="white", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        result_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Results labels
        self.years_to_retirement = tk.Label(result_frame, text="Years to Retirement: 0", bg="white")
        self.years_to_retirement.pack(anchor="w", pady=10)
        
        self.projected_savings = tk.Label(result_frame, text="Projected Savings: S$0", bg="white")
        self.projected_savings.pack(anchor="w", pady=10)
        
        self.required_amount = tk.Label(result_frame, text="Required Amount: S$0", bg="white")
        self.required_amount.pack(anchor="w", pady=10)
        
        self.shortfall = tk.Label(result_frame, text="Shortfall: S$0", bg="white", fg="#d32f2f")
        self.shortfall.pack(anchor="w", pady=10)
    
    def calculate(self):
        try:
            current_age = float(self.current_age.get())
            retirement_age = float(self.retirement_age.get())
            current_savings = float(self.current_savings.get())
            monthly_savings = float(self.monthly_savings.get())
            expected_return = float(self.expected_return.get())
            retirement_income = float(self.retirement_income.get())
            
            years_to_retirement = max(0, retirement_age - current_age)
            months = years_to_retirement * 12
            monthly_rate = expected_return / 100 / 12
            
            # Future value of current savings
            future_current = current_savings * (1 + monthly_rate) ** months
            
            # Future value of monthly savings
            if monthly_rate == 0:
                future_monthly = monthly_savings * months
            else:
                future_monthly = monthly_savings * ((1 + monthly_rate) ** months - 1) / monthly_rate
            
            total_at_retirement = future_current + future_monthly
            
            # Required amount (25x rule)
            required_amount = retirement_income * 12 * 25
            shortfall = required_amount - total_at_retirement
            
            self.years_to_retirement.config(text=f"Years to Retirement: {years_to_retirement:.0f}")
            self.projected_savings.config(text=f"Projected Savings: {FinancialCalculator.format_currency(total_at_retirement)}")
            self.required_amount.config(text=f"Required Amount: {FinancialCalculator.format_currency(required_amount)}")
            
            if shortfall > 0:
                self.shortfall.config(text=f"Shortfall: {FinancialCalculator.format_currency(shortfall)}", fg="#d32f2f")
            else:
                self.shortfall.config(text=f"Surplus: {FinancialCalculator.format_currency(-shortfall)}", fg="#388e3c")
                
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields")


class CPFCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent, "CPF Contribution Calculator")
        self.create_widgets()
        
    def create_widgets(self):
        # Left panel - Inputs
        input_frame = tk.LabelFrame(self.container, text="CPF Details", bg="white", 
                                  font=("Arial", 10, "bold"), padx=10, pady=10)
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Salary
        tk.Label(input_frame, text="Monthly Salary (SGD):", bg="white", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.salary = tk.Entry(input_frame)
        self.salary.insert(0, "5000")
        self.salary.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Age
        tk.Label(input_frame, text="Age:", bg="white", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.age = tk.Entry(input_frame)
        self.age.insert(0, "30")
        self.age.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Employee rate
        tk.Label(input_frame, text="Employee Contribution Rate (%):", bg="white", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.employee_rate = tk.Entry(input_frame)
        self.employee_rate.insert(0, "20")
        self.employee_rate.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Employer rate
        tk.Label(input_frame, text="Employer Contribution Rate (%):", bg="white", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.employer_rate = tk.Entry(input_frame)
        self.employer_rate.insert(0, "17")
        self.employer_rate.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate", command=self.calculate).grid(row=4, column=0, columnspan=2, pady=10)
        
        # CPF rates info
        cpf_info = tk.Label(input_frame, 
                           text="CPF Contribution Rates by Age (2024):\n"
                                "Age ≤35: Employee 20% + Employer 17% = 37%\n"
                                "Age 36-45: Employee 20% + Employer 16% = 36%\n"
                                "Age 46-55: Employee 20% + Employer 16% = 36%\n"
                                "Age 56-60: Employee 13% + Employer 13% = 26%\n"
                                "Age 61-65: Employee 7.5% + Employer 9% = 16.5%",
                           bg="#fff3e0", justify="left", anchor="w", padx=10, pady=10)
        cpf_info.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Right panel - Results
        result_frame = tk.LabelFrame(self.container, text="CPF Contributions", bg="white", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        result_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Results labels
        self.employee_contrib = tk.Label(result_frame, text="Employee Contribution: S$0", bg="white")
        self.employee_contrib.pack(anchor="w", pady=10)
        
        self.employer_contrib = tk.Label(result_frame, text="Employer Contribution: S$0", bg="white")
        self.employer_contrib.pack(anchor="w", pady=10)
        
        self.total_monthly = tk.Label(result_frame, text="Total Monthly: S$0", 
                                    bg="white", font=("Arial", 12))
        self.total_monthly.pack(anchor="w", pady=10)
        
        self.annual_contrib = tk.Label(result_frame, text="Annual Contribution: S$0", 
                                     bg="white", fg="#388e3c")
        self.annual_contrib.pack(anchor="w", pady=10)
    
    def calculate(self):
        try:
            salary = float(self.salary.get())
            employee_rate = float(self.employee_rate.get()) / 100
            employer_rate = float(self.employer_rate.get()) / 100
            
            employee_contrib = salary * employee_rate
            employer_contrib = salary * employer_rate
            total_monthly = employee_contrib + employer_contrib
            annual_contrib = total_monthly * 12
            
            self.employee_contrib.config(text=f"Employee Contribution: {FinancialCalculator.format_currency(employee_contrib)}")
            self.employer_contrib.config(text=f"Employer Contribution: {FinancialCalculator.format_currency(employer_contrib)}")
            self.total_monthly.config(text=f"Total Monthly: {FinancialCalculator.format_currency(total_monthly)}")
            self.annual_contrib.config(text=f"Annual Contribution: {FinancialCalculator.format_currency(annual_contrib)}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields")


if __name__ == "__main__":
    app = FinancialCalculator()
    app.mainloop()