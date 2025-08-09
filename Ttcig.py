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
from rich.columns import Columns
from rich.prompt import Prompt
from rich.text import Text
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from lunarcalendar import Converter, Solar  # Thêm để hỗ trợ lịch âm

console = Console()

# ────────── HÀM TIỆN ÍCH ──────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(dl):
    for i in range(dl, -1, -1):
        console.print(Panel.fit(
            f"[bold magenta][PHUOCAN][/] [yellow][{i} Giây]",
            style="bold magenta", title="ĐỢI CHỜ"
        ), end='\r')
        time.sleep(1)
    console.print(" " * 50, end='\r')

def bongoc(so):
    console.print(Panel.fit("─" * (so * 4), style="red", title=""))

# ────────── BANNER VÀ GIAO DIỆN MỚI ──────────
def banner():
    # Panel thông tin admin (kèm Tool by...)
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

# ────────── CHỨC NĂNG TOOL ──────────
def coin(ckvp):
    h_xu = {'user-agent': 'Mozilla/5.0 (Linux; Android 11; Live 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.28 Mobile Safari/537.36', 'cookie': ckvp}
    x = requests.post('https://vipig.net/home.php', headers=h_xu).text
    xu = x.split('"soduchinh">')[1].split('<')[0]
    return xu

def cookie(token):
    ck = requests.post('https://vipig.net/logintoken.php', headers={'Content-type': 'application/x-www-form-urlencoded'}, data={'access_token': token})
    return 'PHPSESSID=' + (ck.cookies)['PHPSESSID']

def get_nv(type, ckvp):
    headers = {
        'content-type': 'text/html; charset=UTF-8', 'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'referer': 'https://vipig.net/kiemtien/', 'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?1', 'user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty', 'cookie': ckvp
    }
    a = requests.post(f'https://vipig.net/kiemtien{type}/getpost.php', headers=headers).json()
    return a

def nhan_tien(list, ckvp, type):
    data_xu = 'id=' + str(list)
    data_nhan = str(len(data_xu))
    headers = {
        'content-length': data_nhan, 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-mobile': '?1', 'x-requested-with': 'XMLHttpRequest', 'sec-fetch-site': 'same-origin',
        'origin': 'https://vipig.net', 'sec-ch-ua-platform': '"Android"', 'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty', 'referer': f'https://vipig.net/kiemtien{type}/', 'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5', 'cookie': ckvp
    }
    a = requests.post(f'https://vipig.net/kiemtien{type}/nhantien.php', headers=headers, data=data_xu).text
    return a

def nhan_sub(list, ckvp):
    data_xu = 'id=' + str(list[0:len(list)-1])
    data_nhan = str(len(data_xu))
    headers = {
        'content-length': data_nhan, 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-mobile': '?1', 'x-requested-with': 'XMLHttpRequest', 'sec-fetch-site': 'same-origin',
        'origin': 'https://vipig.net', 'sec-ch-ua-platform': '"Android"', 'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty', 'referer': 'https://vipig.net/kiemtien/subcheo', 'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5', 'cookie': ckvp
    }
    a = requests.post('https://vipig.net/kiemtien/subcheo/nhantien2.php', headers=headers, data=data_xu).json()
    return a

def name(cookie):
    try:
        headers = {
            'Host': 'www.instagram.com', 'cache-control': 'max-age=0', 'viewport-width': '980',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"', 'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document', 'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5', 'cookie': cookie
        }
        a = requests.get('https://www.instagram.com/', headers=headers).text
        user = re.search(r'contacts":null,"username":"(.*?)"', a).group(1)
        id = cookie.split('ds_user_id=')[1].split(';')[0]
        return user, id
    except:
        return 'die', 'die'

def cau_hinh(id_ig, ckvp):
    headers = {
        'content-length': '23', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'accept': '*/*', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest', 'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty', 'referer': 'https://vipig.net/cauhinh/datnick.php',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5', 'cookie': ckvp
    }
    a = requests.post('https://vipig.net/cauhinh/datnick.php', headers=headers, data={'iddat[]': id_ig}).text
    return a

