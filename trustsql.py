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
		print(content)

		ppInfoKey = create_string_buffer(c_char*(len(infoKey)+1))
		ppInfoKey.value = infoKey.encode('utf-8')

		ppContent = create_string_buffer(c_char*(len(json.dumps(json.loads(content))) + 1))
		ppContent.value = json.dumps(json.loads(content)).encode('utf-8')

		ppNotes = create_string_buffer(c_char*(len(json.dumps(json.loads(notes))) + 1))
		ppNotes.value = json.dumps(json.loads(notes)).encode('utf-8')

		ppCommitTime = create_string_buffer(c_char*(len(commitTime) + 1))
		ppCommitTime.value = commitTime.encode('utf-8')

		pSign = (c_char*98)()
		pInfoKey = ppInfoKey
		nInfoVersion = c_uint(int(infoVersion))
		nState = c_uint(int(state))
		pContent = ppContent
		pNotes = ppNotes
		pCommitTime = ppCommitTime
		pPrvkey = prvkey.encode('utf-8')
		retcode = self.libc.IssSign(pInfoKey, nInfoVersion, nState, pContent, pNotes, pCommitTime, pPrvkey, pSign)

		return str(pSign.value, 'utf-8')


	def issVerifySign(self, infoKey, infoVersion, state, content, notes, commitTime, pubkey, sign):
		retcode = self.libc.IssVerifySign(infoKey.encode('utf-8'), c_uint(int(infoVersion)), c_uint(int(state)), content.encode('utf-8'), notes.encode('utf-8'), commitTime.encode('utf-8'), pubkey.encode('utf-8'), sign.encode('utf-8'))
		print(retcode)


	def iss_append(self, info_key, info_version, state, content, notes, commit_time, prvkey_key, public_key):
		url = self.host + '/trustsql_iss_append.cgi'
		sign = self.issSign(info_key, info_version, state, content, notes, commit_time, prvkey_key)
		print('sign: ' + sign)
		address = self.generateAddrByPubkey(public_key)


		data = {
			"address": address,
			"commit_time": commit_time,
			"content": json.dumps(json.loads(content)),
			"info_key": info_key,
			"info_version": info_version,
			"mch_id": self.mch_id,
			"notes": json.dumps(json.loads(notes)),
			"public_key": public_key,
			"sign": sign,
			"sign_type": self.sign_type,
			"state": state,
			"version": self.version
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
		address = self.generateAddrByPubkey(self.mch_pubkey)

		timestamp = int(time.time())
		data = {
			'address': address,
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

		post_data = {
			'address': address,
			'mch_id': self.mch_id,
			'sign_type': self.sign_type,
			'timestamp': str(timestamp),
			'version': self.version,
			'mch_sign': mch_sign_result
		}

		r = requests.post(url, data=post_data)
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







