sid = None
deviceId = None
uid = None


# By Bovonos
# Solved By SirLez
class Headers:
    def __init__(self):
        if deviceId: self.deviceId = deviceId
        if not deviceId: self.deviceId = "22F67FB1D87173A6C295BD38AAE7806CCC0173C2A788F6D8E6D66C0A3F29D038C10CD30964D672AB56"
        self.headers = {
            "NDCDEVICEID": self.deviceId,
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; Redmi Note 8 Build/PKQ1.190616.001; com.narvii.amino.master/3.4.33578)",
            "AUID": "dfec1b8a-92f7-4cf0-928c-3b60aa33429a",
            "SMDEVICEID": "6e28d4c5-2d25-4977-93ec-9a4ce077fb7b",
            "Host": "service.narvii.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        self._headers = {
            "NDCDEVICEID": self.deviceId,
        }
        self.web_headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ar,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "x-requested-with": "xmlhttprequest",
        }

        if sid:
            self.headers["NDCAUTH"] = sid
            self._headers["NDCAUTH"] = sid
            self.web_headers["cookie"] = sid
        if uid: self.uid = uid


# By SirLez
class AdHeaders:
    def __init__(self):
        # watch ad data and headers by Marshall (Smile, Texaz)
        # And the headers is Marshall (Smile, Texaz) headers
        self.data = {
            "reward": {
                "ad_unit_id": "255884441431980_807351306285288",
                "credentials_type": "publisher",
                "custom_json": {
                    "hashed_user_id": None
                },
                "demand_type": "sdk_bidding",
                "event_id": None,
                "network": "facebook",
                "placement_tag": "default",
                "reward_name": "Amino Coin",
                "reward_valid": "true",
                "reward_value": 2,
                "shared_id": "dc042f0c-0c80-4dfd-9fde-87a5979d0d2f",
                "version_id": "1569147951493",
                "waterfall_id": "dc042f0c-0c80-4dfd-9fde-87a5979d0d2f"
            },
            "app": {
                "bundle_id": "com.narvii.amino.master",
                "current_orientation": "portrait",
                "release_version": "3.4.33567",
                "user_agent": "Dalvik\/2.1.0 (Linux; U; Android 10; G8231 Build\/41.2.A.0.219; com.narvii.amino.master\/3.4.33567)"
            },
            "date_created": 1620295485,
            "session_id": "49374c2c-1aa3-4094-b603-1cf2720dca67",
            "device_user": {
                "country": "US",
                "device": {
                    "architecture": "aarch64",
                    "carrier": {
                        "country_code": 602,
                        "name": "Vodafone",
                        "network_code": 0
                    },
                    "is_phone": "true",
                    "model": "GT-S5360",
                    "model_type": "Samsung",
                    "operating_system": "android",
                    "operating_system_version": "29",
                    "screen_size": {
                        "height": 2260,
                        "resolution": 2.55,
                        "width": 1080
                    }
                },
                "do_not_track": "false",
                "idfa": "7495ec00-0490-4d53-8b9a-b5cc31ba885b",
                "ip_address": "",
                "locale": "en",
                "timezone": {
                    "location": "Asia\/Seoul",
                    "offset": "GMT+09: 00"
                },
                "volume_enabled": "true"
            }
        }
        self.headers = {
            "cookies": "__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096",
            "authorization": "Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA=="
        }
        if uid: self.data["reward"]["custom_json"]["hashed_user_id"] = uid
