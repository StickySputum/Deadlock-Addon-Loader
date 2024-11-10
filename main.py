from tkinter import Tk
from app.gui import DeadlockAddonManager

if __name__ == "__main__":
    root = Tk()
    app = DeadlockAddonManager(root)
    root.mainloop()
