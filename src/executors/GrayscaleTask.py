"""
    GrayscaleTask — Converts input image to grayscale using threshold or auto mode.
"""

import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageFilters.src.utils.response import build_grayscale_response
from components.ImageFilters.src.models.PackageModel import PackageModel


class GrayscaleTask(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.req_data = self.request.model.configs.executor.value.value
        self.image = self.req_data.inputs.inputImage

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        selector = self.req_data.configs.gray_selector
        mode = selector.value

        if mode.name == "manual_mode":
            thresh_val = mode.thresh_val.value
            gray = cv2.cvtColor(img.value, cv2.COLOR_BGR2GRAY)
            _, result = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
            img.value = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

        elif mode.name == "auto_mode":
            img.value = cv2.cvtColor(img.value, cv2.COLOR_BGR2GRAY)
            img.value = cv2.cvtColor(img.value, cv2.COLOR_GRAY2BGR)

        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_grayscale_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
