import asyncio
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Union

from _pysilk import silkDecode, silkEncode

T_input = Union[bytes, str, Path, BytesIO, BinaryIO]


def validate_silk_data(raw: bytes) -> bool:
    return raw[:10] == b"\x02#!SILK_V3" or raw[:9] == b"#!SILK_V3"


def get_bytes(input: T_input) -> bytes:
    if isinstance(input, bytes):
        return input
    if isinstance(input, str):
        return Path(input).read_bytes()
    if isinstance(input, Path):
        return input.read_bytes()
    if isinstance(input, BytesIO):
        return input.getvalue()
    if isinstance(input, BinaryIO):
        return input.read()
    raise TypeError(
        "The type of `input` must be one of [bytes, str, Path, BytesIO, BinaryIO]"
    )


def encode(input: T_input, sample_rate: int = 24000, tencent: bool = False) -> bytes:
    """Encode pcm to silk
    :param input: The source to encode, str and Path means local file path.
    :param sample_rate: Sampling rate in Hz
    :param tencent: Compatible with QQ/Wechat
    """
    return silkEncode(get_bytes(input), sample_rate, tencent)


def decode(input: T_input, sample_rate: int = 24000) -> bytes:
    """Decode silk to pcm
    :param input: The source to decode, str and Path means local file path.
    :param sample_rate: Sampling rate in Hz
    """
    raw_bytes = get_bytes(input)
    if validate_silk_data(raw_bytes):
        return silkDecode(raw_bytes, sample_rate)
    raise ValueError("Invalid silk data")


async def async_encode(
    input: T_input, sample_rate: int = 24000, tencent: bool = False
) -> bytes:
    """Encode pcm to silk
    :param input: The source to encode, str and Path means local file path
    :param sample_rate: Sampling rate in Hz
    :param tencent: Compatible with QQ/Wechat
    """
    return await asyncio.get_event_loop().run_in_executor(
        None, encode, input, sample_rate, tencent
    )


async def async_decode(input: T_input, sample_rate: int = 24000) -> bytes:
    """Decode silk to pcm
    :param input: The source to decode, str and Path means local file path
    :param sample_rate: Sampling rate in Hz
    """
    return await asyncio.get_event_loop().run_in_executor(
        None, decode, input, sample_rate
    )
