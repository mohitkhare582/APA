from time import time
import requests
import logging as logger

from bs4 import BeautifulSoup

from .config import getValueOrDefault
from .oprexceptions import SoupObjectError
# Helper Functions


def isBlank(string: str) -> bool:
    return string is None or string == None or string == "" or len(string) == 0


def isNotBlank(string: str) -> bool:
    return not isBlank(string)


def hasNumbers(string: str) -> bool:
    if isNotBlank(string):
        return any(char.isdigit() for char in string)
    return False


def startsWith(string: str, ch: str) -> bool:
    if isNotBlank(string) and isNotBlank(ch):
        return string[0:len(ch)] == ch
    return False


def endsWith(string: str, ch: str) -> bool:
    if isNotBlank(string) and isNotBlank(ch):
        return string[-1*len(ch):] == ch
    return False


def isEmpty(array: list) -> bool:
    return len(array) == 0 or array is None


def isNotEmpty(array: list) -> bool:
    return not isEmpty(array)


def ToString(array: list) -> str:
    return " ".join(array)


def AsOne(array: list) -> list:
    result = []
    for arr in array:
        result.extend(arr)
    return result


# Soup cache implementation
def GetPageSoup(headers, url):
    retryCount = 0
    soup = None
    t = getValueOrDefault("Requests", "RetryCount", 5)
    retry = True
    while retryCount < t and retry:
        try:
            session = requests.Session()
            session.headers['User-Agent'] = headers
            soup = BeautifulSoup(session.get(url).content, 'html.parser')
            session.close()
            retry = False
        except Exception as ex:
            time.sleep(5)
            retryCount += 1
    if soup is None:
        raise SoupObjectError
    return soup