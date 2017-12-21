from ctypes import *
import requests
import json
import time

class Trustsql(object):
	"""docstring for Trustsql"""
	def __init__(self):
		self.libc = cdll.LoadLibrary('../TrustSQL_SDK_V1.1.so')
		self.host = 'https://open.trustsql.qq.com/cgi-bin/v1.0'

		self.version = "1.0"
		self.sign_type = "ECDSA"
		self.mch_id = "gb8061f6b549ddc4f"
		self.mch_sign = "MEQCIHTM2q87F9PTUeSdZzNAN39eLwBaDKuPPnEdcHzizpTCAiBHn8pb+zasMGvcF/6qbJrG+1J1+bC+ilfnkZqwZmECwg=="
		self.mch_prvkey = "oe0xdfkch4a1VXaGH4VUmS+taXlj3gyvqUfbPl6tQ00="
		self.mch_pubkey = "BGCuRRVFPK8XGU6EVDxvALjKnjm/uURkZv9jV7q3aJYQqANoOHWhvd4HyE4e5ju74DXI4ZopcvoJUn/E52hujPo="
		self.mch_address = "15kcSqCvrpEbrAgqDjPuW5mdSHULzvYNUD"

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
		# ppInfoKey = create_string_buffer(len(infoKey)+1)
		# ppInfoKey.value = infoKey.encode()

		# ppContent = create_string_buffer(len(json.dumps(eval(content))) + 1)
		# ppContent.value = json.dumps(eval(content)).encode()

		# ppNotes = create_string_buffer(len(json.dumps(eval(notes))) + 1)
		# ppNotes.value = json.dumps(eval(notes)).encode()

		# ppCommitTime = create_string_buffer(len(commitTime) + 1)
		# ppCommitTime.value = commitTime.encode()
		# print(ppCommitTime.raw)

		# pSign = (c_char*98)()
		# pInfoKey = ppInfoKey
		# nInfoVersion = c_uint(int(infoVersion))
		# nState = c_uint(int(state))
		# pContent = ppContent
		# pNotes = ppNotes
		# pCommitTime = ppCommitTime
		# pPrvkey = prvkey.encode()

		pSign = (c_char*98)()
		pInfoKey = c_char_p(infoKey.encode())
		nInfoVersion = c_uint(int(infoVersion))
		nState = c_uint(int(state))
		pContent = c_char_p(json.dumps(eval(content)).encode())
		pNotes = c_char_p(json.dumps(eval(notes)).encode())
		pCommitTime = c_char_p(commitTime.encode())
		pPrvkey = c_char_p(prvkey.encode())

		retcode = self.libc.IssSign(pInfoKey, nInfoVersion, nState, pContent, pNotes, pCommitTime, pPrvkey, pSign)

		return str(pSign.value, 'utf-8')


	def issVerifySign(self, infoKey, infoVersion, state, content, notes, commitTime, pubkey, sign):
		pInfoKey = c_char_p(infoKey.encode())
		nInfoVersion = c_uint(int(infoVersion))
		nState = c_uint(int(state))
		pContent = c_char_p(json.dumps(eval(content)).encode())
		pNotes = c_char_p(json.dumps(eval(notes)).encode())
		pCommitTime = c_char_p(commitTime.encode())
		pPubkey = c_char_p(pubkey.encode())
		pSign = c_char_p(sign.encode())
		retcode = self.libc.IssVerifySign(pInfoKey, nInfoVersion, nState, pContent, pNotes, pCommitTime, pPubkey, pSign)
		print('---------retcode----------')
		print(retcode)


	def iss_append(self, info_key, info_version, state, content, notes, commit_time, prvkey_key, public_key):
		url = self.host + '/trustsql_iss_append.cgi'
		sign = self.issSign(info_key, info_version, state, content, notes, commit_time, prvkey_key)
		print('sign: ' + sign)

		self.issVerifySign(info_key, info_version, state, content, notes, commit_time, public_key, sign)

		address = self.generateAddrByPubkey(public_key)

		data = {
			'address': address,
			'commit_time': commit_time,
			'content': json.dumps(eval(content)),
			'info_key': info_key,
			'info_version': info_version,
			'mch_id': self.mch_id,
			'notes': json.dumps(eval(notes)),
			'public_key': public_key,
			'sign': sign,
			'sign_type': self.sign_type,
			'state': state,
			'version': self.version
		}

		mch_sign_string = ""
		for k, v in data.items():
			if k == "version":
				mch_sign_string += k + '=' + v
			else:
				mch_sign_string += k + '=' + v + '&'


		print(mch_sign_string)
		mch_sign_result = self.signString(self.mch_prvkey, mch_sign_string)
		data['mch_sign'] = mch_sign_result

		print(data)
		print(type(data))


		r = requests.post(url, data=data)
		print(r.json())
		return r.json()


	def iss_query(self, info_key, info_version, state, content, notes, range, address, t_hash, page_no, page_limit, prvkey_key, public_key):
		url = self.host + '/trustsql_iss_query.cgi'
		address = self.generateAddrByPubkey(public_key)

		timestamp = int(time.time())
		data = {
			'address': address,
			'content': json.dumps(eval(content)),
			'mch_id': self.mch_id,
			'sign_type': self.sign_type,
			'timestamp': str(timestamp),
			'version': self.version
		}

		mch_sign_string = ''
		for k, v in data.items():
			if k == 'version':
				mch_sign_string += k + '=' + v
			else:
				mch_sign_string += k + '=' + v + '&'

		mch_sign_result = self.signString(self.mch_prvkey, mch_sign_string)
		data['mch_sign'] = mch_sign_result

		r = requests.post(url, data=data)
		print(r.json())
		return r.json()


	def user_register(self, user_id, public_key, user_fullName):
		print(user_id)
		print(public_key)
		print(user_fullName)
		url = 'https://open.trustsql.qq.com' + '/api/user_cert/register'
		data = {
			'user_id': user_id,
			'public_key': public_key,
			'user_fullName': user_fullName
		}

		r = requests.post(url, data=data)
		print(r.status_code)
		print(r.content)
		print(r.text)
		print(r.json())
		return r.json()







