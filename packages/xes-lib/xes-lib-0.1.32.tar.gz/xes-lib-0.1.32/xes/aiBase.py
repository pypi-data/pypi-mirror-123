"""
编程ai接口通用请求模块
"""
import requests
from xes import common, uploader

"""
通用请求接口
参数:
  api - string，接口地址
  params - dictionary，参数字典
返回值:
  结果字典
异常:
  服务异常等错误信息
"""
def request(api, params):
    cookies = common.getCookies()
    headers = {"Cookie": cookies}
    rep = requests.get(api, params=params, headers=headers)
    repDic = common.jsonLoads(rep.text)
    if repDic is None:
        raise Exception("服务异常,请稍后再试")
    if repDic["stat"] != 1:
        raise Exception(repDic["msg"])
    if repDic["data"]["err"] != 0:
        raise Exception(repDic["data"]["msg"])
    return repDic["data"]["res"]

"""
文件上传
参数:
  fileName - string，文件名，例如"abc.png"
返回值:
  结果字典
异常:
  文件不存在
"""
def upload(fileName):
    return uploader.XesUploader().upload(fileName)