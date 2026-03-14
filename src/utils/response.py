
from sdks.novavision.src.helper.package import PackageHelper
from components.ImageFilters.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    # Grayscale
    GrayscaleExecutor,
    GrayscaleOutputs,
    GrayscaleResponse,
    OutputImage,
    # Blender
    BlenderExecutor,
    BlenderOutputs,
    BlenderResponse,
    OutputMessage,
)


def build_grayscale_response(context):
    outputImage = OutputImage(value=context.image)
    outputs = GrayscaleOutputs(outputImage=outputImage)
    response = GrayscaleResponse(outputs=outputs)
    grayscaleExecutor = GrayscaleExecutor(value=response)
    executor = ConfigExecutor(value=grayscaleExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_blender_response(context):
    outputImage = OutputImage(value=context.image)
    outputMessage = OutputMessage(value=context.message)
    outputs = BlenderOutputs(outputImage=outputImage, outputMessage=outputMessage)
    response = BlenderResponse(outputs=outputs)
    blenderExecutor = BlenderExecutor(value=response)
    executor = ConfigExecutor(value=blenderExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
