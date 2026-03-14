from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

# ==========================================
# 1. ORTAK VERİ TİPLERİ (Giriş/Çıkışlar)
# ==========================================
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

# ==========================================
# 2. GRAYSCALE ZİNCİRİ (Executor 0)
# ==========================================
class ManualModeThresh(Config):
    name: Literal["thresh_val"] = "thresh_val"
    value: int = Field(default=127, ge=0, le=255)
    type: Literal["number"] = "number"
    field: Literal["numberInput"] = "numberInput"
    class Config: title = "Threshold Value"

class ManualMode(Config):
    name: Literal["manual_mode"] = "manual_mode"
    value: ManualModeThresh
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Manual Threshold"

class AutoModeCheck(Config):
    name: Literal["use_auto"] = "use_auto"
    value: bool = Field(default=True)
    type: Literal["bool"] = "bool"
    field: Literal["checkbox"] = "checkbox"
    class Config: title = "Use Auto Threshold"

class AutoMode(Config):
    name: Literal["auto_mode"] = "auto_mode"
    value: AutoModeCheck
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Auto Threshold"

class GrayscaleSelector(Config):
    name: Literal["gray_selector"] = "gray_selector"
    value: Union[ManualMode, AutoMode]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: 
        title = "Grayscale Method"
        # Alt menülerin açılması için bu şart!
        json_schema_extra = {"target": "value"}

class GrayscaleConfigs(Configs):
    gray_selector: GrayscaleSelector

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

# ==========================================
# 3. BLENDER ZİNCİRİ (Executor 1)
# ==========================================
class OpacityModeVal(Config):
    name: Literal["opacity_val"] = "opacity_val"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["numberInput"] = "numberInput"
    class Config: title = "Opacity (0.0 - 1.0)"

class OpacityMode(Config):
    name: Literal["opacity_mode"] = "opacity_mode"
    value: OpacityModeVal
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Weighted Blend"

class TextModeVal(Config):
    name: Literal["watermark_text"] = "watermark_text"
    value: str = Field(default="Demo")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Watermark Text"

class TextMode(Config):
    name: Literal["text_mode"] = "text_mode"
    value: TextModeVal
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Text Overlay"

class BlenderSelector(Config):
    name: Literal["blend_selector"] = "blend_selector"
    value: Union[OpacityMode, TextMode]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: 
        title = "Blender Method"
        # Alt menülerin açılması için bu şart!
        json_schema_extra = {"target": "value"}

class BlenderConfigs(Configs):
    blend_selector: BlenderSelector

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

# ==========================================
# 4. ANA KONFİGÜRASYON (Dispatcher)
# ==========================================
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GrayscaleExecutor, BlenderExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    
    # UI'ın kendini yenilemesi ve giriş/çıkış portlarını (1 resimden 2 resme) güncellemesi için şart:
    restart: Literal[True] = True
    
    class Config:
        title = "Select Task"
        # DİKKAT: Burada json_schema_extra KESİNLİKLE YOK! (Arayüz çakışmasını engellemek için FaceRecognition mantığına geçtik)

class PackageConfigsOuter(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigsOuter
    type: Literal["component"] = "component"
    name: Literal["ImageFilters"] = "ImageFilters"
    # Eski icon/image satırı kaldırıldı, sisteme hata verdirmesin diye.
