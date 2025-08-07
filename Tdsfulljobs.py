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

    def follow(self, id):
        data = {
            'av': self.user_id, '__user': self.user_id, '__a': '1', 'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest, 'lsd': 'avkT3cHA', 'uid': id
        }
        try:
            response = requests.post(f'https://mbasic.facebook.com/a/subscribe.php?profile_id={id}', headers=self.headers, data=data)
            return "Thành công" in response.text
        except:
            return False

    def like(self, id):
        data = {
            'fb_dtsg': self.fb_dtsg, 'jazoest': self.jazoest, 'ft_id': id,
            'action_type': 'like'
        }
        try:
            response = requests.post(f'https://mbasic.facebook.com/reactions/picker/?ft_id={id}', headers=self.headers, data=data)
            return "Thành công" in response.text
        except:
            return False

    def comment(self, id, message):
        data = {
            'fb_dtsg': self.fb_dtsg, 'jazoest': self.jazoest, 'comment_text': message,
            'comment_action': 'submit', 'post_id': id
        }
        try:
            response = requests.post(f'https://mbasic.facebook.com/{id}', headers=self.headers, data=data)
            return "Thành công" in response.text
        except:
            return False

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

    def get_job(self, type_job):
        try:
            response = requests.get(f'https://traodoisub.com/api/?fields=job&access_token={self.token}&type={type_job}').json()
            return response['data'] if 'data' in response else False
        except:
            return False

    def nhan_xu(self, job_id):
        try:
            response = requests.get(f'https://traodoisub.com/api/nhanxu.php?access_token={self.token}&id={job_id}').json()
            return response['status'] if 'status' in response else False
        except:
            return False

# ────────── BANNER VÀ GIAO DIỆN ──────────
def banner():
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

    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%d/%m/%Y")

    solar = Solar(now.year, now.month, now.day)
    lunar = Converter.Solar2Lunar(solar)
    lunar_str = f"{lunar.day}/{lunar.month}/{lunar.year} (Âm lịch)"

    time_panel = Panel.fit(
        f"[bold cyan]⏰ Giờ hiện tại:[/] {time_str}\n"
        f"[bold green]📅 Dương lịch:[/] {date_str}\n"
        f"[bold magenta]🌙 Âm lịch:[/] {lunar_str}",
        title="[bold white]🕓 Thời Gian",
        border_style="bright_blue"
    )

    console.print(Columns([admin_panel, time_panel]))
    
def Nhap_Cookie():
    list_cookie = []
    i = 0
    while True:
        i += 1
        cookie = Prompt.ask(f"[cyan]=> [/cyan][green]Nhập Cookie Facebook Thứ: {i}[/green]")
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
                chon = Prompt.ask("[cyan]=> [/cyan][green]Nhập ===>[/green]")
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

        # Nhập cookie và chạy nhiệm vụ
        cookies = Nhap_Cookie()
        if not cookies:
            console.print(Panel.fit(
                "Không có cookie nào được nhập! Thoát tool.",
                style="red", title="LỖI"
            ))
            break

        # Chạy các nhiệm vụ
        job_types = ['follow', 'like', 'comment']  # Các loại nhiệm vụ mẫu
        dem = 0
        while True:
            for cookie in cookies:
                fb = Facebook_Api(cookie)
                for job_type in job_types:
                    job = tds.get_job(job_type)
                    if job and len(job) > 0:
                        job_id = random.choice(job)['id']
                        if job_type == 'follow':
                            if fb.follow(job_id):
                                dem += 1
                                hoanthanh(dem, job_id, 'Follow', 'Hoàn thành', xu)
                                if tds.nhan_xu(job_id):
                                    console.print(Panel.fit(
                                        f"Nhận {xu} xu thành công cho job {job_id}",
                                        style="green", title="THÀNH CÔNG"
                                    ))
                                nghingoi(5, 10)
                            else:
                                error(job_id, 'Follow')
                                chongblock(10)
                        elif job_type == 'like':
                            if fb.like(job_id):
                                dem += 1
                                hoanthanh(dem, job_id, 'Like', 'Hoàn thành', xu)
                                if tds.nhan_xu(job_id):
                                    console.print(Panel.fit(
                                        f"Nhận {xu} xu thành công cho job {job_id}",
                                        style="green", title="THÀNH CÔNG"
                                    ))
                                nghingoi(5, 10)
                            else:
                                error(job_id, 'Like')
                                chongblock(10)
                        elif job_type == 'comment':
                            message = f"Comment {random.randint(1, 100)}"
                            if fb.comment(job_id, message):
                                dem += 1
                                hoanthanh(dem, job_id, 'Comment', 'Hoàn thành', xu)
                                if tds.nhan_xu(job_id):
                                    console.print(Panel.fit(
                                        f"Nhận {xu} xu thành công cho job {job_id}",
                                        style="green", title="THÀNH CÔNG"
                                    ))
                                nghingoi(5, 10)
                            else:
                                error(job_id, 'Comment')
                                chongblock(10)
                    else:
                        console.print(Panel.fit(
                            f"Không tìm thấy job {job_type}!",
                            style="yellow", title="THÔNG BÁO"
                        ))
                        time.sleep(5)
            
            # Hỏi xem muốn tiếp tục hoặc thoát
            console.print(Panel.fit(
                "[bold cyan]Nhấn Enter để tiếp tục, hoặc nhập 'q' để thoát.[/bold cyan]",
                title="🔄 QUAY LẠI", border_style="bright_blue"
            ))
            choice = Prompt.ask("[bold yellow]👉 Lựa chọn của bạn[/bold yellow]").strip().lower()
            if choice == 'q':
                console.print(Panel.fit(
                    "[red]Đã thoát tool![/red]",
                    title="❌ THOÁT", border_style="red"
                ))
                sleep(1)
                break
            clear_screen()

if __name__ == '__main__':
    main()
