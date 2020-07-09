from IG_downloader import Downloader
from multiprocessing import Process


if __name__ == "__main__":

    hashtag_list = ['love', 'instagood']
    ig_account = [{'account':'??@gmail.com', 'password':'??'},
                  {'account':'??@gmail.com', 'password':'??'}]


    process = []
    for i in range(len(hashtag_list)):
        downloader = Downloader(hashtag=hashtag_list[i], 
                                target_download_numbers=1200, 
                                ig_account=ig_account[i]['account'],
                                ig_password=ig_account[i]['password'])

        p = Process(target=downloader.start_download)
        p.start()
        process.append(p)