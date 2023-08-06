#### Installing

-----

Install with **pip**

```shell
pip install nest-encrypt==1.0.2
```




#### Usage

------

MD5 encryption

```python
>>> from pyencrypt.encrypt import md5
>>> raw = "hello beatiful girl"
>>> key = "fa58f7b9ce8640a19bd7eb21851db5e7"
>>> print(md5(raw))
66815e6b5255cf54a707877ec1b14afc
>>> print(md5(raw, salt=key))
08c21cf72b9a8de5482a257ddb1dd223
```

SHA1 encryption

```python
>>> from pyencrypt.encrypt import sha1
>>> raw = "hello beatiful girl"
>>> key = "fa58f7b9ce8640a19bd7eb21851db5e7"
>>> print(sha1(raw))
a0094a14aa1517ab259d5ac568ffe14173274765
>>> print(sha1(raw, salt=key))
9c337d95643209884d124e7ddbb58183af7e5478
```

SHA256 encryption

```python
>>> from pyencrypt.encrypt import sha256
>>> raw = "hello beatiful girl"
>>> key = "fa58f7b9ce8640a19bd7eb21851db5e7"
>>> print(sha256(raw))
253661d5a0d4bf76ad19638c07b910fb4c655679cb48c3e75c5454dc81329e34
>>> print(sha256(raw, salt=key))
50e0bfd2dcf4ce54cad9812049471b95db5ee3705b62e1dd1f5259eedcfa476f
```

SHA512 encryption

```python
>>> from pyencrypt.encrypt import sha512
>>> raw = "hello beatiful girl"
>>> key = "fa58f7b9ce8640a19bd7eb21851db5e7"
>>> print(sha512(raw))
f3ac26b13078a7f88442ca30e6e2ac281f4e17737b0c4e1cd1a79680c53bdb0d3f64d4d17549407b539f3e74f7d0c086ec6b7d5088d4f3155be2f89459a34904
>>> print(sha512(raw, salt=key))
58808567d8d891131659618c578852ed1a613bf5e778795ac035548ef7f952abb82b437b9025fb473b5b088ccf9a8802c292b364eac41a71e44c764c841aadec
```

Symmetric encryption

```shell
>>> from pyencrypt.encrypt import symmetric_encryption
>>> raw = "hello beatiful girl"
>>> key = "fa58f7b9ce8640a19bd7eb21851db5e7"
>>> print(symmetric_encryption(raw, key))
U2FsdGVkX18il7bfR+7FZnEJr9zQGGad1/ch8ccAna6FCS5Tjg0tho1/yRGe72Ky
```

Symmetric decryption

```shell
>>> from pyencrypt.encrypt import symmetric_decryption
>>> raw = "U2FsdGVkX18il7bfR+7FZnEJr9zQGGad1/ch8ccAna6FCS5Tjg0tho1/yRGe72Ky"
>>> key = "fa58f7b9ce8640a19bd7eb21851db5e7"
>>> print(symmetric_decryption(raw, key))
hello beatiful girl
```

Generate public-private key

