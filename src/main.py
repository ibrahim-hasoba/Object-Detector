import tkinter as tk
import logging

from app import YOLODetectorApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    """Application entry point"""
    root = tk.Tk()
    app = YOLODetectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()