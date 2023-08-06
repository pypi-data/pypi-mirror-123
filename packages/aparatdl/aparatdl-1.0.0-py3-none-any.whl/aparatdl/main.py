from aparatdl.scraper import Scraper
import requests
from aparatdl.exceptions import DownloadError
import speedtest


class Main:
    def __init__(self, url, quality):
        self.url = url
        self.quality = str(quality) if quality[-1] == 'p' else quality +'p'
        self.scraper = Scraper(self.url,self.quality)

    def speed_download(self):
        st = int(speedtest.Speedtest().download())
        return st

    def download(self):
        video_url = self.scraper.get_link()
        video_name = video_url.split('/')[-1][:41] + self.quality
        with open(video_name,'wb') as f:
            print('start downloading...')
            result = requests.get(video_url,stream=True)
            total_video_size = int(result.headers.get('content-length'))

            if total_video_size is None:
                raise DownloadError('An unpredictable problem has occurred. Please try again')
            else:
                download = 0
                st = self.speed_download()
                Estimation_time_dl = round(total_video_size*8 / st,2)
                print(f'speed download {round(st/1000000,2)} Mb/s')
                print(f'download video per {Estimation_time_dl} second')
                for data in result.iter_content(chunk_size=4096):
                    f.write(data)
                    download +=len(data)
                    done = int(50 * download / total_video_size)
                    print("\r[%s %s]" % ('=' * done, ' ' * (50 - done)), end='')
        print('\nvideo downloaded...')

m = Main('https://www.aparat.com/v/7CUzr/','144')
m.download()
# print(m.speed_download())
