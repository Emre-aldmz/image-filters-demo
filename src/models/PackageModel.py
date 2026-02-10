from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

# INPUTLAR 
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Main Image"

class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Second Image (For Blender)"

# OUTPUTLAR (iki Cikis) 
class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Result Image"

class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: str
    type: Literal["string"] = "string"
    class Config: title = "Status Message"

# AYARLAR

# 1. Grayscale 
class ThreshVal(Config):
    name: Literal["thresh_val"] = "thresh_val"
    value: int = Field(default=127, ge=0, le=255)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Threshold (Int)"

class GrayOption(Config):
    name: Literal["gray_mode"] = "gray_mode"
    value: ThreshVal
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Grayscale Mode"

# 2. Blender 
class OpacityVal(Config):
    name: Literal["opacity_val"] = "opacity_val"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Opacity (Float)"

class BlendOption(Config):
    name: Literal["blend_mode"] = "blend_mode"
    value: OpacityVal
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Blender Mode"

# Ana Secim
class OperationSelector(Config):
    name: Literal["operation_mode"] = "operation_mode"
    value: Union[GrayOption, BlendOption]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Select Operation"

# YAPISTIRICI KISIM 
class PackageInputs(Inputs):
    inputImage: InputImage
    inputImage2: Optional[InputImage2]

class PackageConfigsInner(Configs):
    operation_mode: OperationSelector

# Cikislar Listesi (iki Tane)
class PackageOutputs(Outputs):
    outputImage: OutputImage
    outputMessage: OutputMessage

class PackageRequest(Request):
    inputs: Optional[PackageInputs]
    configs: PackageConfigsInner
    class Config:
        json_schema_extra = {"target": "configs"}

class PackageResponse(Response):
    outputs: PackageOutputs

class PackageExecutor(Config):
    name: Literal["Package"] = "Package"
    value: Union[PackageRequest, PackageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Package"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[PackageExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task"
        json_schema_extra = {"target": "value"}

class PackageConfigsOuter(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigsOuter
    type: Literal["component"] = "component"
    name: Literal["DemoImageFilters"] = "DemoImageFilters"
