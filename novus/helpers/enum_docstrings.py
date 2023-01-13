"""
Copyright (c) Kae Bartlett

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from enum import Enum

__all__ = (
    'enum_docstrings',
)


def enum_docstrings(enum: Type[Enum]) -> Type[Enum]:
    """
    Go through the attributes of an enum and assign them docstrings based on
    the docstring of the enum itself.

    There are some caveats, however:
    * Will only work for correct indentation,
    * and only indentation that uses spaces rather than tabs.
    * This also assumes that there is only a single line for your docstring
    (ie no multiline docs for the enum attributes),
    * And you're using Google's styleguide for docstrings.
    """

    if not enum.__doc__:
        return enum

    found_attrs: bool = False
    attribute_docs: dict[str, str] = {}
    indent = 0

    attribute_name = None
    builder = []
    for line in enum.__doc__.split("\n"):

        # Go until we get to the attributes sectionh
        if not found_attrs:
            if line.lstrip().startswith("Attributes"):
                indent = len(line) - len(line.lstrip())
                found_attrs = True
            continue

        # If we don't have an attribute name, this line is probably it
        if not line.strip():
            continue
        if line.strip().startswith("-"):
            continue
        if attribute_name is None:
            attribute_name = line.strip().split(":")[0]
            if not attribute_name.isupper():
                builder = []
                break
            continue

        # See if we're still indented
        if line.startswith(" " * (indent + 4)):
            builder.append(line.strip())
            continue

        # See if we're dedented now
        elif line.startswith(" " * indent):
            attribute_docs[attribute_name] = " ".join(builder)
            attribute_name = line.strip().split(":")[0]
            builder = []
            continue
    if builder and attribute_name:
        attribute_docs[attribute_name] = " ".join(builder)

    # And now we modify the items' docs
    for item in enum:
        if item.name in attribute_docs:
            item.__doc__ = attribute_docs[item.name].strip()
    return enum
