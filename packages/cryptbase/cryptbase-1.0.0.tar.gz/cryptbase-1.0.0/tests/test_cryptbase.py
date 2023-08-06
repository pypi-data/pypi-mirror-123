
import base64
import random
import secrets
import string

import cryptbase

aes_n = 256
key_bytes = int(aes_n / 8)
population = string.ascii_letters + string.digits + string.punctuation
length = 2048


def test_main():
    assert cryptbase.__version__ == '0.0.0'


def test_string_key():
    try:
        cryptbase.cryptbase.AES256CTREncryptor(secrets.token_bytes(key_bytes))
        assert False
    except ValueError:
        pass


def test_clear():
    encryptor = cryptbase.cryptbase.AES256CTREncryptor(bytearray(secrets.token_bytes(key_bytes)))
    assert '_AES256CTREncryptor__key' in encryptor.__dict__.keys()
    assert '_AES256CTREncryptor__protect' in encryptor.__dict__.keys()
    encryptor.clear()
    for i in range(key_bytes):
        assert encryptor.__dict__['_AES256CTREncryptor__key'][i] == 0
        assert encryptor.__dict__['_AES256CTREncryptor__protect'][i] == 0


def test_contextmgr():
    with cryptbase.cryptbase.AES256CTREncryptor(bytearray(secrets.token_bytes(key_bytes))) as encryptor:
        e = encryptor
        assert '_AES256CTREncryptor__key' in encryptor.__dict__.keys()
        assert '_AES256CTREncryptor__protect' in encryptor.__dict__.keys()
    for i in range(key_bytes):
        assert e.__dict__['_AES256CTREncryptor__key'][i] == 0
        assert e.__dict__['_AES256CTREncryptor__protect'][i] == 0


def test_crypto():
    for _ in range(16):
        encryptor = cryptbase.cryptbase.AES256CTREncryptor(bytearray(secrets.token_bytes(key_bytes)))
        for _ in range(32):
            plaintext = ''.join(random.choices(population, k=length)).encode('ascii')
            assert plaintext == encryptor.decrypt(*encryptor.encrypt(plaintext))


def test_encryptor():
    try:
        cryptbase.cryptbase.AES256CTREncryptor(None)
        assert False
    except ValueError:
        pass

    try:
        cryptbase.cryptbase.AES256CTREncryptor(bytes([]))
        assert False
    except ValueError:
        pass

    try:
        key = secrets.token_bytes(1)
        cryptbase.cryptbase.AES256CTREncryptor(key)
        assert False
    except ValueError:
        pass


def test_container_bad_key_length():
    aes_n = 128
    key_bytes = int(aes_n / 8)
    try:
        cryptbase.cryptbase.AES256CTREncryptor(bytearray(secrets.token_bytes(key_bytes)))
        assert False
    except ValueError:
        pass

    aes_n = 512
    key_bytes = int(aes_n / 8)
    try:
        cryptbase.cryptbase.AES256CTREncryptor(bytearray(secrets.token_bytes(key_bytes)))
        assert False
    except ValueError:
        pass


def test_containter_encrypt():
    for _ in range(16):
        with cryptbase.cryptbase.AES256CTREncryptor(bytearray(secrets.token_bytes(key_bytes))) as encryptor:
            for _ in range(32):
                plaintext = ''.join(random.choices(population, k=length))
                container = cryptbase.cryptbase.CryptoContainer(encryptor=encryptor, plaintext=plaintext)

                assert container.plaintext == plaintext
                assert str(container) == '@'.join([container.ciphertext, container.iv])

                cipher_b64 = container.ciphertext
                iv_b64 = container.iv

                ciphertext = base64.b64decode(cipher_b64)
                iv = base64.b64decode(iv_b64)
                decrypted = encryptor.decrypt(ciphertext, iv).decode('utf-8')
                assert type(plaintext) == type(decrypted)
                assert len(plaintext) == len(decrypted)
                assert plaintext == decrypted

                decontainer = cryptbase.cryptbase.CryptoContainer.from_encrypted(str(container), encryptor)
                assert decontainer.plaintext == plaintext
                assert decontainer.iv == iv_b64
                assert decontainer.ciphertext == cipher_b64


def test_container_init():
    try:
        cryptbase.cryptbase.CryptoContainer()
        assert False
    except ValueError:
        pass

    try:
        cryptbase.cryptbase.CryptoContainer(encryptor=None)
        assert False
    except ValueError:
        pass

    try:
        cryptbase.cryptbase.CryptoContainer(encryptor=None, plaintext=None)
        assert False
    except ValueError:
        pass

    class DummyEncryptor(cryptbase.cryptbase.Encryptor):
        def encrypt(self, plaintext):
            return None, None

        def decrypt(self, ct, iv):
            return None

    try:
        cryptbase.cryptbase.CryptoContainer(encryptor=DummyEncryptor(), plaintext=None)
        assert False
    except AttributeError:
        pass

    try:
        cryptbase.cryptbase.CryptoContainer(encryptor=None, ciphertext=None)
        assert False
    except ValueError:
        pass

    try:
        cryptbase.cryptbase.CryptoContainer(encryptor=None, iv=None)
        assert False
    except ValueError:
        pass

    try:
        cryptbase.cryptbase.CryptoContainer(encryptor=None, ciphertext=None, iv=None)
        assert False
    except ValueError:
        pass

    try:
        cryptbase.cryptbase.CryptoContainer(encryptor=DummyEncryptor(), ciphertext=None, iv=None)
        assert False
    except AttributeError:
        pass
