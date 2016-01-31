import requests
import imghdr
import os
import json
import sys
import tempfile

def split_cookie(string):
	cookie_list = string.split(';')
	for i in range(0,len(cookie_list)):
		if cookie_list[i].find('M_WEIBOCN_PARAMS')!=-1:
			break
	part_b = cookie_list.pop(i)+';'
	cookie_list.append(' ')
	part_a = ';'.join(cookie_list)
	return part_a,part_b

def getCookie(M_WEIBOCN_PARAMS=None):
	if M_WEIBOCN_PARAMS == None:
		try:
			respon = requests.get('http://127.0.0.1:8765/WeiboCookie')
		except:
			print 'Server not running.'
			sys.exit(0)
		part_a,part_b = split_cookie(respon.content)
		return part_a + part_b
	else:
		try:
			respon = requests.get('http://127.0.0.1:8765/WeiboCookie')
		except:
			print 'Server not running.'
			sys.exit(0)
		part_a,part_b = split_cookie(respon.content)
		return part_a + M_WEIBOCN_PARAMS


def GetPicType(File):
	#,SysPath_Temp='%temp%'
	#Temp=FileHandle.read()
	#FileHandle_0=tempfile.NamedTemporaryFile()#open('.temppic','wb')
	#FileHandle_0.write(Temp)
	#FileHandle_0.close()
	Type=imghdr.what(File)
	#FileHandle_0.close()
	#os.system('rm -rf .temppic')
	#os.system('del .temppic')
	if Type!=None:
		return Type
	else:
		return 'None'

Cookie=getCookie()

Head={
	'Host': 'm.weibo.cn',
	'Connection': 'Keep-Alive',
	#'Content-Length': '1112036',
	#'Accept-Encoding': None,
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Origin': 'http://m.weibo.cn',
	'X-Requested-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
	#'Content-Type': 'multipart/form-data',# boundary=----WebKitFormBoundary'+Boundary,
	'DNT': '1',
	'Referer': 'http://m.weibo.cn/mblog',
	'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
	'Cookie': Cookie
}

def reload_cookie():
	r = requests.get('http://m.weibo.cn/',headers=Head)
	string = ''
	for i in requests.utils.dict_from_cookiejar(r.cookies):
		string+=i
		string+='='
		string+=requests.utils.dict_from_cookiejar(r.cookies)[i]
	return string

def Upload(Path):
	new_part_b = reload_cookie()
	global Head
	Head['Cookie'] = getCookie(M_WEIBOCN_PARAMS=new_part_b)
	Path=list(Path)
	FileName=Path[1]
	if Path[0]=='':
		Path[0]='.'
	Path='/'.join(Path)
	if os.path.getsize(Path)/1000/1000 > 5:
		print 'Warning: file size large than 5MB, server will return nothing.'
	Respon=requests.post('http://m.weibo.cn/mblogDeal/addPic',headers=Head,data={'type':'json'},files={'pic':(FileName,open(Path,'rb'),'image/'+GetPicType(Path))})
	JSON=json.loads(Respon.content)
	if JSON['ok']==1:
		os.system('echo '+JSON['pic_url'].replace('thumbnail','large')+' | clip')
		print 'SUCCESS',JSON['pic_url'].replace('thumbnail','large')
		return JSON['pic_url'].replace('thumbnail','large')
	else:
		print 'Maybe there is an error.\nok: '+str(JSON['ok'])+'\nUrl: '+str(JSON['pic_url'])+'\nmsg: '+JSON['msg']
		return 'ERROR',''

if __name__=='__main__':
	if len(sys.argv)==1:
		print 'Error: no file input.\nPlease use '+os.path.split(sys.argv[0])[-1]+' [PictureFile].'
	else:
		Folder = 'WeiboPic'
		try:
			Folder = sys.argv[2]
		except:
			pass
		if sys.argv[1]=='-f':
			for f in os.listdir('WeiboPic'):
				Upload(os.path.split('WeiboPic\\'+f))
			raw_input()
		else:
			Upload(os.path.split(sys.argv[1]))
			raw_input()