# -*- coding:utf-8 -*-

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

"""StatusType."""
from enum import Enum


class StatusType(Enum):
    """StatusType."""

    KILLED = 1
    RUNNING = 2
    WAITTING = 3
    FINISHED = 4
    PORMOTED = 5
