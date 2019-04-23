from api.sdk.oss import *
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'Accept': '*/*',
}
URL='https://sm-breeze-public.oss-cn-shenzhen.aliyuncs.com/source%2Fadmin%2F1%2F0%2F7.jpg?OSSAccessKeyId=LTAIAVwi7Mh67lZm&Expires=1556028740&Signature=tm9UEDayWYTmRD695WN39ZA51C0%3D'
def put_file_to_oss(url,filename):
    with open(filename,'rb') as f:
        res=requests.put(url,f,headers=headers)
        print(res.status_code)
if __name__=='__main__':
    i=1
    if i==1:
        put_file_to_oss(url=URL,filename='./static/1.jpg')
    else:
        pass