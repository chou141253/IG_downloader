from IG_downloader import Downloader
from hashtag_reader import read
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--begin", type=int, required=True, help="the first downloaded hashtag")
    parser.add_argument("--end", type=int, required=True, help="the last downloaded hashtag")
    parser.add_argument("--account", type=str, required=True, help="ig account")
    parser.add_argument("--passwd", type=str, required=True, help="ig passwd")
    parser.add_argument("--tagFile", type=str, default="./instagram_rank.json", help="path to tag file")
    parser.add_argument("--chromeDriver", type=str, default="./web_driver/chromedriver_linux64/chromedriver", help="path to chrome driver")
    args = parser.parse_args()

    hashtagTable = read(args.tagFile)
    
    ix = args.begin
    
    while ix < args.end + 1:
        
        start_time = time.time() # just for print time cost
        
        downloader = Downloader(hashtag=hashtagTable[str(ix)][1:],
                                ig_account=args.account,
                                ig_password=args.passwd,
                                target_download_numbers=1200,
                                chrome_driver=args.chromeDriver
                                )
        check = downloader.start_download()
        if 'fail' in check:
            ix -= 1
        ix += 1
        
        print("cost time: {} secs".format(time.time()-start_time))
        time.sleep(0.5)
        
        
