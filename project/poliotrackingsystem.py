from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class Polio:
    def __init__(self, root):
        self.root = root
        self.root.title("Polio Tracking System Designed By Samijazz")
        self.root.geometry("1540x800+0+0")

        # Load the background image
        self.bg_image = PhotoImage(file="images/Eradicating-Polio-1030x686.png")

        # Create a Canvas widget to display the image
        self.canvas = Canvas(self.root, width=1540, height=800)
        self.canvas.pack(fill=BOTH, expand=True)

        # Add the image to the Canvas
        self.canvas.create_image(0, 0, anchor=NW, image=self.bg_image)

        # Title
        lbltitle = Label(self.root, bd=20, relief=RIDGE, text="+ POLIO TRACKING SYSTEM", fg="red", bg="white", font=("times new roman", 50, "bold"))
        lbltitle.place(x=0, y=0, width=1540, height=100)

        # Main Buttons
        btnAdminLogin = Button(self.root, text="Admin Login", font=("arial", 12, "bold"), width=23, height=2, padx=2, pady=6, command=self.admin_login)
        btnAdminLogin.place(x=650, y=300)

        btnAdminSignup = Button(self.root, text="Admin Signup", font=("arial", 12, "bold"), width=23, height=2, padx=2, pady=6, command=self.admin_signup)
        btnAdminSignup.place(x=650, y=400)

        # Initialize database
        self.conn = sqlite3.connect('polio.db')
        self.create_tables()

    def create_tables(self):
        # Create admin table if not exists
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Create patients table if not exists
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                gender TEXT,
                age INTEGER,
                address TEXT,
                phone TEXT,
                email TEXT,
                symptoms TEXT,
                culture_sample TEXT,
                poliovirus_type TEXT,
                community TEXT,
                vaccine_administered TEXT,
                medical_care_given TEXT,
                isolation_location TEXT
            )
        ''')
        self.conn.commit()

    def admin_login(self):
        self.new_window = Toplevel(self.root)
        self.app = AdminLogin(self.new_window, self.conn, self.root)

    def admin_signup(self):
        self.new_window = Toplevel(self.root)
        self.app = AdminSignup(self.new_window, self.conn)

    def __del__(self):
        self.conn.close()

class AdminLogin:
    def __init__(self, root, conn, main_root):
        self.root = root
        self.conn = conn
        self.main_root = main_root
        self.root.title("Admin Login")
        self.root.geometry("400x400+450+150")

        self.username = StringVar()
        self.password = StringVar()

        lbltitle = Label(self.root, text="Admin Login", font=("arial", 20, "bold"))
        lbltitle.pack(pady=20)

        lblUser = Label(self.root, text="Username", font=("arial", 12, "bold"))
        lblUser.pack(pady=5)
        txtUser = Entry(self.root, textvariable=self.username, font=("arial", 12, "bold"))
        txtUser.pack(pady=5)

        lblPass = Label(self.root, text="Password", font=("arial", 12, "bold"))
        lblPass.pack(pady=5)
        txtPass = Entry(self.root, textvariable=self.password, font=("arial", 12, "bold"), show="*")
        txtPass.pack(pady=5)

        btnLogin = Button(self.root, text="Login", font=("arial", 12, "bold"), command=self.login)
        btnLogin.pack(pady=20)

        lblForgotPassword = Label(self.root, text="Forgotten Password?", font=("arial", 10, "bold"), fg="blue", cursor="hand2")
        lblForgotPassword.pack()
        lblForgotPassword.bind("<Button-1>", self.forgot_password)

    def login(self):
        username = self.username.get()
        password = self.password.get()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE username=? AND password=?', (username, password))
        row = cursor.fetchone()
        if row:
            messagebox.showinfo("Login Success", "Welcome Admin!")
            self.open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def open_dashboard(self):
        self.root.destroy()
        dashboard(self.main_root, self.conn)

    def forgot_password(self, event):
        self.new_window = Toplevel(self.root)
        self.app = ForgotPassword(self.new_window, self.conn)

class AdminSignup:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.root.title("Admin Signup")
        self.root.geometry("400x400+450+150")

        self.username = StringVar()
        self.password = StringVar()
        self.confirm_password = StringVar()

        lbltitle = Label(self.root, text="Admin Signup", font=("arial", 20, "bold"))
        lbltitle.pack(pady=20)

        lblUser = Label(self.root, text="Username", font=("arial", 12, "bold"))
        lblUser.pack(pady=5)
        txtUser = Entry(self.root, textvariable=self.username, font=("arial", 12, "bold"))
        txtUser.pack(pady=5)

        lblPass = Label(self.root, text="Password", font=("arial", 12, "bold"))
        lblPass.pack(pady=5)
        txtPass = Entry(self.root, textvariable=self.password, font=("arial", 12, "bold"), show="*")
        txtPass.pack(pady=5)

        lblConfirmPass = Label(self.root, text="Confirm Password", font=("arial", 12, "bold"))
        lblConfirmPass.pack(pady=5)
        txtConfirmPass = Entry(self.root, textvariable=self.confirm_password, font=("arial", 12, "bold"), show="*")
        txtConfirmPass.pack(pady=5)

        btnSignup = Button(self.root, text="Signup", font=("arial", 12, "bold"), command=self.signup)
        btnSignup.pack(pady=20)

    def signup(self):
        username = self.username.get()
        password = self.password.get()
        confirm_password = self.confirm_password.get()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE username=?', (username,))
        row = cursor.fetchone()
        if row:
            messagebox.showerror("Signup Failed", "Username already exists")
        elif password == confirm_password:
            cursor.execute('INSERT INTO admin (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            messagebox.showinfo("Signup Success", "Admin registered successfully!")
            self.root.destroy()
        else:
            messagebox.showerror("Signup Failed", "Passwords do not match")

class ForgotPassword:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.root.title("Forgot Password")
        self.root.geometry("400x400+450+150")

        self.username = StringVar()
        self.new_password = StringVar()
        self.confirm_new_password = StringVar()

        lbltitle = Label(self.root, text="Reset Password", font=("arial", 20, "bold"))
        lbltitle.pack(pady=20)

        lblUser = Label(self.root, text="Username", font=("arial", 12, "bold"))
        lblUser.pack(pady=5)
        txtUser = Entry(self.root, textvariable=self.username, font=("arial", 12, "bold"))
        txtUser.pack(pady=5)

        lblNewPass = Label(self.root, text="New Password", font=("arial", 12, "bold"))
        lblNewPass.pack(pady=5)
        txtNewPass = Entry(self.root, textvariable=self.new_password, font=("arial", 12, "bold"), show="*")
        txtNewPass.pack(pady=5)

        lblConfirmNewPass = Label(self.root, text="Confirm New Password", font=("arial", 12, "bold"))
        lblConfirmNewPass.pack(pady=5)
        txtConfirmNewPass = Entry(self.root, textvariable=self.confirm_new_password, font=("arial", 12, "bold"), show="*")
        txtConfirmNewPass.pack(pady=5)

        btnReset = Button(self.root, text="Reset Password", font=("arial", 12, "bold"), command=self.reset_password)
        btnReset.pack(pady=20)

    def reset_password(self):
        username = self.username.get()
        new_password = self.new_password.get()
        confirm_new_password = self.confirm_new_password.get()
        cursor = self.conn.cursor()
        cursor.execute('UPDATE admin SET password=? WHERE username=?', (new_password, username))
        self.conn.commit()
        messagebox.showinfo("Reset Success", "Password reset successfully!")
        self.root.destroy()

def dashboard(main_root, conn):
    root = Toplevel(main_root)
    root.title("Admin Dashboard")
    root.geometry("800x600+300+150")

    lbltitle = Label(root, text="Admin Dashboard", font=("arial", 20, "bold"))
    lbltitle.pack(pady=20)

    # Patient Entry Section
    frame_patient_entry = LabelFrame(root, text="Add Polio Patient to Records", font=("arial", 15, "bold"))
    frame_patient_entry.pack(fill="both", expand="yes", padx=20, pady=10)

    # Labels and Entry fields for patient details
    Label(frame_patient_entry, text="Patient First Name:", font=("arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=30).grid(row=0, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Patient Last Name:", font=("arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=30).grid(row=1, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Gender:", font=("arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5)
    gender_var = StringVar()
    gender_var.set("Male")
    Radiobutton(frame_patient_entry, text="Male", variable=gender_var, value="Male", font=("arial", 12)).grid(row=2, column=1)
    Radiobutton(frame_patient_entry, text="Female", variable=gender_var, value="Female", font=("arial", 12)).grid(row=2, column=2)

    Label(frame_patient_entry, text="Age:", font=("arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=10).grid(row=3, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Address:", font=("arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=30).grid(row=4, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Phone No.:", font=("arial", 12, "bold")).grid(row=5, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=20).grid(row=5, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Email:", font=("arial", 12, "bold")).grid(row=6, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=30).grid(row=6, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Symptoms:", font=("arial", 12, "bold")).grid(row=7, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=30).grid(row=7, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Culture Sample:", font=("arial", 12, "bold")).grid(row=8, column=0, padx=10, pady=5)
    culture_var = StringVar()
    culture_var.set("Stool")
    ttk.Combobox(frame_patient_entry, textvariable=culture_var, values=["Stool", "Throat Swab"], font=("arial", 12), width=27).grid(row=8, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Poliovirus Type:", font=("arial", 12, "bold")).grid(row=9, column=0, padx=10, pady=5)
    polio_var = StringVar()
    polio_var.set("PV Type 1")
    ttk.Combobox(frame_patient_entry, textvariable=polio_var, values=["PV Type 1", "PV Type 2", "PV Type 3", "Vaccine-derived polioviruses vDPVs"], font=("arial", 12), width=27).grid(row=9, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Community:", font=("arial", 12, "bold")).grid(row=10, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=30).grid(row=10, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Vaccine Administered:", font=("arial", 12, "bold")).grid(row=11, column=0, padx=10, pady=5)
    Entry(frame_patient_entry, font=("arial", 12), width=30).grid(row=11, column=1, padx=10, pady=5)

    Label(frame_patient_entry, text="Medical Care Given:", font=("arial", 12, "bold")).grid(row=12, column=0, padx=10, pady=5)
    medical_care_var = StringVar()
    Checkbutton(frame_patient_entry, text="Pain Management", variable=medical_care_var, onvalue="Pain Management", offvalue="", font=("arial", 12)).grid(row=12, column=1, sticky=W)
    Checkbutton(frame_patient_entry, text="Physical Therapy", variable=medical_care_var, onvalue="Physical Therapy", offvalue="", font=("arial", 12)).grid(row=12, column=2, sticky=W)
    Checkbutton(frame_patient_entry, text="Respiratory Support", variable=medical_care_var, onvalue="Respiratory Support", offvalue="", font=("arial", 12)).grid(row=12, column=3, sticky=W)

    Label(frame_patient_entry, text="Isolation Location:", font=("arial", 12, "bold")).grid(row=13, column=0, padx=10, pady=5)
    isolation_var = StringVar()
    ttk.Combobox(frame_patient_entry, textvariable=isolation_var, values=["Hospital", "Treatment Centers", "Quarantine Facility", "Home Isolation"], font=("arial", 12), width=27).grid(row=13, column=1, padx=10, pady=5)

    # Buttons
    Button(root, text="Add Polio Patient", font=("arial", 12, "bold"), width=20).pack(pady=10)
    Button(root, text="Edit Patient Record", font=("arial", 12, "bold"), width=20).pack(pady=10)
    Button(root, text="Delete Patient Record", font=("arial", 12, "bold"), width=20).pack(pady=10)
    Button(root, text="View Patients", font=("arial", 12, "bold"), width=20).pack(pady=10)
    Button(root, text="Save to Database", font=("arial", 12, "bold"), width=20).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = Polio(root)
    root.mainloop()
