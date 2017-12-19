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

	def signString(self, prvkey, p_Str):
		pSign = (c_char*98)()
		pPrvkey = prvkey.encode('utf-8')
		pStr = p_Str.encode('utf-8')

		retcode = self.libc.SignString(pPrvkey, pStr, c_int(len(pStr)), pSign);
		return str(pSign.value, 'utf-8')

	def issSign(self, infoKey, infoVersion, state, content, notes, commitTime, prvkey):
		pSign = (c_char*98)()
		pInfoKey = infoKey.encode('utf-8')
		nInfoVersion = c_uint(infoVersion)
		nState = c_uint(state)
		pContent = content.encode('utf-8')
		pNotes = notes.encode('utf-8')
		pCommitTime = commitTime.encode('utf-8')
		pPrvkey = prvkey.encode('utf-8')

		retcode = self.libc.IssSign(pInfoKey, nInfoVersion, nState, pContent, pNotes, pCommitTime, pPrvkey, pSign)
		return str(pSign.value, 'utf-8')




