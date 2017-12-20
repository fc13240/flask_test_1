from ctypes import *
import requests
import json

class Trustsql(object):
	"""docstring for Trustsql"""
	def __init__(self):
		self.libc = cdll.LoadLibrary('../TrustSQL_SDK_V1.1.so')
		self.host = 'https://open.trustsql.qq.com/cgi-bin/v1.0'

		self.version = '1.0'
		self.sign_type = 'ECDSA'
		self.mch_id = 'gb8061f6b549ddc4f'
		self.mch_sign = 'MEQCIHTM2q87F9PTUeSdZzNAN39eLwBaDKuPPnEdcHzizpTCAiBHn8pb+zasMGvcF/6qbJrG+1J1+bC+ilfnkZqwZmECwg=='
		self.mch_prvkey = 'oe0xdfkch4a1VXaGH4VUmS+taXlj3gyvqUfbPl6tQ00='
		self.mch_pubkey = 'BGCuRRVFPK8XGU6EVDxvALjKnjm/uURkZv9jV7q3aJYQqANoOHWhvd4HyE4e5ju74DXI4ZopcvoJUn/E52hujPo='
		self.mch_address = '15kcSqCvrpEbrAgqDjPuW5mdSHULzvYNUD'

	def generatePairkey(self):
		pPrvkey = (c_char*45)()
		pPubkey = (c_char*90)()

		retcode = self.libc.GeneratePairkey(pPrvkey, pPubkey)
		return (str(pPrvkey.value, 'utf-8'), str(pPubkey.value, 'utf-8'))

	def generatePubkeyByPrvkey(self, pPrvkey):
		pPubkey = (c_char*90)()

		retcode = self.libc.GeneratePubkeyByPrvkey(pPrvkey, pPubkey)
		return str(pPubkey.value, 'utf-8')


	def generateAddrByPubkey(self, pPubkey):
		pAddr = (c_char*35)()
		retcode = self.libc.GenerateAddrByPubkey(pPubkey, pAddr)

		return str(pAddr.value, 'utf-8')


	def signString(self, prvkey, p_Str):
		pSign = (c_char*98)()
		pPrvkey = prvkey.encode('utf-8')
		pStr = p_Str.encode('utf-8')
		retcode = self.libc.SignString(pPrvkey, pStr, c_int(len(pStr)), pSign)

		return str(pSign.value, 'utf-8')

	def verifySign(self, pPubkey, pStr, pSign):
		retcode = self.libc.VerifySign(pPubkey.encode('utf-8'), pStr.encode('utf-8'), c_int(len(pStr)), pSign.encode('utf-8'))

		print(retcode)


	def issSign(self, infoKey, infoVersion, state, content, notes, commitTime, prvkey):
		pSign = (c_char*98)()
		pInfoKey = infoKey.encode('utf-8')
		nInfoVersion = c_uint(int(infoVersion))
		nState = c_uint(int(state))
		pContent = json.dumps(json.loads(content)).encode('utf-8')
		pNotes = json.dumps(json.loads(notes)).encode('utf-8')
		pCommitTime = commitTime.encode('utf-8')
		pPrvkey = prvkey.encode('utf-8')
		retcode = self.libc.IssSign(pInfoKey, nInfoVersion, nState, pContent, pNotes, pCommitTime, pPrvkey, pSign)

		return str(pSign.value, 'utf-8')


	def iss_append(self, info_key, info_version, state, content, notes, commit_time, prvkey_key, public_key):
		url = self.host + '/trustsql_iss_append.cgi'
		sign = self.issSign(info_key, info_version, state, content, notes, commit_time, self.mch_prvkey)
		print('sign: ' + sign)
		# address = self.generateAddrByPubkey(public_key)

		print(type(content))
		print(type(json.loads(content)))

		data = {
			'version': self.version,
			'sign_type': self.sign_type,
			'mch_id': self.mch_id,
			'mch_sign': self.mch_sign,
			'info_key': info_key,
			'info_version': info_version,
			'state': state,
			'content': json.loads(content),
			'notes': json.loads(notes),
			'commit_time': commit_time,
			'address': self.mch_address,
			'public_key': self.mch_pubkey,
			'sign': sign
		}

		print(data)

		r = requests.post(url, data=data)
		print(r.json())
		return r.json()








