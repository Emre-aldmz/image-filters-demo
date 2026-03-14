"""
    BlenderTask — Blends two input images using opacity or adds a text watermark.
"""

import os
import cv2
import sys
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.model import Image as ImageModel
from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageFilters.src.utils.response import build_blender_response
from components.ImageFilters.src.models.PackageModel import PackageModel


class BlenderTask(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.req_data = self.request.model.configs.executor.value.value
        self.image = self.req_data.inputs.inputImage
        self.image2 = self.req_data.inputs.inputImage2
        self.message = ""

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        img1 = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image2, redis_db=self.redis_db)

        selector = self.req_data.configs.blend_selector
        mode = selector.value

        if mode.name == "opacity_mode":
            opacity_val = mode.opacity_val.value
            opacity_val = max(0.0, min(1.0, opacity_val))

            h1, w1 = img1.value.shape[:2]
            img2_resized = cv2.resize(img2.value, (w1, h1))

            blended = cv2.addWeighted(img1.value, opacity_val, img2_resized, 1.0 - opacity_val, 0)
            img1.value = blended
            self.message = f"Blended with opacity: {opacity_val}"

        elif mode.name == "text_mode":
            watermark_text = mode.watermark_text.value
            h, w = img1.value.shape[:2]
            position = (int(w * 0.05), int(h * 0.95))
            cv2.putText(
                img1.value,
                watermark_text,
                position,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )
            self.message = f"Watermark applied: {watermark_text}"

        self.image = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_blender_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
