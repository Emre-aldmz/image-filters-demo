import os
import cv2
import sys
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

try:
    from models.PackageModel import PackageModel
    from utils.response import build_response
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
    from components.ImageFilters.src.models.PackageModel import PackageModel
    from components.ImageFilters.src.utils.response import build_response

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.executor_config = self.request.model.configs.executor
        self.active_request = self.executor_config.value.value
        self.outputImage = None
        self.outputMessage = None   

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run_grayscale(self):
        print("DEBUG: Grayscale Gorevi Baslatiliyor...")
        
        if not self.active_request.inputs or not self.active_request.inputs.inputImage:
            print("HATA: Giris resmi yok!")
            return
            
        img_input = self.active_request.inputs.inputImage
        img_ref = img_input[0] if isinstance(img_input, list) else img_input
        
        img_obj = Image.get_frame(img=img_ref, redis_db=self.redis_db)
        if img_obj is None or img_obj.value is None: return

        setting_obj = self.active_request.configs.setting.value  
        setting_name = setting_obj.name 
        
        result = img_obj.value.copy()
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        
        thresh_val = 127
        mode_text = "AUTO"
        
        if setting_name == "manual_mode":
            thresh_val = int(setting_obj.value.value)
            mode_text = f"MANUAL: {thresh_val}"
            _, result = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
            
        elif setting_name == "auto_mode":
            use_auto = bool(setting_obj.value.value)
            mode_text = f"AUTO: {use_auto}"
            if use_auto:
                thresh_val, result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            else:
                result = gray

        if len(result.shape) == 2:
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            
        cv2.putText(result, f"TASK 1: {mode_text}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        img_obj.value = result
        self.outputImage = Image.set_frame(img=img_obj, package_uID=self.uID, redis_db=self.redis_db)

    def run_blender(self):
        print("DEBUG: Blender Gorevi Baslatiliyor...")
        
        if not self.active_request.inputs: return
        
        in1 = self.active_request.inputs.inputImage
        ref1 = in1[0] if isinstance(in1, list) else in1
        img_obj1 = Image.get_frame(img=ref1, redis_db=self.redis_db)
        
        in2 = self.active_request.inputs.inputImage2
        ref2 = in2[0] if isinstance(in2, list) else in2
        img_obj2 = Image.get_frame(img=ref2, redis_db=self.redis_db)
        
        if img_obj1 is None: return
        
        main_img = img_obj1.value.copy()
        
        setting_obj = self.active_request.configs.setting.value
        setting_name = setting_obj.name 
        
        msg = "Islem Basarili"
        
        if setting_name == "opacity_mode":
            opacity = float(setting_obj.value.value)
            msg = f"Blend Modu. Opaklik: {opacity}"
            
            if img_obj2 is not None and img_obj2.value is not None:
                sec_img = img_obj2.value
                h, w, _ = main_img.shape
                sec_resized = cv2.resize(sec_img, (w, h))
                main_img = cv2.addWeighted(main_img, opacity, sec_resized, 1.0 - opacity, 0.0)
            else:
                msg = "HATA: 2. Resim Yok!"
                cv2.putText(main_img, "NO 2ND IMAGE", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

        elif setting_name == "text_mode":
            text_to_write = str(setting_obj.value.value)
            msg = f"Yazi Modu: {text_to_write}"
            cv2.putText(main_img, text_to_write, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            
        cv2.putText(main_img, "TASK 2: BLENDER", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        img_obj1.value = main_img
        self.outputImage = Image.set_frame(img=img_obj1, package_uID=self.uID, redis_db=self.redis_db)
        self.outputMessage = str(msg)

    def run(self):
        print(f"DEBUG: Secilen Gorev -> {self.task_name}")
        
        if self.task_name == "GrayscaleTask":
            self.run_grayscale()
        elif self.task_name == "BlenderTask":
            self.run_blender()
        else:
            print(f"Bilinmeyen Gorev: {self.task_name}")
        
        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
