# pyCryptoFile

pyCryptoFile contains some functions to encrypt/decrypt using ssh keys.

[The source for this project is available here][src].

---

pyCryptoFile module can be called in command line : python3 pyCryptoFile.py -h

    usage: pyCryptoFile.py [-h] [-V] [-f FILE] [-m {encrypt,decrypt}] [-k KEYFILE]

    pyCryptoFile is a python3 program that encrypts, decrypts using ssh key encryption

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pyCryptoFile
    -f FILE, --file FILE  file to encrypt/decrypt
    -m {encrypt,decrypt}, --mode {encrypt,decrypt}
                            encrypt/decrypt mode
    -k KEYFILE, --keyfile KEYFILE
                            public key file if encrypt mode or private key file if decrypt mode

example to encrypt a file content and put in another file :

    python3 pyCryptoFile.py -f mytext2.txt -k ~/.ssh/id_rsa.pub > mytextcrypted.txt

example to decrypt a file content and put in another file :

    python3 pyCryptoFile.py -f mytextcrypted.txt -k ~/.ssh/id_rsa -m decrypt > mydecrypted.txt

---

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/stormalf/file_transfer
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional

# release notes

1.0.7 fix on pyCryptoFile function wrong tab before return encoded and also fixing the bytes to crypt and encrypt to 128 and 344.
