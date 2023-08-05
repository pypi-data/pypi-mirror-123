from amino.lib.util import device


sid = None

class Headers:
    def __init__(self, data = None, type = None, deviceId: str = None, sig: str = None):
        dev = device.DeviceGenerator(deviceId=deviceId if deviceId else None)

        headers = {
            "NDCDEVICEID": dev.device_id,
            "NDC-MSG-SIG": sig,
            "Accept-Language": "en-US",
            "Content-Type": "text/javascript; charset=UTF-8",
            "User-Agent": dev.user_agent,
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Upgrade"
        }

        if data: headers["Content-Length"] = str(len(data))
        if sid: headers["NDCAUTH"] = f"sid={sid}"
        if type: headers["Content-Type"] = type
        self.headers = headers

class ApipHeaders:
    def __init__(self, type=None, deviceId: str = None):
        dev = device.DeviceGenerator(deviceId=deviceId if deviceId else None)

        headers = {
            "NDCDEVICEID": dev.device_id
        }

        if sid:
            headers["NDCAUTH"] = f"sid={sid}"
        if type:
            headers["Content-Type"] = type
        self.headers = headers

class WebHeaders:
    def __init__(self, coockie=None):
        web_headers = {
            "x-requested-with": "xmlhttprequest",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "cookie": "session=.eJwdy8EKgkAQANBfiTl3yAUvgjcrDHZEWR12LlK6pKsrIZaZ-O9F7_5WKB9mdNfBDBME0_g0e6jNq61M2dYQrLC7QQBS1Q2rzGrFHYqiSc7aZ1f0SGy1yDpNhWVK54SyBilepNMfpHxhVR1QHN_4_5dWRieXUOzLqP-d1NfiYtmi05TPTLHHUefhPQxh276zQDOY.YVdIIA.Fhodnlf5muxqriMZCe6g7-qDxnU;"
        }

        if coockie:
            web_headers["cookie"] = coockie
        self.headers = web_headers
