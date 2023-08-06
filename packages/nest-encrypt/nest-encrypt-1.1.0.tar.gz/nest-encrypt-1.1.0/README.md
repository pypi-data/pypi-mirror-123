#### Installing

-----

Install with **pip**

```shell
pip install nest-encrypt==1.1.0
```


#### Usage

------

- MD5 encryption

  > :explain: md5加密
  >
  > :syntax: md5(raw: object, salt:str="") -> str
  >
  > :param: raw， 需要加密的数据
  >
  > :param: salt， 盐值，默认为""
  >
  > :return: md5加密后的字符串

  ```python
  >>> from pyencrypt.encrypt import md5
  >>> raw = "123456"
  >>> key = "abc"
  >>> print(md5(raw))
  >>> "e10adc3949ba59abbe56e057f20f883e"
  >>> print(md5(raw, salt=key))
  >>> "df10ef8509dc176d733d59549e7dbfaf"
  ```



- SHA1 encryption

  > :explain: sha1加密
  >
  > :syntax:sha1(raw: object, salt:str="") -> str
  >
  > :param: raw， 需要加密的数据
  >
  > :param: salt， 盐值，默认为""
  >
  > :return: sha1加密后的字符串

  ```python
  >>> from pyencrypt.encrypt import sha1
  >>> raw = "123456"
  >>> key = "abc"
  >>> print(sha1(raw))
  >>> "7c4a8d09ca3762af61e59520943dc26494f8941b"
  >>> print(sha1(raw, salt=key))
  >>> "a172ffc990129fe6f68b50f6037c54a1894ee3fd"
  ```

  

- SHA256 encryption

  > :explain: sha256加密
  >
  > :syntax: sha256(raw: object, salt:str="") -> str
  >
  > :param: raw， 需要加密的数据
  >
  > :param: salt， 盐值，默认为""
  >
  > :return: sha256加密后的字符串

  ```shell
  >>> from pyencrypt.encrypt import sha256
  >>> raw = "123456"
  >>> key = "abc"
  >>> print(sha256(raw))
  >>> "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
  >>> print(sha256(raw, salt=key))
  >>> "931145d4ddd1811be545e4ac88a81f1fdbfaf0779c437efba16b884595274d11"
  ```

  

- SHA512 encryption

  > :explain: sha512加密
  >
  > :syntax: sha512(raw: object, salt:str="") -> str
  >
  > :param: raw， 需要加密的数据
  >
  > :param: salt， 盐值，默认为""
  >
  > :return: sha512加密后的字符串

  ```python
  >>> from pyencrypt.encrypt import sha512
  >>> raw = "123456"
  >>> key = "abc"
  >>> print(sha512(raw))
  >>> "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413"
  >>> print(sha512(raw, salt=key))
  >>> "8756869d440a13e93979197b5d7839c823de87c2b115bce0dee62030af3b5b63114a517f1ab02509bfefa88527369ae0ad7946990f27dcb37711a7d6fb9bc893"
  ```



- Symmetric encryption

  > :explain: 对称加密
  >
  > :syntax: symmetric_encryption(key: str, raw: str)  -> str
  >
  > :param: raw， 需要加密的数据
  >
  > :param: key， 密钥
  >
  > :return: 对称加密后的字符串

  ```python
  >>> from pyencrypt.encrypt import symmetric_encryption
  >>> raw = "123456"
  >>> key = "abc
  >>> print(symmetric_encryption(key, raw))
  >>> "U2FsdGVkX1/Fy5cRpcVwYtccSo6PQPk6QVFiffta+Qs="
  ```

  

- Symmetric decryption

  > :explain: 对称解密
  >
  > :syntax: symmetric_decryption(key: str, raw: str)  -> str
  >
  > :param: raw， 需要解密的数据
  >
  > :param: key， 密钥
  >
  > :return: 对称解密后的字符串

  ```python
  >>> from pyencrypt.encrypt import symmetric_decryption
  >>> raw = "U2FsdGVkX19K3aZwm2coZc7SgcFNWfMnDHAWAzYGgpE="
  >>> key = "abc"
  >>> print(symmetric_decryption(key, raw))
  >>> "123456"
  ```

  

- Generate public-private key

  > :explain: rsa生成公私钥
  >
  > :syntax: asymmetric_generate_key() -> dict
  >
  > :return: rsa生成公私钥

  ```python
  >>> from pyencrypt.encrypt import asymmetric_generate_key
  >>> print(asymmetric_generate_key())
  >>> {
      	'pub': b'-----BEGIN PUBLIC KEY-----省略-----END PUBLIC KEY-----', 
      	'pri': b'-----BEGIN RSA PRIVATE KEY-----省略-----END RSA PRIVATE KEY-----'
      }
  ```

  

- Asymmetric encryption

  > :explain: 非对称加密
  >
  > :syntax: asymmetric_encryption(pub: str, raw:str) -> str
  >
  > :param: raw， 需要加密的数据
  >
  > :param: pub， 公钥
  >
  > :return: 非对称加密后的字符串

  ```python
  >>> from pyencrypt.encrypt import asymmetric_encryption
  >>> raw = "123456"
  >>> pub = '-----BEGIN PUBLIC KEY-----省略-----END PUBLIC KEY-----'
  >>> print(asymmetric_encryption(pub, raw))
  >>> "CTngFmQEqnc2OTNCi5/Nm9Kovp06CAp5TKjYS/aaXf/0Cn/8CcQyhpZTQSKlUHelLO5fb64AcRvZSI+E1qsKDlchEYnHMAmR8F8O6F9k/9v1yf8Ckocvb54l4IhS/9alPiFjewcLYr+Lnc5i7jByHjs7bEx/aROf+79dG326RnxqAJI8wMS3PfdoPJCj8k9bp8G7KH5aRn2noqDq1rHHjSTioVduE3ydT2iCBHiAw1OHSpW5/yPsZ8jd8DF4Vz5JAujPPKjE37B/WeG4OcVczaKuCA/H0dbHJv23cNfD/Jz/YwpKmTlgpqECrTjXpEkIMP0e++4jU3h+swmw9Fpw/Q=="
  ```

  

- Asymmetric decryption

  > :explain: 非对称解密
  >
  > :syntax: asymmetric_decryption(pri: str, raw:str) -> str
  >
  > :param: raw， 需要解密的数据
  >
  > :param: pri， 私钥
  >
  > :return: 非对称解密后的字符串

  ```python
  >>> from pyencrypt.encrypt import asymmetric_decryption
  >>> raw = "CTngFmQEqnc2OTNCi5/Nm9Kovp06CAp5TKjYS/aaXf/0Cn/8CcQyhpZTQSKlUHelLO5fb64AcRvZSI+E1qsKDlchEYnHMAmR8F8O6F9k/9v1yf8Ckocvb54l4IhS/9alPiFjewcLYr+Lnc5i7jByHjs7bEx/aROf+79dG326RnxqAJI8wMS3PfdoPJCj8k9bp8G7KH5aRn2noqDq1rHHjSTioVduE3ydT2iCBHiAw1OHSpW5/yPsZ8jd8DF4Vz5JAujPPKjE37B/WeG4OcVczaKuCA/H0dbHJv23cNfD/Jz/YwpKmTlgpqECrTjXpEkIMP0e++4jU3h+swmw9Fpw/Q=="
  >>> pri = '-----BEGIN RSA PRIVATE KEY-----省略-----END RSA PRIVATE KEY-----'
  >>> print(asymmetric_decryption(pri, raw))
  >>> "123456"
  ```





