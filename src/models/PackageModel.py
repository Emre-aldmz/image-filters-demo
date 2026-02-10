from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        return "list" if isinstance(values.get('value'), list) else "object"
    class Config: title = "Main Image"

class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        return "list" if isinstance(values.get('value'), list) else "object"
    class Config: title = "Second Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        return "list" if isinstance(values.get('value'), list) else "object"
    class Config: title = "Result Image"

class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: str
    type: Literal["string"] = "string"
    class Config: title = "Status Message"

class ManualThreshVal(Config):
    name: Literal["thresh_val"] = "thresh_val"
    value: int = Field(default=127, ge=0, le=255)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Threshold Value"

class GrayOptionManual(Config):
    name: Literal["manual_mode"] = "manual_mode"
    value: ManualThreshVal
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Manual Threshold"

class AutoBoolVal(Config):
    name: Literal["use_auto"] = "use_auto"
    value: bool = Field(default=True)
    type: Literal["bool"] = "bool"
    field: Literal["checkbox"] = "checkbox"
    class Config: title = "Use Auto Threshold"

class GrayOptionAuto(Config):
    name: Literal["auto_mode"] = "auto_mode"
    value: AutoBoolVal
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Auto Threshold"

class GrayscaleSelector(Config):
    name: Literal["gray_selector"] = "gray_selector"
    value: Union[GrayOptionManual, GrayOptionAuto]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: 
        title = "Grayscale Method"
        json_schema_extra = {"target": "value"}

class GrayscaleConfigs(Configs):
    setting: GrayscaleSelector

class GrayscaleInputs(Inputs):
    inputImage: InputImage

class GrayscaleOutputs(Outputs):
    outputImage: OutputImage

class GrayscaleRequest(Request):
    inputs: Optional[GrayscaleInputs]
    configs: GrayscaleConfigs
    class Config: json_schema_extra = {"target": "configs"}

class GrayscaleResponse(Response):
    outputs: GrayscaleOutputs

class GrayscaleExecutor(Config):
    name: Literal["GrayscaleTask"] = "GrayscaleTask"
    value: Union[GrayscaleRequest, GrayscaleResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Grayscale Filter"
        json_schema_extra = {"target": {"value": 0}}

class OpacityVal(Config):
    name: Literal["opacity_val"] = "opacity_val"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Opacity (0.0 - 1.0)"

class BlendOptionOpacity(Config):
    name: Literal["opacity_mode"] = "opacity_mode"
    value: OpacityVal
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Weighted Blend"

class TextVal(Config):
    name: Literal["watermark_text"] = "watermark_text"
    value: str = Field(default="Demo")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Watermark Text"

class BlendOptionText(Config):
    name: Literal["text_mode"] = "text_mode"
    value: TextVal
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Text Overlay"

class BlenderSelector(Config):
    name: Literal["blend_selector"] = "blend_selector"
    value: Union[BlendOptionOpacity, BlendOptionText]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: 
        title = "Blender Method"
        json_schema_extra = {"target": "value"}

class BlenderConfigs(Configs):
    setting: BlenderSelector

class BlenderInputs(Inputs):
    inputImage: InputImage
    inputImage2: InputImage2

class BlenderOutputs(Outputs):
    outputImage: OutputImage
    outputMessage: OutputMessage

class BlenderRequest(Request):
    inputs: Optional[BlenderInputs]
    configs: BlenderConfigs
    class Config: json_schema_extra = {"target": "configs"}

class BlenderResponse(Response):
    outputs: BlenderOutputs

class BlenderExecutor(Config):
    name: Literal["BlenderTask"] = "BlenderTask"
    value: Union[BlenderRequest, BlenderResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Image Blender"
        json_schema_extra = {"target": {"value": 1}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GrayscaleExecutor, BlenderExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    
    restart: Literal[True] = True

    class Config:
        title = "Select Task"
        json_schema_extra = {"target": "value"}

class PackageConfigsOuter(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigsOuter
    type: Literal["component"] = "component"
    name: Literal["ImageFilters"] = "ImageFilters"
