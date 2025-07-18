import sys
from PyQt5.QtWidgets import QApplication
from database import initialize_db, close_db
from gui import ExpenseTrackerApp

def main():
    # Initialize the database (create tables if needed)
    initialize_db()

    # Start the GUI application
    app = ExpenseTrackerApp()
    app.mainloop()

    # Handle app closure and cleanup
    close_db()
    sys.exit()

if __name__ == "__main__":
    main()