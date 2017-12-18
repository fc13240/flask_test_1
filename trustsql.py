from ctypes import *

class Trustsql(object):
	"""docstring for Trustsql"""
	def __init__(self):
		self.libc = cdll.LoadLibrary('../TrustSQL_SDK_V1.1.so')

	def generatePairkey(self):
		pPrvkey = (c_byte*45)()
		pPubkey = (c_byte*90)()

		retcode = self.libc.GeneratePairkey(pPrvkey, pPubkey)
		print(pPrvkey.value, pPubkey.value)
		keys = {"prvkey": pPrvkey.value, "pubkey": pPubkey.value}
		return keys


