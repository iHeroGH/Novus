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

from dataclasses import dataclass
from datetime import datetime as dt
from typing import TYPE_CHECKING

from typing_extensions import Self

from ..utils import MISSING, DiscordDatetime, parse_timestamp

if TYPE_CHECKING:
    from ..payloads.embed import Embed as EmbedPayload
    from ..payloads.embed import _EmbedAuthor as AuthorPayload
    from ..payloads.embed import _EmbedField as FieldPayload
    from ..payloads.embed import _EmbedFooter as FooterPayload
    from ..payloads.embed import _EmbedMedia as MediaPayload
    from .guild_member import GuildMember
    from .user import User

__all__ = (
    'Embed',
)


@dataclass
class EmbedFooter:
    text: str
    icon_url: str | None = None
    proxy_icon_url: str | None = None

    def _to_data(self) -> FooterPayload:
        v: FooterPayload = {
            "text": str(self.text)
        }
        if self.icon_url:
            v["icon_url"] = self.icon_url
        return v


@dataclass
class EmbedMedia:
    url: str
    proxy_url: str | None = None
    height: int | None = None
    width: int | None = None

    def _to_data(self) -> MediaPayload:
        return {
            "url": self.url
        }


@dataclass
class EmbedVideo:
    url: str | None = None
    proxy_url: str | None = None
    height: int | None = None
    width: int | None = None


@dataclass
class EmbedProvider:
    name: str | None = None
    url: str | None = None


@dataclass
class EmbedAuthor:
    name: str
    url: str | None = None
    icon_url: str | None = None
    proxy_icon_url: str | None = None

    def _to_data(self) -> AuthorPayload:
        v: AuthorPayload = {
            "name": str(self.name)
        }
        if self.url:
            v["url"] = self.url
        if self.icon_url:
            v["icon_url"] = self.icon_url
        return v


@dataclass
class EmbedField:
    name: str
    value: str
    inline: bool = True

    def _to_data(self) -> FieldPayload:
        return {
            "name": str(self.name),
            "value": str(self.value),
            "inline": self.inline,
        }


