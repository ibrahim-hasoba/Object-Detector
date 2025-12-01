"""YOLO model management"""

from typing import Optional, Tuple, Dict, List
import logging
from ultralytics import YOLO

logger = logging.getLogger(__name__)


class ModelManager:
    """Handles YOLO model loading and operations"""
    
    def __init__(self):
        self.model: Optional[YOLO] = None
    
    def load_model(self, model_options: List[str]) -> Tuple[bool, str]:
        """
        Attempt to load YOLO model from available options
        
        Args:
            model_options: List of model file names to try
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        for model_name in model_options:
            try:
                logger.info(f"Attempting to load model: {model_name}")
                self.model = YOLO(model_name)
                logger.info(f"Successfully loaded: {model_name}")
                return True, f"✓ تم تحميل {model_name} بنجاح"
            except Exception as e:
                logger.error(f"Failed to load {model_name}: {str(e)}")
                continue
        
        return False, "✗ فشل تحميل الموديل"
    
    def get_class_names(self) -> Dict[int, str]:
        """
        Get available class names from model
        
        Returns:
            Dictionary mapping class IDs to names
        """
        if self.model:
            return self.model.names
        return {}
    
    def detect(self, image, confidence: float):
        """
        Run detection on image
        
        Args:
            image: Input image (numpy array)
            confidence: Confidence threshold
            
        Returns:
            Detection results
            
        Raises:
            RuntimeError: If model is not loaded
        """
        if not self.model:
            raise RuntimeError("Model not loaded")
        return self.model(image, conf=confidence)
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None

