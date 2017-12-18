from ctypes import *

class Trustsql(object):
	"""docstring for Trustsql"""
	def __init__(self, arg):
		libc = cdll.LoadLibrary('../TrustSQL_SDK_V1.1.so')

	def generatePairkey():
		pPrvkey = c_byte('')
		pPubkey = c_byte('')

		retcode = self.libc.generatePairkey(pPrvkey, pPubkey)

		return pPrvkey.value, pPubkey.value


