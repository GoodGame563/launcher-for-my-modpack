import tkinter
import os
import customtkinter

from tkinter.messagebox import showerror

import subprocess
import json

from pydantic import ValidationError
from git_work import element_git
from models import Settings
from random_username.generate import generate_username
from threading import Thread
from forge_work import class_minecraft
from transfer_data import transfer
from PIL import ImageTk, Image
from result import Ok, Err, Result, is_ok, is_err

customtkinter.set_appearance_mode("Dark")  
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

current_max = 0
setting_path = "settings.json"
def create_settings() -> Result[None, str]:
    try:
        with open(setting_path, 'w', encoding='utf-8') as file: 
            file.write(Settings(version='middle',nick=generate_username(1)[0], enable_resource=True, enable_custom_settings=False, download_mine=False).json())
        return Ok(None)    
    except Exception as e:
        return Err(f"Ошибка создания файла настроек: {e}")

def check_settings() -> Result[Settings, str]:
    if not os.path.exists(setting_path):
        if create_settings().is_err():
            assert()
    with open(setting_path, 'r', encoding='utf-8') as file:
        try: 
            return Ok(Settings(**json.load(file))) 
        except ValidationError as e:
            if create_settings().is_err():
                assert()
        except Exception as e:
            return Err(f"Ошибка чтения файла: {e}")
    with open(setting_path, 'r', encoding='utf-8') as file:
        return Ok(Settings(**json.load(file))) 


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.repo_url = "https://github.com/GoodGame563/RPG-modpack.git" 
        self.repo_path = "repo"
        self.maincraft_path = "RPG_modpack"
        if not os.path.exists(self.maincraft_path):
            os.makedirs(self.maincraft_path)

        data = check_settings()
        if data.is_err():
            showerror("Попробуйте запустить от имени администратора")
            self.destroy()
        self.settings = data.ok_value
        self.versions = ["potato", "potato-ru", "middle-ru", "middle", "beautiful-ru", "beatiful"]

        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Minecraft", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox = customtkinter.CTkComboBox(self.sidebar_frame, values=self.versions, command=self.combobox_callback)
        self.combobox.grid(row=3, column=0, padx=20, pady=10)
        self.combobox.set(self.settings.version)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text='Настройки')
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.entry = customtkinter.CTkEntry(self)
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entry.insert(0, self.settings.nick)

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Play', command=self.main_button_event)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.image_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.image_frame.grid(row=0, column=1,columnspan = 3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.bg_image = ImageTk.PhotoImage(Image.open("1.png"))
        self.bg_image_label = customtkinter.CTkLabel(self.image_frame, image=self.bg_image, text="")
        self.bg_image_label.pack(fill="both", expand=True)

        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=4, column=1,columnspan = 4, padx=(20, 0), pady=(0, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(3, weight=1)
        self.progressbar = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar.grid(row=1, column=0, padx=(0, 20), pady=(0, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=2, column=0, padx=(0, 20), pady=(0, 10), sticky="ew")
        self.slider_progressbar_frame.grid_remove()


    def combobox_callback(self, choice):
        self.settings.version = choice
        with open("settings.json", 'w', encoding='utf-8') as file:
            file.write(self.settings.json())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def main_button_event(self):
        self.main_button_1.configure(text="Запуск", state="disabled")
        self.settings.nick = self.entry.get()
        with open("settings.json", 'w', encoding='utf-8') as file:
            file.write(self.settings.json())
        Thread(target=self.start_all).start()
        
    def start_all(self):
        self.slider_progressbar_frame.grid(row=4, column=1,columnspan = 4, padx=(20, 0), pady=(0, 0), sticky="nsew")
        e_g = element_git(self.repo_url, self.repo_path, self.settings.version, self.progressbar)
        c_mine = class_minecraft(self.settings, self.maincraft_path, self.progressbar_1)
        t_download_from_git = Thread(target=e_g.start)
        t_download_minecraft = Thread(target=c_mine.download_minecraft)
        if not self.settings.download_mine:
            t_download_minecraft.start()
        t_download_from_git.start()
        t_download_from_git.join()
        t_transfer = Thread(target=transfer, args=(self.repo_path, self.maincraft_path, self.settings))
        t_transfer.start()
        t_transfer.join()
        if not self.settings.download_mine:
            t_download_minecraft.join()
        self.slider_progressbar_frame.grid_remove()
        c_mine.launch_minecraft()
        self.main_button_1.configure(text="Play", state="normal")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
