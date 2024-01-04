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

from typing import TYPE_CHECKING, TypeAlias

__all__ = (
    'AnySnowflake',
    'CommandI',
    'ComponentI',
    'FileT',
    'ComponentGI',
    'CommandGI',
    'GuildMessage',
    'DMMessage',
)

if TYPE_CHECKING:
    import io

    from ..models import BaseGuild, Message
    from ..models.abc import Snowflake
    from ..models.interaction import (
        ApplicationCommandData,
        ContextComandData,
        Interaction,
        MessageComponentData,
    )

    CommandI: TypeAlias = Interaction[ApplicationCommandData] | Interaction[ContextComandData]
    ComponentI: TypeAlias = Interaction[MessageComponentData]
    AnySnowflake: TypeAlias = str | int | Snowflake
    FileT: TypeAlias = str | bytes | io.IOBase

    class ComponentGI(Interaction[MessageComponentData]):
        guild: BaseGuild

    class AppGI(Interaction[ApplicationCommandData]):
        guild: BaseGuild

    class ContextGI(Interaction[ContextComandData]):
        guild: BaseGuild

    CommandGI: TypeAlias = AppGI | ContextGI

    class GuildMessage(Message):
        guild: BaseGuild

    class DMMessage(Message):
        guild: None

else:
    CommandI: TypeAlias = None
    ComponentI: TypeAlias = None
    AnySnowflake: TypeAlias = None
    FileT: TypeAlias = None
    CommandGI: TypeAlias = None
    ComponentGI: TypeAlias = None
    GuildMessage: TypeAlias = None
    DMMessage: TypeAlias = None
