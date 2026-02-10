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

class BlenderTask(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.config_data = self.request.model.configs.executor.value
        self.outputImage = None
        self.outputMessage = None

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        req_inputs = self.config_data.inputs
        if not req_inputs: return build_response(context=self)

        in1 = req_inputs.inputImage
        ref1 = in1[0] if isinstance(in1, list) else in1
        img_obj1 = Image.get_frame(img=ref1, redis_db=self.redis_db)
        
        if img_obj1 is None: return build_response(context=self)
        main_img = img_obj1.value.copy()

        in2 = req_inputs.inputImage2
        ref2 = in2[0] if isinstance(in2, list) else in2
        img_obj2 = Image.get_frame(img=ref2, redis_db=self.redis_db)

        setting_wrapper = self.config_data.configs.setting.value
        mode_name = setting_wrapper.name
        
        msg = "Ready"

        if mode_name == "opacity_mode":
            val = float(setting_wrapper.value.value)
            msg = f"Blend Opacity: {val}"
            
            if img_obj2 and img_obj2.value is not None:
                sec_img = img_obj2.value
                h, w, _ = main_img.shape
                sec_resized = cv2.resize(sec_img, (w, h))
                main_img = cv2.addWeighted(main_img, val, sec_resized, 1.0 - val, 0.0)
            else:
                msg = "ERROR: No 2nd Image"
                cv2.putText(main_img, "NO IMG 2", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

        elif mode_name == "text_mode":
            txt = str(setting_wrapper.value.value)
            msg = f"Text Overlay: {txt}"
            cv2.putText(main_img, txt, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            
        cv2.putText(main_img, "TASK 2: BLENDER", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        img_obj1.value = main_img
        self.outputImage = Image.set_frame(img=img_obj1, package_uID=self.uID, redis_db=self.redis_db)
        self.outputMessage = str(msg)
        
        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
