# -*- coding: utf-8 -*-

############################################################################
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Affero General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or (at your option) any later version.                          #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Affero General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Affero General Public License #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
############################################################################

# Test links (random.bin):
# http://k2s.cc/file/527111edfb9ba/random.bin

import re

from module.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo
from module.plugins.internal.CaptchaService import ReCaptcha


class Keep2shareCC(SimpleHoster):
    __name__ = "Keep2shareCC"
    __type__ = "hoster"
    __pattern__ = r"https?://(?:www\.)?(keep2share|k2s|keep2s)\.cc/file/(?P<ID>\w+)"
    __version__ = "0.07"
    __description__ = """Keep2share.cc hoster plugin"""
    __author_name__ = ("stickell")
    __author_mail__ = ("l.stickell@yahoo.it")

    FILE_NAME_PATTERN = r'File: <span>(?P<N>.+)</span>'
    FILE_SIZE_PATTERN = r'Size: (?P<S>[^<]+)</div>'
    FILE_OFFLINE_PATTERN = r'File not found or deleted|Sorry, this file is blocked or deleted|Error 404'

    DIRECT_LINK_PATTERN = r'To download this file with slow speed, use <a href="([^"]+)">this link</a>'
    WAIT_PATTERN = r'Please wait ([\d:]+) to download this file'

    RECAPTCHA_KEY = '6LcYcN0SAAAAABtMlxKj7X0hRxOY8_2U86kI1vbb'

    FILE_URL_REPLACEMENTS = [(__pattern__, r"http://keep2share.cc/file/\g<ID>")]

    def handleFree(self):
        self.fid = re.search(r'<input type="hidden" name="slow_id" value="([^"]+)">', self.html).group(1)
        self.html = self.load(self.pyfile.url, post={'yt0': '', 'slow_id': self.fid})

        m = re.search(r"function download\(\){.*window\.location\.href = '([^']+)';", self.html, re.DOTALL)
        if m:  # Direct mode
            self.startDownload("http://www.keep2share.cc" + m.group(1))
        else:
            self.handleCaptcha()

            self.setWait(30)
            self.wait()

            self.html = self.load(self.pyfile.url, post={'uniqueId': self.fid, 'free': 1})

            m = re.search(self.DIRECT_LINK_PATTERN, self.html)
            if not m:
                self.parseError("Unable to detect direct link")
            self.startDownload('http://keep2share.cc' + m.group(1))

    def handleCaptcha(self):
        recaptcha = ReCaptcha(self)
        for i in xrange(5):
            challenge, response = recaptcha.challenge(self.RECAPTCHA_KEY)
            post_data = {'recaptcha_challenge_field': challenge,
                         'recaptcha_response_field': response,
                         'CaptchaForm%5Bcode%5D': '',
                         'free': 1,
                         'freeDownloadRequest': 1,
                         'uniqueId': self.fid,
                         'yt0': ''}

            self.html = self.load(self.pyfile.url, post=post_data)

            if 'recaptcha' not in self.html:
                self.correctCaptcha()
                break
            else:
                self.logInfo('Wrong captcha')
                self.invalidCaptcha()
        else:
            self.fail("All captcha attempts failed")

    def startDownload(self, url):
        self.logDebug('Direct Link: ' + url)
        self.download(url, disposition=True)


getInfo = create_getInfo(Keep2shareCC)
