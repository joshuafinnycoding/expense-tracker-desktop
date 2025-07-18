import sys
from PyQt5.QtWidgets import QApplication
from database import initialize_db, close_db
from gui import MainWindow

def main():
    # Initialize the database (create tables if needed)
    initialize_db()

    # Start the GUI application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Handle app closure and cleanup
    exit_code = app.exec_()
    close_db()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()