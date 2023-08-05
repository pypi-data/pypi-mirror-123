import json

from functools import reduce
from base64 import b64decode
from typing import BinaryIO
from zipfile import ZipFile


def generate_device_info() -> dict:
    return {
        "device_id": "22CCEA23A7F868405192250D13EDA48245F4442E89293554E7A7320BA4E3F7C6E79985F239D012C1B2",
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)"
    }

def chat_bubble_file(image_path: str, out_path: str = "./", name: str = "Custom Bubble", allowed_slots: list = None,
                              content_insest_bottom: int = 23, content_insest_right: int = 32, content_insest_top: int = 17, content_insest_left: int = 42,
                              cover_image_url: str = None, zoom_point_in: int = 57, zoom_point_out: int = 39, text_color: str = "#643573", link_color: str = "#e065ff",
                              templateId: str = "71b41f1a-4c09-4e07-ac9e-18ef9bbbe65f", prewiew_background_url: str = None, bubbleId: str = None) -> BinaryIO:
    """
    Generate chat bubble from template.

    **Parameters**
        - **image_path** : Path to bubble image.
        - **name** : Bubble name.
        - **allowed_slots** : Allowed sticker slots.
        - **content_insest_bottom** : Bottom insest.
        - **content_insest_right** : Right insest.
        - **content_insest_top** : Top insest.
        - **content_insest_left** : Left insest.
        - **cover_image_url** : Cover image url.
        - **zoom_point_in** : In zoom point.
        - **zoom_point_out** : Out zoom point.
        - **text_color** : Hex text color.
        - **link_color** : Hex link color.
        - **templateId** : ID tamplate to generate bubble.
        - **prewiew_background_url** : Prewiew background url.

    **Returns**
        - **Success** : :meth:`Chat Bubble File`
        - **Fail** : :meth:`Exceptions`
    """

    config = {
        "status": 0,
        "allowedSlots": [
            {"y": -2, "x": 0, "align": 1},
            {"y": -2, "x": -12, "align": 2},
            {"y": 3, "x": -12, "align": 4},
            {"y": 3, "x": 0, "align": 3}
        ],
        "name": name,
        "vertexInset": 0,
        "contentInsets": [
            content_insest_bottom,
            content_insest_right,
            content_insest_top,
            content_insest_left
        ],
        "coverImage": "http://cb1.narvii.com/8073/09fabdb0e8bcd05e4e27365b1a2b54f536828235r10-349-169_00.png",
        "bubbleType": 1,
        "zoomPoint": [
            zoom_point_in,
            zoom_point_out
        ],
        "version": 1,
        "linkColor": link_color,
        "templateId": templateId,
        "slots": None,
        "backgroundPath": "bg.png",
        "id": bubbleId,
        "color": text_color,
        "previewBackgroundUrl": "http://cb1.narvii.com/images/6846/65d316d6529153c76e2b8e8756739355f2720764_00.png"
    }

    if allowed_slots:
        config["allowedSlots"] = allowed_slots

    if prewiew_background_url:
        config["previewBackgroundUrl"] = prewiew_background_url
    
    if cover_image_url:
        config["coverImage"] = cover_image_url

    with ZipFile(f"{out_path}{name}.zip", 'w') as zip_file:
        zip_file.writestr("config.json", json.dumps(config))
        zip_file.write(image_path, "bg.png")

    return f"{out_path}{name}.zip"


# okok says: please use return annotations :(( https://www.python.org/dev/peps/pep-3107/#return-values

def decode_sid(sid: str) -> dict:
    return json.loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + "=" * (-len(sid) % 4)).encode())[1:-20].decode())

def sid_to_uid(SID: str) -> str: return decode_sid(SID)["2"]

def sid_to_ip_address(SID: str) -> str: return decode_sid(SID)["4"]
