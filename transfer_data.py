import os
import shutil

from models import Settings
from result import Ok, Err, Result, is_ok, is_err


def transfer(repo_url:str, minecraft_url:str, settings:Settings) -> Result[None, Exception]:
    if delete_directory(f"{minecraft_url}\\mods").is_err():
        return Err("Ошибка при удалении папки mods")
    if delete_directory(f"{minecraft_url}\\shaderpacks").is_err():
        return Err("Ошибка при удалении папки shaderpacks")
    if settings.enable_resource:
        if delete_directory(f"{minecraft_url}\\resourcepacks").is_err():
            return Err("Ошибка при удалении папки resourcepacks")
    if not settings.enable_custom_settings:
        if delete_directory(f"{minecraft_url}\\config").is_err():
            return Err("Ошибка при удалении папки config")
        try:
            os.remove(f"{minecraft_url}\\options.txt")
        except FileNotFoundError:
            print("Ошибка при удалении файла options.txt")
    return copy_folder(f"{repo_url}\\.minecraft", minecraft_url)

def delete_directory(url) -> Result[None, str]:
    try:
        if os.path.exists(url):
            shutil.rmtree(url)
        return Ok(None)
    except Exception as e:
        return Err(e)

def copy_folder(src_folder, dest_folder) -> Result[None, Exception]:
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)
        
        try:
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
                print(f"Скопирована папка: {src_path} -> {dest_path}")
            else:
                shutil.copy2(src_path, dest_path)
                print(f"Скопирован файл: {src_path} -> {dest_path}")
        except FileExistsError:
            print(f"Папка назначения уже существует: {dest_path}")
        except Exception as e:
            return Err(e)
    return Ok(None)
