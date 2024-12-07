from tkinter.filedialog import FileDialog

from github import Github
import requests
from tkinter import *
from threading import Thread
from tkinter import filedialog
import zipfile
import os

global selected_directory

def startDownload(item: int):
    downloadThread = Thread(target=lambda : DownloadItem(item))
    downloadThread.start()

def DownloadItem(item: int):
    global selected_directory
    print(selected_directory.get())

    if selected_directory != '':
        pass
    else:
        print("That is not a valid directory")

    print("starting install")
    for asset in releases[item].get_assets():
        print("Installing item")
        response = requests.get(asset.browser_download_url, allow_redirects=True)
        enginezip = open(f"{releases[item].tag_name}.zip", "wb")
        enginezip.write(response.content)
        enginezip.close()
        with zipfile.ZipFile(f'{releases[item].tag_name}.zip', 'r') as zip_ref:
            zip_ref.extractall(selected_directory.get())
            os.mkdir(selected_directory.get()+'/_internal')
            os.mkdir(selected_directory.get() + '/_internal/Assets')
            os.mkdir(selected_directory.get() + '/_internal/Assets/Images')
            os.mkdir(selected_directory.get() + '/_internal/Assets/Sounds')
            open(os.path.join(selected_directory.get(), "main.py"), "w+")
    print("install Finished")

def OpenSelector():
    global selected_directory
    folder = filedialog.askdirectory(initialdir="C:/")
    projectLocation.delete(0, END)
    projectLocation.insert(0, folder)
    selected_directory = folder

releases = []
releases_tags = []

print("Getting repository Releases")
repo = Github().get_repo("Swyftl/Red2D")
for release in repo.get_releases():
    releases.append(release)
    releases_tags.append(release.tag_name)
    print(release.tag_name)

print("Loaded Correctly")

root = Tk()
root.geometry("1280x720")

root.title("Red2D Installer")

clicked = StringVar()
clicked.set(releases_tags[0])

selected_directory = StringVar()
projectLocation = Entry(root, textvariable=selected_directory)
SelectFile = Button(root, text="Select File Location", command=OpenSelector)

dropdown = OptionMenu(root, clicked, str(releases_tags))

install = Button(root, text="Install Selected Version", command= lambda: startDownload(releases_tags.index(clicked.get())))

projectLocation.pack()
SelectFile.pack()
dropdown.pack()
install.pack()

root.mainloop()