```python
>>> from pyencrypt.encrypt import asymmetric_generate_key
>>> print(asymmetric_generate_key())
{'pub': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwsSx1DMgs6scsyDaz6SY\nwGUaSVD9Obl66VY8MegpDzqNrr4ri1eoP3SXAxoKoQZlL5qHeaXZKl+yseG+Van/\nDekSS2fl4q5o9C5YnwLvwUCw5AjyxWJqZqEM5aXzAtHcZUQ/PQ2pL2aWln+teUCp\nYWIlN9qSnLB0oYDdC0KgivLG0iF4/NC670Q/KSOAeTAL1V78Jwj+sNwzrzOfhnvv\n9pVBiVP/aULnMg1Xq+DDi2FNFNWLhnMIUPTB++xeQK+pMjhO8rJD1ZfmGRz1M6EP\nX0pcqPbUGhELCUVXF7oyVU/9Eo1/sq3KtvJmh8jahfwFot8LUwDDcYlRAwcPR8M3\nowIDAQAB\n-----END PUBLIC KEY-----', 'pri': b'-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAwsSx1DMgs6scsyDaz6SYwGUaSVD9Obl66VY8MegpDzqNrr4r\ni1eoP3SXAxoKoQZlL5qHeaXZKl+yseG+Van/DekSS2fl4q5o9C5YnwLvwUCw5Ajy\nxWJqZqEM5aXzAtHcZUQ/PQ2pL2aWln+teUCpYWIlN9qSnLB0oYDdC0KgivLG0iF4\n/NC670Q/KSOAeTAL1V78Jwj+sNwzrzOfhnvv9pVBiVP/aULnMg1Xq+DDi2FNFNWL\nhnMIUPTB++xeQK+pMjhO8rJD1ZfmGRz1M6EPX0pcqPbUGhELCUVXF7oyVU/9Eo1/\nsq3KtvJmh8jahfwFot8LUwDDcYlRAwcPR8M3owIDAQABAoIBAFi2tPUdsKiFqRXi\nQihQJY+EvZtle2H+nQCJWfO1dnZMSlqsnjLi42y700kDZJIB0rcDIPAE3czSOBeT\n5lkojFcusTmNgoVkwcNvFMig0snoiGnltYa4lBRZCQHVO8IuCsBJfLB3d3dyt+an\nE0HmdQA5bxBoy1z5drZVdtl5KJ0AuqICC2Er2wKBABLFgxA8XTKs54TScvi/Pxg7\nxPGURu3iYpkcI6gH/36/y4lg56PtjNZyx63fT9IcCob/RTsUoOa5J2OnPtxIUZc7\nToP9F7cshaRA8wTgbthH0QN+BOpm3+qSJgRhArDk/sllszmkjONxd0GPoH8Jkf6c\nrfukT6ECgYEA22olpsY6sF8SMPVFba39WfB7gvA6BW0FbaIy+vXazvjPdoQZV2er\n/XaUYEqtGiLWVKXsXWlFnPlfo0YOgSLiQH3nthM4G1/hxo+qV1tVWk9Sx12qqJ+P\n2EtfE1G0RRe65RUmdRQCSWrsuZZmXq8VUCiGAv0ZN7fdEo1lXSuJUvECgYEA4z6B\nMv/Rdlnbvg3PogokRDdakwV643RpQHfRHQ/0TWv6qwcpNM3nxVr7drjepf8gPIjh\nzcIBvqdUy4g8YrnyC6cMInMbN9cqrgEKNyVJAiYrDITCf4YsMi2hKn0yM2NV3ob+\nfvKelJ6NDtEMncEaZmht/HL4I8VRgHeDNjg7i9MCgYEAgsVc820qBXxkRzGn05rj\naPtfYcbzjdBQb+tAHzrw0nKQk75frCxp4YMPI+TeDrm8rG7H1VSs3MX0LkfO1UCJ\nQI7Jz0bdJdObqNBvYelZkZ29ZH16/U08WllxrP4BRzzBc0+LwDPQuRk1RddR5BTN\nyxyb4qQep4q6BBip1UHhcsECgYEAvgZfndkEPHap5YTBExxt9UlgiT70401OUmWf\nTTExNqjL5cbIM2rXnFYXn9C6Bo+QUm6YfCn2sYpVwxk6fchGWm4nHIuqwAhCnV0r\nQLACHDT0nLRLvL3jKVa0xcYJe6VeggXavSd/aoInLLOtXCHFRMug5ZDyZV80ZzwJ\nUga17JcCgYEAzYiOclUqEoSuSXx6nIcLagz/dKMS+XRg3xVislbXVNLK5X3BCIr9\nlz4zKbAYOo9punvaQlZCRfjTUHiLDh1DqCg6MCiugz8mIhw6CUNHU+sfQgrSfggV\n3KdLOUFvMhMhXf7RZMllWny6FmlzRvKQB8f/+2UE6yR5JmGxzfNDgQQ=\n-----END RSA PRIVATE KEY-----'}
```

Asymmetric encryption

```shell
>>> from pyencrypt.encrypt import asymmetric_encryption
>>> raw = "hello beatiful girl"
>>> pub = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwsSx1DMgs6scsyDaz6SY\nwGUaSVD9Obl66VY8MegpDzqNrr4ri1eoP3SXAxoKoQZlL5qHeaXZKl+yseG+Van/\nDekSS2fl4q5o9C5YnwLvwUCw5AjyxWJqZqEM5aXzAtHcZUQ/PQ2pL2aWln+teUCp\nYWIlN9qSnLB0oYDdC0KgivLG0iF4/NC670Q/KSOAeTAL1V78Jwj+sNwzrzOfhnvv\n9pVBiVP/aULnMg1Xq+DDi2FNFNWLhnMIUPTB++xeQK+pMjhO8rJD1ZfmGRz1M6EP\nX0pcqPbUGhELCUVXF7oyVU/9Eo1/sq3KtvJmh8jahfwFot8LUwDDcYlRAwcPR8M3\nowIDAQAB\n-----END PUBLIC KEY-----'
>>> print(asymmetric_encryption(pub, raw))
oaSbOdC31Xc/5OGezlAoUj2MxCnt4cSLss0uaMUioikpSLxE8GGooly18vUYnpyA14ZLCWk7AcF+Jiv1OBDVb747YjNIqfOfIhYQHtbrhybN7hCzFLO0CgJiJnRcX7ipwLwQGQf8Utet+dbHbryJ++8Fe2Dkr+6rUGzKtaQ7gCPKVoL+coKCW72bYayfP/uVYg3W9CBAv0oeUVHrdXeXIjBGRFBET8u4gkyNvEOA5gdcnwhSeVBEMBbyZpcLrYv3YRsnMTQA4WNCFIYVTRU8biVX6nucyuGsnfYCdHDhiESVD5P6vJoVs1a3gieyxkhonY0taYCAi2UTpmV7W3v0uA==
```

