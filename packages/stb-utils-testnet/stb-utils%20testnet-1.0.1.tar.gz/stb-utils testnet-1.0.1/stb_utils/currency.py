# --------------------------------------------------------------------
# Copyright (c) stabilaclick. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------

import decimal
from decimal import localcontext
from typing import Union

from stb_utils.types import (
    is_string,
    is_integer
)

MIN_UNIT = 0
MAX_UNIT = 2 ** 256 - 1
UNITS = {
    'unit': decimal.Decimal('1000000')
}


def from_unit(number: int) -> Union[int, decimal.Decimal]:
    """Helper function that will convert a value in UNIT to STB.

    Args:
        number (int): Value in UNIT to convert to STB

    """
    if number == 0:
        return 0

    if number < MIN_UNIT or number > MAX_UNIT:
        raise ValueError("value must be between 1 and 2**256 - 1")

    unit_value = UNITS['unit']

    with localcontext() as ctx:
        ctx.prec = 999
        d_number = decimal.Decimal(value=number, context=ctx)
        result_value = d_number / unit_value

    return result_value


def to_unit(number: int) -> int:
    """Helper function that will convert a value in STB to UNIT.

    Args:
        number (int): Value in STB to convert to UNIT

    """
    if is_integer(number) or is_string(number):
        d_number = decimal.Decimal(value=number)
    elif isinstance(number, float):
        d_number = decimal.Decimal(value=str(number))
    elif isinstance(number, decimal.Decimal):
        d_number = number
    else:
        raise TypeError("Unsupported type.  Must be one of integer, float, or string")

    s_number = str(number)
    unit_value = UNITS['unit']

    if d_number == 0:
        return 0

    if d_number < 1 and '.' in s_number:
        with localcontext() as ctx:
            multiplier = len(s_number) - s_number.index('.') - 1
            ctx.prec = multiplier
            d_number = decimal.Decimal(value=number, context=ctx) * 10 ** multiplier
        unit_value /= 10 ** multiplier

    with localcontext() as ctx:
        ctx.prec = 999
        result_value = decimal.Decimal(value=d_number, context=ctx) * unit_value

    if result_value < MIN_UNIT or result_value > MAX_UNIT:
        raise ValueError("Resulting wei value must be between 1 and 2**256 - 1")

    return int(result_value)
