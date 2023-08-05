import typer
import os

app = typer.Typer()


@app.command()
def gitsubpull():
    """
    Git pull and update git project's submodule\n
    1. it will pull the project based on branch\n
    2. update all submodule\n
    3. checkout all submodule to develop\n
    3. pull again on submodule directory\n
    """
    path = os.getcwd()
    os.system("git pull")
    os.system("git submodule update --init --recursive")
    result = os.popen(f"cat {path}/.gitmodules|grep path|sed 's/path = //g'").read().split()
    for _ in result:
        os.system(f"cd {path}" + '/' + _ + "&& git checkout develop && git pull")
