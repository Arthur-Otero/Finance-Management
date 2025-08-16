#!/usr/bin/env python3
"""
Finance Control Application
A modular application for managing financial records with visual interface
"""

from gui.main_window import MainWindow

def main():
    """Main entry point of the application"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()