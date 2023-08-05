# Harper

Tool to fetch the latest releases in technologies.

## Introduction

The `techharper` Python module allows you to request the latest release information for specified technologies.

This currently searches specifically for GitHub repositories.

## Token

This tool requires a [GitHub Personal Access Token][gh-token]. 

*NOTE - This token has no specific requirements. It simply provides basic authentication in order to increase the API rate limit.*

## Example

An example application is provided [here](https://github.com/BoredTweak/techharper/blob/main/example.py). 

- From a terminal instance in this directory install dependencies by running `pip install -r requirements.txt`
- Run the application by running `py example.py --token YOUR_GITHUB_PAT_HERE --repository 'vercel/next.js'`

## Additional Reading

- [Requests Library](https://requests.kennethreitz.org/en/master/)

[technology-main]: https://www.python.org/downloads/
[gh-token]: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token