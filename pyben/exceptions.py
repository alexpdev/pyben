#! /usr/bin/python3
# -*- coding: utf-8 -*-

#####################################################################
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#####################################################################

class DecodeError(Exception):
    """Error occured during decode process."""

    def __init__(self, val=None, msg=None):
        self.val = val
        self.msg = msg


class EncodeError(Exception):
    """Error occured during encoding process."""

    def __init__(self, val=None, msg=None):
        self.val = val
        self.msg = msg

class FilePathError(Exception):
    """Bad path error."""

    def __init__(self, obj=None, msg=None):
        self.obj = obj
        self.msg = msg
