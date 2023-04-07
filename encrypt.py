import encryptANDdecrypt
import pathlib

if '__main__' == __name__:
    ead = encryptANDdecrypt.EAD()

    # if 'win' in platform.platform():
    priv = pathlib.Path('X:\\privkey.pem')
    # else:
        # priv = pathlib.Path('')

    while True:
        # print(priv.exists())

        if priv.exists():
            ead.load_keys(priv)
            print('loaded keys')
            break

    ead.encrypt(pathlib.Path('./target.pdf'), pathlib.Path('./target.encrypt.pdf'))
    # ead.decrypt(pathlib.Path('./target.encrypt.pdf'), pathlib.Path('./target.pdf'))

    pathlib.Path('./target.pdf').unlink()
