from api.sdk.oss import *
import requests
URL='http://sm-breeze-01.oss-cn-shenzhen.aliyuncs.com/source%2Fadmin%2F0%2F1%2F11.jpg?OSSAccessKeyId=LTAIAVwi7Mh67lZm&Expires=1555855789&Signature=ed78di5LplMmNfw6k6j5KPrs%2B0c%3D'
def put_file_to_oss(url,filename):
    with open(filename,'rb') as f:
        res=requests.put(url,f)
        print(res.status_code)
if __name__=='__main__':
    i=1
    if i==1:
        put_file_to_oss(url=URL,filename='./static/1.jpg')
    else:
        pass