import atexit
import json
import os
import pathlib
import sys

import msal
import pywikibot
import requests
import hashlib
import utils

logger = utils.getLogger("ImgHost")

HUALIQS_CONFIG = {
    'token': '',
    'apiType': 'bilibili',
}

CSS_PAGE = "User:ONIzhBot/odImg.css"
IMG_DIR = os.path.join("ImgHost", "images")
CSS_DIR = os.path.join("ImgHost", "out", "images.css")
JSON_DIR = os.path.join("ImgHost", "out", "images.json")
SUCCESS_DIR = os.path.join("ImgHost", "out", "success.json")
ERROR_DIR = os.path.join("ImgHost", "out", "error.json")
UNUSED_DIR = os.path.join("ImgHost", "out", "unused.json")
SECRETS_DIR = os.path.join("ImgHost", "secrets.json")
MS_CACHE_DIR = os.path.join("ImgHost", "ms_cache.bin")
pathlib.Path(IMG_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.join("ImgHost", "out")).mkdir(parents=True, exist_ok=True)


def get_secrets(name):
    if name in os.environ:
        return os.environ.get(name)
    with open(SECRETS_DIR, 'r') as f:
        j = json.load(f)
    return j[name]


ONEDRIVE_FOLDER = "webimg"
FOLDER_AUTHKEY = "AEjDC4tmctPSNRE"
MS_CONFIG = {
    "authority": "https://login.microsoftonline.com/Common",
    'username': os.environ.get("OD_USERNAME") or 'oni-zh-cn@outlook.com',
    "client_id": get_secrets('MS_CLIENT_ID'),
    "scope": ["Files.Read", "Files.Read.All", "Files.ReadWrite", "Files.ReadWrite.All"],
    "secret": get_secrets('MS_SECRET'),
    "url_list": f"https://graph.microsoft.com/v1.0/me/drive/root:/{ONEDRIVE_FOLDER}:/children",
    "url_upload": f"https://graph.microsoft.com/v1.0/me/drive/root:/{ONEDRIVE_FOLDER}/$1:/content",
    "url_file": f"http://storage.live.com/items/$1?authkey={FOLDER_AUTHKEY}",
}


