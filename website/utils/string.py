"""
    Source of juleslasne.com/.net/.me/.fr
    Copyright (C) 2018-2019 Jules Lasne - <jules@juleslasne.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import collections

from typing import Union


def decode_bytes(inp: Union[bytes, str])-> str:
    """
    Will take in bytes or string and will return a string
    :param inp: The bytes or string to decode
    :return: Returns a string
    """
    ret = inp.decode() if isinstance(inp, bytes) else inp
    return ret


def convert_dict(data):
    """
    This function will convert from a unicode object to a string the keys and values of dict.

    :param data: The dictionary to convert

    :return: Returns the converted dict
    """

    if isinstance(data, collections.Mapping):
        return dict(map(convert_dict, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_dict, data))
    else:
        return data
