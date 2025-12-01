import cv2
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Handles image processing operations"""
    
    @staticmethod
    def load_image(path: str) -> Optional[any]:
        """
        Load image from file path
        
        Args:
            path: Path to image file
            
        Returns:
            Image as numpy array or None if failed
        """
        try:
            image = cv2.imread(path)
            if image is None:
                raise ValueError(f"Failed to load image: {path}")
            return image
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            return None
    
    @staticmethod
    def resize_for_display(image, max_width: int, max_height: int):
        """
        Resize image to fit display constraints
        
        Args:
            image: Input image
            max_width: Maximum width
            max_height: Maximum height
            
        Returns:
            Resized image
        """
        height, width = image.shape[:2]
        scale = min(max_width / width, max_height / height, 1.0)
        
        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(image, (new_width, new_height), 
                            interpolation=cv2.INTER_AREA)
        return image
    
    @staticmethod
    def bgr_to_rgb(image):
        """Convert BGR to RGB color space"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    @staticmethod
    def rgb_to_bgr(image):
        """Convert RGB to BGR color space"""
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def save_image(image, path: str) -> bool:
        """
        Save image to file
        
        Args:
            image: Image to save
            path: Destination path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cv2.imwrite(path, image)
            return True
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            return False
