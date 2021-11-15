import requests
from datetime import date, timedelta
url = "http://aes.cryptohack.org/flipping_cookie/"

def strxor(a, b):     
    if len(a) > len(b):
       return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
       return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def get_cookies():
	r = requests.get(url+'get_cookie/')
	a = r.json()
	iv = a['cookie'].decode('hex')[:16]
	ciphertext = a['cookie'].decode('hex')[16:]
	return iv, ciphertext

def check(cookie, iv):
	r = requests.get(url+'check_admin/'+cookie+'/'+iv+'/')
	a = r.json()
	return a['flag']




expires_at = (date.today() + timedelta(days=1)).strftime("%s")
cookie = "admin=False;expiry="+expires_at
crib = "\x00\x00\x00\x00\x00\x00False;expiry="+expires_at
deletion = '\x00\x00\x00\x00\x00\x00True;expiry='+expires_at

xor_with_iv = strxor(crib, deletion)
iv, cipher = get_cookies()
new_iv = strxor(iv, xor_with_iv)

print check(cipher.encode('hex'), new_iv.encode('hex'))