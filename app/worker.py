import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from itertools import islice
import glob, shutil
import pathlib
import os
from moviepy.editor import *

folder_path = str(pathlib.Path(__file__).parent.resolve())
scroller = False

def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def handle_delete_all():
    clear_folder(folder_path + '\\videos')
    clear_folder(folder_path + '\\music')
    clear_folder(folder_path + '\\results')


def get_video(filter='cat', amount=5):
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--lang=en")
    prefs = {"download.default_directory": folder_path + '\\videos'}
    options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    browser.maximize_window()
    time.sleep(1)
    browser.get("https://www.pexels.com/uk-ua/search/videos/" + filter)
    time.sleep(1)

    if scroller:
        for _ in range(10):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight-200);")
            time.sleep(2)
    
    links = browser.find_elements(By.CLASS_NAME, 'BreakpointGrid_item__erUQQ')
    random.shuffle(links)
    for link in islice(links, amount):
        article = link.find_element(By.TAG_NAME, "article")
        a = article.find_element(By.TAG_NAME, "a")
        browser.get(a.get_attribute('href') + 'download')
        time.sleep(3)
        os.chdir(folder_path + '\\videos')
        j=0
        while glob.glob("*.crdownload") and j < 60:
            j+=1
            time.sleep(1)

    browser.close()


def get_song(filter='cat', amount=5):
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    prefs = {"download.default_directory": folder_path + '\\music'}
    options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    browser.maximize_window()
    time.sleep(1)
    browser.get("https://pixabay.com/music/search/" + filter)
    time.sleep(1)

    if scroller:
        for _ in range(10):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

    audio = browser.find_elements(By.CLASS_NAME, 'audio-download')
    random.shuffle(audio)
    links = []

    amount = max(len(os.listdir(folder_path + '\\videos')) *2,amount)
    for link in islice(audio, amount):
        links.append(link.get_attribute('href'))
        os.chdir(folder_path + '\\music')
        browser.get(link.get_attribute('href'))
        
        j = 0
        while glob.glob("*.crdownload") and j < 60:
            j += 1
            time.sleep(1)
    browser.close()


def add_music_to_video():
    i = 1
    os.chdir(folder_path + '\\videos')
    videos = glob.glob("*.mp4")
    os.chdir(folder_path + '\\music')
    musics = glob.glob("*.mp3")

    for link in videos:
        file_name = link.split("?")[0]

        song = random.choice(musics)
        videoclip  = VideoFileClip(folder_path + '\\videos\\' + file_name)
        duration = min(videoclip.duration,30)
        videoclip = videoclip.subclip(0,duration)
        audioclip = AudioFileClip(folder_path + f"\\music\\{song}").subclip(0, duration)
        
        videoclip = videoclip.set_audio(audioclip)

        videoclip.write_videofile(folder_path + f"\\results\\vid_{i}.mp4")

        videoclip.close()
        audioclip.close()
        i += 1