def file_sha1(f_path):
    buf_size = 65536  # lets read stuff in 64kb chunks!
    sha1 = hashlib.sha1()
    if pathlib.Path(f_path).is_file():
        with open(f_path, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()
    return ""


def download(site=pywikibot.Site("zh", "oni")):
    files = list(site.allimages(content=True))
    file_records = {}
    if pathlib.Path(IMG_DIR).is_file():
        with open(JSON_DIR, 'r') as f:
            file_records = json.load(f)
    for i, f in enumerate(files):
        if i % 10 == 0:
            logger.info(f"Downloaded {i} of {len(files)}")
        if not isinstance(f, pywikibot.FilePage):
            continue
        t = f.title(with_ns=False)
        if t in file_records and file_records[t]['sha1'] == f.latest_file_info.sha1:
            continue
        if file_sha1(os.path.join(IMG_DIR, t)) != f.latest_file_info.sha1:
            f.download(os.path.join(IMG_DIR, t))
        file_records[t] = {
            "url": f.get_file_url(),
            "sha1": f.latest_file_info.sha1,
            "mime": pywikibot.FilePage(f).latest_file_info.mime,
        }
    with open(JSON_DIR, 'w') as f:
        json.dump(file_records, f, indent=2)


def upload_hualiqs(f_name, img_records: dict, success: list, error: list):
    with open(os.path.join(IMG_DIR, f_name), "rb") as f:
        r = requests.post('https://www.hualigs.cn/api/upload', data=HUALIQS_CONFIG, files={"image": f})

    if r.status_code == 200:
        try:
            response = r.json()
            if response["code"] == 200:
                cdn = response["data"]["url"][HUALIQS_CONFIG['apiType']]
                success.append({"source": f_name, "cdn": cdn})
                img_records[f_name]['cdn'] = cdn
                logger.info(f"Uploaded: {f_name} -- {cdn}")
            else:
                error.append({"code": response["code"], "msg": response["msg"]})
        except json.decoder.JSONDecodeError as e:
            logger.warning(e)
    else:
        error.append({"source": f_name, "code": r.status_code, "msg": "HTTP Code"})


class SharePoint:
    @staticmethod
    def get_cache():
        cache = msal.SerializableTokenCache()
        if os.path.exists(MS_CACHE_DIR):
            cache.deserialize(open(MS_CACHE_DIR, "r").read())

        def on_exit():
            if cache.has_state_changed:
                with open(MS_CACHE_DIR, 'w') as f:
                    f.write(cache.serialize())

        atexit.register(on_exit)
        return cache

    def __init__(self):
        self.app = None
        self.header = None
        self.exist_files = {}
        cache = SharePoint.get_cache()
        self.app = msal.PublicClientApplication(
            MS_CONFIG["client_id"], authority=MS_CONFIG["authority"],
            token_cache=cache
        )

        result = None
        accounts = self.app.get_accounts(username=MS_CONFIG["username"])
        if accounts:
            result = self.app.acquire_token_silent(MS_CONFIG["scope"], account=accounts[0])
        if not result:
            flow = self.app.initiate_device_flow(scopes=MS_CONFIG["scope"])
            if "user_code" not in flow:
                raise ValueError(
                    "Fail to create device flow. Err: %s" % json.dumps(flow, indent=2))
            sys.stdout.flush()
            logger.warning(flow["message"])
            result = self.app.acquire_token_by_device_flow(flow)
            open(MS_CACHE_DIR, "w").write(cache.serialize())
        if "access_token" in result:
            self.header = {'Authorization': f'Bearer {result["access_token"]}'}

            curr_req = MS_CONFIG["url_list"]
            first = True
            while True:
                result = requests.get(
                    curr_req,
                    headers=self.header,
                    params={
                        "$select": ','.join(["name", "id", "file"]),
                    } if first else None).json()
                first = False
                for e in result['value']:
                    self.exist_files[e['name']] = e
                if "@odata.nextLink" in result:
                    curr_req = result["@odata.nextLink"]
                else:
                    break
        else:
            logger.fatal(result.get("error"))
            logger.fatal(result.get("error_description"))
            logger.fatal(result.get("correlation_id"))  # You may need this when reporting a bug

    def update(self, f_name, img_records: dict, success: list, error: list):
        if f_name in self.exist_files:
            self.exist_files[f_name]['used'] = True
        f_record = img_records[f_name]
        local_hash = f_record['sha1']
        if f_name in self.exist_files:
            exist_current = self.exist_files[f_name]
            if exist_current['file']['hashes']['sha1Hash'].upper() == local_hash.upper():
                cdn = MS_CONFIG['url_file'].replace('$1', exist_current['id'])
                success.append({"source": f_name, "cdn": cdn})
                f_record['cdn'] = cdn
                logger.info(f"Hash matches: {f_name} -- {cdn}")
                return
        with open(os.path.join(IMG_DIR, f_name), "rb") as f:
            try:
                r = requests.put(
                    MS_CONFIG['url_upload'].replace('$1', f_name),
                    headers={**self.header, 'Content-Type': f_record['mime']},
                    data=f
                )
                if r.status_code == 200 or r.status_code == 201:

                    response = r.json()
                    cdn = MS_CONFIG['url_file'].replace('$1', response['id'])
                    success.append({"source": f_name, "cdn": cdn})
                    f_record['cdn'] = cdn
                    logger.info(f"Uploaded: {f_name} -- {cdn}")

                else:
                    error.append({"source": f_name, "code": r.status_code, "msg": "HTTP Code"})

            except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
                logger.warning(e)
                error.append({"source": f_name, "e": str(e)})

    def un_used(self):
        return [self.exist_files[x] for x in self.exist_files if not self.exist_files[x].get('used')]


def upload(method='ms'):
    success = []
    error = []
    share_point = SharePoint()
    upload_methods = {
        'hualiqs': upload_hualiqs,
        'ms': share_point.update,
    }

    with open(JSON_DIR, mode="r") as f:
        img_records = json.load(f)

    for i, f_name in enumerate(img_records):
        if i % 10 == 0:
            logger.info(f"Uploaded {i} of {len(img_records)}")
        upload_methods[method](f_name, img_records, success, error)

        with open(JSON_DIR, 'w') as f:
            json.dump(img_records, f, indent=2)
        with open(SUCCESS_DIR, 'w') as f:
            json.dump(success, f, indent=2)
        with open(ERROR_DIR, 'w') as f:
            json.dump(error, f, indent=2)

    if method == 'ms':
        with open(UNUSED_DIR, 'w') as f:
            json.dump(share_point.un_used(), f, indent=2)


def create_css():
    with open(JSON_DIR, mode="r") as f:
        img_records = json.load(f)

    with open(CSS_DIR, 'w', encoding="utf-8") as f:
        f_names = [f_name for f_name in img_records if 'cdn' in img_records[f_name]]
        f_names = sorted(f_names, key=lambda k: img_records[k]['cdn'])
        for f_name in f_names:
            if 'cdn' in img_records[f_name]:
                f.write(f'''img[data-image-name="{f_name}"]{{
    content:url("{img_records[f_name]['cdn']}");
}}\n''')


def upload_css(site):
    p = pywikibot.Page(site, CSS_PAGE)
    with open(CSS_DIR, 'r', encoding='utf-8') as f:
        p.text = f.read()
    p.save("Update Image links")


if __name__ == "__main__":
    # oni_zh = pywikibot.Site('zh', 'oni')
    # download(oni_zh)
    # upload('ms')
    # create_css()
    # upload_css(oni_zh)
    pass
