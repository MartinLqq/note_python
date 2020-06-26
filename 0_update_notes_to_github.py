"""
Notes in Gitee: private
Update notes to Github: public

在当前解释器环境下安装 GitPython:
    pip install GitPython

更新机制:
    Gitee 本地仓库的更新 ---> Github 远程仓库
	1. 把对应 Gitee 仓库的本地仓库中 需要更新的目录/文件 的路径添加到 CONFIG['includes'] 白名单中
	2. 通过遍历白名单目录/文件, 将目标文件提交到 Github 远程仓库
注意:
    0. 配置好目标仓库的用户和密码/ssh key
	1. 不要随便修改笔记中已确定的目录名和文件名, 如果必须修改, 则必须在白名单中进行更新
	2. 本脚本的位置不可变动, 名称可修改
"""
import logging
import os
import shutil

from datetime import datetime
from pathlib import Path
from typing import List

from git import Repo, GitCommandError

CONFIG = {
    # 指定更新哪些顶级目录到 github
    'includes': [

        # python 笔记
        r'G:\Important重要\Learning-Notes\notes',

        # 前端笔记
        r'G:\Important重要\Learning-Notes\前端',

        # 其他目录
        # ...

        # 当前路径下的指定文件
        r"G:\Important重要\Learning-Notes\0_必背网址.txt",
        r"G:\Important重要\Learning-Notes\github等使用技巧.md",
        r"G:\Important重要\Learning-Notes\Links.md",
        r"G:\Important重要\Learning-Notes\Markdown使用技巧.md",
        r"G:\Important重要\Learning-Notes\Tools.md",
        r"G:\Important重要\Learning-Notes\0_update_notes_to_github.py",
    ],
    # 排除 includes 指定的路径下的子目录/文件
    'excludes': [
        'node_modules',
        'myenv',
        'myvenv',
        'env-restful',
    ]
}

SRC_LOCAL = './'
SRC_REPO_NAME = 'Learning-Notes'
# SRC_REMOTE = ''
DST_LOCAL = r'G:\Important重要\note_python'
DST_REMOTE = 'https://github.com/MartinLqq/note_python.git'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(lineno)d: %(message)s',
    handlers=[
        # logging.FileHandler(filename='git.log'),
        logging.StreamHandler()
    ]
)


class Git:
    """Git inteface."""

    def __init__(self, path):
        self.path = path
        self.repo = Repo(self.path)
        self.git = self.repo.git
        # self.index = self.repo.index
        # 获取远程仓库
        self.remote = self.repo.remote()

    @property
    def _is_dirty(self):
        return self.repo.is_dirty()

    @property
    def _untracked_files(self):
        files = self.repo.untracked_files
        logging.info('untracked_files: %s', files)
        return files

    @property
    def branch(self):
        return self.repo.active_branch

    def add(self, files: List[str]):
        self.git.add(files)

    def commit(self, message: str = None):
        if message is None:
            message = 'Update notes from Gitee. {}'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        self.git.commit('-m', message)

    def push(self):
        """推送本地修改到远程仓库."""
        self.remote.push()

    def work(self):
        try:
            self.add(['.'])
            self.commit()
            self.push()
            logging.info('git push success.')
        except GitCommandError as err:
            if 'nothing to commit' in str(err):
                logging.info('nothing to commit.')
                self.push()
                return
            else:
                logging.error(err)
                raise



def can_exclude(path: str):
    excludes = CONFIG['excludes']
    exclude = False
    for exc in excludes:
    	# 如果绝对路径中包含配置的过滤字符串
        if exc in path:
            exclude = True
            break
    return exclude


def tree(top):
    for path, names, fnames in os.walk(top):
        for fname in fnames:
            if can_exclude(str(path)):
                logging.info('exclude: [%s]', path)
                continue
            yield os.path.join(os.path.abspath(path), fname)


def copy(path):
    sub = path.split(SRC_REPO_NAME)[-1]
    dst_path = DST_LOCAL + sub
    logging.info('copy [%s] to [%s]', path, dst_path)
    Path(dst_path).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src=path, dst=dst_path)


def src_local_to_dst():
    """Copy items from src local to dst local."""

    includes = CONFIG['includes']
    for top in includes:
        if not os.path.isdir(top):
            copy(top)
        else:
            for file in tree(top):
                copy(file)


if __name__ == '__main__':
    # src = Git(path=SRC_LOCAL)
    dst = Git(path=DST_LOCAL)
    src_local_to_dst()
    dst.work()

