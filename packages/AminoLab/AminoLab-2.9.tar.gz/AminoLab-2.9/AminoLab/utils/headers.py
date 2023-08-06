sid = None
user_Id = None
device_Id = None

class Headers:
    def __init__(self, device_Id: str = None, sid: str = None):
        self.headers = {
            "cookie": sid,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36",
            "x-requested-with": "xmlhttprequest"
            }
        self.headers["set-cookie"] = sid 
        if user_Id:
                self.user_Id = user_Id
      

        self.headers_v2 = {"NDCDEVICEID": device_Id, "NDCAUTH": sid}