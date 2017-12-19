from ctypes import *
from sys import getsizeof

class Trustsql(object):
	"""docstring for Trustsql"""
	def __init__(self):
		self.libc = cdll.LoadLibrary('../TrustSQL_SDK_V1.1.so')

	def generatePairkey(self):
		pPrvkey = (c_char*45)()
		pPubkey = (c_char*90)()

		retcode = self.libc.GeneratePairkey(pPrvkey, pPubkey)
		return (str(pPrvkey.value, 'utf-8'), str(pPubkey.value, 'utf-8'))

	def generatePubkeyByPrvkey(self, pPrvkey):
		pPubkey = (c_char*90)()

		retcode = self.libc.GeneratePubkeyByPrvkey(pPrvkey, pPubkey)
		return str(pPubkey.value, 'utf-8')

	def signString(self, prvkey, pStr):
		pSign = (c_char*98)()

		print(prvkey)
		print(pStr)

		print(pStr.encode('utf-8'))
		print(len(pStr))

		retcode = self.libc.SignString(prvkey, pStr, getsizeof(pStr.encode('utf-8'))-1, pSign);
		print(pSign)
		print(str(pSign.value, 'utf-8'))
		return str(pSign.value, 'utf-8')


