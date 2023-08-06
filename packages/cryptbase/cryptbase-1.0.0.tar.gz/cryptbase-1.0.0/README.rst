========
Overview
========

Protect yourself and your customers with database encryption.

* Free software: MIT license

Installation
============

    pip install cryptbase


Usage
============

You can use cryptbase with django ORM or with SQLAlchemy.

To use with SQLAlchemy:

    from cryptbase import EncryptedText
    sensitive = Column(EncryptedText(key=DB_KEY))

To use with django:

    from cryptbase import EncryptedTextField
    sensitive = EncryptedTextField(key=DB_KEY)

DB_KEY is 32 bytes encryption key as hex encoded string. Fields behave as TEXT fields, data are transparently encrypted
when storing into the database and decrypted on retrieval.


Development
===========

To run all the tests run::

    tox
