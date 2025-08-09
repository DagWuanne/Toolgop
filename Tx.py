import os
import json
import random
import time
import uuid
import psutil
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.columns import Columns
from lunarcalendar import Converter, Solar  # Thêm để hỗ trợ lịch âm

console = Console()
DATA_DIR = "users"
os.makedirs(DATA_DIR, exist_ok=True)
DEVICE_DB = "devices.json"

# ────────── HÀM TIỆN ÍCH ──────────
def load_json(path):
    if os.path.exists(path):
        return json.load(open(path))
    return {}

def save_json(path, data):
    json.dump(data, open(path, "w"), indent=2)

def get_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except:
        return "0.0.0.0"

def get_mac():
    return uuid.getnode()

def device_registered():
    devices = load_json(DEVICE_DB)
    ip = get_ip()
    mac = str(get_mac())
    return devices.get(ip) or devices.get(mac)

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

    # Lấy thời gian hiện tại (06:02 PM +07, 09/08/2025)
    now = datetime.now()
    time_str = now.strftime("%I:%M %p %z")  # Định dạng 06:02 PM +0700
    date_str = now.strftime("%d/%m/%Y")  # 09/08/2025

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

# ────────── CHỨC NĂNG CHÍNH ──────────
def register():
    ip = get_ip()
    mac = str(get_mac())
    if device_registered():
        console.print(Panel(
            "[red]⚠️ Thiết bị này đã dùng để tạo tài khoản rồi![/red]",
            title="⛔ LỖI", border_style="red"
        ))
        return None
    username = Prompt.ask("🔐 [cyan]Nhập tên tài khoản muốn tạo[/]").strip()
    user_file = os.path.join(DATA_DIR, username + ".json")
    if os.path.exists(user_file):
        console.print(Panel(
            "[red]Tên tài khoản đã tồn tại![/red]",
            title="⛔ LỖI", border_style="red"
        ))
        return None
    data = {
        "username": username, "balance": 10000,
        "last_checkin": "", "history": [],
        "total": 0, "win": 0, "lose": 0
    }
    save_json(user_file, data)
    dev = load_json(DEVICE_DB)
    dev[ip] = username
    dev[mac] = username
    save_json(DEVICE_DB, dev)
    console.print(Panel(
        f"[green]✅ Đăng ký thành công! Tài khoản: {username}, được tặng 10k khởi đầu[/green]",
        title="🎉 THÀNH CÔNG", border_style="green"
    ))
    return username

def login():
    username = Prompt.ask("🔐 [green]Nhập tài khoản đăng nhập[/]").strip()
    user_file = os.path.join(DATA_DIR, username + ".json")
    if os.path.exists(user_file):
        console.print(Panel(
            f"[cyan]✅ Đăng nhập thành công: {username}[/cyan]",
            title="🎉 THÀNH CÔNG", border_style="cyan"
        ))
        return username
    console.print(Panel(
        "[red]❌ Tài khoản không tồn tại![/red]",
        title="⛔ LỖI", border_style="red"
    ))
    return None

def load_user(u):
    return load_json(os.path.join(DATA_DIR, u + ".json"))

def save_user(u, d):
    save_json(os.path.join(DATA_DIR, u + ".json"), d)

def checkin(u, d):
    today = datetime.now().strftime("%Y-%m-%d")
    if d["last_checkin"] != today:
        d["balance"] += 5000000
        d["last_checkin"] = today
        console.print(Panel(
            "[bold green]🎁 Điểm danh thành công +1 jack[/bold green]",
            title="✅ HOÀN THÀNH", border_style="green"
        ))
        save_user(u, d)
    else:
        console.print(Panel(
            "[yellow]⚠️ Hôm nay đã điểm danh rồi[/yellow]",
            title="ℹ️ THÔNG BÁO", border_style="yellow"
        ))

def show_stats(u, d):
    win = d["win"]
    lose = d["lose"]
    t = d["total"]
    rate = (win / t * 100) if t > 0 else 0
    console.print(Panel(
        f"🧾 [cyan]TK {u}[/]: SD={d['balance']} | Ván={t} | Win/Loss={[win, lose]} | Win%={rate:.2f}%",
        title="📊 THÔNG TIN", border_style="cyan"
    ))

def leaderboard():
    table = Table(title="🏆 BXH Người Chơi", title_style="bold yellow", box=box.ROUNDED, border_style="bright_magenta")
    table.add_column("Top", justify="center", style="bold white")
    table.add_column("User", style="bold green")
    table.add_column("Balance", style="bold cyan")
    items = []
    for fn in os.listdir(DATA_DIR):
        d = load_json(os.path.join(DATA_DIR, fn))
        items.append((d["username"], d["balance"]))
    items.sort(key=lambda x: x[1], reverse=True)
    for i, (u, b) in enumerate(items[:10], 1):
        table.add_row(str(i), u, str(b))
    console.print(table)

def shake():
    with Progress(SpinnerColumn(), TextColumn("{task.description}")) as p:
        task = p.add_task("🌀 Đang lắc...", total=None)
        time.sleep(random.uniform(1.5, 2.5))

