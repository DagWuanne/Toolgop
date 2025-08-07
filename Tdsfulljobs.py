import requests
import random
import string
import hashlib
import os
import time
import math
import json
import sys
from datetime import datetime
from random import randint
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.columns import Columns
from faker import Faker
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import uuid
import re
from bs4 import BeautifulSoup

console = Console()

# ────────── KHAI BÁO HÀM TIỆN ÍCH ──────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def bongoc(so):
    console.print(Panel.fit("─" * so, style="red", title=""))

def hoanthanh(dem, id, type, msg, xu):
    uid = id.split('_')[1] if '_' in id else id
    time = datetime.now().strftime("%H:%M:%S")
    console.print(Panel.fit(
        f"[red][{dem}][red] | [cyan]{time}[red] | [cyan]{type}[red] | [yellow]{uid}[red] | [green]{msg}[red] | [yellow]{xu}[red]",
        style="red", title="HOÀN THÀNH"
    ))

def error(id, type):
    time = datetime.now().strftime("%H:%M:%S")
    uid = id.split('_')[1] if '_' in id else id
    console.print(Panel.fit(
        f"Đang Lỗi Gì Đó Mong Thông Cảm Nhé | ID: {uid} | Type: {type} | Time: {time}",
        style="red", title="LỖI"
    ))
    time.sleep(2)

def chongblock(delaybl):
    for i in range(delaybl, -1, -1):
        console.print(Panel.fit(
            f"Đang hoạt động chống block sẽ chạy lại sau {i} giây",
            style="yellow", title="CHỐNG BLOCK"
        ), end='\r')
        time.sleep(1)
        console.print(" " * 50, end='\r')

def nghingoi(delaymin, delaymax):
    delay = randint(delaymin, delaymax)
    for i in range(delay, -1, -1):
        time.sleep(1)

# ────────── LỚP FACEBOOK API ──────────
class Facebook_Api:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = cookie.split('c_user=')[1].split(';')[0]
        self.headers = {
            'authority': 'mbasic.facebook.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'origin': 'https://mbasic.facebook.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://mbasic.facebook.com/',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': cookie
        }

    def get_thongtin(self):
        try:
            home = requests.get('https://mbasic.facebook.com/profile.php', headers=self.headers).text
            self.fb_dtsg = home.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
            self.jazoest = home.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
            ten = home.split('<title>')[1].split('</title>')[0]
            return ten, self.user_id
        except:
            return 0

    # (Các hàm follow, page, group, reac_cmt, like, comment, share giữ nguyên như mã gốc)

# ────────── LỚP TRAO ĐỔI SUB API ──────────
class TraoDoiSub_Api:
    def __init__(self, token):
        self.token = token

    def main(self):
        try:
            main = requests.get('https://traodoisub.com/api/?fields=profile&access_token=' + self.token).json()
            return main['data'] if 'data' in main else False
        except:
            return False

    # (Các hàm run, get_job, nhan_xu giữ nguyên như mã gốc)

# ────────── BANNER VÀ GIAO DIỆN ──────────
def banner():
    clear_screen()
    logo = [
        "╔════════════════════╗",
        "║      TOOL TDS      ║",
        "╚════════════════════╝"
    ]
    logo_panel = Panel.fit("\n".join(logo), style="cyan", title="[bold white]THÔNG TIN TOOL", border_style="green")
    
    contact_panel = Panel.fit(
        "YouTube: https://www.youtube.com/channel/UCGJmaIZ_JbAwoOrHeBZru6A\n"
        "Zalo: https://zalo.me/g/wyboil196",
        style="yellow", title="[bold white]LIÊN HỆ", border_style="blue"
    )
    
    console.print(Columns([logo_panel, contact_panel]))
    console.print(Panel.fit(
        f"Thời gian hiện tại: {datetime.now().strftime('%H:%M:%S')} - {datetime.now().strftime('%d/%m/%Y')}",
        style="magenta", title="[bold white]THÔNG TIN"
    ))

def Nhap_Cookie():
    list_cookie = []
    i = 0
    while True:
        i += 1
        cookie = Prompt.ask(f"[cyan][>] => [/cyan][green]Nhập Cookie Facebook Thứ: {i}[/green]")
        if not cookie and i > 1:
            break
        fb = Facebook_Api(cookie)
        name = fb.get_thongtin()
        if name != 0:
            ten = name[0]
            console.print(Panel.fit(
                f"Tên Facebook: [green]{ten}[/green]",
                style="red", title="THÀNH CÔNG"
            ))
            list_cookie.append(cookie)
        else:
            console.print(Panel.fit(
                "Cookie Facebook Die! Vui Lòng Nhập Lại!!!",
                style="red", title="THẤT BẠI"
            ))
    return list_cookie

def main():
    banner()
    while True:
        if os.path.exists('configtds.txt'):
            with open('configtds.txt', 'r') as f:
                token = f.read()
            tds = TraoDoiSub_Api(token)
            data = tds.main()
            try:
                console.print(Panel.fit(
                    f"Giữ Lại Tài Khoản: [green]{data['user']}[/green]",
                    style="blue", title="THÔNG BÁO"
                ))
                console.print(Panel.fit(
                    "Nhập [1] Giữ Access Token | Nhập [2] Nhập Mới",
                    style="blue", title="LỰA CHỌN"
                ))
                chon = Prompt.ask("[cyan][>] => [/cyan][green]Nhập ===>[/green]")
                if chon == '2':
                    os.remove('configtds.txt')
                elif chon == '1':
                    pass
                else:
                    console.print(Panel.fit(
                        "Lựa chọn không xác định!!!",
                        style="red", title="LỖI"
                    ))
                    bongoc(14)
                    continue
            except:
                os.remove('configtds.txt')
        if not os.path.exists('configtds.txt'):
            token = Prompt.ask("[cyan][>] => [/cyan][green]Nhập Access Token TDS:[/green]")
            with open('configtds.txt', 'w') as f:
                f.write(token)
        with open('configtds.txt', 'r') as f:
            token = f.read()
        tds = TraoDoiSub_Api(token)
        data = tds.main()
        try:
            xu = data['xu']
            xudie = data['xudie']
            user = data['user']
            break
        except:
            console.print(Panel.fit(
                "Access Token Không Hợp Lệ! Xin Thử Lại",
                style="red", title="LỖI"
            ))
            os.remove('configtds.txt')
            continue
        console.print(Panel.fit(
            f"Tên Tài Khoản: [green]{user}[/green] | Xu: [yellow]{xu}[/yellow] | Xu Bị Phạt: [red]{xudie}[/red]",
            style="blue", title="THÔNG TIN TÀI KHOẢN"
        ))

        # (Phần nhập cookie và chạy nhiệm vụ giữ nguyên logic, chỉ thay đổi giao diện bằng Panel)

if __name__ == '__main__':
    main()
