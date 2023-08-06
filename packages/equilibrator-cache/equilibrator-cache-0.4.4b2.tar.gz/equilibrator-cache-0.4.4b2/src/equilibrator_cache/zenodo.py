"""Handles downloading an caching of files from Zenodo."""
# The MIT License (MIT)
#
# Copyright (c) 2013 The Weizmann Institute of Science.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich, Switzerland.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import hashlib
import logging
import pathlib
from io import BytesIO
from json import JSONDecodeError
from typing import Dict, NamedTuple, Optional

import appdirs
import httpx
from tenacity import retry, stop_after_attempt, wait_random
from tqdm import tqdm


logger = logging.getLogger(__name__)


class ZenodoSettings(NamedTuple):
    """
    Bundle the configuration for interacting with Zenodo.org.

    Attributes
    ----------
    doi : str
        The DOI of the equilibrator cache entry.
    filename : str
        The filename of the SQLite database.
    md5 : str
        The MD5 checksum of the SQLite database file.
    url : str
        The base URL of the API.

    """

    doi: str
    filename: str
    md5: str
    url: str


DEFAULT_COMPOUND_CACHE_SETTINGS = ZenodoSettings(
    doi="10.5281/zenodo.4128543",
    filename="compounds.sqlite",
    md5="9b66b85a886926d09755a66a3b452b6b",
    url="https://zenodo.org/api/",
)


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_random(min=5, max=10),
)
def find_record_by_doi(client: httpx.Client, doi: str) -> Optional[dict]:
    """Find a Zenodo record by its DOI and return all the metadata.

    Parameters
    ----------
    client: httpx.Client
        An httpx client configured with the base URL and desired timeout.
    doi : str
        The DOI of the requested entry.

    Returns
    -------
    dict
        Containing all of the metadata.

    """
    response = client.get(f"records/{doi.rsplit('.', 1)[1]}")
    response.raise_for_status()
    result = response.json()
    if result["doi"] != doi:
        raise ValueError(f"Cannot find a Zenodo record with doi:{doi}.")
    return result


@retry(
    reraise=True, stop=stop_after_attempt(3), wait=wait_random(min=5, max=10)
)
def download_from_url(client: httpx.Client, url: str) -> BytesIO:
    """Download a file from a given URL.

    Parameters
    ----------
    client: httpx.Client
        An httpx client configured with the base URL and desired timeout.
    url : str
        The URL address of the file.

    Returns
    -------
    BytesIO
        Bytes buffer of the downloaded file.

    """
    data = BytesIO()
    with client.stream("GET", url) as response:
        response.raise_for_status()
        total = int(response.headers["Content-Length"])
        md5 = response.headers["content-md5"]

        num_bytes = 0
        with tqdm(
            total=total, unit_scale=True, unit_divisor=1024, unit="B"
        ) as progress:
            for chunk in response.iter_bytes():
                data.write(chunk)
                progress.update(len(chunk))
                num_bytes += len(chunk)

    if hashlib.md5(data.getvalue()).hexdigest() != md5:
        raise IOError(f"MD5 mismatch while trying to download file from {url}.")

    data.seek(0)
    return data


def get_zenodo_files(
    settings: ZenodoSettings, timeout: float = 5.0
) -> Dict[str, BytesIO]:
    """Download all files from a Zenodo entry synchronously."""
    with httpx.Client(base_url=settings.url, timeout=timeout) as client:
        data = find_record_by_doi(client, settings.doi)
        fnames = [d["key"] for d in data["files"]]
        urls = [d["links"]["self"] for d in data["files"]]
        data_streams = [download_from_url(client, url) for url in urls]
    return dict(zip(fnames, data_streams))


def get_cached_filepath(settings: ZenodoSettings) -> pathlib.Path:
    """Get data from a file stored in Zenodo (or from cache, if available).

    Parameters
    ----------
    settings : ZenodoSettings
        Configuration for the interaction with Zenodo.org.

    Returns
    -------
    pathlib.Path
        The path to the locally cached file.

    """

    cache_directory = pathlib.Path(
        appdirs.user_cache_dir(appname="equilibrator")
    )
    cache_directory.mkdir(parents=True, exist_ok=True)

    cache_fname = cache_directory / settings.filename

    if cache_fname.exists():
        logging.info(
            "Validate the cached copy using MD5 checksum '%s'.", settings.md5
        )
        if hashlib.md5(cache_fname.read_bytes()).hexdigest() == settings.md5:
            return cache_fname

    # If the checksum is not okay, it means the file is corrupted or
    # exists in an older version. Therefore, we ignore it and replace it
    # with a new version.
    logging.info("Fetching a new version of the Compound Cache from Zenodo.")
    try:
        dataframe_dict = get_zenodo_files(settings)
    except JSONDecodeError:
        raise IOError(
            "Some required data needs to be downloaded from Zenodo.org, but "
            "there is a communication problem at the "
            "moment. Please wait and try again later."
        )

    cache_fname.write_bytes(dataframe_dict[settings.filename].getbuffer())

    logging.info(
        "Validate the downloaded copy using MD5 checksum '%s'.", settings.md5
    )
    md5 = hashlib.md5(cache_fname.read_bytes()).hexdigest()
    if md5 != settings.md5:
        raise IOError(
            f"The newly downloaded Zenodo file (DOI: {settings.doi} -> "
            f"{settings.filename}) did not pass the MD5 "
            f"checksum test: expected ({settings.md5}) != actual ({md5})."
        )

    return cache_fname
