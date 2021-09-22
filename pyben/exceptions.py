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

"""Exceptions used throughout the PyBen Package/Library."""


class DecodeError(Exception):

    """
    Error occured during decode process.

    Args
    ------
    val: any
        Value that cause the exception
    """

    def __init__(self, val=None):
        """Construct Exception DecodeError."""
        msg = f"Decoder is unable to interpret {type(val)} type = {str(val)}"
        super().__init__(msg)


class EncodeError(Exception):

    """
    Error occured during encoding process.

    Args
    ------
    val: any
        Value that cause the exception
    """

    def __init__(self, val=None):
        """Construct Exception EncodeError."""
        msg = f"Encoder is unable to interpret {type(val)} type = {str(val)}"
        super().__init__(msg)



class FilePathError(Exception):

    """
    Bad path error.

    Args
    ------
    val: any
        Value that cause the exception
    """

    def __init__(self, obj=None):
        """Construct Exception Subclass FilePathError."""
        msg = f"{str(obj)} doesn't exist or is unavailable."
        super().__init__(msg)
