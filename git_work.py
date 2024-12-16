import git
import os
import shutil
import customtkinter as ctk

from result import Ok, Err, Result, is_ok, is_err
 
class element_git():
    def __init__(self, repo_url:str, save_path:str, graphics_quality: str, progressbar: ctk.CTkProgressBar = None):
        self.repo_url = repo_url
        self.save_path = save_path
        self.progressbar = progressbar
        self.gq = graphics_quality

    def progress(self, op_code, cur_count, max_count, message):
        if self.progressbar is None: 
            return
        progress = cur_count / max_count if max_count else 0
        self.progressbar.set(progress)

    def start(self) -> Result[None, str]:
        print(self.save_path)
        if os.path.exists(self.save_path) :
            if self.check_rep_exists():
                return self.pull_repo()  
        else:
            if self.clone_repo().is_err():
                print("Cloning repo failed")
                return Err("Проверьте доступ к интернету") 
            branch_version = self.check_version_branch()
            if branch_version.is_err():
                print("Не удалось получить текущую ветку репозитория.")
                return Err("Не ожиданная ошибка попробуйте удалить файл репозитории")
            if not (branch_version == self.gq):
                check_branch = self.checkout_branch()
                if check_branch.is_err:
                    return check_branch
            return self.pull_repo()
  
    def check_rep_exists(self) -> bool:
        try:
            git.Repo(self.save_path)
            return True
        except:
            return False

    def check_version_branch(self) -> Result[str, str]:
        try:
            repo = git.Repo(self.save_path)
            return Ok(repo.active_branch.name)
        except Exception as e:
            return Err(f"Ошибка при получении текущей ветки: {e}")

    def pull_repo(self) -> Result[None, str]:
        try:
            repo = git.Repo(self.save_path)
            if repo.is_dirty():
                repo.git.reset('--hard')
            origin = repo.remotes.origin
            pull_result = origin.pull(progress=self.progress)
            for fetch_info in pull_result:
                print(f"Обновлена ветка {fetch_info.ref}: {fetch_info.commit.summary}")
            return Ok(None)
        except Exception as e:
            return Err(f"Couldn't clone repository {e}") 

    def clone_repo(self) -> Result[None, str]:
        try:
            if os.path.exists(self.save_path):
                shutil.rmtree(self.save_path)
            git.Repo.clone_from(self.repo_url, self.save_path, progress=self.progress)
            return Ok(None)
        except Exception as e:
            return Err(f"Couldn't clone repository {e}")

    def checkout_branch(self) -> Result[None, str]:
        try:
            repo = git.Repo(self.save_path)
            repo.git.checkout(self.gq)
            return(Ok(None))
        except Exception as e:
            return(Err(f"Ошибка при переключении на ветку: {e}"))