import rsa
import pathlib

# (pubkey, privkey) = rsa.newkeys(4096, poolsize=12)

# # 保存公钥到文件
# with open('pubkey.pem', 'wb') as f:
#     f.write(pubkey._save_pkcs1_pem())
# # 保存私钥到文件
# with open('privkey.pem', 'wb') as f:
#     f.write(privkey._save_pkcs1_pem())

class EAD:
    def __init__(self) -> None:
        self.pubkey = None
        self.privkey = None

    def load_keys(self, priv: pathlib.Path):
        with open('pubkey.pem', 'rb') as f:
            self.pubkey = rsa.PublicKey._load_pkcs1_pem(f.read())

        with open(priv, 'rb') as f:
            self.privkey = rsa.PrivateKey._load_pkcs1_pem(f.read())

    def encrypt(self, filename: pathlib.Path, output: pathlib.Path):
        with open(filename, 'rb') as f:
            data = f.read()

        # 分块大小为公钥长度减去11，参考https://stackoverflow.com/questions/49677614/overflow-exception-when-encrypting-message-with-python-rsa
        chunk_size = self.pubkey.n.bit_length() // 8 - 11
        # 将数据分块
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        # 对每个块进行加密，并将加密后的数据拼接起来
        crypted_data = b''.join([rsa.encrypt(chunk, self.pubkey) for chunk in chunks])

        with open(output, 'wb') as f:
            f.write(crypted_data)

    def decrypt(self, filename: pathlib.Path, output: pathlib.Path):
        with open(filename, 'rb') as f:
            crypted_data = f.read()

        # 分块大小为私钥长度
        chunk_size = self.privkey.n.bit_length() // 8
        # 将数据分块
        chunks = [crypted_data[i:i+chunk_size] for i in range(0, len(crypted_data), chunk_size)]
        # 对每个块进行解密，并将解密后的数据拼接起来
        data = b''.join([rsa.decrypt(chunk, self.privkey) for chunk in chunks])

        with open(output, 'wb') as f:
            f.write(data)

# encrypt(pathlib.Path('./test.pdf'), pathlib.Path('./target.encrypt.pdf'))
# decrypt(pathlib.Path('./en.pdf'), pathlib.Path('./test2.pdf'))