class Embed:
    """
    A model for an embed object.

    Parameters
    ----------
    title: str
        The title on the embed.
    description: str
        The description of the embed.
    url: str
        The url of the embed, attached to the title.
    timestamp: datetime.datetime
        The timestamp in the footer of the bot.
    color: int
        The color of the embed.

    Attributes
    ----------
    title : str | None
        The title of the embed.
    type : str | None
        The type of the embed.
    description : str | None
        The description of the embed.
    url : str | None
        The URL of the embed.
    timestamp : datetime.datetime | None
        The timestamp in the embed footer.
    color : int | None
        The colour integer of the embed.
    footer : object | None
        The footer of the embed.
        An object containing the following attributes:

        * ``text``: `str`
        * ``icon_url``: `str` | `None`
        * ``proxy_icon_url``: `str` | `None`
    image : object | None
        The image added to the embed.
        An object containing the following attributes:

        * ``url``: `str`
        * ``proxy_url``: `str` | `None`
        * ``height``: `int` | `None`
        * ``width``: `int` | `None`
    thumbnail : object | None
        The image added to the embed.
        An object containing the following attributes:

        * ``url``: `str`
        * ``proxy_url``: `str` | `None`
        * ``height``: `int` | `None`
        * ``width``: `int` | `None`
    video : object | None
        The video added to the embed.
        An object containing the following attributes:

        * ``url``: `str` | `None`
        * ``proxy_url``: `str` | `None`
        * ``height``: `int` | `None`
        * ``width``: `int` | `None`
    provider : object | None
        The provider information.
        An object containing the following attributes:

        * ``name``: `str` | `None`
        * ``url``: `str` | `None`
    author : object | None
        The author of the embed.
        An object containing the following attributes:

        * ``name``: `str`
        * ``url``: `str` | `None`
        * ``icon_url``: `str` | `None`
        * ``proxy_icon_url``: `str` | `None`
    fields : list[object]
        A list of fields added to the embed.
        An a field is an object containing the following attributes:

        * ``name``: `str`
        * ``value``: `str`
        * ``inline``: `bool`
    """

    def __init__(
            self,
            *,
            title: str | None = None,
            type: str = "rich",
            description: str | None = None,
            url: str | None = None,
            timestamp: dt | None = None,
            color: int | None = None) -> None:
        self.title: str | None = title
        self.type: str = type
        self.description: str | None = description
        self.url: str | None = url
        self.timestamp: dt | None = timestamp
        self.color: int | None = color

        self._footer: EmbedFooter | None = None
        self._image: EmbedMedia | None = None
        self._thumbnail: EmbedMedia | None = None
        self._video: EmbedVideo | None = None
        self._provider: EmbedProvider | None = None
        self._author: EmbedAuthor | None = None
        self._fields: list[EmbedField] = []

    def _to_data(self) -> EmbedPayload:
        v: EmbedPayload = {}
        if self.title is not None:
            v["title"] = str(self.title)
        if self.description is not None:
            v["description"] = str(self.description)
        if self.url is not None:
            v["url"] = self.url
        if self.timestamp is not None:
            v["timestamp"] = self.timestamp.isoformat()
        if self.color is not None:
            v["color"] = self.color
        if self._footer is not None:
            v["footer"] = self._footer._to_data()
        if self._image is not None:
            v["image"] = self._image._to_data()
        if self._thumbnail is not None:
            v["thumbnail"] = self._thumbnail._to_data()
        if self._author is not None:
            v["author"] = self._author._to_data()
        if self._fields is not None:
            v["fields"] = [i._to_data() for i in self._fields]
        return v

    @classmethod
    def _from_data(cls, data: EmbedPayload) -> Self:
        timestamp = data.get("timestamp")
        timestamp_o: DiscordDatetime | None = None
        if timestamp is not None:
            timestamp_o = parse_timestamp(timestamp)
        embed = cls(
            title=data.get("title"),
            type=data.get("type") or "rich",
            description=data.get("description"),
            url=data.get("url"),
            timestamp=timestamp_o,
            color=data.get("color"),
        )
        if "footer" in data:
            embed._footer = EmbedFooter(**data["footer"])
        if "image" in data:
            embed._image = EmbedMedia(**data["image"])
        if "thumbnail" in data:
            embed._thumbnail = EmbedMedia(**data["thumbnail"])
        if "video" in data:
            embed._video = EmbedVideo(**data["video"])
        if "provider" in data:
            embed._provider = EmbedProvider(**data["provider"])
        if "author" in data:
            embed._author = EmbedAuthor(**data["author"])
        if "fields" in data:
            embed._fields = [
                EmbedField(**d)
                for d in data["fields"]
            ]
        return embed

    @property
    def footer(self) -> EmbedFooter | None:
        return self._footer

    def update(
            self,
            *,
            title: str | None = MISSING,
            description: str | None = MISSING,
            url: str | None = MISSING,
            timestamp: dt | None = MISSING,
            color: int | None = MISSING) -> Self:
        """
        Set an attribute of the embed via a single ``.update`` method.

        Parameters
        ----------
        title : str | None
            The title of the embed.
        description : str | None
            The description of the embed.
        url : str | None
            The URL of the embed.
        timestamp : datetime.datetime | None
            The timestamp in the embed footer.
        color : int | None
            The colour integer of the embed.

        Returns
        -------
        novus.Embed
            The embed instance.
        """

        if title is not MISSING:
            self.title = title
        if description is not MISSING:
            self.description = description
        if url is not MISSING:
            self.url = url
        if timestamp is not MISSING:
            self.timestamp = timestamp
        if color is not MISSING:
            self.color = color
        return self

    def set_footer(
            self,
            text: str,
            *,
            icon_url: str | None = None) -> Self:
        """
        Set the footer of the embed.

        Parameters
        ----------
        text : str
            The text to be added to the footer. Does not support markdown.
        icon_url : str | None
            The url of the icon to be used in the footer. Only supports HTTP(S)
            and attachments.
        """

        self._footer = EmbedFooter(
            text=text,
            icon_url=icon_url,
        )
        return self

    def remove_footer(self) -> Self:
        """
        Remove the footer of the embed.
        """

        self._footer = None
        return self

    @property
    def image(self) -> EmbedMedia | None:
        return self._image

    def set_image(self, url: str) -> Self:
        """
        Set an image for the embed.

        Parameters
        ----------
        url : str
            The source url of the image. Only supports HTTP(S) and attachments.
        """

        self._image = EmbedMedia(url)
        return self

    def remove_image(self) -> Self:
        """
        Remove the image of the embed.
        """

        self._image = None
        return self

    @property
    def thumbnail(self) -> EmbedMedia | None:
        return self._thumbnail

    def set_thumbnail(self, url: str) -> Self:
        """
        Set an thumbnail for the embed.

        Parameters
        ----------
        url : str
            The source url of the thumbnail. Only supports HTTP(S) and
            attachments.
        """

        self._thumbnail = EmbedMedia(url)
        return self

    def remove_thumbnail(self) -> Self:
        """
        Remove the thumbnail of the embed.
        """

        self._thumbnail = None
        return self

    @property
    def video(self) -> EmbedVideo | None:
        return self._video

    @property
    def provider(self) -> EmbedProvider | None:
        return self._provider

    @property
    def author(self) -> EmbedAuthor | None:
        return self._author

    def set_author(
            self,
            name: str,
            *,
            url: str | None = None,
            icon_url: str | None = None) -> Self:
        """
        Set the author of the embed.

        Parameters
        ----------
        name : str
            The name of the author in the embed.
        url : str | None
            The URL attached to the author's name in the embed.
        icon_url : str | None
            The url of the author's icon.
        """

        self._author = EmbedAuthor(
            name=name,
            url=url,
            icon_url=icon_url,
        )
        return self

    def set_author_from_user(self, user: User | GuildMember) -> Self:
        """
        Set the author of the embed with the attributes present on a user.

        Parameters
        ----------
        user : novus.User | novus.GuildMember
            The user that you want to set into the embed.
        """

        avatar = user.avatar or user.default_avatar
        return self.set_author(
            name=str(user),
            icon_url=avatar.get_url()
        )

    def remove_author(self) -> Self:
        """
        Remove the author of the embed.
        """

        self._author = None
        return self

    @property
    def fields(self) -> list[EmbedField]:
        return self._fields

    def add_field(
            self,
            name: str,
            value: str,
            *,
            inline: bool = True) -> Self:
        """
        Add a field to the embed.

        Parameters
        ----------
        name : str
            The name of the field.
        value : str
            The value of the embed.
        inline : bool
            Whether or not the field should be inline.
        """

        self._fields.append(
            EmbedField(
                name=name,
                value=value,
                inline=inline,
            )
        )
        return self

    def remove_field(self, index: int) -> Self:
        """
        Remove a field at a given index.

        Parameters
        ----------
        index : int
            The index of the field.
        """

        self._fields.pop(index)
        return self

    def insert_field_at(
            self,
            index: int,
            name: str,
            value: str,
            *,
            inline: bool = True) -> Self:
        """
        Add a field to the embed at a specified location.

        Parameters
        ----------
        index : int
            The index that you want to add the field at.
        name : str
            The name of the field.
        value : str
            The value of the embed.
        inline : bool
            Whether or not the field should be inline.
        """

        self._fields.insert(
            index,
            EmbedField(
                name=name,
                value=value,
                inline=inline,
            )
        )
        return self

    def clear_fields(self) -> Self:
        """
        Remove all of the fields from the embed.
        """

        self._fields.clear()
        return self
