from api.sdk.oss import *
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'Accept': '*/*',
}
URL='https://sm-breeze-public.oss-cn-shenzhen.aliyuncs.com/source%2Fadmin%2F1%2F0%2F3.jpg?OSSAccessKeyId=LTAIAVwi7Mh67lZm&Expires=1556518082&Signature=eLi6meds8vpKHWMuiWX2lP5UkME%3D'
LOCAL_URL='http://127.0.0.1:8000/api/v1/source/upload'
def put_file_to_oss(url,filename):
    with open(filename,'rb') as f:
        res=requests.put(url,f,headers=headers)
        print(res.status_code)
def post_filr_to_local(url,filename):
    with open(filename,'rb') as f:
        #请求头 文件上传形式 Content-Type: multipart/form-data
        res=requests.post(url,files={'file': f},headers=headers)
        print(res.status_code,res.text)
if __name__=='__main__':
    i=2
    if i==1:
        put_file_to_oss(url=URL,filename='./static/3.jpg')
    elif i==2:
        post_filr_to_local(url=LOCAL_URL, filename='./static/4.zip')
