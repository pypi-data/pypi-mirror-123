# -*- coding:utf-8 -*-

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

"""Lazy import cyclesr bodys."""

from vega.common.class_factory import ClassFactory


ClassFactory.lazy_register("vega.networks.pytorch.cyclesrbodys", {
    "cyclesr_net": ["CycleSRModel"],
})
