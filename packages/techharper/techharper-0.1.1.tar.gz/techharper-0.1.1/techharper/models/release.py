from datetime import datetime

class Release():
    releaseUrl: str
    releaseNotes: str
    version: str
    publishDate: str
    
    def publishDateAsDate(self) -> datetime:
        return datetime.strptime(self.publishDate, "%Y-%m-%dT%H:%M:%SZ") # 2021-08-31T05:16:04Z

    def publishedSince(self, date: datetime) -> bool:
        return self.publishDateAsDate() > date 

    def to_json(self):
        return self.__dict__  
