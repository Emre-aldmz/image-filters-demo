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

class GrayscaleTask(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        self.req_data = self.request.model.configs.executor.value.value
        
        self.outputImage = None

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # self.req_data kullanıyoruz
        req_inputs = self.req_data.inputs
        if not req_inputs or not req_inputs.inputImage:
            return build_response(context=self)

        img_in = req_inputs.inputImage
        img_ref = img_in[0] if isinstance(img_in, list) else img_in
        
        img_obj = Image.get_frame(img=img_ref, redis_db=self.redis_db)
        if img_obj is None or img_obj.value is None:
            return build_response(context=self)

        setting_wrapper = self.req_data.configs.setting.value
        mode_name = setting_wrapper.name
        
        img = img_obj.value.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        info_text = "AUTO"
        
        if mode_name == "manual_mode":
            thresh_val = int(setting_wrapper.value.value)
            _, res = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
            info_text = f"MANUAL: {thresh_val}"
        else: 
            use_auto = bool(setting_wrapper.value.value)
            if use_auto:
                _, res = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                info_text = "AUTO: ON"
            else:
                res = gray
                info_text = "AUTO: OFF"
        
        if len(res.shape) == 2:
            res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
            
        cv2.putText(res, f"TASK 1: {info_text}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        img_obj.value = res
        self.outputImage = Image.set_frame(img=img_obj, package_uID=self.uID, redis_db=self.redis_db)
        
        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
