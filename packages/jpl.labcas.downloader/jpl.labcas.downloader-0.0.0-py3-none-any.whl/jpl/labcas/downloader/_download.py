# encoding: utf-8

'''JPL LabCAS Downloader: download implementation.'''

import logging, requests, urllib.parse, os
from pathlib import Path


_logger   = logging.getLogger(__name__)

_timeout  = 10        # How long to wait for the query to return (in seconds)
_max_rows = 99999999  # How many rows max to retrieve; this code breaks if there's more data than this
_bufsiz   = 512       # Buffer size in bytes for retrieving data


def _enumerate_files(url: str, data_id: str, auth: tuple) -> list:
    '''Enumerate files.

    This asks the data access API at ``url`` for the files that match the ``data_id``, using the optional
    ``auth`` tuple. It returns a list of matching URLs to fetch.
    '''
    _logger.debug('𝑓 _enumerate_files %s, %s, auth=%r', url, data_id, auth is not None)
    request_type = 'datasets' if '/' in data_id else 'collections'
    if not url.endswith('/'): url += '/'
    url = url + request_type + f'/list?rows={_max_rows}&q=id:' + data_id
    _logger.debug('Constructed URL for file list is «%s»', url)
    _logger.info('Requesting matching files for %s from the API', data_id)
    response = requests.get(url, timeout=_timeout, auth=auth)
    matches = [i for i in response.text.split('\n') if i.strip()]
    _logger.info('Got %d files', len(matches))
    return matches


def _fetch(url: str, target: Path, auth: tuple):
    '''Fetch data.

    This retrieves the file at ``url`` and writes it to ``target``, using ``auth`` to log in if
    it's not None.
    '''
    _logger.debug('𝑓 _fetch %s to %s, auth=%r', url, target, auth is not None)
    rel_path = urllib.parse.unquote(url.split('id')[1][1:])
    response = requests.get(url, stream=True, auth=auth)
    os.makedirs(os.path.join(target, os.path.dirname(rel_path)), exist_ok=True)
    with open(os.path.join(target, rel_path), 'wb') as outfile:
        for chunk in response.iter_content(chunk_size=_bufsiz):
            if chunk: outfile.write(chunk)


def download(url: str, data_id: str, target: Path, username: str, password: str):
    '''Download data from LabCAS.

    This accesses the LabCAS API at ``url``, authenticating with ``username`` and ``password`` to
    retrieve the collection or dataset identified by ``data_id`` and writing the data to ``target``.
    '''
    if username and password:
        auth = (username, password)
    else:
        auth = None

    files = _enumerate_files(url, data_id, auth)
    for file in files:
        _fetch(file, target, auth)