def like(id, cookie):
    headers = {
        "x-ig-app-id": "1217981644879628", "x-asbd-id": "198387", "x-instagram-ajax": "c161aac700f",
        "accept": "*/*", "content-length": "0", "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
        "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0], "x-requested-with": "XMLHttpRequest",
        "cookie": cookie
    }
    like = requests.post(f'https://www.instagram.com/web/likes/{id}/like/', headers=headers).text
    return '2' if 'ok' in like else '1'

def get_id(link):
    headers = {
        "x-ig-app-id": "1217981644879628", "x-asbd-id": "198387", "x-instagram-ajax": "c161aac700f",
        "accept": "*/*", "content-length": "0", "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
        "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0], "x-requested-with": "XMLHttpRequest",
        "cookie": cookie
    }
    try:
        a = requests.get(link, headers=headers).text
        id = a.split('media?id=')[1].split('"')[0]
        return id
    except:
        return False

def follow(id, cookie):
    headers = {
        "x-ig-app-id": "1217981644879628", "x-asbd-id": "198387", "x-instagram-ajax": "c161aac700f",
        "accept": "*/*", "content-length": "0", "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
        "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0], "x-requested-with": "XMLHttpRequest",
        "cookie": cookie
    }
    fl = requests.post(f"https://i.instagram.com/web/friendships/{id}/follow/", headers=headers).text
    return '2' if 'ok' in fl else '1'

def cmt(msg, id, cookie):
    headers = {
        "x-ig-app-id": "1217981644879628", "x-asbd-id": "198387", "x-instagram-ajax": "c161aac700f",
        "accept": "*/*", "content-length": "0", "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
        "x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0], "x-requested-with": "XMLHttpRequest",
        "cookie": cookie
    }
    cmt = requests.post(f'https://i.instagram.com/api/v1/web/comments/{id}/add/', headers=headers, data={'comment_text': msg}).json()
    return 'ok' if cmt.get('status') == 'ok' else '1'

