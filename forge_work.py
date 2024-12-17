import minecraft_launcher_lib
import subprocess
import customtkinter as ctk
from models import Settings
from result import Ok, Err, Result, is_ok, is_err

class class_minecraft():
    def __init__(self, settings:Settings, minecraft_directory:str, progressbar: ctk.CTkProgressBar = None):
        self.progressbar = progressbar
        self.settings = settings
        self.minecraft_directory = minecraft_directory
        self.options =  {'username': self.settings.nick}

    def set_progress(self, progress: int):
        if self.progressbar is None: 
            return
        if current_max != 0:
            self.progressbar.set(progress / current_max) 

    def set_max(self, new_max: int):
        global current_max
        current_max = new_max

    def launch_minecraft(self) -> Result[None, str]:
        forge_version = '1.20.1-47.3.12'
        try:
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version=f'{forge_version.split("-")[0]}-forge-{forge_version.split("-")[1]}', minecraft_directory=self.minecraft_directory, options=self.options)
            subprocess.run(minecraft_command)
            return Ok(None)
        except Exception as e:
            print("Error just lunch minecraft")
            self.download_minecraft()
            return self.launch_minecraft()
      
    def download_minecraft(self) -> Result[None, str]:
        callback = {
            "setProgress": self.set_progress,
            "setMax": self.set_max
        }
        forge_version = '1.20.1-47.3.12'
        try: 
            minecraft_launcher_lib.forge.install_forge_version(forge_version, self.minecraft_directory, callback)
            self.settings.download_mine = True
            with open("settings.json", 'w', encoding='utf-8') as file:
                file.write(self.settings.model_dump_json())
            return Ok(None)
        except Exception as e:
            return Err(e)

   