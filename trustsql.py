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
		print(content)
		print('pContent: ' + json.dumps(json.loads(content)))
		pSign = (c_char*98)()
		pInfoKey = infoKey.encode('utf-8')
		nInfoVersion = c_uint(int(infoVersion))
		nState = c_uint(int(state))
		pContent = json.dumps(json.loads(content)).encode('utf-8')
		pNotes = json.dumps(json.loads(notes)).encode('utf-8')
		pCommitTime = commitTime.encode('utf-8')
		pPrvkey = prvkey.encode('utf-8')
		retcode = self.libc.IssSign(pInfoKey, nInfoVersion, nState, pContent, pNotes, pCommitTime, pPrvkey, pSign)
		print(pContent)
		return str(pSign.value, 'utf-8')


	def issVerifySign(self, infoKey, infoVersion, state, content, notes, commitTime, pubkey, sign):
		retcode = self.libc.IssVerifySign(infoKey.encode('utf-8'), c_uint(int(infoVersion)), c_uint(int(state)), content.encode('utf-8'), notes.encode('utf-8'), commitTime.encode('utf-8'), pubkey.encode('utf-8'), sign.encode('utf-8'))
		print(retcode)


	def iss_append(self, info_key, info_version, state, content, notes, commit_time, prvkey_key, public_key):
		url = self.host + '/trustsql_iss_append.cgi'
		sign = self.issSign(info_key, info_version, state, content, notes, commit_time, prvkey_key)
		print('sign: ' + sign)
		address = self.generateAddrByPubkey(public_key)

		self.issVerifySign(info_key, info_version, state, content, notes, commit_time, public_key, sign)

		print(type(content))
		print(type(json.loads(content)))

		mch_sign_string = str(address=address&commit_time=commit_time&content=json.loads(content)&info_key=info_key&info_version=int(info_version)&mch_id=self.mch_id&notes=json.loads(notes)&public_key=public_key&state=int(state)&sign=sign&sign_type=self.sign_type&version=self.version)
		print(mch_sign_string)
		mch_sign_result = self.signString(prvkey_key, mch_sign_string)
		print(mch_sign_result)


		data = {
			'version': self.version,
			'sign_type': self.sign_type,
			'mch_id': self.mch_id,
			'mch_sign': mch_sign_result,
			'info_key': info_key,
			'info_version': int(info_version),
			'state': int(state),
			'content': json.loads(content),
			'notes': json.loads(notes),
			'commit_time': commit_time,
			'address': address,
			'public_key': public_key,
			'sign': sign
		}

		print(data)

		r = requests.post(url, data=data)
		print(r.json())
		return r.json()








