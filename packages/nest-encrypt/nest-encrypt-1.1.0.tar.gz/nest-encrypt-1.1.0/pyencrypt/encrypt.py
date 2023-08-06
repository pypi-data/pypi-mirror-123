# -*- coding: utf-8 -*-
import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5, AES
from Crypto.PublicKey import RSA


# md5 加密
def md5(raw: str, salt: str = '') -> str:
    md5_object = hashlib.md5()
    md5_string = raw + salt
    md5_object.update(md5_string.encode("utf-8"))
    return md5_object.hexdigest()


# sha1 加密
def sha1(raw: str, salt: str = '') -> str:
    sha1_object = hashlib.sha1()
    sha1_string = raw + salt
    sha1_object.update(sha1_string.encode("utf-8"))
    return sha1_object.hexdigest()


# sha256 加密
def sha256(raw: str, salt: str = '') -> str:
    sha256_object = hashlib.sha256()
    sha256_string = raw + salt
    sha256_object.update(sha256_string.encode("utf-8"))
    return sha256_object.hexdigest()


# sha512 加密
def sha512(raw: str, salt: str = '') -> str:
    sha512_object = hashlib.sha512()
    sha512_string = raw + salt
    sha512_object.update(sha512_string.encode("utf-8"))
    return sha512_object.hexdigest()


# 生成公私钥
def asymmetric_generate_key() -> dict:
    ae = _AsymmetricEncryption()
    return ae.generate_key()


# 非对称加密
def asymmetric_encryption(key: bytes, raw: str) -> str:
    ae = _AsymmetricEncryption()
    return ae.encryption(key, raw)


# 非对称解密
def asymmetric_decryption(key: bytes, raw: str) -> str:
    ae = _AsymmetricEncryption()
    return ae.decryption(key, raw)


# 对称加密
def symmetric_encryption(key: str, raw: str) -> str:
    sen = _SymmetricEncryption(key)
    return sen.encryption(raw).decode()


# 对称解密
def symmetric_decryption(key: str, raw: str) -> str:
    sen = _SymmetricEncryption(key)
    return sen.decryption(raw).decode()


# 对称加密类
class _SymmetricEncryption:
    # 初始化
    def __init__(self, key: str = '') -> None:
        self.key = bytes(key, 'utf-8')

    def _pad(self, data: str) -> str:
        length = 16 - (len(data) % 16)
        return data + (chr(length) * length)

    def _unpad(self, data: str) -> bool:
        return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

    def _bytes_to_key(self, data: str, salt: str, output: int = 48) -> str:
        data += salt
        key = self._md5(data)
        final_key = key
        while len(final_key) < output:
            key = self._md5(key + data)
            final_key += key
        return final_key[:output]

    # 加密
    def encryption(self, message: str) -> bytes:
        salt = Random.new().read(8)
        key_iv = self._bytes_to_key(self.key, salt, 32 + 16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(b"Salted__" + salt +
                                aes.encrypt(self._pad(message).encode("utf-8")))

    # 解密
    def decryption(self, encrypted: str) -> str:
        encrypted = base64.b64decode(encrypted)
        assert encrypted[0:8] == b"Salted__"
        salt = encrypted[8:16]
        key_iv = self._bytes_to_key(self.key, salt, 32 + 16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return self._unpad(aes.decrypt(encrypted[16:]))

    # MD5方法
    def _md5(self, raw: str) -> str:
        md5_object = hashlib.md5()
        md5_object.update(raw)
        return md5_object.digest()


# 非对称加密
class _AsymmetricEncryption:
    # 默认生成器
    _random_generator = None

    # 生成公私钥
    def generate_key(self) -> dict:
        # 获取一个伪随机数生成器
        self._random_generator = Random.new().read
        # 获取一个rsa算法对应的密钥对生成器实例
        rsa = RSA.generate(2048, self._random_generator)
        # 生成私钥
        pri_key = rsa.exportKey()
        # 生成公钥
        pub_key = rsa.publickey().exportKey()
        # 返回值
        return {
            "pub": pub_key,
            "pri": pri_key,
        }

    # 加密
    def encryption(self, key: bytes, raw: str) -> str:
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = base64.b64encode(cipher.encrypt(raw.encode('utf-8')))
        return text.decode('utf-8')

    # 解密
    def decryption(self, key: bytes, raw: str) -> str:
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(raw), self._random_generator)
        return text.decode('utf-8')