Asymmetric decryption

```shell
>>> from pyencrypt.encrypt import asymmetric_decryption
>>> raw = "oaSbOdC31Xc/5OGezlAoUj2MxCnt4cSLss0uaMUioikpSLxE8GGooly18vUYnpyA14ZLCWk7AcF+Jiv1OBDVb747YjNIqfOfIhYQHtbrhybN7hCzFLO0CgJiJnRcX7ipwLwQGQf8Utet+dbHbryJ++8Fe2Dkr+6rUGzKtaQ7gCPKVoL+coKCW72bYayfP/uVYg3W9CBAv0oeUVHrdXeXIjBGRFBET8u4gkyNvEOA5gdcnwhSeVBEMBbyZpcLrYv3YRsnMTQA4WNCFIYVTRU8biVX6nucyuGsnfYCdHDhiESVD5P6vJoVs1a3gieyxkhonY0taYCAi2UTpmV7W3v0uA=="
>>> pri = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAwsSx1DMgs6scsyDaz6SYwGUaSVD9Obl66VY8MegpDzqNrr4r\ni1eoP3SXAxoKoQZlL5qHeaXZKl+yseG+Van/DekSS2fl4q5o9C5YnwLvwUCw5Ajy\nxWJqZqEM5aXzAtHcZUQ/PQ2pL2aWln+teUCpYWIlN9qSnLB0oYDdC0KgivLG0iF4\n/NC670Q/KSOAeTAL1V78Jwj+sNwzrzOfhnvv9pVBiVP/aULnMg1Xq+DDi2FNFNWL\nhnMIUPTB++xeQK+pMjhO8rJD1ZfmGRz1M6EPX0pcqPbUGhELCUVXF7oyVU/9Eo1/\nsq3KtvJmh8jahfwFot8LUwDDcYlRAwcPR8M3owIDAQABAoIBAFi2tPUdsKiFqRXi\nQihQJY+EvZtle2H+nQCJWfO1dnZMSlqsnjLi42y700kDZJIB0rcDIPAE3czSOBeT\n5lkojFcusTmNgoVkwcNvFMig0snoiGnltYa4lBRZCQHVO8IuCsBJfLB3d3dyt+an\nE0HmdQA5bxBoy1z5drZVdtl5KJ0AuqICC2Er2wKBABLFgxA8XTKs54TScvi/Pxg7\nxPGURu3iYpkcI6gH/36/y4lg56PtjNZyx63fT9IcCob/RTsUoOa5J2OnPtxIUZc7\nToP9F7cshaRA8wTgbthH0QN+BOpm3+qSJgRhArDk/sllszmkjONxd0GPoH8Jkf6c\nrfukT6ECgYEA22olpsY6sF8SMPVFba39WfB7gvA6BW0FbaIy+vXazvjPdoQZV2er\n/XaUYEqtGiLWVKXsXWlFnPlfo0YOgSLiQH3nthM4G1/hxo+qV1tVWk9Sx12qqJ+P\n2EtfE1G0RRe65RUmdRQCSWrsuZZmXq8VUCiGAv0ZN7fdEo1lXSuJUvECgYEA4z6B\nMv/Rdlnbvg3PogokRDdakwV643RpQHfRHQ/0TWv6qwcpNM3nxVr7drjepf8gPIjh\nzcIBvqdUy4g8YrnyC6cMInMbN9cqrgEKNyVJAiYrDITCf4YsMi2hKn0yM2NV3ob+\nfvKelJ6NDtEMncEaZmht/HL4I8VRgHeDNjg7i9MCgYEAgsVc820qBXxkRzGn05rj\naPtfYcbzjdBQb+tAHzrw0nKQk75frCxp4YMPI+TeDrm8rG7H1VSs3MX0LkfO1UCJ\nQI7Jz0bdJdObqNBvYelZkZ29ZH16/U08WllxrP4BRzzBc0+LwDPQuRk1RddR5BTN\nyxyb4qQep4q6BBip1UHhcsECgYEAvgZfndkEPHap5YTBExxt9UlgiT70401OUmWf\nTTExNqjL5cbIM2rXnFYXn9C6Bo+QUm6YfCn2sYpVwxk6fchGWm4nHIuqwAhCnV0r\nQLACHDT0nLRLvL3jKVa0xcYJe6VeggXavSd/aoInLLOtXCHFRMug5ZDyZV80ZzwJ\nUga17JcCgYEAzYiOclUqEoSuSXx6nIcLagz/dKMS+XRg3xVislbXVNLK5X3BCIr9\nlz4zKbAYOo9punvaQlZCRfjTUHiLDh1DqCg6MCiugz8mIhw6CUNHU+sfQgrSfggV\n3KdLOUFvMhMhXf7RZMllWny6FmlzRvKQB8f/+2UE6yR5JmGxzfNDgQQ=\n-----END RSA PRIVATE KEY-----'
>>> print(asymmetric_decryption(pri, raw))
hello beatiful girl
```





