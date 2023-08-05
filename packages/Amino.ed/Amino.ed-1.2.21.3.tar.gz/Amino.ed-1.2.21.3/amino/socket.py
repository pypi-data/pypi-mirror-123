import time
import json
import requests
import websocket
import threading
import contextlib

from sys import _getframe as getframe

from .lib.util import objects


class SocketHandler:
    def __init__(self, client, socket_trace=False, debug=False):
        if socket_trace:
            websocket.enableTrace(True)
        self.client = client
        self.debug = debug
        self.active = True
        self.socket = None
        self.socket_thread = None
        self.reconnect = True
        self.socket_stoped = False
        self.socketDelay = 0
        self.socket_trace = socket_trace
        self.socketDelayFetch = 120  # Reconnects every 120 seconds.
        self.active_vc = False

    def run_socket(self):
        threading.Thread(target=self.reconnect_handler, args=(True, )).start()
        websocket.enableTrace(self.socket_trace)

    def reconnect_handler(self, start_socket = False):
        # Made by enchart#3410 thx
        # Fixed by The_Phoenix#3967
        # Fixed by enchart again lmao
        # Fixed by Phoenix one more time lol
        # Fixed by alert ahahahhah...

        if start_socket:
            self.start()

        while True:
            if self.debug:
                print(f"[socket][reconnect_handler] socketDelay : {self.socketDelay}")

            if self.socketDelay >= self.socketDelayFetch and self.active:
                if self.debug:
                    print(f"[socket][reconnect_handler] socketDelay >= {self.socketDelayFetch}, Reconnecting Socket")

                self.close()
                self.start()
                self.socketDelay = 0

            self.socketDelay += 5

            if not self.reconnect:
                if self.debug:
                    print(f"[socket][reconnect_handler] reconnect is False, breaking")
                break

            time.sleep(5)

    def on_open(self):
        if self.debug:
            print("[socket][on_open] Socket Opened")
        self.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")

    def on_close(self):
        if self.debug:
            print("[socket][on_close] Socket Closed")

        self.active = False

        if self.reconnect:
            if self.debug:
                print("[socket][on_close] reconnect is True, Opening Socket")

    def on_ping(self, data):
        if self.debug:
            print("[socket][on_ping] Socket Pinged")

        contextlib.suppress(self.socket.sock.pong(data))

    def handle_message(self, data):
        self.client.handle_socket_message(data)
        return

    def send(self, data):
        if self.debug:
            print(f"[socket][send] Sending Data : {data}")

        self.socket.send(data)

    def get_websocket_url(self):
        headers = {"cookie": f"sid={self.client.sid};"}
        response = requests.get(f"{self.client.web_api}/chat/web-socket-url", headers=headers)
        if response.status_code != 200:
            raise Exception(response.json())
        else:
            return response.json()["result"]["url"]

    def start(self):
        if self.debug:
            print(f"[socket][start] Starting Socket")
        
        if not self.socket_stoped:
            Warning("[socket][start] Old socket is not closed.")

        self.socket = websocket.WebSocketApp(
            self.get_websocket_url(),
            on_message=self.handle_message,
            on_open=self.on_open,
            on_close=self.on_close,
            on_ping=self.on_ping
        )

        threading.Thread(target=self.socket.run_forever).start()
        self.reconnect = True
        self.active = True

        if self.debug:
            print(f"[socket][start] Socket Started")

    def close(self):
        if self.debug:
            print(f"[socket][close] Closing Socket")

        self.reconnect = False
        self.active = False
        try:
            self.socket.close()
            self.socket_stoped = True
        except Exception as closeError:
            if self.debug:
                print(f"[socket][close] Error while closing Socket : {closeError}")

        return
    

    # SOCKET FUNCTIONS
    def join_voice_chat(self, comId: str, chatId: str, joinType: int = 1):
        """
        Joins a Voice Chat

        **Parameters**
            - **comId** : ID of the Community
            - **chatId** : ID of the Chat
        """

        # Made by Light, Ley and Phoenix

        data = json.dumps({
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"
            },
            "t": 112
        })
        self.send(data)

    def join_video_chat(self, comId: str, chatId: str, joinType: int = 1):
        """
        Joins a Video Chat

        **Parameters**
            - **comId** : ID of the Community
            - **chatId** : ID of the Chat
        """

        # Made by Light, Ley and Phoenix

        data = json.dumps({
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "channelType": 5,
                "id": "2154531"
            },
            "t": 108
        })
        self.send(data)

    def join_video_chat_as_viewer(self, comId: str, chatId: str):
        data = json.dumps({
            "o":
                {
                    "ndcId": int(comId),
                    "threadId": chatId,
                    "joinRole": 2,
                    "id": "72446"
                },
            "t": 112
        })
        self.send(data)

    def run_vc(self, comId: str, chatId: str, joinType: str):
        while self.active_vc:
            data = json.dumps({
                "o": {
                    "ndcId": comId,
                    "threadId": chatId,
                    "joinRole": joinType,
                    "id": "2154531"
                },
                "t": 112
            })
            self.send(data)
            time.sleep(1)

    def start_vc(self, comId: str, chatId: str, joinType: int = 1):
        data = json.dumps({
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"
            },
            "t": 112
        })

        self.send(data)
        data = json.dumps({
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "channelType": 1,
                "id": "2154531"
            },
            "t": 108
        })
        self.send(data)
        self.active_vc = True
        threading.Thread(target=self.run_vc, args=[comId, chatId, joinType])

    def end_vc(self, comId: str, chatId: str, joinType: int = 2):
        self.active_vc = False
        data = json.dumps({
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"
            },
            "t": 112
        })
        self.send(data)
    
    def send_action(self, comId: str, actions: list, chatId: str = None, chatType: int = 2,
            blogId: str = None, quizId: str = None, lastAction: bool = False):
        # Action List
        # - Browsing
        # - Chatting
        # - Typing

        if lastAction is True: t = 306
        else: t = 304

        data = {
            "o": {
                "actions": actions,
                "target": f"ndc://x{comId}/",
                "ndcId": int(comId),
                "id": "831046"
            },
            "t": t
        }

        if blogId is not None or quizId is not None and chatId is None:
            data["target"] = f"ndc://x{comId}/blog/{blogId}"

            if blogId or quizId: data["params"] = {}
            if blogId is not None: data["params"]["blogType"] = 0
            if quizId is not None: data["params"]["blogType"] = 6
        
        if chatId is not None and blogId is None and quizId is None:
            data["target"] = f"ndc://x{comId}/chat-thread/{chatId}"
            if chatType: data["params"] = {"threadType": chatType}

        return self.send(json.dumps(data))

