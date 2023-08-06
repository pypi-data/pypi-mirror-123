import sys
import os
from pathlib import Path

BASEDIR = os.getcwd()
BASEDIR= Path(BASEDIR)
env_path = Path(f"{BASEDIR}/.YAFPA-env")
print(env_path)

def create_env():
    env = open(env_path, "w", encoding="utf-8")
    vault = str(input("Please provide your obsidian vault path : "))
    blog = str(input("Please provide the blog repository path : "))
    blog_link = str(
        input("Please provide the blog link (as https://yourblog.netlify.app) : ")
    )
    env.write(f"vault={vault}\n")
    env.write(f"blog_path={blog}\n")
    env.write(f"blog={blog_link}\n")
    env.close()
