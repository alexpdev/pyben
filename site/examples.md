# PyBen Usage Examples

PyBen is small bencode encode/decode library, designed to mimic the python standard lib's pickle/json modules.

-----

## Importing pyben

> importing the library

    `>>> import pyben`  

## Example 1

> Encode most builtin python data types to a bencoded byte sequence.

- identical to json and pickle modules.

    `>>> data = [1, "hello", 2, ["world"], {3: "!"}]`  
    `>>> encoded = pyben.dumps(data)`  
    `>>> encoded`  
    `b'li1e5:helloi2el5:worldedi3e1:!ee'`  

## Example 2

> Write Bencoded python builtin data types to file.

- Unlike the json and pickle modules, pyben accepts a str or PathLike object as
    the second argument and automatically open the path in bytes, write mode(`'wb'`), or you can
    open supply an opened ioStream yourself just like json and pickle.

    `>>> pyben.dump(data, "path/to/save/filename")`  
    or  
    `>>> with open('path/to/save/filename','wb') as binfile:`  
    `>>>     pyben.dump(data, binfile)`  

## Example 3

> Decode a Bencoded bytes-like object

- Identical to json and pickle modules.

    `>>> decoded = pyben.loads(encoded)`  
    `>>> decoded`  
    `[1, 'hello', 2, ['world'], {3: '!'}]`  

## Example 4

> Decode the bencoded contents of a file.

- Mimics the behaviour of the json/pickle library's `load` method.
- Pyben accepts Path-Like and path strings as input arguement as well as an opened file buffer.

    `>>> decoded_contents = pyben.load('path/to/save/filename')`  
    or  
    `>>> decoded_contents = pyben.load(open('path/to/save/filename', 'rb'))`  
    `>>> decoded_contents`  
    `[1, 'hello', 2, ['world'], {3: '!'}]`  
