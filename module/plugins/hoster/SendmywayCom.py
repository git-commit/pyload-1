# -*- coding: utf-8 -*-
from module.plugins.hoster.XFileSharingPro import XFileSharingPro, create_getInfo


class SendmywayCom(XFileSharingPro):
    __name__ = "SendmywayCom"
    __type__ = "hoster"
    __pattern__ = r"http://(?:\w*\.)*?sendmyway.com/\w{12}"
    __version__ = "0.01"
    __description__ = """SendMyWay hoster plugin"""
    __author_name__ = ("zoidberg")
    __author_mail__ = ("zoidberg@mujmail.cz")

    FILE_NAME_PATTERN = r'<p class="file-name" ><.*?>\s*(?P<N>.+)'
    FILE_SIZE_PATTERN = r'<small>\((?P<S>\d+) bytes\)</small>'
    HOSTER_NAME = "sendmyway.com"


getInfo = create_getInfo(SendmywayCom)
