import tkinter as tk

# Define root
root = tk.Tk()

def show_login_screen():
    # Hide the current screen
    root.withdraw()

    # Create the login screen
    login_screen = tk.Toplevel(root)
    # Add widgets to the login screen here
    # ...

    # Show the login screen
    login_screen.deiconify()

def show_main_screen():
    # Hide the current screen
    root.withdraw()

    # Create the main screen
    main_screen = tk.Toplevel(root)
    # Add widgets to the main screen here
    # ...

    # Show the main screen
    main_screen.deiconify()

# Show the login screen initially
show_login_screen()

# Start the main loop
root.mainloop()
