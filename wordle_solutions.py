#!/usr/bin/env python3

import requests
import re
import sys
import base64
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
from datetime import date, timedelta

base_url = "https://wordle.danielfrg.com"

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = b""
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def decrypt(ct, password, key_length=32):
    bs = AES.block_size
    salt = ct[:bs][8:]
    i = len(salt)+8
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = b""
    finished = False
    res = b""
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(ct[i:i+1024*bs])
        i += 1024 * bs
        if len(next_chunk) == 0:
            padding_length = chunk[-1]
            chunk = chunk[:-padding_length]
            finished = True
        res += chunk
    return res

def get_wordle_app():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    r = requests.get(base_url, headers=headers)
    m = re.search(r"/_next/static/chunks/pages/_app-[a-f0-9]+.js", r.text)
    r = requests.get(base_url + m.group(0), headers=headers)
    return r.text


def parse_javascript_data(js):
    m = re.search(r"o=\[\"[^\]]+\]", js)
    str_arr = m.group(0)
    str_arr = str_arr.lstrip("o=[")
    str_arr = str_arr.rstrip("]")
    enc_words = [i.strip('"') for i in str_arr.split(",")]

    m = re.findall(r"(\w)=atob\(\"((?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)\"\)", js)
    salt = base64.b64decode(m[0][1])
    key = base64.b64decode(m[1][1])
    dec_words = []
    for w in enc_words:
        data = base64.b64decode(w)
        dec_words.append(decrypt(data, key)[len(salt):].decode("utf-8"))

    m = re.search(r"\d{4}-\d{2}-\d{2}", js)
    ref_date = date.fromisoformat(m.group(0))
    ret = {}
    for i in range(len(dec_words)):
        ret[str(ref_date + timedelta(i))] = dec_words[i]
        
    return ret

if __name__ == "__main__":
    js = get_wordle_app()
    print(parse_javascript_data(js))
