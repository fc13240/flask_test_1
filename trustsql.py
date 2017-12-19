from ctypes import *

class Trustsql(object):
	"""docstring for Trustsql"""
	def __init__(self):
		self.libc = cdll.LoadLibrary('../TrustSQL_SDK_V1.1.so')
		self.getErrorStr = self.libc.GetErrorStr()

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
		nLen = c_int()

		print(prvkey)
		print(pStr)

		retcode = self.libc.SignString(prvkey, pStr, nLen, pSign);
		print(self.getErrorStr)
		print(str(pSign.value, 'utf-8'))
		return str(pSign.value, 'utf-8')


