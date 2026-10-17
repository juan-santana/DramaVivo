import base64
import zlib
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

play_info = "h0HbcPDqIOzAZLYr38F3utURgLGe9pjy46kh9o/Iv1fnJJfo1Fipzxw4rwVVKMmtWtBjVhZgpcFrO9aOVDiij9HUCHkLRzpuqgaLPOTRjyS9AbU9+0Xp6tjDAzJ96M6bsgB71pKAulnWSwnKfvX4+7aw18AVVu+5wTDr6MvkxNMx2XGSyWzZ1HQu11xKRrZXSWMadwsmVc9leOUfauL1zf3xmqxeRdE8ghanLb/Q3fWoQNFPRVCkBNIkQdy0NgnRf4ulsge3L6kQpn14w2fZ1od1b8Ix3cHqpXPmY6uDKf4kXnHRxRn4uHqkF7CcV4KU2llWOM/zcldHH9EMDP1mQkQesETDlEKt0yFuYLSncM44Yuwp2x6DA65IparN3CROMgpjdt6ao9CON8BNP6gRedsdDylAUtbfhyPLKGBUycb+afib3aJ4fJusotFECCRIRSNVOiKWEMXP1ObTZcTqfIAi5YOoN1ldM8Bh+U/67rka34QpOKWbwP2gK5SNB3XccknGyRse9r0C2miAHhwuZe6/TUftHDgegs8+YNpsKL6dh0qy5AMNURCeLYFllb5HBG4h+G3pnZpUoCfLD6l+JDDqRW4iOHPworj+aXhfTmq+Zkaa5XsM3T6+9V2XL0w4zG0BxEFhamoTO8zQVvJypjJ3R4KLcmK3xkHUnonxWLFv888S/Htnzh+qS2LytFxy23/DkKpHe8Sy+3j7vglc4A=="

key = b"VvRSNGFynLBW7aCP"
iv = b"gLn8sxqpzyNjehDP"

encrypted_bytes = base64.b64decode(play_info)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
decrypted = decryptor.update(encrypted_bytes) + decryptor.finalize()

# Remove PKCS7 padding
pad_len = decrypted[-1]
if pad_len <= 16:
    decrypted = decrypted[:-pad_len]

# Base64 decode the decrypted string
zlib_data = base64.b64decode(decrypted)
result_json = zlib.decompress(zlib_data).decode("utf-8")

print("SUCCESS: REELSHORT VIDEO PAYLOAD DECRYPTED 100%!")
parsed = json.loads(result_json)
print(json.dumps(parsed, indent=2))
