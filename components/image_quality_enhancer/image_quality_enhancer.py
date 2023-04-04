
import typing
from typing import Optional
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from core.workflows.abstract_workflow import AbstractWorkflow


class ImageUpload(BaseModel):
    image: UploadFile


class ImageComparison(BaseModel):
    original_image: bytes
    enhanced_image: bytes
    edits: typing.List[str]


class EnhancedImage(BaseModel):
    enhanced_image: bytes


class ImageQualityEnhancer(AbstractWorkflow):
    def __init__(self) -> None:
        super().__init__()

    async def transform(
        self, args: ImageUpload, callbacks: typing.Any
    ) -> typing.Tuple[ImageComparison, EnhancedImage]:
        results_dict = await super().transform(args=args, callbacks=callbacks)

        original_image = results_dict[0].original_image
        enhanced_image = results_dict[1].enhanced_image
        edits = results_dict[2].edits

        image_comparison = ImageComparison(
            original_image=original_image,
            enhanced_image=enhanced_image,
            edits=edits,
        )

        enhanced_image_output = EnhancedImage(enhanced_image=enhanced_image)

        return image_comparison, enhanced_image_output


image_quality_enhancer_app = FastAPI()


@image_quality_enhancer_app.post("/transform/")
async def transform(
    args: ImageUpload,
) -> typing.Tuple[ImageComparison, EnhancedImage]:
    image_quality_enhancer = ImageQualityEnhancer()
    return await image_quality_enhancer.transform(args, callbacks=None)
