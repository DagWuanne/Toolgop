import os
import requests
import json
from time import sleep
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.columns import Columns
from lunarcalendar import Converter, Solar

os.environ['TZ'] = 'Asia/Ho_Chi_Minh'

console = Console()

headers = {
    'authority': 'traodoisub.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'user-agent': 'traodoisub tiktok tool',
}

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

def login_tds(token):
    try:
        r = requests.get('https://traodoisub.com/api/?fields=profile&access_token='+token, headers=headers, timeout=5).json()
        if 'success' in r:
            console.print(Panel.fit(
                f"[green]Đăng nhập thành công!\n[white]User: [yellow]{r['data']['user']}[/yellow] | Xu hiện tại: [yellow]{r['data']['xu']}[/yellow]",
                title="[bold green]ĐĂNG NHẬP", border_style="green"
            ))
            return 'success'
        else:
            console.print(Panel.fit(
                f"[red]Token TDS không hợp lệ, hãy kiểm tra lại![/red]",
                title="[bold red]LỖI", border_style="red"
            ))
            return 'error_token'
    except:
        console.print(Panel.fit(
            f"[red]Lỗi kết nối server![/red]",
            title="[bold red]LỖI", border_style="red"
        ))
        return 'error'

def load_job(type_job, token):
    try:
        r = requests.get('https://traodoisub.com/api/?fields='+type_job+'&access_token='+token, headers=headers, timeout=5).json()
        if 'data' in r:
            return r
        elif "countdown" in r:
            console.print(Panel.fit(
                f"[red]{r['error']}[/red]\nChờ {r['countdown']} giây...",
                title="[bold red]THÔNG BÁO", border_style="red"
            ))
            sleep(round(r['countdown']))
            return 'error_countdown'
        else:
            console.print(Panel.fit(
                f"[red]{r['error']}[/red]",
                title="[bold red]LỖI", border_style="red"
            ))
            return 'error_error'
    except:
        console.print(Panel.fit(
            f"[red]Lỗi kết nối server![/red]",
            title="[bold red]LỖI", border_style="red"
        ))
        return 'error'

def duyet_job(type_job, token, uid):
    try:
        r = requests.get(f'https://traodoisub.com/api/coin/?type={type_job}&id={uid}&access_token={token}', headers=headers, timeout=5).json()
        if "cache" in r:
            return r['cache']
        elif "success" in r:
            console.print(Panel.fit(
                f"[cyan]Nhận thành công {r['data']['job_success']} nhiệm vụ[/cyan]\n[green]{r['data']['msg']}[/green]\n[yellow]Xu: {r['data']['xu']}[/yellow]",
                title="[bold green]THÀNH CÔNG", border_style="green"
            ))
            return 'error'
        else:
            console.print(Panel.fit(
                f"[red]{r['error']}[/red]",
                title="[bold red]LỖI", border_style="red"
            ))
            return 'error'
    except:
        console.print(Panel.fit(
            f"[red]Lỗi kết nối server![/red]",
            title="[bold red]LỖI", border_style="red"
        ))
        return 'error'

def check_tiktok(id_tiktok, token):
    try:
        r = requests.get('https://traodoisub.com/api/?fields=tiktok_run&id='+id_tiktok+'&access_token='+token, headers=headers, timeout=5).json()
        if 'success' in r:
            console.print(Panel.fit(
                f"[green]{r['data']['msg']}[/green]\n[white]ID: [yellow]{r['data']['id']}[/yellow]",
                title="[bold green]KIỂM TRA ID TIKTOK", border_style="green"
            ))
            return 'success'
        else:
            console.print(Panel.fit(
                f"[red]{r['error']}[/red]",
                title="[bold red]LỖI", border_style="red"
            ))
            return 'error_token'
    except:
        console.print(Panel.fit(
            f"[red]Lỗi kết nối server![/red]",
            title="[bold red]LỖI", border_style="red"
        ))
        return 'error'

