# A python tool for downloading images by hashtag from Instagram

## Prerequisite
1. Chrome Driver
    1. please check your [chrome version](https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have) and download its corresponding driver shown below.(查詢chrome的版本，下載對應的驅動)
2. 
    1. [version==84](https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/)
    2. [version==83](https://chromedriver.storage.googleapis.com/index.html?path=83.0.4103.39/)
    3. [version==82](https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.138/)

3. git clone or downlaod the this repository (clone 或 下載 這個repository)
    1. git clone https://github.com/chou141253/IG_downloader.git 

3. Enter the repository (在本機進入該資料夾，並將下載的chrome驅動放到指定資料夾)
    1. extract the file downloaded at the step 2. and place "chromedriver.exe" or "chromedriver" in ./web_driver/chromedriver_linux64

4. install packages used in the program (bs4, selenium)
    1. python -m pip install -r requirements.txt (windows)
    2. pip install -r requirements.txt (linux)

## Run

The following shows how to run the program and download images from Instagram (espescially for all menbers in NTNU AIOTLab, and Thank for all your help!!!)
```
python main.py --begin 1000 --end 2000 --account ntnuaiotlab2020.x@gmail.com --passwd xxxxxxxx

--begin: start index of hashtag for downloading (AIOTLab的同學，我們會提供)
--end: end index of hashtag for downloading (AIOTLab的同學，我們會提供)
--account: your ig account (we apply for some accounts for all members in aiotlab) (AIOTLab的同學，我們會提供)
--passwd: you ig password (we would send password to all members in aiotlab) (AIOTLab的同學，我們會提供)

```
## Under Construction
Multiprocess still causes some problems, so don't run this:
```
python multiprocess_main.py # may be block by instagram
```

<!-- | 參數  | 用途 |
|-----|-----|
| hashtag  | 要下載哪個hashtag  |
| target_download_numbers| 要下載多少張 |
| ig_account | IG帳號|
| ig_password | IG密碼 |
|root_savepath|想存在哪(default:'./instagram_datas/')|
|browser_type|目前只測試在chorme|
|has_monitor|要不要讓網頁顯示出來|
|basic_scroll_step|每次往多少畫面|
|refersh_toppost_times|刷新多少次top posts|
|save_rate|下載多少張圖片存一次json|
|load_prvs_json|須不需要從上次下載的之後繼續下載|
|log|要不要顯示 console log| -->
