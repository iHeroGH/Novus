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

import os
from typing import TYPE_CHECKING, Literal

import dotenv
from typing_extensions import Self

from ..utils import MISSING, generate_repr

if TYPE_CHECKING:
    from . import (
        Application,
        Emoji,
        Guild,
        GuildMember,
        GuildPreview,
        OauthGuild,
        PartialEmoji,
        PartialGuild,
        Role,
        ScheduledEvent,
        Sticker,
        Team,
        User,
        Webhook,
    )

__all__ = (
    'Asset',
)


dotenv.load_dotenv()


class Asset:
    """
    A representation of a discord image model.

    Attributes
    ----------
    resource : str
        The path assicated with the URL.
    animated : bool
        Whether or not the asset is animated.
    """

    BASE = os.getenv(
        "NOVUS_API_URL",
        "https://cdn.discordapp.com"
    )

    __slots__ = (
        'resource',
        'animated',
        'default_format',
    )

    def __init__(
            self,
            resource: str,
            animated: bool = MISSING,
            default_format: str | None = None):
        self.resource: str = resource
        if animated is MISSING:
            animated = self.resource.split("/")[-1].startswith("a_")
        self.animated: bool = animated
        self.default_format = default_format or "webp"

    def __str__(self) -> str:
        return self.get_url()

    __repr__ = generate_repr(('resource', 'animated',))

    def get_url(
            self,
            format: Literal["webp", "jpg", "jpeg", "png", "gif", "json"] = MISSING,
            size: int = MISSING) -> str:
        """
        Get the URL for the image with different formatting and size than the
        CDN default.

        Parameters
        ----------
        format : str
            The format that you want to get the URL as.
        """

        return (
            f"{self.BASE}{self.resource}."
            f"{format if format else self.default_format}"
            f"?size={size if size else 1024}"
        )

    @classmethod
    def from_guild_icon(cls, guild: Guild | GuildPreview | OauthGuild | PartialGuild) -> Self:
        return cls(f"/icons/{guild.id}/{guild.icon_hash}")

    @classmethod
    def from_guild_splash(cls, guild: Guild | GuildPreview | PartialGuild) -> Self:
        return cls(f"/splashes/{guild.id}/{guild.splash_hash}")

    @classmethod
    def from_guild_discovery_splash(cls, guild: Guild | GuildPreview) -> Self:
        return cls(f"/discovery-splashes/{guild.id}/{guild.discovery_splash_hash}")

    @classmethod
    def from_guild_banner(cls, guild: Guild | PartialGuild) -> Self:
        return cls(f"/banners/{guild.id}/{guild.banner_hash}")

    @classmethod
    def from_emoji(cls, emoji: Emoji | PartialEmoji) -> Self:
        return cls(f"/emojis/{emoji.id}", animated=emoji.animated)

    @classmethod
    def from_role(cls, role: Role) -> Self:
        return cls(f"/role-icons/{role.id}/{role.icon_hash}")

    @classmethod
    def from_sticker(cls, sticker: Sticker) -> Self:
        return cls(f"/stickers/{sticker.id}")

    @classmethod
    def from_user_avatar(cls, user: User | GuildMember | Webhook) -> Self:
        return cls(f"/avatars/{user.id}/{user.avatar_hash}")

    @classmethod
    def from_user_banner(cls, user: User | GuildMember) -> Self:
        return cls(f"/banners/{user.id}/{user.avatar_hash}")

    @classmethod
    def from_guild_member_avatar(cls, user: GuildMember) -> Self:
        return cls(f"/guilds/{user.guild.id}/users/{user.id}/avatars/{user.guild_avatar_hash}")

    # @classmethod
    # def from_guild_member_banner(cls, user: GuildMember) -> Self:
    #     return cls(f"/guilds/{user.guild.id}/users/{user.id}/banners/{user.guild_banner_hash}")

    @classmethod
    def from_event_image(cls, event: ScheduledEvent) -> Self:
        return cls(f"/guild-events/{event.id}/{event.image_hash}")

    @classmethod
    def from_application(cls, application: Application) -> Self:
        return cls(f"/app-icons/{application.id}/{application.icon_hash}")

    @classmethod
    def from_application_cover_image(cls, application: Application) -> Self:
        return cls(f"/app-icons/{application.id}/{application.cover_image_hash}")

    @classmethod
    def from_team(cls, team: Team) -> Self:
        return cls(f"/team-icons/{team.id}/{team.icon_hash}.png")
