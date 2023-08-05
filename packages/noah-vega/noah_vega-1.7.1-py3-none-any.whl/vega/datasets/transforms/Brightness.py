# -*- coding: utf-8 -*-

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

"""This is a class for Brightness."""
from PIL import ImageEnhance
from .ops import float_parameter
from vega.common import ClassFactory, ClassType


@ClassFactory.register(ClassType.TRANSFORM)
class Brightness(object):
    """Applies Brightness to 'img'.

    The Brightness operation adjusts the brightness of the image, level = 0 gives a black image,
    whereas level = 1 gives the original image.
    :param level: Strength of the operation specified as an Integer from [0, 'PARAMETER_MAX'].
    :type level: int
    """

    def __init__(self, level):
        """Construct the Brightness class."""
        self.level = level

    def __call__(self, img):
        """Call function of Brightness.

        :param img: input image
        :type img: numpy or tensor
        :return: the image after transform
        :rtype: numpy or tensor
        """
        v = float_parameter(self.level, 1.8) + .1
        return ImageEnhance.Brightness(img).enhance(v)
