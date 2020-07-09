from IG_downloader import Downloader


if __name__ == "__main__":


    downloader = Downloader(hashtag='love', 
                            target_download_numbers=1200, 
                            ig_account='x@gmail.com',
                            ig_password='x?x?')

    downloader.start_download()

