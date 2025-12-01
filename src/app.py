import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from PIL import Image, ImageTk
from typing import Optional
import logging

from config import Config
from model_manager import ModelManager
from image_processor import ImageProcessor
from detection_analyzer import DetectionAnalyzer

logger = logging.getLogger(__name__)


class YOLODetectorApp:
    """Main application class"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.config = Config()
        self.model_manager = ModelManager()
        self.image_processor = ImageProcessor()
        self.analyzer = DetectionAnalyzer()
        
        self.current_image_path: Optional[str] = None
        self.result_image: Optional[any] = None
        
        self._setup_window()
        self._setup_ui()
        self._initialize_model()
    
    def _setup_window(self):
        """Configure main window"""
        self.root.title(self.config.WINDOW_TITLE)
        self.root.geometry(self.config.WINDOW_SIZE)
        self.root.configure(bg=self.config.COLOR_BG)
    
    def _setup_ui(self):
        """Create user interface"""
        self._create_title_bar()
        self._create_control_panel()
        self._create_progress_bar()
        self._create_main_content()
        self._create_status_bar()
    
    def _create_title_bar(self):
        """Create title bar"""
        title_frame = tk.Frame(self.root, bg=self.config.COLOR_PRIMARY, height=80)
        title_frame.pack(fill=tk.X)
        
        tk.Label(
            title_frame,
            text="🎯 كاشف الكائنات ",
            font=("Arial", 18, "bold"),
            bg=self.config.COLOR_PRIMARY,
            fg="white"
        ).pack(pady=20)
    
    def _create_control_panel(self):
        """Create control panel with buttons and settings"""
        control_frame = tk.Frame(self.root, bg=self.config.COLOR_BG)
        control_frame.pack(pady=10)
        
        # Buttons row
        btn_row = tk.Frame(control_frame, bg=self.config.COLOR_BG)
        btn_row.pack(pady=5)
        
        self.select_btn = self._create_button(
            btn_row, "📁 اختر صورة", self.detect_objects, 
            self.config.COLOR_INFO
        )
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = self._create_button(
            btn_row, "💾 حفظ النتيجة", self.save_result, 
            self.config.COLOR_SUCCESS, state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = self._create_button(
            btn_row, "🔄 إعادة تعيين", self.reset, 
            self.config.COLOR_DANGER
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Settings row
        self._create_confidence_slider(control_frame)
    
    def _create_button(self, parent, text: str, command, bg_color: str, 
                      state=tk.NORMAL) -> tk.Button:
        """Create styled button"""
        return tk.Button(
            parent, text=text, command=command, font=("Arial", 11, "bold"),
            bg=bg_color, fg="white", padx=15, pady=8, 
            cursor="hand2", state=state
        )
    
    def _create_confidence_slider(self, parent):
        """Create confidence threshold slider"""
        settings_row = tk.Frame(parent, bg=self.config.COLOR_BG)
        settings_row.pack(pady=5)
        
        tk.Label(
            settings_row, text="🎚️ نسبة الثقة:", font=("Arial", 10, "bold"),
            bg=self.config.COLOR_BG
        ).pack(side=tk.LEFT, padx=5)
        
        self.confidence_var = tk.DoubleVar(value=self.config.DEFAULT_CONFIDENCE)
        
        tk.Scale(
            settings_row, from_=self.config.CONFIDENCE_RANGE[0],
            to=self.config.CONFIDENCE_RANGE[1],
            resolution=self.config.CONFIDENCE_STEP,
            orient=tk.HORIZONTAL, variable=self.confidence_var,
            length=200, bg=self.config.COLOR_BG
        ).pack(side=tk.LEFT, padx=5)
        
        self.conf_label = tk.Label(
            settings_row, text=f"{self.config.DEFAULT_CONFIDENCE:.2f}",
            font=("Arial", 10, "bold"), bg=self.config.COLOR_BG, width=4
        )
        self.conf_label.pack(side=tk.LEFT, padx=5)
        
        self.confidence_var.trace('w', self._update_confidence_label)
    
    def _create_progress_bar(self):
        """Create progress bar"""
        self.progress = ttk.Progressbar(
            self.root, mode='indeterminate', length=400
        )
    
    def _create_main_content(self):
        """Create main content area"""
        main_frame = tk.Frame(self.root, bg=self.config.COLOR_BG)
        main_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Image panel
        self._create_image_panel(main_frame)
        
        # Info panel
        self._create_info_panel(main_frame)
    
    def _create_image_panel(self, parent):
        """Create image display panel"""
        left_frame = tk.Frame(
            parent, bg="white", relief=tk.SUNKEN, borderwidth=2
        )
        left_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        self.panel = tk.Label(
            left_frame,
            text="لم يتم اختيار صورة بعد\n\nاضغط على 'اختر صورة' للبدء",
            font=("Arial", 12), bg="white", fg="gray"
        )
        self.panel.pack(expand=True)
    
    def _create_info_panel(self, parent):
        """Create information panel"""
        right_frame = tk.Frame(
            parent, bg=self.config.COLOR_PANEL, 
            relief=tk.SUNKEN, borderwidth=2
        )
        right_frame.pack(side=tk.RIGHT, padx=5, fill=tk.BOTH)
        right_frame.config(width=300)
        
        tk.Label(
            right_frame, text="📊 معلومات الكشف",
            font=("Arial", 12, "bold"), bg=self.config.COLOR_PRIMARY,
            fg="white", pady=8
        ).pack(fill=tk.X)
        
        self.info_text = scrolledtext.ScrolledText(
            right_frame, width=self.config.INFO_PANEL_WIDTH, height=30,
            font=("Courier", 9), bg=self.config.COLOR_PANEL, wrap=tk.WORD
        )
        self.info_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
    
    def _create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(
            self.root, bg=self.config.COLOR_PRIMARY, height=40
        )
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame, text="في انتظار التحميل...",
            font=("Arial", 10), bg=self.config.COLOR_PRIMARY,
            fg="white", anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=8)
    
    def _initialize_model(self):
        """Initialize YOLO model"""
        self._update_status("جاري تحميل الموديل...")
        
        success, message = self.model_manager.load_model(
            self.config.MODEL_OPTIONS
        )
        
        if success:
            self._update_status(message)
            self._display_available_classes()
        else:
            self._show_model_error()
            self._update_status(message)
    
    def _show_model_error(self):
        """Show model loading error dialog"""
        messagebox.showerror(
            "خطأ",
            "فشل تحميل الموديل!\n\n"
            "الحلول:\n"
            "1. تأكد من الاتصال بالإنترنت\n"
            "2. حمل الموديل يدوياً من:\n"
            "   https://github.com/ultralytics/assets/releases\n"
            "3. ضع ملف yolov8n.pt في نفس مجلد البرنامج"
        )
    
    def _display_available_classes(self):
        """Display available detection classes"""
        class_names = self.model_manager.get_class_names()
        info_text = self.analyzer.format_class_list(class_names)
        self._update_info_panel(info_text)
    
    def _update_confidence_label(self, *args):
        """Update confidence label"""
        self.conf_label.config(text=f"{self.confidence_var.get():.2f}")
    
    def _update_status(self, message: str):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update()
    
    def _update_info_panel(self, text: str):
        """Update information panel text"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
    
    def _show_progress(self):
        """Show progress bar"""
        self.progress.pack(pady=5)
        self.progress.start(10)
    
    def _hide_progress(self):
        """Hide progress bar"""
        self.progress.stop()
        self.progress.pack_forget()
    
    def detect_objects(self):
        """Main detection workflow"""
        if not self.model_manager.is_loaded():
            messagebox.showerror("خطأ", "الموديل غير محمل!")
            return
        
        path = filedialog.askopenfilename(
            title="اختر صورة",
            filetypes=self.config.IMAGE_FILETYPES
        )
        
        if not path:
            return
        
        self._process_image(path)
    
    def _process_image(self, path: str):
        """Process image and run detection"""
        try:
            self.current_image_path = path
            self._update_status("جاري معالجة الصورة...")
            self._show_progress()
            
            # Load image
            image = self.image_processor.load_image(path)
            if image is None:
                raise ValueError("فشل قراءة الصورة")
            
            # Run detection
            conf_threshold = self.confidence_var.get()
            results = self.model_manager.detect(image, conf_threshold)
            
            # Process results
            annotated = results[0].plot()
            annotated = self.image_processor.bgr_to_rgb(annotated)
            
            # Store and display
            self.result_image = annotated.copy()
            self._display_result(annotated, results[0], conf_threshold)
            
            self.save_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            logger.error(f"Detection error: {str(e)}")
            messagebox.showerror(
                "خطأ", 
                f"حدث خطأ أثناء معالجة الصورة:\n{str(e)}"
            )
            self._update_status("✗ فشلت عملية الكشف")
        finally:
            self._hide_progress()
    
    def _display_result(self, image, result, confidence: float):
        """Display detection results"""
        # Resize for display
        display_image = self.image_processor.resize_for_display(
            image, 
            self.config.MAX_DISPLAY_WIDTH,
            self.config.MAX_DISPLAY_HEIGHT
        )
        
        # Update image panel
        img = Image.fromarray(display_image)
        img_tk = ImageTk.PhotoImage(img)
        self.panel.configure(image=img_tk, text="")
        self.panel.image = img_tk
        
        # Analyze and display statistics
        stats = self.analyzer.analyze_results(
            result, 
            self.model_manager.get_class_names()
        )
        info_text = self.analyzer.format_statistics(stats)
        self._update_info_panel(info_text)
        
        # Update status
        detected_count = stats["count"]
        self._update_status(
            f"✓ تم اكتشاف {detected_count} كائن في الصورة "
            f"(ثقة: {confidence:.2f})"
        )
    
    def save_result(self):
        """Save detection result"""
        if self.result_image is None:
            messagebox.showwarning("تحذير", "لا توجد نتائج لحفظها!")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=self.config.SAVE_FILETYPES
        )
        
        if not save_path:
            return
        
        result_bgr = self.image_processor.rgb_to_bgr(self.result_image)
        
        if self.image_processor.save_image(result_bgr, save_path):
            messagebox.showinfo(
                "نجح", 
                f"تم حفظ الصورة في:\n{save_path}"
            )
            self._update_status("✓ تم حفظ النتيجة")
        else:
            messagebox.showerror("خطأ", "فشل حفظ الصورة")
    
    def reset(self):
        """Reset application state"""
        self.panel.configure(
            image='',
            text="لم يتم اختيار صورة بعد\n\nاضغط على 'اختر صورة' للبدء"
        )
        self.panel.image = None
        self.current_image_path = None
        self.result_image = None
        self.save_btn.config(state=tk.DISABLED)
        self._update_status("✓ تم إعادة التعيين - جاهز للاستخدام")
        self._display_available_classes()