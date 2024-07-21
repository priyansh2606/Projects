import subprocess
import tkinter as tk

# Global variables to store connection and cursor objects
con = None
cursor = None

def connect_to_db():
    global con, cursor
    
    # Get connection details from the input fields
    global username, password
    username = username_entry.get()
    password = password_entry.get()
    hostname = "asus-pc"  # Default hostname
    port = "1521"  # Default port
    service_name = "XE"  # Default service name
    
    # Construct the SQL*Plus command
    sqlplus_command = f"sqlplus {username}/{password}@{hostname}:{port}/{service_name}"

    try:
        # Execute the SQL*Plus command
        sqlplus_process = subprocess.Popen(sqlplus_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        # Create connection and cursor objects
        con = sqlplus_process
        cursor = sqlplus_process.stdin

        # Disable username and password entry fields
        username_entry.config(state="disabled")
        password_entry.config(state="disabled")

        # Enable SQL query entry field and buttons
        sql_query_entry.config(state="normal")
        run_button.config(state="normal")
        clear_button.config(state="normal")
        exit_button.config(state="normal")
        
        # Display message
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Connected to database.")
    except Exception as e:
        error_text.delete(1.0, tk.END)
        error_text.insert(tk.END, f"An error occurred: {e}")

def run_sqlplus():
    global con, cursor
    connect_to_db()
    # Check if the connection is established
    if con is None or cursor is None:
        error_text.delete(1.0, tk.END)
        error_text.insert(tk.END, "Please connect to the database first.")
        return

    # Get SQL queries from the input field
    queries = sql_query_entry.get("1.0", tk.END).strip().split(";")
    
    try:
        # Execute each SQL query
        for query in queries:
            if query.strip():
                cursor.write((query.strip() + ";\n").encode())
        cursor.write(b"COMMIT;\n")  # Ensure changes are committed
        cursor.flush()  # Flush the buffer

        # Read the output until EOF is reached
        stdout, stderr = con.communicate()

        # Display the output
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, stdout.decode())

        # Check for errors
        if stderr:
            error_text.delete(1.0, tk.END)
            error_text.insert(tk.END, stderr.decode())
    except Exception as e:
        error_text.delete(1.0, tk.END)
        error_text.insert(tk.END, f"An error occurred: {e}")

def clear_text():
    # Clear input and output text boxes
    sql_query_entry.delete(1.0, tk.END)
    output_text.delete(1.0, tk.END)
    error_text.delete(1.0, tk.END)

def exit_program():
    # Close the application
    window.destroy()

# Create a Tkinter window
window = tk.Tk()
window.title("DBMS GUI")

# Set window size
window.geometry("900x900")

# Create a frame for the input fields
input_frame = tk.Frame(window)
input_frame.pack(pady=10)

# Create input fields
tk.Label(input_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(input_frame, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(input_frame, show="*", font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Create buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=5)

connect_button = tk.Button(button_frame, text="Connect to DB", command=connect_to_db, font=("Arial", 12))
connect_button.grid(row=0, column=0, padx=5, pady=5)

run_button = tk.Button(button_frame, text="Run SQL*Plus", command=run_sqlplus, state="disabled", font=("Arial", 12))
run_button.grid(row=0, column=1, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear Box", command=clear_text, state="disabled", font=("Arial", 12))
clear_button.grid(row=0, column=2, padx=5, pady=5)

exit_button = tk.Button(button_frame, text="Exit", command=exit_program, state="disabled", font=("Arial", 12))
exit_button.grid(row=0, column=3, padx=5, pady=5)

# Create SQL query entry field
tk.Label(window, text="SQL Queries:", font=("Arial", 12)).pack()
sql_query_entry = tk.Text(window, height=5, width=70, state="disabled", font=("Arial", 12))
sql_query_entry.pack(padx=10, pady=5)

# Create output and error display
output_text = tk.Text(window, height=35, width=90, font=("Arial", 12))
output_text.pack(padx=10, pady=(5, 10))

error_text = tk.Text(window, height=3, width=90, font=("Arial", 12))
error_text.pack(padx=10, pady=(0, 5))

# Run the Tkinter event loop
window.mainloop()