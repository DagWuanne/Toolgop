from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from datetime import datetime
from lunarcalendar import Converter, Solar

console = Console()

# Thông báo cập nhật tool
console.print(
    Panel.fit(
        "[bold red]🚧 Tool này đang được cập nhật. Vui lòng quay lại sau! 🚧",
        title="[bold yellow]Thông Báo",
        border_style="red"
    )
)

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
