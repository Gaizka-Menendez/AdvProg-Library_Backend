import jwt # Jason Web Tokens

# HEADER:ALGORITHM & TOKEN TYPE
# {
#   "alg": "HS256",
#   "typ": "JWT"
# }
# PAYLOAD:DATA
# {
#   "sub": "1234567890",
#   "name": "Gaizka men",
#   "iat": 1516239022
# }


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, options={"verify_signature": False})

jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
            "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkdhaXprYSBtZW4iLCJpYXQiOjE1MTYyMzkwMjJ9." \
            "HgVY6GajeBkpY0DYMd48jn0PA9zeFqFMVFeJSGlL8xs"
            
payload = decode_jwt(jwt_token)
print("Contenido del JWT:")
print(payload)
for k, v in payload.items():
    print(f"K: {k} and V: {v}")