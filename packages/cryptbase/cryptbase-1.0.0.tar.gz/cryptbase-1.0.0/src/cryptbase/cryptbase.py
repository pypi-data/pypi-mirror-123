import base64
import secrets
from abc import ABC
from abc import abstractmethod
from typing import Tuple

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


class Encryptor(ABC):
    """Abstract base class defining interface for encryptors."""

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> Tuple[bytes, bytes]:
        """Transform plaintext into a pair of ciphertext and IV."""
        pass

    @abstractmethod
    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        """Transform ciphertext and IV into plaintext."""
        pass


class AES256CTREncryptor(Encryptor):
    """Encryptor using AES with 256-bit long keys using CTR mode."""

    KEY_LENGTH = 32
    IV_LENGTH = 16

    def __init__(self, key: bytearray):
        if not isinstance(key, bytearray):
            raise ValueError()
        if not len(key) == AES256CTREncryptor.KEY_LENGTH:
            raise ValueError()
        self.__protect = bytearray(secrets.token_bytes(AES256CTREncryptor.KEY_LENGTH))
        self.__key = AES256CTREncryptor.__obfuscate(key, self.__protect)

    def __del__(self):
        self.clear()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.clear()

    def clear(self):
        if '_AES256CTREncryptor__key' in self.__dict__.keys():
            for i in range(len(self.__key)):
                self.__key[i] = 0
        if '_AES256CTREncryptor__protect' in self.__dict__.keys():
            for i in range(len(self.__protect)):
                self.__protect[i] = 0

    @staticmethod
    def __obfuscate(secret: bytearray, key: bytearray) -> bytearray:
        if not len(secret) == len(key):
            raise ValueError()
        result = bytearray(len(key))
        for i in range(len(secret)):
            result[i] = secret[i] ^ key[i]
        return result

    def encrypt(self, plaintext: bytes) -> Tuple[bytes, bytes]:
        iv = secrets.token_bytes(AES256CTREncryptor.IV_LENGTH)
        cipher = Cipher(algorithms.AES(AES256CTREncryptor.__obfuscate(self.__key, self.__protect)), modes.CTR(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return ciphertext, iv

    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(AES256CTREncryptor.__obfuscate(self.__key, self.__protect)), modes.CTR(iv))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()


class CryptoContainer:
    """
    CryptoContainer is providing unified interface to encryptors.
    Enter the encryptor instance and either plaintext string or
    ciphertext and iv bytes in constructor. Then access plaintext,
    ciphertext and IV strings in properties.
    Ciphertext and IV strings properties yield base64 encoded strings.
    Converting this container to string yields a concatenation of
    ciphertext and IV in a single string. Calling from_encrypted
    static method will construct CryptoContainer from such concatenation,
    allowing access to plaintext.
    """

    def __init__(self, **kwargs):
        if 'encryptor' not in kwargs:
            raise ValueError()
        if not isinstance(kwargs['encryptor'], Encryptor):
            raise ValueError(type(kwargs['encryptor']))

        if 'plaintext' in kwargs:
            self.__plaintext = kwargs['plaintext']
            self.__ciphertext, self.__iv = kwargs['encryptor'].encrypt(self.__plaintext.encode('utf-8'))
        elif 'ciphertext' in kwargs and 'iv' in kwargs:
            self.__ciphertext = kwargs['ciphertext']
            self.__iv = kwargs['iv']
            self.__plaintext = kwargs['encryptor'].decrypt(self.__ciphertext, self.__iv).decode('utf-8')
        else:
            raise ValueError()

    @property
    def plaintext(self) -> str:
        """Provide plaintext."""
        return self.__plaintext

    @property
    def ciphertext(self) -> str:
        """Provide base64 encoded ciphertext as string."""
        return base64.b64encode(self.__ciphertext).decode('ascii')

    @property
    def iv(self) -> str:
        """Provide base64 encoded IV as string."""
        return base64.b64encode(self.__iv).decode('ascii')

    def __str__(self):
        """Concatenate ciphertext and IV to store in the database."""
        return '@'.join([self.ciphertext, self.iv])

    @staticmethod
    def from_encrypted(container_str: str, encryptor: Encryptor):
        """
        Builds a CryptoContainer from a string as provided by __str__,
        allowing access to plaintext.
        """
        ciphertext, iv = container_str.split('@')
        return CryptoContainer(ciphertext=base64.b64decode(ciphertext),
                               iv=base64.b64decode(iv),
                               encryptor=encryptor)
