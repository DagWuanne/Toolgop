import os
import requests
import json
import base64
import uuid
import re
from time import sleep
from random import randint
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.columns import Columns
from lunarcalendar import Converter, Solar

os.environ['TZ'] = 'Asia/Ho_Chi_Minh'

console = Console()

def banner():
    # Panel thông tin admin
    admin_panel = Panel.fit(
        """[bold blue]Tool by:[/] [bold pink]Đăng Quân [bold green]x [bold red]Đăng Khoa
        
[bold cyan]Facebook Admin 1:[/] facebook.com/admin1
[bold cyan]Facebook Admin 2:[/] facebook.com/admin2
[bold yellow]Zalo Admin:[/] 039xxxx / 039xxxx
[bold red]YouTube:[/] youtube.com/xxxx
[bold blue]Box Zalo:[/] zalo.me/xxx""",
        title="[bold white]Liên hệ Admin",
        border_style="green"
    )

    # Lấy thời gian hiện tại
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%d/%m/%Y")

    # Chuyển sang lịch âm
    solar = Solar(now.year, now.month, now.day)
    lunar = Converter.Solar2Lunar(solar)
    lunar_str = f"{lunar.day}/{lunar.month}/{lunar.year} (Âm lịch)"

    # Panel thời gian & ngày tháng
    time_panel = Panel.fit(
        f"[bold cyan]⏰ Giờ hiện tại:[/] {time_str}\n"
        f"[bold green]📅 Dương lịch:[/] {date_str}\n"
        f"[bold magenta]🌙 Âm lịch:[/] {lunar_str}",
        title="[bold white]🕓 Thời Gian",
        border_style="bright_blue"
    )

    # Hiển thị song song 2 cột
    console.print(Columns([admin_panel, time_panel]))

def Delay(value):
    total = value
    bar_len = 24  # Chiều dài thanh
    step = 0

    while value > 0:
        done = int(((total - value) / total) * bar_len)
        todo = bar_len - done

        # Gradient động: đổi dần từ xanh mint → xanh dương
        bar = "["
        for i in range(bar_len):
            if i < done:
                t = (step + i) % 100 / 100
                r = int(160 + (0 - 160) * t)
                g = int(231 + (128 - 231) * t)
                b = int(229 + (255 - 229) * t)
                bar += f"\033[38;2;{r};{g};{b}m#\033[0m"
            else:
                bar += "."
        bar += "]"

        console.print(bar, end='\r')
        sleep(0.1)
        value -= 0.1
        step += 3  # Đổi màu dần mỗi lần lặp

    console.print(" " * (bar_len + 10), end='\r')  # Xóa dòng sau khi xong

