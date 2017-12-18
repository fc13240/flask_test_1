from ctypes import *

class Trustsql(object):
	"""docstring for Trustsql"""
	def __init__(self, arg):
		self.libc = cdll.LoadLibrary('../TrustSQL_SDK_V1.1.so')

	def generatePairkey():
		pPrvkey = (c_byte*45)()
		pPubkey = (c_byte*90)()

		retcode = self.libc.generatePairkey(pPrvkey, pPubkey)

		return pPrvkey.value, pPubkey.value


