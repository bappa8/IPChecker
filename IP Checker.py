import requests
import tkinter as tk
import threading

# ---------------------------
# FUNCTIONS
# ---------------------------

def fetch_ip_info():
    """Fetch IP info quickly in a thread-safe way."""
    try:
        # Basic IPv4 info
        try:
            url = "http://ip-api.com/json/?fields=status,query,country,city,isp,proxy"
            res = requests.get(url, timeout=2)  # short timeout
            data = res.json()
        except:
            info_var.set("❌ Error fetching data")
            return

        if data.get("status") != "success":
            info_var.set("❌ Error fetching data")
            return

        vpn = "Yes" if data.get("proxy") else "No"

        # IPv6 fetch with short timeout
        try:
            ipv6_response = requests.get("https://api64.ipify.org?format=json", timeout=2)
            ipv6 = ipv6_response.json().get("ip", "N/A") if ipv6_response.status_code == 200 else "N/A"
        except:
            ipv6 = "N/A"

        # TOR detection with short timeout
        try:
            tor_data = requests.get(f"https://check.torproject.org/api/ip?ip={data['query']}", timeout=2).json()
            tor_status = "Yes" if tor_data.get("IsTor") else "No"
        except:
            tor_status = "Unknown"

        # Align keys
        keys = ["IPv4", "IPv6", "Country", "City", "ISP", "VPN/Proxy", "TOR"]
        values = [data["query"], ipv6, data["country"], data["city"], data["isp"], vpn, tor_status]
        max_key_len = max(len(k) for k in keys)

        lines = [f"{k.ljust(max_key_len)} : {v}" for k, v in zip(keys, values)]
        text = "\n".join(lines)

        info_var.set(text)

    except:
        info_var.set("❌ Connection error")


def get_ip_info():
    """Run fetch_ip_info in a separate thread to prevent GUI hang."""
    info_var.set("Loading...")
    threading.Thread(target=fetch_ip_info, daemon=True).start()


def refresh():
    """Manual refresh button."""
    get_ip_info()


def copy_all():
    text = info_var.get()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)

# ---------------------------
# UI (Dark Mode)
# ---------------------------

root = tk.Tk()
root.title("IP Checker")
root.geometry("400x330")
root.resizable(False, False)

bg = "#1e1e1e"
fg = "#ffffff"
accent = "#4CAF50"
btn = "#2d2d2d"

root.configure(bg=bg)

info_var = tk.StringVar()
info_var.set("Click Refresh")

title = tk.Label(root, text="IP Checker",
                 font=("Segoe UI", 14, "bold"),
                 bg=bg, fg="#8A0303")
title.pack(pady=10)

info_label = tk.Label(root, textvariable=info_var,
                      font=("Consolas", 12),
                      bg=bg, fg=accent,
                      justify="left")
info_label.pack(pady=10)

frame = tk.Frame(root, bg=bg)
frame.pack(pady=10)

refresh_btn = tk.Button(frame, text="Refresh",
                        command=refresh,
                        bg=btn, fg=fg,
                        activebackground=accent,
                        width=12)
refresh_btn.grid(row=0, column=0, padx=5)

copy_btn = tk.Button(frame, text="Copy All",
                     command=copy_all,
                     bg=btn, fg=fg,
                     activebackground=accent,
                     width=12)
copy_btn.grid(row=0, column=1, padx=5)

footer = tk.Label(root, text="© Bappa Ghosh. All rights reserved.",
                  font=("Segoe UI", 10),
                  bg=bg, fg="#00BFFF")  # better blue color
footer.pack(side="bottom", pady=5)

# ---------------------------
# START WITH INITIAL FETCH
# ---------------------------

get_ip_info()

root.mainloop()