def main():
    os.system('clear')
    banner()

    while True:
        try:
            with open('TDS.txt', 'r') as f:
                token_tds = f.read().strip()
            cache = 'old'
        except FileNotFoundError:
            token_tds = Prompt.ask("[bold cyan]Nhập token TDS[/bold cyan]")
            cache = 'new'

        for _ in range(3):
            check_log = login_tds(token_tds)
            if check_log in ['success', 'error_token']:
                break
            else:
                sleep(2)

        if check_log == 'success':
            if cache == 'old':
                console.print(Panel.fit(
                    """[bold green]1.[/] Tiếp tục sử dụng acc TDS đã lưu
[bold green]2.[/] Sử dụng acc TDS mới""",
                    title="[bold cyan]LỰA CHỌN ACC TDS", border_style="bright_magenta"
                ))
                while True:
                    try:
                        choice = IntPrompt.ask("[bold yellow]Lựa chọn của bạn (1 hoặc 2)[/bold yellow]")
                        if choice in [1, 2]:
                            break
                        else:
                            os.system('clear')
                            console.print(Panel.fit(
                                f"[red]Lỗi lựa chọn! Chỉ nhập 1 hoặc 2[/red]",
                                title="[bold red]LỖI", border_style="red"
                            ))
                    except:
                        os.system('clear')
                        console.print(Panel.fit(
                            f"[red]Lỗi lựa chọn! Chỉ nhập 1 hoặc 2[/red]",
                            title="[bold red]LỖI", border_style="red"
                        ))

                os.system('clear')
                if choice == 1:
                    break
                else:
                    os.remove('TDS.txt')
            else:
                with open('TDS.txt', 'w') as f:
                    f.write(token_tds)
                break
        else:
            sleep(1)
            os.system('clear')

    if check_log == 'success':
        # Nhập user TikTok
        while True:
            id_tiktok = Prompt.ask("[bold cyan]Nhập ID TikTok chạy (lấy ở mục cấu hình web)[/bold cyan]")
            for _ in range(3):
                check_log = check_tiktok(id_tiktok, token_tds)
                if check_log in ['success', 'error_token']:
                    break
                else:
                    sleep(2)

            if check_log == 'success':
                break
            elif check_log == 'error_token':
                os.system('clear')
                console.print(Panel.fit(
                    f"[red]ID TikTok chưa được thêm vào cấu hình, vui lòng thêm vào cấu hình rồi nhập lại![/red]",
                    title="[bold red]LỖI", border_style="red"
                ))
            else:
                os.system('clear')
                console.print(Panel.fit(
                    f"[red]Lỗi server, vui lòng nhập lại![/red]",
                    title="[bold red]LỖI", border_style="red"
                ))

        # Lựa chọn nhiệm vụ
        console.print(Panel.fit(
            """[bold green]1.[/] Follow
[bold green]2.[/] Tym""",
            title="[bold cyan]DANH SÁCH NHIỆM VỤ", border_style="bright_magenta"
        ))
        while True:
            try:
                choice = IntPrompt.ask("[bold yellow]Lựa chọn nhiệm vụ muốn làm (1 hoặc 2)[/bold yellow]")
                if choice in [1, 2]:
                    break
                else:
                    os.system('clear')
                    console.print(Panel.fit(
                        f"[red]Lỗi lựa chọn! Chỉ nhập 1 hoặc 2[/red]",
                        title="[bold red]LỖI", border_style="red"
                    ))
            except:
                os.system('clear')
                console.print(Panel.fit(
                    f"[red]Lỗi lựa chọn! Chỉ nhập 1 hoặc 2[/red]",
                    title="[bold red]LỖI", border_style="red"
                ))

        # Nhập delay nhiệm vụ
        while True:
            try:
                delay = IntPrompt.ask("[bold yellow]Thời gian delay giữa các job (giây)[/bold yellow]")
                if delay > 2:
                    break
                else:
                    os.system('clear')
                    console.print(Panel.fit(
                        f"[red]Delay tối thiểu là 3[/red]",
                        title="[bold red]LỖI", border_style="red"
                    ))
            except:
                os.system('clear')
                console.print(Panel.fit(
                    f"[red]Vui lòng nhập một số > 2[/red]",
                    title="[bold red]LỖI", border_style="red"
                ))

        # Nhập max nhiệm vụ
        while True:
            try:
                max_job = IntPrompt.ask("[bold yellow]Dừng lại khi làm được số nhiệm vụ[/bold yellow]")
                if max_job > 9:
                    break
                else:
                    os.system('clear')
                    console.print(Panel.fit(
                        f"[red]Tối thiểu là 10[/red]",
                        title="[bold red]LỖI", border_style="red"
                    ))
            except:
                os.system('clear')
                console.print(Panel.fit(
                    f"[red]Vui lòng nhập một số > 9[/red]",
                    title="[bold red]LỖI", border_style="red"
                ))

        os.system('clear')

        if choice == 1:
            type_load = 'tiktok_follow'
            type_duyet = 'TIKTOK_FOLLOW_CACHE'
            type_nhan = 'TIKTOK_FOLLOW'
            type_type = 'FOLLOW'
            api_type = 'TIKTOK_FOLLOW_API'
        elif choice == 2:
            type_load = 'tiktok_like'
            type_duyet = 'TIKTOK_LIKE_CACHE'
            type_nhan = 'TIKTOK_LIKE'
            api_type = 'TIKTOK_LIKE_API'
            type_type = 'TYM'

        dem_tong = 0

        while True:
            list_job = load_job(type_load, token_tds)
            sleep(2)
            if isinstance(list_job, dict):
                for job in list_job['data']:
                    uid = job['id']
                    link = job['link']
                    os.system(f'termux-open-url {link}')
                    check_duyet = duyet_job(type_duyet, token_tds, uid)

                    if check_duyet != 'error':
                        dem_tong += 1
                        t_now = datetime.now().strftime("%H:%M:%S")
                        console.print(Panel.fit(
                            f"[yellow][{dem_tong}][/yellow] | [cyan]{t_now}[/cyan] | [pink]{type_type}[/pink] | [light_gray]{uid}[/light_gray]",
                            title="[bold green]NHIỆM VỤ", border_style="green"
                        ))

                        if check_duyet > 9:
                            sleep(3)
                            duyet_job(type_nhan, token_tds, api_type)

                    if dem_tong == max_job:
                        break
                    else:
                        for i in range(delay, -1, -1):
                            console.print(f"[green]Vui lòng đợi: {i} giây[/green]", end='\r')
                            sleep(1)

            if dem_tong == max_job:
                console.print(Panel.fit(
                    f"[green]Hoàn thành {max_job} nhiệm vụ![/green]",
                    title="[bold green]HOÀN THÀNH", border_style="green"
                ))
                break

if __name__ == "__main__":
    main()
