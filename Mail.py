import requests
from bs4 import BeautifulSoup
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.columns import Columns
from datetime import datetime
from lunarcalendar import Converter, Solar  # Thêm để hỗ trợ lịch âm

console = Console()

# ────────── HÀM TIỆN ÍCH ──────────
def get_temp_email():
    url = "https://10minutemail.net/?lang=vi"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    session = requests.Session()
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        email_input = soup.find("input", {"id": "fe_text"})
        email = email_input["value"] if email_input else "Không lấy được email"
        return email, session.cookies.get_dict()
    else:
        return "Lỗi kết nối", {}

def keep_email_alive(cookies):
    url = "https://10minutemail.net/mailbox.ajax.php?_="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    session = requests.Session()
    session.cookies.update(cookies)

    console.print(Panel("[bold green]📬 Đang kiểm tra hộp thư...[/bold green]", title="MAILBOX", border_style="bright_blue"))
    
    while True:
        with Progress(SpinnerColumn(), TextColumn("[cyan]⏳ Đang tải email mới...[/cyan]"), transient=True) as progress:
            task = progress.add_task("wait", total=None)
            response = session.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            mails = soup.find_all("tr", style="font-weight: bold; cursor: pointer;")
            if mails:
                for mail in mails:
                    sender = mail.find("a", class_="row-link").text.strip()
                    content = mail.find_all("a", class_="row-link")[1].text.strip()

                    table = Table(title="📨 Thư Mới", title_style="bold yellow", box=box.ROUNDED, border_style="bright_magenta")
                    table.add_column("👤 NGƯỜI GỬI", justify="center", style="bold white")
                    table.add_column("📝 NỘI DUNG", style="bold green")
                    table.add_row(sender, content)
                    console.print(table)
            else:
                console.print(Panel(
                    "[bold yellow]📭 Không có thư mới.[/bold yellow]",
                    title="ℹ️ THÔNG BÁO", border_style="yellow"
                ))
        else:
            console.print(Panel(
                "[bold red]❌ Lỗi kết nối tới mailbox[/bold red]",
                title="⛔ LỖI", border_style="red"
            ))
        time.sleep(10)

# ────────── BANNER VÀ GIAO DIỆN ──────────
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

    # Lấy thời gian hiện tại (06:04 PM +07, Saturday, August 09, 2025)
    now = datetime.now()
    time_str = now.strftime("%I:%M %p %z")  # Định dạng 06:04 PM +0700
    date_str = now.strftime("%d/%m/%Y (%A)")  # 09/08/2025 (Saturday)
    day_of_week = now.strftime("%A")  # Saturday

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

if __name__ == "__main__":
    console.clear()
    banner()
    email, cookies = get_temp_email()
    console.print(Panel(
        f"[bold cyan]{email}[/bold cyan]",
        title="📧 EMAIL TẠM THỜI", border_style="bright_green"
    ))
    keep_email_alive(cookies)