def read_proxy_file(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

class Facebook_Api(object):
    def __init__(self, cookie, proxy=None):
        try:
            self.lsd = ''
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.actor_id = self.cookie.split('c_user=')[1].split(';')[0]
            self.proxies = None
            self.headers = {
                'authority': 'www.facebook.com',
                'accept': '*/*',
                'cookie': self.cookie,
                'origin': 'https://www.facebook.com',
                'referer': 'https://www.facebook.com/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin'
            }
            if proxy:
                try:
                    proxy_parts = proxy.strip().split(':')
                    if len(proxy_parts) == 4:
                        host, port, user, password = proxy_parts
                        self.proxies = {
                            'http': f'http://{user}:{password}@{host}:{port}',
                            'https': f'http://{user}:{password}@{host}:{port}'
                        }
                except Exception as e:
                    console.print(Panel.fit(
                        f"[red]Lỗi khởi tạo proxy: {str(e)}[/red]",
                        title="[bold red]LỖI", border_style="red"
                    ))
                    self.proxies = None
            url = requests.get(f'https://www.facebook.com/{self.actor_id}', headers=self.headers, proxies=self.proxies).url
            response = requests.get(url, headers=self.headers, proxies=self.proxies).text
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg = matches[0]
                self.jazoest = re.findall(r'jazoest=(.*?)\"', response)[0]
                self.lsd = re.findall(r'\["LSD",\[\],\{"token":"(.*?)"\}', response)[0]
        except:
            console.print(Panel.fit(
                f"[red]Lỗi khởi tạo API Facebook![/red]",
                title="[bold red]LỖI", border_style="red"
            ))

    def info(self):
        get = requests.get('https://www.facebook.com/me', headers=self.headers, proxies=self.proxies).text
        try:
            name = get.split('<title>')[1].split('</title>')[0]
            return {'success': 200, 'id': self.actor_id, 'name': name}
        except:
            return {'error': 200}

    def Checkspam(self):
        data = {
            "av": self.actor_id,
            "__user": self.actor_id,
            "__a": "1",
            "__req": "8",
            "__hs": "20038.HYP:comet_pkg.2.1..2.1",
            "dpr": "1",
            "__ccg": "EXCELLENT",
            "__rev": "1018089718",
            "__s": "mtrukx:3ui1ys:yphvdu",
            "__hsi": "7435940161710523784",
            "__dyn": "7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D8vwRwlE-U2zxe2GewbS361qw8Xwn82Lx-0lK3qazo720Bo2ZwrU6C0hq1Iwqo35wvodo7u2-2K0UE",
            "__csr": "gzl5849ahWFaeU-rK4Uyii9VAmWl6zpUCUgK3K2mi2q2Ki687W08Pyo1yp9Esw14e0OE1u80now05XXw0Dhw0eNi",
            "__comet_req": "15",
            "fb_dtsg": self.fb_dtsg,
            "jazoest": self.jazoest,
            "lsd": self.lsd,
            "__spin_r": "1018089718",
            "__spin_b": "trunk",
            "__spin_t": "1731314734",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "FBScrapingWarningMutation",
            "variables": "{}",
            "server_timestamps": "true",
            "doc_id": "6339492849481770"
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        return response.text

    def reaction(self, id, type):
        reac = {
            "LIKE": "1635855486666999",
            "LOVE": "1678524932434102",
            "CARE": "613557422527858",
            "HAHA": "115940658764963",
            "WOW": "478547315650144",
            "SAD": "908563459236466",
            "ANGRY": "444813342392137"
        }
        idreac = reac.get(type)
        data = {
            'av': self.actor_id,
            '__usid': r'6-Tsfgotwhb2nus:Psfgosvgerpwk:0-Asfgotw11gc1if-RV=6:F=',
            '__aaid': '0',
            '__user': self.actor_id,
            '__a': '1',
            '__req': '2c',
            '__hs': '19896.HYP:comet_pkg.2.1..2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1014402108',
            '__s': '5vdtpn:wbz2hc:8r67q5',
            '__hsi': '7383159623287270781',
            '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C17xt3odE98K361twYwJyE24wJwpUe8hwaG1sw9u0LVEtwMw65xO2OU7m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwqo31wiE567Udo5qfK0zEkxe2GewyDwkUe9obrwKxm5oe8464-5pUfEdK261eBx_wHwdG7FoarCwLyES0Io88cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13whEeE4WVU-4EdrxG1fy8bUaU',
            '__csr': 'gug_2A4A8gkqTf2Ih6RFnbk9mBqaBaTs8_tntineDdSyWqiGRYCiPi_SJuLCGcHBaiQXtLpXsyjIymm8oFJswG8CSGGLzAq8AiWZ6VGDgyQiiTBKU-8GczE9USmi4A9DBABHgWEK3K9y9prxaEa9KqQV8qUlxW22u4EnznDxSewLxq3W2K16BxiE5VqwbW1dz8qwCwjoeEvwaKVU6q0yo5a2i58aE7W0CE5O0fdw1jim0dNw7ewPBG0688025ew0bki0cow3c8C05Vo0aNF40BU0rmU3LDwaO06hU06RG6U1g82Bw0Gxw6Gw',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            '__spin_r': '1014402108',
            '__spin_b': 'trunk',
            '__spin_t': '1719025807',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
            'variables': f'{{"input":{{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,1719027162723,322693,4748854339,,","feedback_id":"{encode_to_base64("feedback:"+str(id))}","feedback_reaction_id":"{idreac}","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"tracking":["AZWUDdylhKB7Q-Esd2HQq9i7j4CmKRfjJP03XBxVNfpztKO0WSnXmh5gtIcplhFxZdk33kQBTHSXLNH-zJaEXFlMxQOu_JG98LVXCvCqk1XLyQqGKuL_dCYK7qSwJmt89TDw1KPpL-BPxB9qLIil1D_4Thuoa4XMgovMVLAXncnXCsoQvAnchMg6ksQOIEX3CqRCqIIKd47O7F7PYR1TkMNbeeSccW83SEUmtuyO5Jc_wiY0ZrrPejfiJeLgtk3snxyTd-JXW1nvjBRjfbLySxmh69u-N_cuDwvqp7A1QwK5pgV49vJlHP63g4do1q6D6kQmTWtBY7iA-beU44knFS7aCLNiq1aGN9Hhg0QTIYJ9rXXEeHbUuAPSK419ieoaj4rb_4lA-Wdaz3oWiWwH0EIzGs0Zj3srHRqfR94oe4PbJ6gz5f64k0kQ2QRWReCO5kpQeiAd1f25oP9yiH_MbpTcfxMr-z83luvUWMF6K0-A-NXEuF5AiCLkWDapNyRwpuGMs8FIdUJmPXF9TGe3wslF5sZRVTKAWRdFMVAsUn-lFT8tVAZVvd4UtScTnmxc1YOArpHD-_Lzt7NDdbuPQWQohqkGVlQVLMoJNZnF_oRLL8je6-ra17lJ8inQPICnw7GP-ne_3A03eT4zA6YsxCC3eIhQK-xyodjfm1j0cMvydXhB89fjTcuz0Uoy0oPyfstl7Sm-AUoGugNch3Mz2jQAXo0E_FX4mbkMYX2WUBW2XSNxssYZYaRXC4FUIrQoVhAJbxU6lomRQIPY8aCS0Ge9iUk8nHq4YZzJgmB7VnFRUd8Oe1sSSiIUWpMNVBONuCIT9Wjipt1lxWEs4KjlHk-SRaEZc_eX4mLwS0RcycI8eXg6kzw2WOlPvGDWalTaMryy6QdJLjoqwidHO21JSbAWPqrBzQAEcoSau_UHC6soSO9UgcBQqdAKBfJbdMhBkmxSwVoxJR_puqsTfuCT6Aa_gFixolGrbgxx5h2-XAARx4SbGplK5kWMw27FpMvgpctU248HpEQ7zGJRTJylE84EWcVHMlVm0pGZb8tlrZSQQme6zxPWbzoQv3xY8CsH4UDu1gBhmWe_wL6KwZJxj3wRrlle54cqhzStoGL5JQwMGaxdwITRusdKgmwwEQJxxH63GvPwqL9oRMvIaHyGfKegOVyG2HMyxmiQmtb5EtaFd6n3JjMCBF74Kcn33TJhQ1yjHoltdO_tKqnj0nPVgRGfN-kdJA7G6HZFvz6j82WfKmzi1lgpUcoZ5T8Fwpx-yyBHV0J4sGF0qR4uBYNcTGkFtbD0tZnUxfy_POfmf8E3phVJrS__XIvnlB5c6yvyGGdYvafQkszlRrTAzDu9pH6TZo1K3Jc1a-wfPWZJ3uBJ_cku-YeTj8piEmR-cMeyWTJR7InVB2IFZx2AoyElAFbMuPVZVp64RgC3ugiyC1nY7HycH2T3POGARB6wP4RFXybScGN4OGwM8e3W2p-Za1BTR09lHRlzeukops0DSBUkhr9GrgMZaw7eAsztGlIXZ_4"],"session_id":"{uuid.uuid4()}","actor_id":"{self.actor_id}","client_mutation_id":"3"}},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}}',
            'server_timestamps': 'true',
            'doc_id': '7047198228715224',
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        if '{"data":{"feedback_react":{"feedback":{"id":' in response.text:
            return True
        else:
            return False

    def reactioncmt(self, id, type):
        reac = {
            "LIKE": "1635855486666999",
            "LOVE": "1678524932434102",
            "CARE": "613557422527858",
            "HAHA": "115940658764963",
            "WOW": "478547315650144",
            "SAD": "908563459236466",
            "ANGRY": "444813342392137"
        }
        g_now = datetime.now()
        d = g_now.strftime("%Y-%m-%d %H:%M:%S.%f")
        datetime_object = datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f")
        timestamp = str(datetime_object.timestamp())
        starttime = timestamp.replace('.', '')
        id_reac = reac.get(type)
        data = {
            'av': self.actor_id,
            '__aaid': '0',
            '__user': self.actor_id,
            '__a': '1',
            '__req': '1a',
            '__hs': '19906.HYP:comet_pkg.2.1..2.1',
            'dpr': '1',
            '__ccg': 'GOOD',
            '__rev': '1014619389',
            '__s': 'z5ciff:vre7af:23swxc',
            '__hsi': '7387045920424178191',
            '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C17xt3odE98K360CEboG0x8bo6u3y4o2Gwn82nwb-q7oc81xoswMwto886C11wBz83WwgEcEhwGxu782lwv89kbxS1Fwc61awkovwRwlE-U2exi4UaEW2G1jwUBwJK2W5olwUwgojUlDw-wUwxwjFovUaU3qxW2-VEbUGdG0HE88cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13whEeE4WVU-4EdrxG1fy8bUaU',
            '__csr': 'gJ0AH5n4n4PhcQW4Oh4JFsIH4f5ji9iWuzqSltFlETn_trnbH_YIJX9iWiAiQBpeht9uYyhrvOOaiSV9CKmriyF4EzjBGh4XRqy8O4Z4HGypAaDAG8DzE-iKii5bUGaiXyocA22iayUOUG9BKUkxe2vBBxe5898S5k48fogxqQU9oO1bwiU9FpEowOBwYwLCw86u2y0Eo885-1uwFwOwpU1jo7-0IU108iw8i0kq0bVw6gBxa4E1g83tw0_yBw2hE012EoG0uG0gh068w23Q0dlw0wKw68Aw0huU0a7VU0jkw0E-w8W0cPK6U',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            '__spin_r': '1014619389',
            '__spin_b': 'trunk',
            '__spin_t': '1719930656',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
            'variables': f'{{"input":{{"attribution_id_v2":"CometVideoHomeNewPermalinkRoot.react,comet.watch.injection,via_cold_start,1719930662698,975645,2392950137,,","feedback_id":"{encode_to_base64("feedback:"+str(id))}","feedback_reaction_id":"{id_reac}","feedback_source":"TAHOE","is_tracking_encrypted":true,"tracking":[],"session_id":"{str(uuid.uuid4())}","downstream_share_session_id":"{str(uuid.uuid4())}","downstream_share_session_origin_uri":"https://fb.watch/t3OatrTuqv/?mibextid=Nif5oz","downstream_share_session_start_time":"{starttime}","actor_id":"{self.actor_id}","client_mutation_id":"1"}},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}}',
            'server_timestamps': 'true',
            'doc_id': '7616998081714004',
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        if '{"data":{"feedback_react":{"feedback":{"id":' in response.text:
            return True
        else:
            return False

    def share(self, id):
        data = {
            'av': self.actor_id,
            '__usid': r'6-Tsftw3x1vqj8dz:Psftw2g2c595x:0-Asftw3x1etit7l-RV=6:F=',
            '__aaid': '0',
            '__user': self.actor_id,
            '__a': '1',
            '__req': '1o',
            '__hs': '19901.HYP:comet_pkg.2.1..2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1014511729',
            '__s': '8zktjb:5quia4:fu1x9q',
            '__hsi': '7384980750065440159',
            '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C17xt3odE98K360CEboG0x8bo6u3y4o2Gwn82nwb-q7oc81xoswMwto886C11wBz83WwgEcEhwGxu782lwv89kbxS1Fwc61awkovwRwlE-U2exi4UaEW2G1jwUBwJK2W5olwUwgojUlDw-wUwxwjFovUaU3qxW2-VEbUGdG0HE88cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13whEeE4WVU-4EdrxG1fy8bUaU',
            '__csr': 'gdk8MPs4dNYQYp4iOSD9sG2fZqN79mKHYBH4qrNP5bifl8IyAF-CDQGFdBdlTmeimHGOWJKhCKRWDLjGmV94uVpprh6FaDD_GcG5F4ECVqgCqhqRAKhd2oGAUBzaUCibGVHy9EFeayEjCxim598oxmmCETxObKuuUyfzF8411e2e7VHyq-dG8AK4oW4ogK69XzEy7U4aFQ4EdE426UKdxm7E98sG15Cw8Oi1awgUaolwvUO8wrU3ewNwt9UOvwko16o1z81uo1gA0cww1pHxGQE2Kw0sv80Ii6E03c4U9olw1N21Cw1eu05rE1oUmxiew0iIU0e5k0m-02jW1RyU2pwPw3uU0u3w4wAo0Xi0Bk',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            '__spin_r': '1014511729',
            '__spin_b': 'trunk',
            '__spin_t': '1719449821',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ComposerStoryCreateMutation',
            'variables': f'{{"input":{{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"{str(uuid.uuid4())}_FEED","source":"WWW","attachments":[{{"link":{{"share_scrape_data":"{{\\"share_type\\":22,\\"share_params\\":[{id}]}}"}}}}],"reshare_original_post":"RESHARE_ORIGINAL_POST","audience":{{"privacy":{{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}}}},"is_tracking_encrypted":true,"tracking":["AZWWGipYJ1gf83pZebtJYQQ-iWKc5VZxS4JuOcGWLeB-goMh2k74R1JxqgvUTbDVNs-xTyTpCI4vQw_Y9mFCaX-tIEMg2TfN_GKk-PnqI4xMhaignTkV5113HU-3PLFG27m-EEseUfuGXrNitybNZF1fKNtPcboF6IvxizZa5CUGXNVqLISUtAWXNS9Lq-G2ECnfWPtmKGebm2-YKyfMUH1p8xKNDxOcnMmMJcBBZkUEpjVzqvUTSt52Xyp0NETTPTVW4zHpkByOboAqZj12UuYSsG3GEhafpt91ThFhs7UTtqN7F29UsSW2ikIjTgFPy8cOddclinOtUwaoMaFk2OspLF3J9cwr7wPsZ9CpQxU21mcFHxqpz7vZuGrjWqepKQhWX_ZzmHv0LR8K07ZJLu8yl51iv-Ram7er9lKfWDtQsuNeLqbzEOQo0UlRNexaV0V2m8fYke8ubw3kNeR5XsRYiyr958OFwNgZ3RNfy-mNnO9P-4TFEF12NmNNEm4N6h0_DRZ-g74n-X2nGwx9emPv4wuy9kvQGeoCqc636BfKRE-51w2GFSrHAsOUJJ1dDryxZsxQOEGep3HGrVp_rTsVv7Vk3JxKxlzqt3hnBGDgi6suTZnJw69poVOIz6TPCTthRhj7XUu4heyKBSIeHsjBRC2_s3NwuZ4kKNCQ2JkVuBXz_hsRhDmbAnBi6WUFIJhLHO_bGgKbEASuU4vtj4FNKo_G8p-J1kYmCo0Pi72Csi3EikuocfjHFwfSD3cCbetr3V8Yp6OmSGkqX63FkSqzBoAcHFeD-iyCAkn0UJGqU-0o670ZoR-twkUDcSJPXDN2NYQfqiyb9ZknZ7j04w1ZfAyaE7NCiCc-lDt1ic79XyHunjOyLStgXIW30J4OEw_hAn86LlRHbYVhi-zBBTZWWnEl9piuUz0qtnN-qEd002DjNYaMy0aDAbL9oOYDdN8mHvnXq1aKove9I4Jy0WtlxeN8279ayz7NdDZZ9LrajY_YxIJJqdZtJIuRYTunEeDsFrORpu3RYRbFwpGnQbHeSLH1YvwOyOJRXhYYmVLJEGD2N9r5wkPbgbx2HoWsGjWj_DpkEAyg59eBJy4RYPJHvOsetBQABEWmGI7nhUDYTPdhrzVxqB_g4fQ9JkPzIbEhcoEZjmspGZcR4z4JxUDJCNdAz2aK4lR4P5WTkLtj2uXMDD_nzbl8r_DMcj23bjPiSe0Fubu-VIzjwr7JgPNyQ1FYhp5u4lpqkkBkGtfyAaUjCgFhg4FW-H3d3vPVMO--GxbhK9kN0QAcOE3ZqQR2dRz6NbhcvTyNfDxy0dFTRw-f-vxn04gjJB5ZEG3WfSzQv0VbqDYm6-NFYAzIxbDLoiCu34WAa2lckx5qxncXBhQj6Fro2gXGPXo4d32DvqQg7_RHQ-SF_WLqdxRCXF91NIqxYmFZsOJAuQ5m6TafzuNnQoJB3OQFoknv8Uy5O4FKuwazh1rvLrsj-1QEMi3sTrr9KxJkZy9EKXs92ndlb3edgfycLOffTil-gW2BvxeNiMQzqF1xJqFBKHDyatgwpXDX81HDwxkuMEaGPREIeQLuOlBJrL_20RD1e4Gu4tjQD8vRsb29UNG60DqpDvc-H4Z2oxeppm0KIwQNaCTtGUxxmvT807fXMnuVEf5QI5qTx9YRJh56GiWLoHC_zPMhoikMbAybIVWh9HtVgZGgImDmz0l9P4LgtpKNnKbQj_2ZKn2ZhOYKZLdt1P2Jq2Z2z76MtbRQTrpZpFb14zWVnh1LFCSFPAB7sqC1-u-KQOf2_SjEecztPccso8xZB2nkhLetyPn9aFuO-J_LCZydQeiroXx4Z8NxhDpbLoOpw2MbRCVB_TxfnLGNn1QD0To9TTChxK5AHNRRLDaj3xK1e0jd37uSmHTkT6QJVHFHEYMVLBcuV1MQcoy0wsvc1sRb",null],"logging":{{"composer_session_id":"{str(uuid.uuid4())}"}},"navigation_data":{{"attribution_id_v2":"FeedsCometRoot.react,comet.most_recent_feed,tap_bookmark,1719641912186,189404,608920319153834,,"}},"event_share_metadata":{{"surface":"newsfeed"}},"actor_id":"{self.actor_id}","client_mutation_id":"3"}},"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":false,"renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":true,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometIsAdaptiveUFIEnabledrelayprovider":true,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__IncludeCommentWithAttachmentrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__StoriesRingrelayprovider":false,"__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider":false}}',
            'server_timestamps': 'true',
            'doc_id': '8167261726632010'
        }
        response = requests.post("https://www.facebook.com/api/graphql/", headers=self.headers, data=data, proxies=self.proxies)
        if '"errors"' not in response.text:
            return True
        else:
            return False

    def like_page(self, id):
        data = {
            'av': self.actor_id,
            '__aaid': '0',
            '__user': self.actor_id,
            '__a': '1',
            '__req': 'v',
            '__hs': '20038.HYP:comet_pkg.2.1..2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1018088939',
            '__s': 'z2jloc:ulhc8m:wfcq07',
            '__hsi': '7435892510460455151',
            '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2CE4i5QdwSwAyUco5S3O2Saw8i2S1DwUx60GE5O0BU2_CxS320qa2OU7m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwqo31wiE567Udo5qfK0zEkxe2GewyDwkUe9obrwh8lwUwgojUlDw-wUwxwjFovUaU3qxW2-VEbUGdG0HE88cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13xe3a3Gfw-Kufxa3mUqwjVqwLwHwea',
            '__csr': 'goMkMmFYnk44OdtsAixBEr5ndERq8jiFnqsLeGayYyWJmqOH9dhJW8XiXZ5GKl2aji8WjAmG8AWlBF5hFtVppFFLhVo-rWiJ4Az-l13hGAy5-qmFGKbp4AS8BBxCWAAz8y8UjyFpAV-cAKchoC8UO2afgmx-lUF1emeCBXyo88C6U8Egz41DK262O788UOfgC3m6oS2-i48Z3E9lxu69U8e2a4o4TwhEdo6q2y1Ywk84W1lweim1jwywj8fE1r80NK053E14aS01LRwuE0d2E02Xbwlo18A0iLg0g5w1f-091w2MU0NK1-w3WE0row0AXw0sNovwOK0lq0EU0nNw208',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            '__spin_r': '1018088939',
            '__spin_b': 'trunk',
            '__spin_t': '1731314734',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometPageLikeSubscriptionMutation',
            'variables': f'{{"input":{{"actor_id":"{self.actor_id}","page_id":"{id}","subscribe_location":"COMET_PAGE_PROFILE","actor_subscription_level":"FULL","subscribee_id":"{id}"}}}}',
            'server_timestamps': 'true',
            'doc_id': '6771492972874691'
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        if '"errors"' not in response.text:
            return True
        else:
            return False

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    Delay(3)  # Hiển thị thanh tiến trình trước khi vào

    # Nhập cookie
    console.print(Panel.fit(
        "[bold cyan]Nhập cookie Facebook (hoặc đường dẫn file chứa cookie)[/bold cyan]",
        title="[bold green]NHẬP COOKIE", border_style="green"
    ))
    cookie_input = Prompt.ask("[bold yellow]Cookie[/bold yellow]").strip()
    if os.path.exists(cookie_input):
        with open(cookie_input, 'r') as f:
            cookies = [line.strip() for line in f if line.strip()]
    else:
        cookies = [cookie_input]

    # Nhập proxy
    console.print(Panel.fit(
        "[bold cyan]Nhập file proxy (hoặc bỏ qua để không dùng proxy)[/bold cyan]",
        title="[bold green]NHẬP PROXY", border_style="green"
    ))
    proxy_file = Prompt.ask("[bold yellow]File proxy[/bold yellow]").strip()
    proxies = read_proxy_file(proxy_file) if proxy_file else []

    # Kiểm tra cookie
    accounts = []
    for i, cookie in enumerate(cookies):
        proxy = proxies[i % len(proxies)] if proxies else None
        fb = Facebook_Api(cookie, proxy)
        info = fb.info()
        if 'success' in info:
            console.print(Panel.fit(
                f"[green]Cookie hợp lệ! ID: [yellow]{info['id']}[/yellow] | Name: [yellow]{info['name']}[/yellow]",
                title="[bold green]KIỂM TRA COOKIE", border_style="green"
            ))
            accounts.append(fb)
        else:
            console.print(Panel.fit(
                f"[red]Cookie không hợp lệ![/red]",
                title="[bold red]LỖI", border_style="red"
            ))

    if not accounts:
        console.print(Panel.fit(
            f"[red]Không có cookie hợp lệ, thoát chương trình![/red]",
            title="[bold red]LỖI", border_style="red"
        ))
        return

    # Lựa chọn nhiệm vụ
    console.print(Panel.fit(
        """[bold green]1.[/] Like bài viết
[bold green]2.[/] Reaction bài viết
[bold green]3.[/] Reaction bình luận
[bold green]4.[/] Share bài viết
[bold green]5.[/] Like page""",
        title="[bold cyan]DANH SÁCH NHIỆM VỤ", border_style="bright_magenta"
    ))
    while True:
        try:
            choice = IntPrompt.ask("[bold yellow]Lựa chọn nhiệm vụ (1-5)[/bold yellow]")
            if choice in [1, 2, 3, 4, 5]:
                break
            else:
                console.print(Panel.fit(
                    f"[red]Lỗi lựa chọn! Chỉ nhập 1-5[/red]",
                    title="[bold red]LỖI", border_style="red"
                ))
        except:
            console.print(Panel.fit(
                f"[red]Lỗi lựa chọn! Chỉ nhập 1-5[/red]",
                title="[bold red]LỖI", border_style="red"
            ))

    # Nhập ID và loại reaction (nếu cần)
    post_id = Prompt.ask("[bold yellow]Nhập ID bài viết hoặc page[/bold yellow]").strip()
    reaction_type = None
    if choice in [2, 3]:
        console.print(Panel.fit(
            """[bold green]1.[/] LIKE
[bold green]2.[/] LOVE
[bold green]3.[/] CARE
[bold green]4.[/] HAHA
[bold green]5.[/] WOW
[bold green]6.[/] SAD
[bold green]7.[/] ANGRY""",
            title="[bold cyan]LOẠI REACTION", border_style="bright_magenta"
        ))
        while True:
            try:
                reac_choice = IntPrompt.ask("[bold yellow]Lựa chọn loại reaction (1-7)[/bold yellow]")
                if reac_choice in [1, 2, 3, 4, 5, 6, 7]:
                    reaction_types = ["LIKE", "LOVE", "CARE", "HAHA", "WOW", "SAD", "ANGRY"]
                    reaction_type = reaction_types[reac_choice - 1]
                    break
                else:
                    console.print(Panel.fit(
                        f"[red]Lỗi lựa chọn! Chỉ nhập 1-7[/red]",
                        title="[bold red]LỖI", border_style="red"
                    ))
            except:
                console.print(Panel.fit(
                    f"[red]Lỗi lựa chọn! Chỉ nhập 1-7[/red]",
                    title="[bold red]LỖI", border_style="red"
                ))

    # Nhập delay
    while True:
        try:
            delay = IntPrompt.ask("[bold yellow]Thời gian delay giữa các hành động (giây)[/bold yellow]")
            if delay > 2:
                break
            else:
                console.print(Panel.fit(
                    f"[red]Delay tối thiểu là 3[/red]",
                    title="[bold red]LỖI", border_style="red"
                ))
        except:
            console.print(Panel.fit(
                f"[red]Vui lòng nhập một số > 2[/red]",
                title="[bold red]LỖI", border_style="red"
            ))

    # Thực hiện nhiệm vụ
    for i, fb in enumerate(accounts):
        console.print(Panel.fit(
            f"[cyan]Đang xử lý tài khoản {i+1}/{len(accounts)} (ID: [yellow]{fb.actor_id}[/yellow])[/cyan]",
            title="[bold green]TIẾN TRÌNH", border_style="green"
        ))
        if choice == 1:
            result = fb.reaction(post_id, "LIKE")
            action = "Like bài viết"
        elif choice == 2:
            result = fb.reaction(post_id, reaction_type)
            action = f"Reaction {reaction_type} bài viết"
        elif choice == 3:
            result = fb.reactioncmt(post_id, reaction_type)
            action = f"Reaction {reaction_type} bình luận"
        elif choice == 4:
            result = fb.share(post_id)
            action = "Share bài viết"
        elif choice == 5:
            result = fb.like_page(post_id)
            action = "Like page"

        if result:
            console.print(Panel.fit(
                f"[green]{action} thành công![/green]",
                title="[bold green]THÀNH CÔNG", border_style="green"
            ))
        else:
            console.print(Panel.fit(
                f"[red]{action} thất bại![/red]",
                title="[bold red]LỖI", border_style="red"
            ))
        Delay(delay)

    console.print(Panel.fit(
        f"[green]Hoàn thành tất cả nhiệm vụ![/green]",
        title="[bold green]HOÀN THÀNH", border_style="green"
    ))

if __name__ == "__main__":
    main()