def update_res(u, d, win):
    d["total"] += 1
    if win:
        d["win"] += 1
    else:
        d["lose"] += 1

# ────────── CÁC CHẾ ĐỘ CHƠI ──────────
def mode_taixiu(u, d):
    bet = int(Prompt.ask("💵 Cược (max 5k)", default="50000"))
    if bet > d["balance"]:
        console.print(Panel(
            "[red]Không đủ tiền[/red]",
            title="⛔ LỖI", border_style="red"
        ))
        return
    pick = Prompt.ask("Tài hay Xỉu", choices=["t", "x"])
    shake()
    dice = [random.randint(1, 6) for _ in range(3)]
    tot = sum(dice)
    res = "t" if tot >= 11 else "x"
    console.print(Panel(
        f"🎲 {dice} → Total={tot} → {'Tài' if res == 't' else 'Xỉu'}",
        title="🎲 KẾT QUẢ", border_style="yellow"
    ))
    if pick == res:
        d["balance"] += bet
        console.print(Panel(
            f"[green]✅ Win +{bet}[/green]",
            title="🎉 THÀNH CÔNG", border_style="green"
        ))
        update_res(u, d, True)
    else:
        d["balance"] -= bet
        console.print(Panel(
            f"[red]❌ Lose -{bet}[/red]",
            title="⛔ THẤT BẠI", border_style="red"
        ))
        update_res(u, d, False)
    save_user(u, d)

def mode_3cang(u, d):
    bet = int(Prompt.ask("💵 Cược (max 5k)", default="50000"))
    if bet > d["balance"]:
        console.print(Panel(
            "[red]Không đủ tiền[/red]",
            title="⛔ LỖI", border_style="red"
        ))
        return
    num = Prompt.ask("Nhập 3 số (vd:123)")
    shake()
    res = "".join(str(random.randint(0, 9)) for _ in range(3))
    console.print(Panel(
        f"🔢 Kết quả: {res}",
        title="🎲 KẾT QUẢ", border_style="yellow"
    ))
    if num == res:
        win = bet * 500
        d["balance"] += win
        console.print(Panel(
            f"[green]🎉 Trúng +{win}[/green]",
            title="🎉 THÀNH CÔNG", border_style="green"
        ))
        update_res(u, d, True)
    else:
        d["balance"] -= bet
        console.print(Panel(
            f"[red]❌ Thua -{bet}[/red]",
            title="⛔ THẤT BẠI", border_style="red"
        ))
        update_res(u, d, False)
    save_user(u, d)

def mode_lode(u, d):
    bet = int(Prompt.ask("💵 Cược (max 5k)", default="50000"))
    if bet > d["balance"]:
        console.print(Panel(
            "[red]Không đủ tiền[/red]",
            title="⛔ LỖI", border_style="red"
        ))
        return
    num = Prompt.ask("Nhập 2 số (vd:23)")
    shake()
    res = f"{random.randint(0, 99):02}"
    console.print(Panel(
        f"🎯 Kết quả: {res}",
        title="🎲 KẾT QUẢ", border_style="yellow"
    ))
    if num == res:
        win = bet * 70
        d["balance"] += win
        console.print(Panel(
            f"[green]🎉 Win +{win}[/green]",
            title="🎉 THÀNH CÔNG", border_style="green"
        ))
        update_res(u, d, True)
    else:
        d["balance"] -= bet
        console.print(Panel(
            f"[red]❌ Lose -{bet}[/red]",
            title="⛔ THẤT BẠI", border_style="red"
        ))
        update_res(u, d, False)
    save_user(u, d)

def main():
    console.clear()
    banner()
    console.print(Panel(
        "[bold blue]🎲 GAME XÍ NGẦU VIP[/bold blue]",
        title="🎮 CHÀO MỪNG", border_style="blue"
    ))
    while True:
        acc = Prompt.ask("1. Đăng nhập\n2. Đăng ký\n0. Out\n", choices=["1", "2", "0"])
        if acc == "1":
            user = login()
            if user:
                break
        elif acc == "2":
            user = register()
            if user:
                break
        elif acc == "0":
            return

    d = load_user(user)
    while True:
        console.clear()
        banner()
        console.print(Panel(
            f"User: [bold]{user}[/] | SD: [green]{d['balance']}đ[/]",
            title="📋 THÔNG TIN TÀI KHOẢN", border_style="cyan"
        ))
        cmd = Prompt.ask("Chọn \n1:Tài Xỉu\n2:3 Càng\n3:Lô đề\n4:Điểm danh nhận tiền ng mới\n5:Thông tin\n6:Bảng xếp hạng ng chơi\n0:Exit\n",
                         choices=["1", "2", "3", "4", "5", "6", "0"])
        if cmd == "1":
            mode_taixiu(user, d)
        elif cmd == "2":
            mode_3cang(user, d)
        elif cmd == "3":
            mode_lode(user, d)
        elif cmd == "4":
            checkin(user, d)
        elif cmd == "5":
            show_stats(user, d)
        elif cmd == "6":
            leaderboard()
        elif cmd == "0":
            break
        Prompt.ask("Nhấn Enter để về menu")
        console.clear()

if __name__ == "__main__":
    main()
