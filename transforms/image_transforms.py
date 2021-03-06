import torchvision.transforms as transforms
import numpy as np
from typing import Callable, Sequence, Any

from __types import Tensor, TensorOp


def to_tensor() -> Callable[[Any], Tensor]:
    _to_tensor = transforms.ToTensor()

    def _apply(x):
        return _to_tensor(x)
    return _apply


def downsample(factor: int) -> TensorOp:
    def _apply(x):
        # TODO: do this more elegantly, this probably also does unnecessary stuff like stretching if not divisible
        downsampled_size = [int(s // factor) for s in x.size]
        return transforms.functional.resize(x, downsampled_size)
    return _apply


def random_crop_to(size: Sequence[int]) -> TensorOp:
    random_crop = transforms.RandomCrop(size, pad_if_needed=True) # avoids exception if smaller than input dims

    def _apply(x):
        return random_crop(x)
    return _apply


# downsample and random crop st the transformed image covers as much of the original as possible
def random_fit_to(size: Sequence[int]) -> TensorOp:

    def _apply(x):
        # TODO: make elegant
        if x.size[0] <= size[0] or x.size[1] <= size[1]:
            scaling_factor = 0
        else:
            scaling_factor = min(x.size[0] / size[0], x.size[1] / size[1]) // 2 * 2  # min(int(np.log2(x.size[0] // size[0])), int(np.log2(x.size[1] // size[1])))
        if scaling_factor != 0:
            x = downsample(scaling_factor)(x)
        x = random_crop_to(size)(x)
        return x
    return _apply
