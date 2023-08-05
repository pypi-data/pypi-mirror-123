import re
from youtubedown.module1 import asyncmodule


class asyncDown():
    def __init__(self, kwargs):
        # self.title = None if not kwargs['title'] else kwargs['title']
        self.check = kwargs['check']
        # self.path = None if not kwargs['path'] else kwargs['path']
        # self.option = None if not kwargs['option'] else kwargs['option']
        # self.format = None if not kwargs['format'] else kwargs['format']
        self.kwargs = kwargs

    async def lookup(**kwargs):
        '''
          "title": str
          "path": str
          "option": dict
          "format": str
        '''
        if len(kwargs) == 0:
            return ValueError
        if kwargs.get('title') is None:
            return ValueError
        if kwargs.get('path') is None:
            kwargs['path'] = "music"
        if kwargs.get('debug') is None:
            kwargs['debug'] = False
        URL_REGEX = re.compile(
            r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        )
        
        if URL_REGEX.match(kwargs['title']):
            kwargs['check']= True
        else:
            kwargs['check'] = False
        return asyncDown(kwargs)
    async def download(self):
        if self.check is None: return {"result": None}
        if self.check is True:
            module = asyncmodule(self.kwargs)
            result = await asyncmodule.urldown(self)
            return result
        if self.check is False:
            module = asyncmodule(self.kwargs)
            result = await asyncmodule.titledown(self)
            return result
    # async def search(self):
    #     if self.check is None: return {"result": None}
    #     if self.check is True:
    #         result = await asyncmodule.urlsearch(self, title=self.title)
    #         return result
    #     if self.check is False:
    #         result = await asyncmodule.titleserach(self, title=self.title)
    #         return result