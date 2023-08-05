
from datetime import datetime
from .models import Release, Notification
import requests

class GitHubService:
    def __init__(self, token: str):
        self.base_api_url = f'https://api.github.com'
        self.token = token

    def latestRelease(self, repo: str) -> Release:
        r = requests.get(f'{self.base_api_url}/repos/{repo}/releases/latest', headers={'Authorization': self.token})
        results = r.json()
        if(results is None):
            return None
        output = Release()
        output.releaseUrl = results['html_url']
        output.releaseNotes = results['body']
        output.version = results['tag_name']
        output.publishDate = results['published_at']
        return output

    def generateNotification(self, repo: str, sinceDate: datetime = None) -> Notification:
        r = requests.get(f'{self.base_api_url}/repos/{repo}', headers={'Authorization': self.token})
        results = r.json()
        output = Notification()
        output.name = repo
        if('html_url' not in results):
            print(results) # Debug - were we rate limited?
            return output
        output.repoInfo = results['html_url']
        output.releaseInfo = self.latestRelease(repo)
        # If we have release data and a sinceDate then we compare the dates to filter output.
        if(sinceDate is not None and output.releaseInfo is not None and output.releaseInfo.publishedSince(datetime.strptime(sinceDate, "%Y-%m-%d")) is not True):
            return None

        return output
