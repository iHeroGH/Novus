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

from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Literal, overload

from ..models import Channel, Guild, Message, Object, User

if TYPE_CHECKING:
    from .. import Application, DMChannel, Emoji, GuildChannel, ScheduledEvent, Sticker
    from ..models import api_mixins as amix
    from ._http import HTTPConnection

__all__ = (
    'APICache',
    'NothingAPICache',
)


class MaxLenDict(OrderedDict):

    def __init__(self, *, max_size: int):
        self.max_size = max_size
        super().__init__()

    def __setitem__(self, __key: Any, __value: Any) -> None:
        super().__setitem__(__key, __value)
        while len(self) > self.max_size:
            self.popitem(last=False)


class APICache:

    def __init__(self, parent: HTTPConnection):
        self.parent = parent
        self.user: User | None = None
        self.application_id: int | None = None
        self.application: Application | None = None

        self.guild_ids: set[int] = set()
        self.guilds: dict[int, Guild] = {}
        self.users: dict[int, User] = {}
        self.channels: dict[int, Channel] = {}
        self.emojis: dict[int, Emoji] = {}
        self.stickers: dict[int, Sticker] = {}
        self.events: dict[int, ScheduledEvent] = {}
        self.messages: dict[int, Message] = MaxLenDict(max_size=1_000)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} " + (
            f"user={self.user!r} "
            f"application_id={self.application_id!r} "
            f"guilds[{len(self.guilds)}] "
            f"users[{len(self.users)}] "
            f"channels[{len(self.channels)}] "
            f"emojis[{len(self.emojis)}] "
            f"stickers[{len(self.stickers)}] "
            f"events[{len(self.events)}]"
        ).strip() + ">"

    @staticmethod
    def do_nothing(instance: Any, *items: Any) -> None:
        pass

    def add_guilds(self, *items: Guild) -> None:
        for i in items:
            self.guild_ids.add(i.id)
            self.guilds[i.id] = i

    def add_users(self, *items: User) -> None:
        for i in items:
            self.users[i.id] = i

    def add_channels(self, *items: Channel) -> None:
        for i in items:
            self.channels[i.id] = i

    def add_emojis(self, *items: Emoji) -> None:
        for i in items:
            if i.id is None:
                continue
            self.emojis[i.id] = i

    def add_stickers(self, *items: Sticker) -> None:
        for i in items:
            self.stickers[i.id] = i

    def add_events(self, *items: ScheduledEvent) -> None:
        for i in items:
            self.events[i.id] = i

    def add_messages(self, *items: Message) -> None:
        for i in items:
            self.messages[i.id] = i

    @overload
    def get_guild(self, id: None, or_object: bool) -> None:
        ...

    @overload
    def get_guild(self, id: int | str, or_object: Literal[True] = ...) -> Guild | amix.GuildAPIMixin:
        ...

    @overload
    def get_guild(self, id: int | str, or_object: Literal[False] = ...) -> Guild | None:
        ...

    def get_guild(self, id: int | str | None, or_object: bool = False) -> Guild | amix.GuildAPIMixin | None:
        if id is None:
            return None
        v = self.guilds.get(int(id))
        if v:
            return v
        if or_object is False:
            return None
        return Object(id, state=self.parent).add_api(Guild)

    @overload
    def get_user(self, id: int | str, or_object: Literal[True] = ...) -> User | amix.UserAPIMixin:
        ...

    @overload
    def get_user(self, id: int | str, or_object: Literal[False] = ...) -> User | None:
        ...

    def get_user(self, id: int | str, or_object: bool = False) -> User | amix.UserAPIMixin | None:
        v = self.users.get(int(id))
        if v:
            return v
        if or_object is False:
            return None
        return Object(id, state=self.parent).add_api(User)

    @overload
    def get_channel(self, id: None, or_object: bool = ...) -> None:
        ...

    @overload
    def get_channel(self, id: int | str, or_object: Literal[True] = ...) -> GuildChannel | DMChannel | Channel:
        ...

    @overload
    def get_channel(self, id: int | str, or_object: Literal[False] = ...) -> GuildChannel | DMChannel | Channel | None:
        ...

    def get_channel(self, id: int | str | None, or_object: bool = False) -> GuildChannel | DMChannel | Channel | None:
        if id is None:
            return None
        v = self.channels.get(int(id))
        if v:
            return v
        if or_object is False:
            return None
        return Channel.partial(self.parent, id)

    def get_emoji(self, id: int | str) -> Emoji | None:
        return self.emojis.get(int(id))

    def get_sticker(self, id: int | str) -> Sticker | None:
        return self.stickers.get(int(id))

    def get_event(self, id: int | str) -> ScheduledEvent | None:
        return self.events.get(int(id))

    @overload
    def get_message(self, id: int | str, or_object: Literal[True] = ...) -> Message | amix.MessageAPIMixin:
        ...

    @overload
    def get_message(self, id: int | str, or_object: Literal[False] = ...) -> Message | None:
        ...

    def get_message(self, id: int | str, or_object: bool = False) -> Message | amix.MessageAPIMixin | None:
        v = self.messages.get(int(id))
        if v:
            return v
        if or_object is False:
            return None
        return Object(id, state=self.parent).add_api(Message)

    def clear(self) -> None:
        self.user = None
        self.application_id = None
        self.guilds.clear()
        self.users.clear()
        self.channels.clear()
        self.messages.clear()
        self.emojis.clear()
        self.stickers.clear()
        self.events.clear()


class NothingAPICache(APICache):

    def add_guilds(self, *items: Guild) -> None:
        for i in items:
            self.guild_ids.add(i.id)

    def add_users(self, *items: User) -> None:
        pass

    def add_channels(self, *items: Channel) -> None:
        pass

    def add_emojis(self, *items: Emoji) -> None:
        pass

    def add_stickers(self, *items: Sticker) -> None:
        pass

    def add_events(self, *items: ScheduledEvent) -> None:
        pass

    def add_messages(self, *items: Message) -> None:
        pass
