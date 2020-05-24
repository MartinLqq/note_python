import hashlib
import os

from itsdangerous import URLSafeTimedSerializer


secret_key = 'something secret'
csrf_token = hashlib.sha1(os.urandom(64)).hexdigest()
print(csrf_token)
# 如: afa9a053a92c5add6b9686ab6632c8bf1c309549

s = URLSafeTimedSerializer(secret_key, salt='wtf-csrf-token')
token = s.dumps(csrf_token, salt=None)
print(token)
# 如: ImFmYTlhMDUzYTkyYzVhZGQ2Yjk2ODZhYjY2MzJjOGJmMWMzMDk1NDki.EVS9HA.18B7tM5HEUao-CDxRvStrtZx_1w
