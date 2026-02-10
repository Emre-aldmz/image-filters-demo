import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../')) #

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageFilters.src.utils.response import build_response
from components.ImageFilters.src.models.PackageModel import PackageModel

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
         # input unutma
        self.task_settings = self.request.get_param("operation_mode")
        self.image_main = self.request.get_param("inputImage")
        self.image_sec = self.request.get_param("inputImage2")
        
        self.outputImage = None
        self.outputMessage = "Baslangic"

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_image(self, img_main_data, img_sec_data=None):
        result = img_main_data.copy()
        settings_str = str(self.task_settings)
        msg = "Islem Yapildi"

        #  EXECUTOR 1: GRAYSCALE 
        if "gray_mode" in settings_str:
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            thresh = 127
            try:
                if hasattr(self.task_settings, 'value') and hasattr(self.task_settings.value, 'value'):
                    thresh = int(self.task_settings.value.value)
            except:
                pass
            
            _, result = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            
            cv2.putText(result, f"GRAY: {thresh}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            msg = f"Grayscale uygulandi. Esik degeri: {thresh}"

        # EXECUTOR 2: BLENDER 
        elif "blend_mode" in settings_str:
            if img_sec_data is not None:
                h, w, _ = result.shape
                img_sec_resized = cv2.resize(img_sec_data, (w, h))
                
                alpha = 0.5
                try:
                    if hasattr(self.task_settings, 'value') and hasattr(self.task_settings.value, 'value'):
                        alpha = float(self.task_settings.value.value)
                except:
                    pass
                
                beta = 1.0 - alpha
                result = cv2.addWeighted(result, alpha, img_sec_resized, beta, 0.0)
                cv2.putText(result, f"BLEND: {alpha}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                msg = f"Birlestirme yapildi. Opaklik: {alpha}"
            else:
                cv2.putText(result, "2. RESIM YOK!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
                msg = "HATA: Ikinci resim eksik!"
        
        return result, msg

    def run(self):
        # 1. birtinci Resim
        img_obj_main = Image.get_frame(img=self.image_main, redis_db=self.redis_db)
        
        if img_obj_main is None or img_obj_main.value is None:
            return build_response(context=self)

        main_data = img_obj_main.value
        
        # 2. ikinci Resim
        sec_data = None
        if self.image_sec:
            try:
                sec_input = self.image_sec[0] if isinstance(self.image_sec, list) else self.image_sec
                img_obj_sec = Image.get_frame(img=sec_input, redis_db=self.redis_db)
                sec_data = img_obj_sec.value
            except:
                pass

        # 3. isle
        processed_data, message_data = self.process_image(main_data, sec_data)
            
        # 4. kaydet 
        img_obj_main.value = processed_data
        self.outputImage = Image.set_frame(img=img_obj_main, package_uID=self.uID, redis_db=self.redis_db)
        
        # 5. Kaydet 
        self.outputMessage = str(message_data)
        
        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
