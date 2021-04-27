# -*- coding: utf-8 -*-
from lcu_driver import Connector
import tkinter as tk
from tkinter import messagebox
import threading

__author__: str = "UNC3RTAIN"
__version__: str = "1.0.3"

window = tk.Tk()
client = Connector()
name = ""
buttonClick = False
destroyAll = False 

window.title("ARAM Boost")
window.geometry("300x150")
window.minsize(300, 150)
window.maxsize(400, 200)
window.eval('tk::PlaceWindow . center')
window.configure(bg="#000200")

async def get_name(cmd) -> bool:
    summoner = await cmd.request("GET", "/lol-summoner/v1/current-summoner")
    
    if summoner.status == 200: 
        data: dict = await summoner.json()
        global name
        name = data['displayName']
        status.configure(text=f"Status: Connecting [{name}]", fg="#15CCAD")
        return True

    else: return False

async def boostBAS(cmd) -> None:
    req = await cmd.request("POST", "/lol-champ-select/v1/team-boost/purchase")

    if req.status == 204:
        status.configure(text="Status: Activate Boost", fg="#06F422")
        
    elif req.status == 500:
        status.configure(text="Status: Client hotfix is ​​not applied", fg="#ff1919")
        
    else:
        status.configure(text="Status: You are not in champion pick", fg="#ff1919")

    window.after(2500, lambda:status.configure(text=f"Status: Connecting [{name}]", fg="#ffff19"))

def click() -> None:
    global buttonClick
    buttonClick = True

def closeWindow() -> None:
    global destroyAll
    destroyAll = True
    window.destroy()

@client.ready
async def connectLOL(cmd) -> None:

    global buttonClick
    check = await get_name(cmd)

    if check is False:
        messagebox.showerror(title="Dick Error", message="Game not found, launch the game and try again")
        window.destroy()
        await client.stop()

    while check:
        if buttonClick:
            await boostBAS(cmd)
            buttonClick = False
        if destroyAll is True:
            break

header = tk.Label(window, text="UNC3RTAIN", font=("Arial", 19), bg="#000200", fg="#15CCAD")
header.pack(pady=5, padx=5)

button = tk.Button(window, text="Boost", font=("Arial", 12), bg="#F8FBFB", fg="#000200", bd=5, activebackground="#197019", activeforeground="#000000", width=10, height=2, command=click)
button.pack(pady=5, padx=5)

status = tk.Label(window, text="Status: waiting LOL...", font=("Arial", 10), bg="#000200", fg="#15CCAD")
status.pack(pady=5, padx=5)

prcs = threading.Thread(target=client.start)
prcs.start()

window.protocol("WM_DELETE_WINDOW", closeWindow)

window.mainloop()


