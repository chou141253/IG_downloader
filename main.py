from IG_downloader import Downloader


if __name__ == "__main__":


    downloader = Downloader(hashtag='love', 
                            target_download_numbers=1200, 
                            ig_account='ntnuaiotlab2020@gmail.com',
                            ig_password='ntnuaiotlab2020')

    downloader.start_download()

