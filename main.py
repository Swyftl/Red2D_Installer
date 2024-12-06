from github import Github
import requests
from customtkinter import *
import threading

def startDownload(item: int):
    downloadThread = threading.Thread(target=lambda : DownloadItem(item))
    downloadThread.start()

def DownloadItem(item: int):
    print("starting install")
    for asset in releases[item].get_assets():
        print("Installing item")
        response = requests.get(asset.browser_download_url, allow_redirects=True)
        enginezip = open(f"{releases[item].tag_name}.zip", "wb")
        enginezip.write(response.content)
        enginezip.close()
    print("install Finished")

releases = []
releases_tags = []

print("Getting repository Releases")
repo = Github().get_repo("Swyftl/Red2D")
for release in repo.get_releases():
    releases.append(release)
    releases_tags.append(release.tag_name)
    print(release.tag_name)

print("Loaded Correctly")

root = CTk()
root.geometry("1280x720")

root.title("Red2D Installer")

clicked = StringVar()
clicked.set(releases_tags[0])

dropdown = CTkOptionMenu(root, values=releases_tags, variable=clicked)

install = CTkButton(root, text="Install Selected Version", command= lambda: startDownload(releases_tags.index(clicked.get())))

dropdown.pack()
install.pack()

root.mainloop()