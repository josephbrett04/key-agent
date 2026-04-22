import tkinter as tk
import sys
import os

# Ensure Python can find the subfolders
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine_keaton.dashboard_ui import DashboardUI

def main():
    print("Launching Key Agent GUI...")
    # Required for the SRS: The GUI must remain open and not minimize
    root = tk.Tk()
    app = DashboardUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()