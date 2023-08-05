from youtube_dl import YoutubeDL
import youtube_dl
import asyncio


'''
If you specify an option, the meaning of path disappears.
'''
class asyncmodule():
    def __init__(self, kwargs):
        self.kwargs = kwargs
    def option_choice(self, option):
        if self.kwargs['format'] in {"mp3","wav", "mp4",'webm','mkv'}:
            if self.kwargs['format'] in {"mp3", "wav"}:
                option['format'] = 'bestaudio/best'
                option['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': self.kwargs["format"],'preferredquality': '192'}] #audio only
                return option
            else:
                # option['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]' #mp4 1080P
                #option['videoformat'] = "mkv"
                option['outtmpl'] = f'{self.kwargs["path"]}.{self.kwargs["format"]}'
                return option
        else:
            option['format'] = 'bestaudio/best'
            option['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': "mp3",'preferredquality': '192'}]
            return option

    async def urldown(self):
        loop = asyncio.get_event_loop()
        if self.kwargs.get('option') is None:
            if self.kwargs.get('format') is None:
                self.kwargs['format'] = "mp3"
            
            YDL_OPTIONS = {
            'quiet': not self.kwargs['debug'],
            'outtmpl': f'{self.kwargs["path"]}.%(ext)s',
            }
            YDL_OPTIONS = asyncmodule.option_choice(self, YDL_OPTIONS)

        else:
            YDL_OPTIONS = self.kwargs['option']
            
        try:
            with YoutubeDL(YDL_OPTIONS) as ytdl:
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(self.kwargs['title'], download=True))
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
            return {"result": False, "json_result": False}
        try:
            del data['formats']     
            data['result'] = True
            data['json_result'] = True
            return data
        except:
            return {"result": True, "json_result": False}
    async def titledown(self):
        loop = asyncio.get_event_loop()
        if self.kwargs.get('option') is None:
            if self.kwargs.get('format') is None:
                self.kwargs['format'] = "mp3"
            
            YDL_OPTIONS = {
            'quiet': not self.kwargs['debug'],
            'outtmpl': f'{self.kwargs["path"]}.%(ext)s',
            }
            YDL_OPTIONS = asyncmodule.option_choice(self, YDL_OPTIONS)

        else:
            YDL_OPTIONS = self.kwargs['option']
        try:
            with YoutubeDL(YDL_OPTIONS) as ytdl:
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info("ytsearch:{0}".format(self.kwargs['title']), download=True))
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
            return {"result": False, "json_result": False}
        try:
            data = data['entries'][0]
            if data.get('formats'): del data['formats']
            if data.get('automatic_captions'): del data['automatic_captions']
            data['result'] = True
            data['json_result'] = True
            return data
        except:
            return {"result": True, "json_result": False}