class Config:
    """Application configuration constants"""
    WINDOW_SIZE = "1200x750"
    WINDOW_TITLE = " Object Detector - كاشف الكائنات "
    
    # Colors
    COLOR_PRIMARY = "#2c3e50"
    COLOR_SUCCESS = "#27ae60"
    COLOR_DANGER = "#e74c3c"
    COLOR_INFO = "#3498db"
    COLOR_BG = "#f0f0f0"
    COLOR_PANEL = "#ecf0f1"
    
    # Model settings
    MODEL_OPTIONS = ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"]
    DEFAULT_CONFIDENCE = 0.25
    CONFIDENCE_RANGE = (0.1, 0.9)
    CONFIDENCE_STEP = 0.05
    
    # Display settings
    MAX_DISPLAY_WIDTH = 700
    MAX_DISPLAY_HEIGHT = 550
    INFO_PANEL_WIDTH = 35
    
    # File types
    IMAGE_FILETYPES = [
        ("صور", "*.jpg *.jpeg *.png *.bmp *.gif"),
        ("جميع الملفات", "*.*")
    ]
    SAVE_FILETYPES = [
        ("JPEG", "*.jpg"),
        ("PNG", "*.png"),
        ("جميع الملفات", "*.*")
    ]