# ────────── CHẠY TOOL ──────────
if __name__ == '__main__':
    dem = 0
    list_cookie = []

    while True:
        print("\033[1;32m--------------------------------------------")
        token = input('\033[1;32mNhập Access_Token Vipig:\033[1;33m ')
        log = requests.post('https://vipig.net/logintoken.php', headers={'Content-type': 'application/x-www-form-urlencoded'}, data={'access_token': token}).json()
        if log['status'] == 'success':
            user = log['data']['user']
            xu = log['data']['sodu']
            ckvp = cookie(token)
            console.print(Panel.fit(
                f"[green bold]Đăng Nhập Thành Công[/]",
                title="✅ THÀNH CÔNG", border_style="green"
            ))
            break
        elif log['status'] == 'fail':
            console.print(Panel.fit(
                f"[red]{log['mess']}[/red]",
                title="⛔ THẤT BẠI", border_style="red"
            ))

    clear_screen()
    banner()
    console.print(Panel.fit(
        f"[red]════════════════════════════════════════════════════[/]",
        title=""
    ))
    console.print(Panel.fit(
        f"[bold green]Tên Tài Khoản:[/] [yellow]{user}\n"
        f"[bold green]Xu:[/] [yellow]{xu}\n"
        f"[bold green]Số Cookie Đã Lưu:[/] [yellow]{len(list_cookie)}",
        title="", border_style="red"
    ))
    console.print(Panel.fit(
        f"[red]════════════════════════════════════════════════════[/]",
        title=""
    ))

    console.print(Panel.fit(
        "[bold green]Job Hiện Đang Có:[/]",
        title="", border_style="green"
    ))
    console.print(Panel.fit(
        "[green]~♥~ => Nhập [1] Chạy Job LikePost[/]\n"
        "[green]~♥~ => Nhập [2] Chạy Job FollowCheo[/]\n"
        "[green]~♥~ => Nhập [3] Chạy Job Cmtcheo[/]\n"
        "[green]~♥~ => Có thể chạy full NV 😆 VD (123...)[/]",
        title="", border_style="green"
    ))
    console.print(Panel.fit(
        f"[red]════════════════════════════════════════════════════[/]",
        title=""
    ))

    chon = Prompt.ask("[bold cyan][♡] => Nhập NV Cần Chạy :[/]")
    dl = int(Prompt.ask("[bold cyan]Delay Thực Hiện Job: [/]"))
    chong_block = int(Prompt.ask("Sau Bao Nhiêu Nhiệm Vụ Chống Block : "))
    delay_block = int(Prompt.ask(f"Sau {chong_block} Nhiệm Vụ Nghỉ Ngơi "))
    doi_acc = int(Prompt.ask("Sau Bao Nhiêu Nhiệm Vụ Thì Đổi Nick IG: "))
    console.print(Panel.fit(
        f"[red]════════════════════════════════════════════════════[/]",
        title=""
    ))

    while True:
        x = 0
        rvtool247 = 0
        if len(list_cookie) == 0:
            console.print(Panel.fit(
                "[red]Toàn Bộ Cookie Đã Out Vui Lòng Nhập Lại !! [/red]",
                title="⚠️ CẢNH BÁO", border_style="red"
            ))
            while True:
                x += 1
                cookie = Prompt.ask(f"[green]Nhập Cookie Instagram Thứ {x}:[/]")
                if cookie == '' and x > 1:
                    break
                ten = name(cookie)
                if ten[0] != 'die':
                    console.print(Panel.fit(
                        f"[yellow]User Acc IG:[/] [magenta]{ten[0]}",
                        title="✅ THÀNH CÔNG", border_style="green"
                    ))
                    list_cookie.append(cookie)
                else:
                    console.print(Panel.fit(
                        "[red]Cookie Instagram Sai ! Vui Lòng Nhập Lại !!! [/red]",
                        title="⛔ THẤT BẠI", border_style="red"
                    ))
                    x -= 1

        for i in range(len(list_cookie)):
            if rvtool247 == 2:
                break
            loi_like = 0
            loi_cmt = 0
            cookie = list_cookie[i]
            user = name(cookie)
            id_ig = user[1]
            if user[0] == 'die':
                console.print(Panel.fit(
                    "[red]Cookie Instagram Die !!!! [/red]",
                    title="⚠️ LỖI", border_style="red"
                ))
                list_cookie.remove(cookie)
                continue
            ngoc = cau_hinh(id_ig, ckvp)
            if ngoc == '1':
                console.print(Panel.fit(
                    f"[green]Cấu Hình ID Success :[/] [yellow]{id_ig} | [green]User:[/] [yellow]{user[0]}",
                    title="✅ THÀNH CÔNG", border_style="green"
                ))
            else:
                console.print(Panel.fit(
                    f"[red]Cấu Hình Thất Bại ID:[/] [yellow]{id_ig} | [green]User:[/] [yellow]{user[0]} [/red]",
                    title="⛔ THẤT BẠI", border_style="red"
                ))
                delay(3)
                list_cookie.remove(cookie)
                continue
            rvtool247 = 0
            while True:
                if rvtool247 == 1 or rvtool247 == 2:
                    break
                if '1' in chon:
                    get_like = get_nv('', ckvp)
                    if len(get_like) == 0:
                        console.print(Panel.fit(
                            "[yellow]Tạm Thời Hết Nhiệm Vụ Like[/]",
                            title="ℹ️ THÔNG BÁO", border_style="yellow"
                        ), end='\r')
                    if len(get_like) != 0:
                        console.print(Panel.fit(
                            f"[green]Tìm Thấy[/] [yellow]{len(get_like)}[/] [green]Nhiệm Vụ Like[/]",
                            title="ℹ️ THÔNG BÁO", border_style="green"
                        ), end='\r')
                    for x in get_like:
                        link = x['link']
                        uid = x['idpost']
                        id = get_id(link)
                        if id == False:
                            continue
                        lam = like(id, cookie)
                        if lam == '1':
                            user = name(cookie)
                            if user[0] == 'die':
                                console.print(Panel.fit(
                                    "[red]Cookie Instagram Die !!!! [/red]",
                                    title="⚠️ LỖI", border_style="red"
                                ))
                                list_cookie.remove(cookie)
                                rvtool247 = 2
                                break
                            else:
                                console.print(Panel.fit(
                                    f"[red]Tài Khoản {user[0]} Đã Bị Chặn Tương Tác [/red]",
                                    title="⚠️ LỖI", border_style="red"
                                ))
                                list_cookie.remove(cookie)
                                rvtool247 = 2
                                break
                        elif loi_like >= 4:
                            console.print(Panel.fit(
                                f"[red]Tài Khoản {user[0]} Đã Bị Chặn Tương Tác [/red]",
                                title="⚠️ LỖI", border_style="red"
                            ))
                            list_cookie.remove(cookie)
                            rvtool247 = 2
                            break
                        elif lam == '2':
                            nhan = nhan_tien(uid, ckvp, '')
                            if 'mess' in nhan:
                                xu = coin(ckvp)
                                dem += 1
                                tg = datetime.now().strftime("%H:%M:%S")
                                console.print(Panel.fit(
                                    f"[red]|[/] [yellow]{dem}[/] [red]|[/] [cyan]{tg}[/] [red]|[/] [green]LIKE[/] [red]|[/] [magenta]+300xu[/] [red]|[/] [white]{id}[/] [red]|[/] [purple]{user[0]}[/] [red]|[/] [blue]{xu}[/]",
                                    title="✅ HOÀN THÀNH", border_style="red"
                                ))
                                loi_like = 0
                                if dem % chong_block == 0:
                                    delay(delay_block)
                                else:
                                    delay(dl)
                                if dem % doi_acc == 0:
                                    rvtool247 = 1
                                    break
                            else:
                                tg = datetime.now().strftime("%H:%M:%S")
                                console.print(Panel.fit(
                                    f"[green]Like :[/] [white]{id} [/] [red]Thất bại.[/]",
                                    title="⛔ THẤT BẠI", border_style="red"
                                ))
                                loi_like += 1
                                delay(dl)

                if rvtool247 == 1 or rvtool247 == 2:
                    break
                if '2' in chon:
                    get_sub = get_nv('/subcheo', ckvp)
                    if len(get_sub) == 0:
                        console.print(Panel.fit(
                            "[yellow]Tạm Thời Hết Nhiệm Vụ Follow[/]",
                            title="ℹ️ THÔNG BÁO", border_style="yellow"
                        ), end='\r')
                    if len(get_sub) != 0:
                        console.print(Panel.fit(
                            f"[green]Tìm Thấy[/] [yellow]{len(get_sub)}[/] [green]Nhiệm Vụ Follow[/]",
                            title="ℹ️ THÔNG BÁO", border_style="green"
                        ), end='\r')
                    for x in get_sub:
                        id = x['soID']
                        lam = follow(id, cookie)
                        if lam == '1':
                            if user[0] == 'die':
                                console.print(Panel.fit(
                                    "[red]Cookie Instagram Die !!!! [/red]",
                                    title="⚠️ LỖI", border_style="red"
                                ))
                                list_cookie.remove(cookie)
                            else:
                                console.print(Panel.fit(
                                    f"[red]Tài Khoản {user[0]} Đã Bị Chặn Tương Tác [/red]",
                                    title="⚠️ LỖI", border_style="red"
                                ))
                                list_cookie.remove(cookie)
                            rvtool247 = 2
                            break
                        data_id = open(f"{id_ig}.txt", "a+")
                        data_id.write(str(id) + ',')
                        dem += 1
                        tg = datetime.now().strftime("%H:%M:%S")
                        console.print(Panel.fit(
                            f"[red]|[/] [yellow]{dem}[/] [red]|[/] [cyan]{tg}[/] [red]|[/] [green]FOLLOW[/] [red]|[/] [green]SUCCESS[/] [red]|[/] [white]{id}[/]",
                            title="✅ HOÀN THÀNH", border_style="red"
                        ))
                        data_id = open(f"{id_ig}.txt", "r")
                        list = data_id.read()
                        dem_sub = len(list.split(',')) - 1
                        if dem % chong_block == 0:
                            delay(delay_block)
                        else:
                            delay(dl)
                        if dem_sub >= 6:
                            nhan = nhan_sub(list, ckvp)
                            try:
                                xu_them = nhan['sodu']
                                job = xu_them // 600
                                xu = coin(ckvp)
                                console.print(Panel.fit(
                                    f"[green]Nhận Thành Công {job} Nhiệm Vụ Followcheo | [/] [magenta]+{xu_them} | [/] [blue]{xu}[/]",
                                    title="✅ THÀNH CÔNG", border_style="green"
                                ))
                            except:
                                console.print(Panel.fit(
                                    f"[red]{nhan}[/red]",
                                    title="⛔ THẤT BẠI", border_style="red"
                                ))
                            os.remove(f"{id_ig}.txt")
                            dem_sub = 0
                        if dem % doi_acc == 0:
                            rvtool247 = 1
                            break

                if rvtool247 == 1 or rvtool247 == 2:
                    break
                if '3' in chon:
                    get_cmt = get_nv('/cmtcheo', ckvp)
                    if len(get_cmt) == 0:
                        console.print(Panel.fit(
                            "[yellow]Tạm Thời Hết Nhiệm Vụ Comment[/]",
                            title="ℹ️ THÔNG BÁO", border_style="yellow"
                        ), end='\r')
                    if len(get_cmt) != 0:
                        console.print(Panel.fit(
                            f"[green]Tìm Thấy[/] [yellow]{len(get_cmt)}[/] [green]Nhiệm Vụ Comment[/]",
                            title="ℹ️ THÔNG BÁO", border_style="green"
                        ), end='\r')
                    for x in get_cmt:
                        link = x['link']
                        uid = x['idpost']
                        msg = random.choice(json.loads(x['nd']))
                        id = get_id(link)
                        if id == False:
                            continue
                        lam = cmt(msg, id, cookie)
                        if lam == '1':
                            user = name(cookie)
                            if user[0] == 'die':
                                console.print(Panel.fit(
                                    "[red]Cookie Instagram Die !!!! [/red]",
                                    title="⚠️ LỖI", border_style="red"
                                ))
                                list_cookie.remove(cookie)
                                rvtool247 = 2
                                break
                            else:
                                console.print(Panel.fit(
                                    f"[red]Tài Khoản {user[0]} Đã Bị Chặn Tương Tác [/red]",
                                    title="⚠️ LỖI", border_style="red"
                                ))
                                list_cookie.remove(cookie)
                                rvtool247 = 2
                                break
                        elif loi_cmt >= 4:
                            console.print(Panel.fit(
                                f"[red]Tài Khoản {user[0]} Đã Bị Chặn Tương Tác [/red]",
                                title="⚠️ LỖI", border_style="red"
                            ))
                            list_cookie.remove(cookie)
                            rvtool247 = 2
                            break
                        elif lam == 'ok':
                            nhan = nhan_tien(uid, ckvp, '/cmtcheo')
                            if 'mess' in nhan:
                                xu = coin(ckvp)
                                dem += 1
                                tg = datetime.now().strftime("%H:%M:%S")
                                console.print(Panel.fit(
                                    f"[red]|[/] [yellow]{dem}[/] [red]|[/] [cyan]{tg}[/] [red]|[/] [green]CMTCHEO[/] [red]|[/] [magenta]+600xu[/] [red]|[/] [white]{id}[/] [red]|[/] [purple]{user[0]}[/] [red]|[/] [blue]{xu}[/]",
                                    title="✅ HOÀN THÀNH", border_style="red"
                                ))
                                loi_cmt = 0
                                if dem % chong_block == 0:
                                    delay(delay_block)
                                else:
                                    delay(dl)
                                if dem % doi_acc == 0:
                                    rvtool247 = 1
                                    break
                            else:
                                tg = datetime.now().strftime("%H:%M:%S")
                                console.print(Panel.fit(
                                    f"[green]Comment :[/] [white]{id} [/] [red]Thất bại.[/]",
                                    title="⛔ THẤT BẠI", border_style="red"
                                ))
                                loi_cmt += 1
                                delay(dl)
