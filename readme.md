# This is a python tool for download instagram image by hashtag.

run this:
```
python main.py
```

or run this:
```
python multiprocess_main.py # may be block by instagram
```

| 參數  | 用途 |
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
|log|要不要顯示 console log|
