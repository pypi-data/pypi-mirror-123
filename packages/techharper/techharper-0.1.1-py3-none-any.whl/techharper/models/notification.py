from .release import Release

class Notification():
    name: str
    repoInfo: str
    releaseInfo: Release

    def to_json(self):
        return self.__dict__  
