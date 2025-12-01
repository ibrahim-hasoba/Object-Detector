from typing import Dict


class DetectionAnalyzer:
    """Analyzes detection results and generates statistics"""
    
    @staticmethod
    def analyze_results(result, model_names: Dict[int, str]) -> Dict:
        """
        Analyze detection results and return statistics
        
        Args:
            result: YOLO detection result
            model_names: Dictionary of class names
            
        Returns:
            Dictionary containing detection statistics:
            - count: Total number of detections
            - objects: Dict of object types and their confidences
            - unique_types: Number of unique object types
        """
        boxes = result.boxes
        
        if len(boxes) == 0:
            return {"count": 0, "objects": {}, "unique_types": 0}
        
        objects_dict = {}
        
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = model_names[cls_id]
            
            if class_name not in objects_dict:
                objects_dict[class_name] = []
            objects_dict[class_name].append(conf)
        
        return {
            "count": len(boxes),
            "objects": objects_dict,
            "unique_types": len(objects_dict)
        }
    
    @staticmethod
    def format_statistics(stats: Dict) -> str:
        """
        Format detection statistics as readable text
        
        Args:
            stats: Statistics dictionary from analyze_results
            
        Returns:
            Formatted text string
        """
        if stats["count"] == 0:
            return (
                "❌ لم يتم اكتشاف أي كائنات\n\n"
                "💡 نصائح:\n"
                "• قلل نسبة الثقة\n"
                "• جرب صورة أوضح\n"
                "• تأكد من وجود كائنات من القائمة المدعومة\n"
            )
        
        info = f"✅ تم اكتشاف {stats['count']} كائن\n"
        info += "=" * 40 + "\n\n"
        info += "📈 الإحصائيات:\n"
        info += "-" * 40 + "\n"
        
        for idx, (obj_name, confidences) in enumerate(
            sorted(stats["objects"].items()), 1
        ):
            count = len(confidences)
            avg_conf = sum(confidences) / count
            max_conf = max(confidences)
            
            info += f"{idx}. {obj_name.upper()}\n"
            info += f"   العدد: {count}\n"
            info += f"   متوسط الثقة: {avg_conf:.2%}\n"
            info += f"   أعلى ثقة: {max_conf:.2%}\n\n"
        
        info += "=" * 40 + "\n"
        info += f"إجمالي الكائنات: {stats['count']}\n"
        info += f"أنواع مختلفة: {stats['unique_types']}\n"
        
        return info
    
    @staticmethod
    def format_class_list(class_names: Dict[int, str]) -> str:
        """
        Format available classes as readable text
        
        Args:
            class_names: Dictionary of class names
            
        Returns:
            Formatted text string
        """
        classes_list = list(class_names.values())
        info = f"📋 الفئات المتاحة ({len(classes_list)} فئة):\n\n"
        
        for i in range(0, len(classes_list), 4):
            row = classes_list[i:i+4]
            info += "  •  " + "  •  ".join(row) + "\n"
        
        return info