from __future__ import annotations

import asyncio
import typing

from discord.gateway import DiscordVoiceWebSocket

if typing.TYPE_CHECKING:
    from .voice_client import VoiceReceiveClient


async def hook(self: DiscordVoiceWebSocket, msg: dict) -> None:
    """
    A hook to handle the events from the voice websocket.
    """

    op = msg['op']
    data = msg['d']

    if op == self.SESSION_DESCRIPTION:
        await _do_hacks(self)

    elif op == self.SPEAKING:
        user_id = int(data['user_id'])
        vc: VoiceReceiveClient = self._connection
        vc._add_ssrc(user_id, data['ssrc'])
        if vc.guild:
            user = vc.guild.get_member(user_id)
        else:
            user = vc._connection.get_user(user_id)
        vc._connection.dispatch('speaking_update', user, data['speaking'])

    elif op == self.CLIENT_CONNECT:
        self._connection._add_ssrc(int(data['user_id']), data['audio_ssrc'])

    elif op == self.CLIENT_DISCONNECT:
        self._connection._remove_ssrc(user_id=int(data['user_id']))


async def _do_hacks(self: DiscordVoiceWebSocket):
    # Everything below this is a hack because discord keeps breaking things

    # hack #1
    # speaking needs to be set otherwise reconnecting makes you forget that the
    # bot is playing audio and you wont hear it until the bot sets speaking again
    await self.speak()

    # hack #3:
    # you need to wait for some indeterminate amount of time before sending silence
    await asyncio.sleep(0.5)

    # hack #2:
    # sending a silence packet is required to be able to read from the socket
    self._connection.send_audio_packet(b'\xF8\xFF\xFE', encode=False)

    # just so we don't have the speaking circle when we're not actually speaking
    await self.speak(False)


# async def patched_received_message(self, msg):
#     await self._orig_received_message(self, msg)

#     op = msg['op']
#     data = msg.get('d')

#     if op == self.SESSION_DESCRIPTION:
#         await self._do_hacks()

#     elif op == self.SPEAKING:
#         user_id = int(data['user_id'])
#         vc = self._connection
#         vc._add_ssrc(user_id, data['ssrc'])

#         if vc.guild:
#             user = vc.guild.get_member(user_id)
#         else:
#             user = vc._connection.get_user(user_id)

#         vc._connection.dispatch('speaking_update', user, SpeakingState(data['speaking']))

#     elif op == self.CLIENT_CONNECT:
#         self._connection._add_ssrc(int(data['user_id']), data['audio_ssrc'])

#     elif op == self.CLIENT_DISCONNECT:
#         self._connection._remove_ssrc(user_id=int(data['user_id']))


# def patch():
#     VoiceWebSocket = DiscordVoiceWebSocket
#     VoiceWebSocket._orig_received_message = VoiceWebSocket.received_message
#     VoiceWebSocket.received_message = patched_received_message
#     VoiceWebSocket._do_hacks = _do_hacks
