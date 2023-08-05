# -*- coding=utf-8 -*-

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.
"""Default configs."""

from .base import BaseConfig
from vega.common import ConfigSerializable


class FashionMnistCommonConfig(BaseConfig):
    """Default Dataset config for DIV2K."""

    num_workers: 4
    shuffle = True
    transforms = [dict(type='RandomAffine', degrees=15, translate=(0.1, 0.1), scale=(0.9, 1.1), shear=0.1),
                  dict(type='RandomVerticalFlip'),
                  dict(type='ToTensor'),
                  dict(type='Normalize', mean=[0.28604063146254594], std=[0.35302426207299326])]

    @classmethod
    def rules(cls):
        """Return rules for checking."""
        rules_FashionMnistCommon = {"num_workers": {"type": int},
                                    "shuffle": {"type": int},
                                    "transforms": {"type": int}
                                    }
        return rules_FashionMnistCommon


class FashionMnistTrainConfig(FashionMnistCommonConfig):
    """Default Dataset config for Fashion Mnist."""

    pass


class FashionMnistValConfig(FashionMnistCommonConfig):
    """Default Dataset config for Fashion Mnist."""

    pass


class FashionMnistTestConfig(FashionMnistCommonConfig):
    """Default Dataset config for Fashion Mnist."""

    pass


class FashionMnistConfig(ConfigSerializable):
    """Default Dataset config for Fashion Mnist."""

    common = FashionMnistCommonConfig
    train = FashionMnistTrainConfig
    val = FashionMnistValConfig
    test = FashionMnistTestConfig

    @classmethod
    def rules(cls):
        """Return rules for checking."""
        rules_FashionMnist = {"common": {"type": dict},
                              "train": {"type": dict},
                              "val": {"type": dict},
                              "test": {"type": dict}
                              }
        return rules_FashionMnist

    @classmethod
    def get_config(cls):
        """Get sub config."""
        return {'common': cls.common,
                'train': cls.train,
                'val': cls.val,
                'test': cls.test
                }
