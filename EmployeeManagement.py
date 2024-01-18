import tkinter as tk
from tkinter import ttk
import pandas as pd
import random
import matplotlib.pyplot as plt

class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1000x800")  # Increased window size for better display

        # Initialize the DataFrame with random data
        self.generate_random_data()
        self.rand_data_for_survey()
        self.show_main_screen()

    def generate_random_data(self):
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Singh", "Kumar", "Shah", "Sharma", "Sato", "Suzuki", "Takahashi", "Tanaka"]
        first_names = ["Hiroshi", "Akihiro", "Yuki", "Haruka", "Vivaan", "Mira", "Rohan", "Min", "Xiao", "Qing", "Ava", "Sophia", "Jackson", "Lucas", "Liam", "Olivia", "Noah"]

        data = {
            "Last Name": [random.choice(last_names) for _ in range(50)],
            "First Name": [random.choice(first_names) for _ in range(50)],
            "Department": [random.choice(["Management", "Customer service", "Engineering/Repair", "Marketing", "Development"]) for _ in range(50)],
            "Role": [random.choice(["Supervisor", "Manager", "Team Lead", "Analyst", "Senior Member/Specialist", "Associate", "Representative", "Staff Member"]) for _ in range(50)],
            "Years Worked": [random.randint(1, 14) for _ in range(50)],
            "Mentorship Program": [random.choice(["Yes", "No"]) for _ in range(50)],
        }
        data["Email"] = ["{}{}@jingcheng.com".format(name[0].lower(), name[1]) for name in zip(data["First Name"], data["Last Name"])]

        self.df = pd.DataFrame(data)
    
    def rand_data_for_survey(self):
        reasons= ["Better Compensation", "Industry Switch", "Higher Level Position Oppertunity", 
                  "Dissatisfaction with Company Mangement/Environment", "Other"]
        yo= ["Yes", "No"]
        data={
            "Reason For Leaving": [random.choice(reasons) for _ in range(50)],
            "Years Worked" :[random.randint(1, 14) for _ in range(50)],
            "Work Environment Rating": [random.randint(1, 5) for _ in range(50)],
            "Reccomendation to Others" : [random.choice(yo) for _ in range(50)]
            
        }
        self.s_df = pd.DataFrame(data)
    
    def show_main_screen(self):
        self.clear_screen()
        tk.Button(self.root, text="Personnel Data", command=self.show_personnel_screen).pack(pady=10)
        tk.Button(self.root, text="Leave Data", command=self.show_survey_data).pack(pady=10)
        tk.Button(self.root, text="Company Leave Survey", command=self.show_leave_survey).pack(pady=10)
   
    
    def show_survey_data(self):
        self.clear_screen()

        tk.Label(self.root, text="Company Leave Survey Data", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = tk.Frame(self.root)
        tree_frame.pack(expand=True, fill="both")

        # scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        # treeview widget
        tree = ttk.Treeview(tree_frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=20)  
        tree["columns"] = list(self.s_df.columns)
        for col in self.s_df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)  

        for i, row in self.s_df.iterrows():
            tree.insert("", tk.END, values=list(row))

        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        
        tree.pack(expand=True, fill="both")
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        tk.Button(self.root, text="Back", command=self.show_main_screen).pack(pady=10)
        tk.Button(self.root, text="Summary", command=self.show_survey_summary).pack(side="bottom", pady=10)

    def show_survey_summary(self):
        #  summary statistics for survey data
        avg_score = self.s_df["Work Environment Rating"].mean()
        avg_years = self.s_df["Years Worked"].mean()
        reason_category_counts = self.s_df["Reason For Leaving"].value_counts()
        reason_percentage = (reason_category_counts / reason_category_counts.sum()) * 100
        recc_counts = self.s_df["Reccomendation to Others"].value_counts()
        recc_percentage = (recc_counts / recc_counts.sum()) * 100
        work_env_counts = self.s_df["Work Environment Rating"].value_counts().sort_index()

        # Create a new window 
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Company Leave Survey Summary")

        # Pie chart for "Reccomendation" column
        plt.figure(figsize=(4, 4))
        plt.pie(recc_percentage, labels=recc_percentage.index, autopct="%1.1f%%", startangle=140)
        plt.title("Reccomendation Distribution")
        plt.axis("equal")  
        plt.savefig("recc_pie_chart.png")
        recc_chart_image = tk.PhotoImage(file="recc_pie_chart.png")
        recc_chart_label = tk.Label(summary_window, image=recc_chart_image)
        recc_chart_label.image = recc_chart_image
        recc_chart_label.pack(side="right", padx=10)

        # Pie chart for "Reasons for Leave" column
        plt.figure(figsize=(4, 4))
        plt.pie(reason_percentage, labels=reason_percentage.index, autopct="%1.1f%%", startangle=140)
        plt.title("Reasons for Leave Distribution")
        plt.axis("equal")  
        plt.savefig("reason_pie_chart.png")
        reason_chart_image = tk.PhotoImage(file="reason_pie_chart.png")
        reason_chart_label = tk.Label(summary_window, image=reason_chart_image)
        reason_chart_label.image = reason_chart_image
        reason_chart_label.pack(side="left", padx=10)


        # Bar chart for "Work Environment Rating" column
        plt.figure(figsize=(8, 4))
        plt.bar(work_env_counts.index, work_env_counts.values)
        plt.title("Work Environment Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
        plt.savefig("workEnv_bar_chart.png")
        work_env_chart_image = tk.PhotoImage(file="workEnv_bar_chart.png")
        work_env_chart_label = tk.Label(summary_window, image=work_env_chart_image)
        work_env_chart_label.image = work_env_chart_image
        work_env_chart_label.pack(side="top", pady=10)

        # Labels for average score and average years worked
        avg_score_label = tk.Label(summary_window, text=f"Average Work Environment Rating: {avg_score:.2f}", font=("Helvetica", 12))
        avg_score_label.pack(side=tk.BOTTOM, padx=10)

        avg_years_label = tk.Label(summary_window, text=f"Average Years of Work of Leaving Employees: {avg_years:.2f}", font=("Helvetica", 12))
        avg_years_label.pack(side=tk.BOTTOM, padx=10)
   
    def show_personnel_screen(self):
        self.clear_screen()

        tk.Button(self.root, text="Show Personnel", command=self.show_personnel).pack(pady=10)
        tk.Button(self.root, text="Input New Hire", command=self.show_input_new_hire_screen).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_screen).pack(pady=10)

    def show_personnel(self):
        self.clear_screen()

        # Display the DataFrame using ttk.Treeview with scrollbars
        tk.Label(self.root, text="Personnel Data", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = tk.Frame(self.root)
        tree_frame.pack(expand=True, fill="both")

        # scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        # Treeview widget
        tree = ttk.Treeview(tree_frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=20)  # Adjust height as needed
        tree["columns"] = list(self.df.columns)
        for col in self.df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)  # Adjust the width as needed

        for i, row in self.df.iterrows():
            tree.insert("", tk.END, values=list(row))

        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        
        tree.pack(expand=True, fill="both")
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        tk.Button(self.root, text="Back", command=self.show_personnel_screen).pack(pady=10)
        tk.Button(self.root, text="Search For Mentor", command=self.show_search_mentor_screen).pack(side="bottom", pady=10)
    
    def show_search_mentor_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Search For Mentor").pack()

    # Dropdown for department selection
        tk.Label(self.root, text="Select Department:").pack()
        department_var = tk.StringVar()
        department_combobox = ttk.Combobox(self.root, textvariable=department_var, values=["Management", "Customer service", "Engineering/Repair", "Marketing", "Development"])
        department_combobox.pack()

    # Dropdown for role selection
        tk.Label(self.root, text="Select Role:").pack()
        role_var = tk.StringVar()
        role_combobox = ttk.Combobox(self.root, textvariable=role_var, values=["Supervisor", "Manager", "Team Lead", "Analyst", "Senior Member/Specialist", "Associate", "Representative", "Staff Member"])
        role_combobox.pack()

        def search_for_mentor():
            selected_department = department_var.get()
            selected_role = role_var.get()

        # Filter the DataFrame based on selected department, role, and mentorship program
            result_df = self.df[(self.df["Department"] == selected_department) & (self.df["Role"] == selected_role) & (self.df["Mentorship Program"] == "Yes")]

            if result_df.empty:
                tk.Label(self.root, text="No mentor found", font=("Helvetica", 14)).pack()
            else:
                tk.Label(self.root, text="Search Results", font=("Helvetica", 16)).pack()

                tree_frame = tk.Frame(self.root)
                tree_frame.pack(expand=True, fill="both")

                tree = ttk.Treeview(tree_frame)
                tree["columns"] = list(result_df.columns)
                for col in result_df.columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=150)

                for i, row in result_df.iterrows():
                    tree.insert("", tk.END, values=list(row))

                tree.pack(expand=True, fill="both")

        tk.Button(self.root, text="Search", command=search_for_mentor).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_personnel_screen).pack(pady=10)

    def show_input_new_hire_screen(x):
        x.clear_screen()

        tk.Label(x.root, text="Input New Hire").pack()

        tk.Label(x.root, text="First Name:").pack()
        first_name_entry = tk.Entry(x.root)
        first_name_entry.pack()

        tk.Label(x.root, text="Last Name:").pack()
        last_name_entry = tk.Entry(x.root)
        last_name_entry.pack()

        tk.Label(x.root, text="Department:").pack()
        department_var = tk.StringVar()
        department_combobox = ttk.Combobox(x.root, textvariable=department_var, values=["Management", "Customer service", "Engineering/Repair", "Marketing", "Development"])
        department_combobox.pack()

        tk.Label(x.root, text="Role:").pack()
        role_var = tk.StringVar()
        role_combobox = ttk.Combobox(x.root, textvariable=role_var, values=["Supervisor", "Manager", "Team Lead", "Analyst", "Senior Member/Specialist", "Associate", "Representative", "Staff Member"])
        role_combobox.pack()

        def add_new_hire():
            new_hire = {
                "First Name": first_name_entry.get(),
                "Last Name": last_name_entry.get(),
                "Department": department_var.get(),
                "Role": role_var.get(),
                "Mentorship Program": "Yes",
                "Years Worked": 0,
                "Email": "{}{}@jingcheng".format( first_name_entry.get().lower(), last_name_entry.get()),
            }
            x.df = pd.concat([x.df, pd.DataFrame([new_hire])], ignore_index=True)
            x.show_personnel()

        tk.Button(x.root, text="Enter", command=add_new_hire).pack(pady=10)
        tk.Button(x.root, text="Back", command=x.show_personnel_screen).pack(pady=10)
    
    def show_leave_survey(x):
        x.clear_screen()
        reasons= ["Better Compensation", "Industry Switch", "Higher Level Position Oppertunity", 
                  "Dissatisfaction with Company Mangement/Environment", "Other"]
        tk.Label(x.root, text="Company Leave Survey").pack()

        tk.Label(x.root, text="Why are you leaving Jingcheng?").pack()
        reasons_var = tk.StringVar()
        reasons_combobox = ttk.Combobox(x.root, textvariable=reasons_var, values=reasons)
        reasons_combobox.pack()

        tk.Label(x.root, text="How many years have you spent at Jingcheng?").pack()
        year_var = tk.IntVar()
        entry_years = tk.Entry(x.root, textvariable=year_var)
        entry_years.pack()

        tk.Label(x.root, text="How would you rate your work environment?").pack()
        score_var = tk.IntVar()
        score_options = ttk.Combobox(x.root, textvariable=score_var, values=["1", "2", "3", "4", "5"])
        score_options.pack()

        tk.Label(x.root, text="Would you reccomend us as an employer?").pack()
        reccVar= tk.StringVar()
        recc = ttk.Combobox(x.root, textvariable=reccVar, values=["Yes", "No"])
        recc.pack()

        def add_survey_data():
            survey_data = {
            "Reason For Leaving": reasons_var.get(),
            "Years Worked" : year_var.get(),
            "Work Environment Rating":score_var.get() ,
            "Reccomendation to Others" : reccVar.get()

            }
            x.s_df = pd.concat([x.s_df, pd.DataFrame([survey_data])], ignore_index=True)
            x.show_main_screen()

        tk.Button(x.root, text="Enter", command=add_survey_data).pack(pady=10)
        tk.Button(x.root, text="Back", command=x.show_main_screen).pack(pady=10)
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
