import tkinter as tk
from tkinter import ttk
import pandas as pd
import random
import matplotlib.pyplot as plt

class ComplaintPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Complaint Portal")
        self.root.geometry("1000x800") 
        
        
        self.complaint = {
            "Software completely stopped working": 5,
            "Software has minor bugs": 2,
            "Software needs improvement or adjustments": 1,
            "Software is crashing": 3,
            "Software does not meet product requirements": 4
        }
        self.industry = ["Finance", "Manufacturing", "Service", "Government", "Power/Electricity", "Education", "Medical", "Other"]
        self.time = {"1 week": 5, "1 month": 4, "3 months": 3, "6 months": 2, "1 year": 1}

        # Initialize the DataFrame with random data
        self.generate_random_data()
        self.generate_random_service_survey_data()
        self.show_main_screen()


    def generate_random_data(self):
        complaint = {"Software completely stopped working": 5, "Software has minor bugs": 2,
                     "Software needs improvement or adjustments": 1, "Software is crashing": 3,
                     "Software does not meet product requirements": 4}
        industry = ["Finance", "Manufacturing", "Service", "Government", "Power/Electricity", "Education", "Medical",
                    "Other"]
        time = {"1 week": 5, "1 month": 4, "3 months": 3, "6 months": 2, "1 year": 1}
        data = {
            "Client Name": ["Company" + str(random.randint(200, 999)) for _ in range(50)],
            "Complaint Catergory": [random.choice(list(complaint.keys())) for _ in range(50)],
            "Industry": [random.choice(industry) for _ in range(50)],
            "Resolved By": [random.choice(list(time.keys())) for _ in range(50)]
        }
        data["Complaint Severity Score"] = [complaint[category] * time[resolved_by] for category, resolved_by in
                                            zip(data["Complaint Catergory"], data["Resolved By"])]
        self.df = pd.DataFrame(data)

    def show_main_screen(self):
        self.clear_screen()

        tk.Button(self.root, text="Employee Login", command=self.show_login_screen).pack(pady=10)
        tk.Button(self.root, text="File a Complaint", command=self.show_file_complaint_screen).pack(pady=10)
        tk.Button(self.root, text="Service Survey", command=self.show_product_survey_screen).pack(pady=10)
   
    def show_product_survey_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Product Survey", font=("Helvetica", 16)).pack(pady=10)

        satisfaction_var = tk.StringVar()
        tk.Label(self.root, text="Were you satisfied with the delivered service").pack()
        satisfaction_options = ttk.Combobox(self.root, textvariable=satisfaction_var, values=["Yes", "No"])
        satisfaction_options.pack()

        complaint_filed_var = tk.StringVar()
        tk.Label(self.root, text="Did you file a complaint").pack()
        complaint_filed_options = ttk.Combobox(self.root, textvariable=complaint_filed_var, values=["Yes", "No"])
        complaint_filed_options.pack()

        score_var = tk.IntVar()
        tk.Label(self.root, text="Rate your experience with us from 1 to 5").pack()
        score_options = ttk.Combobox(self.root, textvariable=score_var, values=["1", "2", "3", "4", "5"])
        score_options.pack()

        def submit_product_survey():
            new_survey_data = {
                "Satisfaction": satisfaction_var.get(),
                "Complaint Filed": complaint_filed_var.get(),
                "Score": score_var.get()
            }
            self.service_survey_df = pd.concat([self.service_survey_df, pd.DataFrame([new_survey_data])], ignore_index=True)

            self.show_main_screen()

        tk.Button(self.root, text="Done", command=submit_product_survey).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_screen).pack(pady=10)

    def show_data_options_screen(self):
        self.clear_screen()

        tk.Button(self.root, text="Show Complaint Data", command=self.show_complaint_chart).pack(pady=10)
        tk.Button(self.root, text="Show Service Survey Data", command=self.show_service_survey_chart).pack(pady=10)
        tk.Button(self.root, text="Product Survey", command=self.show_product_survey_screen).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_screen).pack(pady=10)

    def show_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self.root, text="Email:").pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")  
        password_entry.pack()

        def login():
            nonlocal email_entry, password_entry

            if email_entry.get().endswith("@jingcheng.com") and password_entry.get() == "password":
                self.show_data_options_screen()
            else:
                tk.Label(self.root, text="Incorrect info. Please try again.", fg="red").pack()

        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_screen).pack(pady=10)
    
    def show_data_options_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Select Data Option", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.root, text="Show Complaint Data", command=self.show_complaint_chart).pack(pady=10)
        tk.Button(self.root, text="Show Service Survey Data", command=self.show_service_survey_chart).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_login_screen).pack(pady=10)
    
    def generate_random_service_survey_data(self):
        satisfaction_options = ["Yes", "No"]
        complaint_filed_options = ["Yes", "No"]
    
        data = {
        "Satisfaction": [random.choice(satisfaction_options) for _ in range(50)],
        "Complaint Filed": [random.choice(complaint_filed_options) for _ in range(50)],
        "Score": [random.randint(1, 5) for _ in range(50)]
        }

        self.service_survey_df = pd.DataFrame(data)

    def show_service_survey_chart(self):
        self.clear_screen()

        tk.Label(self.root, text="Service Survey Chart", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = tk.Frame(self.root)
        tree_frame.pack(expand=True, fill="both")

    # Create a Treeview widget 
        tree = ttk.Treeview(tree_frame, columns=list(self.service_survey_df.columns), show="headings", height=20)
        for col in self.service_survey_df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        for i, row in self.service_survey_df.iterrows():
            tree.insert("", tk.END, values=list(row))

    # scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.config(command=tree.yview)

    # Pack the Treeview and scrollbar
        tree.pack(expand=True, fill="both")
        vsb.pack(side="right", fill="y")

        tk.Button(self.root, text="Back", command=self.show_data_options_screen).pack(pady=10)
        tk.Button(self.root, text="Summary", command=self.show_survey_summary).pack(pady=10)

    def show_survey_summary(self):
# Calculate summary statistics 
        avg_score = self.service_survey_df["Score"].mean()
        
        complaint_counts = (self.service_survey_df["Complaint Filed"].value_counts())
        complaint_percentage = (complaint_counts / complaint_counts.sum()) * 100

        score_counts = self.service_survey_df["Score"].value_counts().sort_index()


        satisfaction_counts = self.service_survey_df["Satisfaction"].value_counts()
        satisfaction_percentage = (satisfaction_counts / satisfaction_counts.sum()) * 100


        # Create a new window for the summary display
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Service Survey Summary")
        
        # Display pie chart for "Satisfaction" category
        plt.figure(figsize=(4, 4))
        plt.pie(satisfaction_percentage, labels=satisfaction_percentage.index, autopct="%1.1f%%", startangle=140)
        plt.title("Satisfaction Distribution")
        plt.axis("equal")  
        plt.savefig("satisfaction_pie_chart.png")

        # Display the pie chart image in the summary window
        satisfaction_chart_image = tk.PhotoImage(file="satisfaction_pie_chart.png")
        satisfaction_chart_label = tk.Label(summary_window, image=satisfaction_chart_image)
        satisfaction_chart_label.image = satisfaction_chart_image
        satisfaction_chart_label.pack(side="right", padx=10)

        plt.figure(figsize=(4, 4))
        plt.pie(complaint_percentage, labels=complaint_percentage.index, autopct="%1.1f%%", startangle=140)
        plt.title("Complaint Distribution")
        plt.axis("equal")  
        plt.savefig("Complaint_pie_chart.png")

        complaint_chart_image = tk.PhotoImage(file="complaint_pie_chart.png")
        complaint_chart_label = tk.Label(summary_window, image=complaint_chart_image)
        complaint_chart_label.image = complaint_chart_image
        complaint_chart_label.pack(side="left", padx=10)

        # Display bar chart for "Score" category
        plt.figure(figsize=(8, 4))
        plt.bar(score_counts.index, score_counts.values)
        plt.title("Score Distribution")
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        plt.savefig("score_bar_chart.png")

        # Display the bar chart image in the summary window
        score_chart_image = tk.PhotoImage(file="score_bar_chart.png")
        score_chart_label = tk.Label(summary_window, image=score_chart_image)
        score_chart_label.image = score_chart_image
        score_chart_label.pack(side="top", pady=10)

        # Display average score and complaint percentage
        avg_score_label = tk.Label(summary_window, text=f"Average Score: {avg_score:.2f}", font=("Helvetica", 12))
        avg_score_label.pack(side="right", padx=10)
     
       

    def show_complaint_chart(self):
        self.clear_screen()

        tk.Label(self.root, text="Complaint Chart", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = tk.Frame(self.root)
        tree_frame.pack(expand=True, fill="both")

        # scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        # Create a Treeview widget
        tree = ttk.Treeview(tree_frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=20)
        tree["columns"] = list(self.df.columns)
        for col in self.df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        for i, row in self.df.iterrows():
            tree.insert("", tk.END, values=list(row))

        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        
        tree.pack(expand=True, fill="both")
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        tk.Button(self.root, text="Back", command=self.show_data_options_screen).pack(pady=10)
        tk.Button(self.root, text="Summary", command=self.show_complaint_summary).pack(pady=10)
    def show_complaint_summary(self):
        # Calculate summary statistics
        avg_score = self.df["Complaint Severity Score"].mean()
        std_dev = self.df["Complaint Severity Score"].std()
        median_score = self.df["Complaint Severity Score"].median()
        complaint_category_counts = self.df["Complaint Catergory"].value_counts()

        # Create a new window for the summary display
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Complaint Summary")

        # Display pie chart for Complaint Category frequency
        plt.figure(figsize=(10,5 ))
        plt.pie(complaint_category_counts, labels=complaint_category_counts.index, autopct="%1.1f%%", startangle=140)
        plt.title("Complaint Category Frequency")
        plt.axis("equal")  
        plt.savefig("complaint_category_pie_chart.png")

        
        chart_image = tk.PhotoImage(file="complaint_category_pie_chart.png")
        chart_label = tk.Label(summary_window, image=chart_image)
        chart_label.image = chart_image
        chart_label.pack(side="left", padx=13)

        # Display summary statistics on the right
        summary_text = f"Average Severity Score: {avg_score:.2f}\n"
        summary_text += f"Standard Deviation: {std_dev:.2f}\n"
        summary_text += f"Median Severity Score: {median_score:.2f}"

        summary_label = tk.Label(summary_window, text=summary_text, font=("Helvetica", 12))
        summary_label.pack(side="right", padx=10)
        
    def show_file_complaint_screen(self):
        complaint = {"Software completely stopped working": 5, "Software has minor bugs": 2,
                     "Software needs improvement or adjustments": 1, "Software is crashing": 3,
                     "Software does not meet product requirements": 4}
        
        time = {"1 week": 5, "1 month": 4, "3 months": 3, "6 months": 2, "1 year": 1}
        self.clear_screen()

        tk.Label(self.root, text="File a Complaint", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self.root, text="Client Name:").pack()
        client_name_entry = tk.Entry(self.root)
        client_name_entry.pack()

        tk.Label(self.root, text="Complaint Category:").pack()
        complaint_category_var = tk.StringVar()
        complaint_category_combobox = ttk.Combobox(self.root, textvariable=complaint_category_var,
                                                   values=list(complaint.keys()))
        complaint_category_combobox.pack()

        tk.Label(self.root, text="Industry:").pack()
        industry_var = tk.StringVar()
        industry_combobox = ttk.Combobox(self.root, textvariable=industry_var, values=["Finance", "Manufacturing",
                                                                                        "Service", "Government",
                                                                                        "Power/Electricity", "Education",
                                                                                        "Medical", "Other"])
        industry_combobox.pack()

        tk.Label(self.root, text="Resolved By:").pack()
        resolved_by_var = tk.StringVar()
        resolved_by_combobox = ttk.Combobox(self.root, textvariable=resolved_by_var, values=list(time.keys()))
        resolved_by_combobox.pack()
 
        
        def file_complaint():
            new_complaint = {
                "Client Name": client_name_entry.get(),
                "Complaint Catergory": complaint_category_var.get(),
            "Industry": industry_var.get(),
            "Resolved By": resolved_by_var.get()
    }

            new_complaint["Complaint Severity Score"] = self.complaint[new_complaint["Complaint Catergory"]] * self.time[
                new_complaint["Resolved By"]]
            
            self.df = pd.concat([self.df, pd.DataFrame([new_complaint])], ignore_index=True)
            self.show_main_screen()

        tk.Button(self.root, text="Done", command=file_complaint).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_screen).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ComplaintPortal(root)
    root.mainloop()
