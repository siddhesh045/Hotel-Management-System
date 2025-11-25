import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import datetime

# --- CONFIGURATION & THEME ---
THEME_BG = "#1a1a2e"        # Dark Navy
THEME_FG = "#e94560"        # Neon Red/Pink
THEME_ACCENT = "#0f3460"    # Deep Blue
THEME_TEXT = "#ffffff"      # White
FONT_MAIN = ("Segoe UI", 10)
FONT_HEAD = ("Segoe UI", 14, "bold")

# --- CONSTANTS ---
EXTENSION_COST = 2.0        # Cost to extend book
EXTENSION_DAYS = 5          # Extra days given

class LibraryDB:
    def __init__(self):
        self.conn = sqlite3.connect("vidyarthi_lib_v4.db")
        self.cur = self.conn.cursor()
        self.setup_db()
        self.add_dummy_data()

    def setup_db(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                price INTEGER,
                days_limit INTEGER,
                is_available INTEGER DEFAULT 1
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                student_name TEXT,
                issue_date TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'BORROWED'
            )
        """)
        self.cur.execute("CREATE TABLE IF NOT EXISTS wallet (student TEXT PRIMARY KEY, balance REAL)")
        self.conn.commit()

    def add_dummy_data(self):
        self.cur.execute("SELECT count(*) FROM books")
        if self.cur.fetchone()[0] == 0:
            data = [
                (101, "Python Essentials", "Vidyarthi Team", 5, 7),
                (102, "The Alchemist", "Paulo Coelho", 3, 14),
                (103, "Atomic Habits", "James Clear", 6, 10),
                (104, "Rich Dad Poor Dad", "Robert Kiyosaki", 4, 7),
                (105, "Harry Potter", "J.K. Rowling", 8, 30),
            ]
            self.cur.executemany("INSERT INTO books VALUES (?,?,?,?,?,1)", data)
            self.conn.commit()

    def get_books(self, available_only=False):
        query = "SELECT * FROM books"
        if available_only:
            query += " WHERE is_available = 1"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_my_books(self, student):
        query = """
            SELECT t.trans_id, b.title, t.issue_date, t.due_date, b.id 
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            WHERE t.student_name = ? AND t.status = 'BORROWED'
        """
        self.cur.execute(query, (student,))
        return self.cur.fetchall()

    def get_wallet(self, student):
        self.cur.execute("SELECT balance FROM wallet WHERE student=?", (student,))
        res = self.cur.fetchone()
        if not res:
            self.cur.execute("INSERT INTO wallet VALUES (?, ?)", (student, 100.0))
            self.conn.commit()
            return 100.0
        return res[0]

    def add_funds(self, student, amount):
        current = self.get_wallet(student)
        new_bal = current + amount
        self.cur.execute("UPDATE wallet SET balance=? WHERE student=?", (new_bal, student))
        self.conn.commit()
        return new_bal

    def borrow_book(self, book_id, price, days, student):
        bal = self.get_wallet(student)
        if bal < price:
            return False, "Insufficient Funds"

        new_bal = bal - price
        self.cur.execute("UPDATE wallet SET balance=? WHERE student=?", (new_bal, student))
        self.cur.execute("UPDATE books SET is_available=0 WHERE id=?", (book_id,))
        
        today = datetime.date.today()
        due = today + datetime.timedelta(days=days)
        self.cur.execute("INSERT INTO transactions (book_id, student_name, issue_date, due_date) VALUES (?,?,?,?)",
                         (book_id, student, today, due))
        
        self.conn.commit()
        return True, "Success"

    def extend_due_date(self, trans_id, current_due_str, student):
        # Check Wallet
        bal = self.get_wallet(student)
        if bal < EXTENSION_COST:
            return False, "Insufficient funds for extension fee."

        # Calculate New Date
        try:
            curr_date = datetime.datetime.strptime(current_due_str, "%Y-%m-%d").date()
        except ValueError:
            # Fallback if date format issues exist in DB
            curr_date = datetime.date.today()

        new_date = curr_date + datetime.timedelta(days=EXTENSION_DAYS)
        
        # Deduct Fee
        new_bal = bal - EXTENSION_COST
        self.cur.execute("UPDATE wallet SET balance=? WHERE student=?", (new_bal, student))
        
        # Update Transaction
        self.cur.execute("UPDATE transactions SET due_date=? WHERE trans_id=?", (new_date, trans_id))
        self.conn.commit()
        
        return True, f"Extended to {new_date}"

    def return_book(self, trans_id, book_id):
        self.cur.execute("UPDATE books SET is_available=1 WHERE id=?", (book_id,))
        self.cur.execute("UPDATE transactions SET status='RETURNED' WHERE trans_id=?", (trans_id,))
        self.conn.commit()

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VIDYARTHI DIGITAL LIBRARY 4.0 (ULTRA)")
        self.root.geometry("1100x650")
        self.root.configure(bg=THEME_BG)
        
        self.db = LibraryDB()
        self.user = "Student_1" 
        
        self.setup_ui()

    def setup_ui(self):
        # --- Header ---
        header = tk.Frame(self.root, bg=THEME_ACCENT, height=60)
        header.pack(fill="x")
        
        tk.Label(header, text="🎓 VIDYARTHI LIBRARY PRO", font=("Orbitron", 18, "bold"), bg=THEME_ACCENT, fg="white").pack(side="left", padx=20, pady=10)
        
        # Wallet Section (Right Side)
        wallet_frame = tk.Frame(header, bg=THEME_ACCENT)
        wallet_frame.pack(side="right", padx=20)

        self.lbl_wallet = tk.Label(wallet_frame, text="Wallet: $---", font=("Consolas", 12), bg=THEME_ACCENT, fg="#00ff00")
        self.lbl_wallet.pack(side="left", padx=10)

        # ADD FUNDS BUTTON (+)
        tk.Button(wallet_frame, text="➕", bg="#00ff00", fg="black", font=("Arial", 10, "bold"), width=3,
                  command=self.add_funds_action).pack(side="left")

        # --- Tabs ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=THEME_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background="#222", foreground="white", padding=[15, 8], font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", THEME_FG)], foreground=[("selected", "white")])

        tabs = ttk.Notebook(self.root)
        tabs.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_store = tk.Frame(tabs, bg=THEME_BG)
        self.tab_bag = tk.Frame(tabs, bg=THEME_BG)

        tabs.add(self.tab_store, text="📖 BROWSE BOOKS")
        tabs.add(self.tab_bag, text="🎒 MY BAG & RETURNS")

        self.build_store_tab()
        self.build_bag_tab()
        self.update_wallet()

    def build_store_tab(self):
        paned = tk.PanedWindow(self.tab_store, orient="horizontal", bg=THEME_BG, sashwidth=4)
        paned.pack(fill="both", expand=True)

        left_frame = tk.Frame(paned, bg=THEME_BG)
        paned.add(left_frame)

        cols = ("ID", "Title", "Author", "Rent", "Days")
        self.tree_store = ttk.Treeview(left_frame, columns=cols, show="headings", height=15)
        
        self.tree_store.heading("ID", text="ID")
        self.tree_store.column("ID", width=50)
        self.tree_store.heading("Title", text="Title")
        self.tree_store.column("Title", width=200)
        self.tree_store.heading("Author", text="Author")
        self.tree_store.heading("Rent", text="Cost ($)")
        self.tree_store.column("Rent", width=80)
        self.tree_store.heading("Days", text="Limit (Days)")
        self.tree_store.column("Days", width=80)
        
        self.tree_store.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_store.bind("<<TreeviewSelect>>", self.on_book_select)
        
        self.refresh_store()

        self.right_frame = tk.Frame(paned, bg="#222", width=300)
        paned.add(self.right_frame)
        
        tk.Label(self.right_frame, text="SELECTED BOOK", font=FONT_HEAD, bg="#222", fg=THEME_FG).pack(pady=20)
        
        self.lbl_title = tk.Label(self.right_frame, text="Select a book...", font=("Segoe UI", 12), bg="#222", fg="white", wraplength=200)
        self.lbl_title.pack(pady=10)
        
        self.lbl_details = tk.Label(self.right_frame, text="", font=("Consolas", 11), bg="#222", fg="#aaa")
        self.lbl_details.pack(pady=5)

        self.btn_borrow = tk.Button(self.right_frame, text="BORROW NOW", bg=THEME_FG, fg="white", font=("Segoe UI", 11, "bold"),
                                   state="disabled", command=self.borrow_action)
        self.btn_borrow.pack(pady=20, fill="x", padx=30)

    def build_bag_tab(self):
        tk.Label(self.tab_bag, text="CURRENTLY BORROWED", font=FONT_HEAD, bg=THEME_BG, fg="white").pack(pady=10, anchor="w")
        
        cols = ("TransID", "Title", "Issued On", "Due Date", "BookID")
        self.tree_bag = ttk.Treeview(self.tab_bag, columns=cols, show="headings")
        self.tree_bag.heading("Title", text="Book Title")
        self.tree_bag.heading("Issued On", text="Issued Date")
        self.tree_bag.heading("Due Date", text="Due Date")
        
        self.tree_bag.column("TransID", width=0, stretch=False)
        self.tree_bag.column("BookID", width=0, stretch=False)
        
        self.tree_bag.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Action Buttons Frame
        btn_frame = tk.Frame(self.tab_bag, bg=THEME_BG)
        btn_frame.pack(fill="x", pady=10, padx=10)

        tk.Button(btn_frame, text="RETURN BOOK", bg="#0f3460", fg="white", font=("Segoe UI", 10), 
                 command=self.return_action).pack(side="left", fill="x", expand=True, padx=5)
        
        tk.Button(btn_frame, text=f"REQUEST EXTENSION (+{EXTENSION_DAYS} Days / ${EXTENSION_COST})", 
                 bg="#e94560", fg="white", font=("Segoe UI", 10, "bold"), 
                 command=self.extend_action).pack(side="left", fill="x", expand=True, padx=5)

    # --- LOGIC HANDLERS ---

    def add_funds_action(self):
        amount = simpledialog.askfloat("Add Funds", "Enter amount to add to wallet ($):", minvalue=1.0, maxvalue=1000.0)
        if amount:
            new_bal = self.db.add_funds(self.user, amount)
            self.update_wallet()
            messagebox.showinfo("Success", f"${amount} added to wallet!\nNew Balance: ${new_bal:.2f}")

    def extend_action(self):
        sel = self.tree_bag.focus()
        if not sel:
            messagebox.showwarning("Selection", "Please select a book to extend.")
            return

        vals = self.tree_bag.item(sel, 'values')
        trans_id = vals[0]
        title = vals[1]
        due_date = vals[3]

        msg = f"Extend '{title}' by {EXTENSION_DAYS} days?\n\nFee: ${EXTENSION_COST} will be deducted."
        if messagebox.askyesno("Confirm Extension", msg):
            success, info = self.db.extend_due_date(trans_id, due_date, self.user)
            if success:
                messagebox.showinfo("Extended", f"Success! New Due Date: {info}")
                self.refresh_bag()
                self.update_wallet()
            else:
                messagebox.showerror("Failed", info)

    def refresh_store(self):
        self.tree_store.delete(*self.tree_store.get_children())
        books = self.db.get_books(available_only=True)
        for b in books:
            self.tree_store.insert("", "end", values=(b[0], b[1], b[2], f"${b[3]}", f"{b[4]} Days"))

    def refresh_bag(self):
        self.tree_bag.delete(*self.tree_bag.get_children())
        books = self.db.get_my_books(self.user)
        for b in books:
            self.tree_bag.insert("", "end", values=b)

    def on_book_select(self, event):
        sel = self.tree_store.focus()
        if sel:
            vals = self.tree_store.item(sel, 'values')
            self.lbl_title.config(text=vals[1])
            self.lbl_details.config(text=f"Author: {vals[2]}\n\nPrice: {vals[3]}\nDuration: {vals[4]}")
            self.btn_borrow.config(state="normal")
            self.selected_book_data = vals

    def borrow_action(self):
        b_id = self.selected_book_data[0]
        price = int(self.selected_book_data[3].replace("$", ""))
        days = int(self.selected_book_data[4].replace(" Days", ""))

        success, msg = self.db.borrow_book(b_id, price, days, self.user)
        
        if success:
            messagebox.showinfo("Success", f"Book Borrowed!\nDue Date set for {days} days from now.")
            self.refresh_store()
            self.refresh_bag()
            self.update_wallet()
            self.btn_borrow.config(state="disabled")
            self.lbl_title.config(text="Select a book...")
            self.lbl_details.config(text="")
        else:
            messagebox.showerror("Error", msg)

    def return_action(self):
        sel = self.tree_bag.focus()
        if not sel:
            return
        
        vals = self.tree_bag.item(sel, 'values')
        trans_id = vals[0]
        book_id = vals[4]
        
        if messagebox.askyesno("Return", f"Return '{vals[1]}'?"):
            self.db.return_book(trans_id, book_id)
            messagebox.showinfo("Returned", "Book returned successfully.")
            self.refresh_bag()
            self.refresh_store()

    def update_wallet(self):
        bal = self.db.get_wallet(self.user)
        self.lbl_wallet.config(text=f"Wallet: ${bal:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()