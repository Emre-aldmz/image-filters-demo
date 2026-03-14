from pydantic import validator
from typing import List, Union, Literal, Optional
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


# ──────────────────────────────────────────────
#  SHARED OUTPUT / INPUT TYPES
# ──────────────────────────────────────────────

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image 2"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputMessage(Output):
    name: Literal["outputMessage"] = "outputMessage"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


# ══════════════════════════════════════════════
#  GRAYSCALE EXECUTOR CHAIN
# ══════════════════════════════════════════════

# --- manual_mode ---

class ManualModeThresh(Config):
    """Threshold value for manual grayscale conversion (0-255)."""
    name: Literal["thresh_val"] = "thresh_val"
    value: int = 128
    type: Literal["number"] = "number"
    field: Literal["numberInput"] = "numberInput"

    class Config:
        title = "Threshold Value"
        json_schema_extra = {
            "shortDescription": "Set threshold (0-255)"
        }


class ManualMode(Config):
    name: Literal["manual_mode"] = "manual_mode"
    thresh_val: ManualModeThresh
    value: Literal["manual_mode"] = "manual_mode"
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Manual Mode"


# --- auto_mode ---

class AutoModeCheck(Config):
    """Enable automatic grayscale conversion."""
    name: Literal["use_auto"] = "use_auto"
    value: bool = True
    type: Literal["boolean"] = "boolean"
    field: Literal["checkbox"] = "checkbox"

    class Config:
        title = "Use Auto"
        json_schema_extra = {
            "shortDescription": "Enable auto grayscale"
        }


class AutoMode(Config):
    name: Literal["auto_mode"] = "auto_mode"
    use_auto: AutoModeCheck
    value: Literal["auto_mode"] = "auto_mode"
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Auto Mode"


# --- Grayscale selector & request ---

class GrayscaleSelector(Config):
    """Select grayscale method: Manual (threshold) or Auto."""
    name: Literal["gray_selector"] = "gray_selector"
    value: Union[ManualMode, AutoMode]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Grayscale Method"
        json_schema_extra = {
            "target": "value"
        }


class GrayscaleInputs(Inputs):
    inputImage: InputImage


class GrayscaleConfigs(Configs):
    gray_selector: GrayscaleSelector


class GrayscaleRequest(Request):
    inputs: Optional[GrayscaleInputs]
    configs: GrayscaleConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class GrayscaleOutputs(Outputs):
    outputImage: OutputImage


class GrayscaleResponse(Response):
    outputs: GrayscaleOutputs


class GrayscaleExecutor(Config):
    name: Literal["GrayscaleExecutor"] = "GrayscaleExecutor"
    value: Union[GrayscaleRequest, GrayscaleResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Grayscale"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# ══════════════════════════════════════════════
#  BLENDER EXECUTOR CHAIN
# ══════════════════════════════════════════════

# --- opacity_mode ---

class OpacityModeVal(Config):
    """Blend opacity value between 0.0 and 1.0."""
    name: Literal["opacity_val"] = "opacity_val"
    value: float = 0.5
    type: Literal["number"] = "number"
    field: Literal["numberInput"] = "numberInput"

    class Config:
        title = "Opacity"
        json_schema_extra = {
            "shortDescription": "Set opacity (0.0-1.0)"
        }


class OpacityMode(Config):
    name: Literal["opacity_mode"] = "opacity_mode"
    opacity_val: OpacityModeVal
    value: Literal["opacity_mode"] = "opacity_mode"
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Opacity Mode"


# --- text_mode ---

class TextModeVal(Config):
    """Watermark text to overlay on the blended image."""
    name: Literal["watermark_text"] = "watermark_text"
    value: str = "NovaVision"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Watermark Text"
        json_schema_extra = {
            "shortDescription": "Enter watermark text"
        }


class TextMode(Config):
    name: Literal["text_mode"] = "text_mode"
    watermark_text: TextModeVal
    value: Literal["text_mode"] = "text_mode"
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Text Mode"


# --- Blender selector & request ---

class BlenderSelector(Config):
    """Select blending method: Opacity blend or Text watermark."""
    name: Literal["blend_selector"] = "blend_selector"
    value: Union[OpacityMode, TextMode]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Blend Method"
        json_schema_extra = {
            "target": "value"
        }


class BlenderInputs(Inputs):
    inputImage: InputImage
    inputImage2: InputImage2


class BlenderConfigs(Configs):
    blend_selector: BlenderSelector


class BlenderRequest(Request):
    inputs: Optional[BlenderInputs]
    configs: BlenderConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class BlenderOutputs(Outputs):
    outputImage: OutputImage
    outputMessage: OutputMessage


class BlenderResponse(Response):
    outputs: BlenderOutputs


class BlenderExecutor(Config):
    name: Literal["BlenderExecutor"] = "BlenderExecutor"
    value: Union[BlenderRequest, BlenderResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blender"
        json_schema_extra = {
            "target": {
                "value": 1
            }
        }


# ══════════════════════════════════════════════
#  CONFIG EXECUTOR (DISPATCHER) & PACKAGE MODEL
# ══════════════════════════════════════════════

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GrayscaleExecutor, BlenderExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["ImageFilters"] = "ImageFilters"
