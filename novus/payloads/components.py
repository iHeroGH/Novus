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
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict, Union

from typing_extensions import NotRequired

if TYPE_CHECKING:
    from .emoji import PartialEmoji

__all__ = (
    'ComponentType',
    'Button',
    'SelectOption',
    'SelectMenu',
    'TextInput',
    'ActionRow',
    'IteractableComponent',
    'LayoutComponent',
    'Component',
)


ComponentType = Literal[
    1,  # Action row
    2,  # Button
    3,  # String select
    4,  # Text input
    5,  # User select
    6,  # Role select
    7,  # Mentionable select
    8,  # Channel select
]


class _ButtonOptional(TypedDict, total=False):
    emoji: PartialEmoji
    url: str
    disabled: bool
    label: str


class Button(_ButtonOptional):
    custom_id: str
    type: Literal[2]
    style: Literal[1, 2, 3, 4, 5]


class _SelectOptionOptional(TypedDict, total=False):
    description: str
    emoji: PartialEmoji
    default: bool


class SelectOption(_SelectOptionOptional):
    label: str
    value: str


class _SelectMenuOptional(TypedDict, total=False):
    options: list[SelectOption]
    channel_types: list[int]
    placeholder: str
    min_values: int
    max_values: int
    disabled: bool


class SelectMenu(_SelectMenuOptional):
    type: Literal[3, 5, 6, 7, 8]
    custom_id: str


class TextInput(TypedDict):
    type: Literal[4]
    custom_id: str
    style: Literal[1, 2]
    label: str
    min_length: NotRequired[int]
    max_length: NotRequired[int]
    required: NotRequired[bool]
    value: NotRequired[str]
    placeholder: NotRequired[str]


IteractableComponent = Union[
    Button,
    SelectMenu,
    TextInput,
]


class ActionRow(TypedDict):
    type: Literal[1]
    components: list[IteractableComponent]


LayoutComponent = ActionRow


Component = Union[IteractableComponent, LayoutComponent]