class Callbacks:
    def __init__(self, client):
        self.client = client
        self.handlers = {}

        self.methods = {
            304: self._resolve_chat_action_start, #wait more events ;)
            306: self._resolve_chat_action_end, #i searching..
            1000: self._resolve_chat_message #lol, what i write.
        }

        self.chat_methods = {
            "0:0": self.on_text_message,
            "0:100": self.on_image_message,
            "0:103": self.on_youtube_message,
            "1:0": self.on_strike_message,
            "2:110": self.on_voice_message,
            "3:113": self.on_sticker_message,
            "50:0": self.TYPE_USER_SHARE_EXURL,
            "51:0": self.TYPE_USER_SHARE_USER,
            "52:0": self.on_voice_chat_not_answered,
            "53:0": self.on_voice_chat_not_cancelled,
            "54:0": self.on_voice_chat_not_declined,
            "55:0": self.on_video_chat_not_answered,
            "56:0": self.on_video_chat_not_cancelled,
            "57:0": self.on_video_chat_not_declined,
            "58:0": self.on_avatar_chat_not_answered,
            "59:0": self.on_avatar_chat_not_cancelled,
            "60:0": self.on_avatar_chat_not_declined,
            "100:0": self.on_delete_message,
            "101:0": self.on_group_member_join,
            "102:0": self.on_group_member_leave,
            "103:0": self.on_chat_invite,
            "104:0": self.on_chat_background_changed,
            "105:0": self.on_chat_title_changed,
            "106:0": self.on_chat_icon_changed,
            "107:0": self.on_voice_chat_start,
            "108:0": self.on_video_chat_start,
            "109:0": self.on_avatar_chat_start,
            "110:0": self.on_voice_chat_end,
            "111:0": self.on_video_chat_end,
            "112:0": self.on_avatar_chat_end,
            "113:0": self.on_chat_content_changed,
            "114:0": self.on_screen_room_start,
            "115:0": self.on_screen_room_end,
            "116:0": self.on_chat_host_transfered,
            "117:0": self.on_text_message_force_removed,
            "118:0": self.on_chat_removed_message,
            "119:0": self.on_text_message_removed_by_admin,
            "120:0": self.on_chat_tip,
            "121:0": self.on_chat_pin_announcement,
            "122:0": self.on_voice_chat_permission_open_to_everyone,
            "123:0": self.on_voice_chat_permission_invited_and_requested,
            "124:0": self.on_voice_chat_permission_invite_only,
            "125:0": self.on_chat_view_only_enabled,
            "126:0": self.on_chat_view_only_disabled,
            "127:0": self.on_chat_unpin_announcement,
            "128:0": self.on_chat_tipping_enabled,
            "129:0": self.on_chat_tipping_disabled,
            "65281:0": self.on_timestamp_message,
            "65282:0": self.on_welcome_message,
            "65283:0": self.on_invite_message
        }

        self.chat_actions_start = {
            "Typing": self.on_user_typing_start,
        }

        self.chat_actions_end = {
            "Typing": self.on_user_typing_end,
        }

    def _resolve_chat_message(self, data):
        key = f"{data['o']['chatMessage']['type']}:{data['o']['chatMessage'].get('mediaType', 0)}"
        return self.chat_methods.get(key, self.default)(data)

    def _resolve_chat_action_start(self, data):
        key = data['o'].get('actions', 0)
        return self.chat_actions_start.get(key, self.default)(data)

    def _resolve_chat_action_end(self, data):
        key = data['o'].get('actions', 0)
        return self.chat_actions_end.get(key, self.default)(data)

    def resolve(self, data):
        data = json.loads(data)
        return self.methods.get(data["t"], self.default)(data)

    def call(self, type, data):
        if type in self.handlers:
            for handler in self.handlers[type]:
                handler(data)

    def event(self, type):
        def registerHandler(handler):
            if type in self.handlers:
                self.handlers[type].append(handler)
            else:
                self.handlers[type] = [handler]
            return handler

        return registerHandler

    def on_text_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_image_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_youtube_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_strike_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_sticker_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def TYPE_USER_SHARE_EXURL(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def TYPE_USER_SHARE_USER(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_chat_not_answered(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_chat_not_cancelled(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_chat_not_declined(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_video_chat_not_answered(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_video_chat_not_cancelled(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_video_chat_not_declined(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_avatar_chat_not_answered(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_avatar_chat_not_cancelled(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_avatar_chat_not_declined(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_delete_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_group_member_join(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_group_member_leave(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_invite(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_background_changed(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_title_changed(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_icon_changed(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_chat_start(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_video_chat_start(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_avatar_chat_start(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_chat_end(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_video_chat_end(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_avatar_chat_end(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_content_changed(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_screen_room_start(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_screen_room_end(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_host_transfered(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_text_message_force_removed(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_removed_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_text_message_removed_by_admin(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_tip(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_pin_announcement(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_chat_permission_open_to_everyone(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_chat_permission_invited_and_requested(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_voice_chat_permission_invite_only(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_view_only_enabled(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_view_only_disabled(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_unpin_announcement(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_tipping_enabled(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_chat_tipping_disabled(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_timestamp_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_welcome_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_invite_message(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_user_typing_start(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def on_user_typing_end(self, data): self.call(
        getframe(0).f_code.co_name, objects.Event(data["o"]).Event)

    def default(self, data): self.call(getframe(0).f_code.co_name, data)
