__version__ = '1.0.0'

import gc

from .cryptbase import AES256CTREncryptor
from .cryptbase import CryptoContainer

try:
    from django.db import models

    class EncryptedTextField(models.TextField):
        """
        Django model field to provide database encryption using AES-256-CTR.
        Simply replace existing TextField with EncryptedTextField and add
        hex encoded 256-bit long encryption key to use. In code, you can
        read and write the data with no further changes. However, in the
        underlying database they will be encrypted.

        Make sure to migrate the data appropriately.
        """
        description = 'Encrypted data'

        def __init__(self, *args, **kwargs):
            if 'key' in kwargs:
                self.encryptor = AES256CTREncryptor(bytearray.fromhex(kwargs['key']))
                del kwargs['key']
                gc.collect()
            super().__init__(*args, **kwargs)

        def get_db_prep_value(self, value, *args, **kwargs):
            if value is None:
                return None
            return str(CryptoContainer(plaintext=value, encryptor=self.encryptor))

        def from_db_value(self, value, expression, connection):
            if value is None:
                return value
            return CryptoContainer.from_encrypted(value, self.encryptor).plaintext

        def to_python(self, value):
            if isinstance(value, str):
                return CryptoContainer.from_encrypted(value, self.encryptor).plaintext
            return None

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            return name, path, args, kwargs
except ImportError:
    pass


try:
    from sqlalchemy import types

    class EncryptedText(types.TypeDecorator):
        """
        SQLAlchemy model field to provide database encryption using AES-256-CTR.
        Simply replace existing TEXT field with EncryptedText field and add
        hex encoded 256-bit long encryption key to use. In code, you can
        read and write the data with no further changes. However, in the
        underlying database they will be encrypted.

        Make sure to migrate the data appropriately.
        """
        impl = types.TEXT

        def __init__(self, *args, **kwargs):
            self.encryptor = AES256CTREncryptor(bytearray.fromhex(kwargs['key']))
            del kwargs['key']
            gc.collect()
            super().__init__(*args, **kwargs)

        def process_bind_param(self, value, dialect):
            return str(CryptoContainer(plaintext=value, encryptor=self.encryptor))

        def process_result_value(self, value, dialect):
            return CryptoContainer.from_encrypted(value, self.encryptor).plaintext
except ImportError:
    pass
