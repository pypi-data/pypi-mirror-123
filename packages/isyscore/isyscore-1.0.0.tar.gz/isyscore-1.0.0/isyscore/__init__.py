import requests
import json


class LicenseCustomer(object):
    enterpriseName: str = ""
    contactEmail: str = ""
    contactName: str = ""
    contactPhone: str = ""


class LicenseData(object):
    licenseCode: str = ""
    customer: LicenseCustomer = None

    @staticmethod
    def fromJson(jsonstr: str):   # LicenseData
        lic = LicenseData()
        try:
            jobj = json.loads(jsonstr)
            lic.licenseCode = jobj['license_code']
            lic.customer = LicenseCustomer()
            lic.customer.enterpriseName = jobj['customer']['enterprise_name']
            lic.customer.contactEmail = jobj['customer']['contact_email']
            lic.customer.contactName = jobj['customer']['contact_name']
            lic.customer.contactPhone = jobj['customer']['contact_phone']
        except json.decoder.JSONDecodeError:
            return None
        except KeyError:
            return None
        else:
            pass
        return lic


class ComponentRegister(object):
    name: str = ""
    showName: str = ""
    description: str = ""
    versionCode: int = 1
    versionName: str = "1.0"
    isOpenSource: int = 0
    isEnabled: int = 1
    isUnderCarriage: int = 0
    compactOsVersion: str = "*"
    producerCompany: str = ""
    producerContact: str = ""
    producerEmail: str = ""
    producerPhone: str = ""
    producerUrl: str = ""


class ResultComponentRegister(object):
    code: int = 0
    message: str = ""
    data: ComponentRegister = None

    @staticmethod
    def fromJson(jsonstr: str):
        r = ResultComponentRegister()
        try:
            jobj = json.loads(jsonstr)
            r.code = jobj['code']
            r.message = jobj['message']
            r.data = ComponentRegister()
            r.data.name = jobj['data']['name']
            r.data.showName = jobj['data']['showName']
            r.data.description = jobj['data']['description']
            r.data.versionCode = jobj['data']['versionCode']
            r.data.versionName = jobj['data']['versionName']
            r.data.isOpenSource = jobj['data']['isOpenSource']
            r.data.isEnabled = jobj['data']['isEnabled']
            r.data.isUnderCarriage = jobj['data']['isUnderCarriage']
            r.data.compactOsVersion = jobj['data']['compactOsVersion']
            r.data.producerCompany = jobj['data']['producerCompany']
            r.data.producerContact = jobj['data']['producerContact']
            r.data.producerEmail = jobj['data']['producerEmail']
            r.data.producerPhone = jobj['data']['producerPhone']
            r.data.producerUrl = jobj['data']['producerUrl']
        except json.decoder.JSONDecodeError:
            return None
        except KeyError:
            return None
        else:
            pass
        return r


class ComponentLicensed(object):
    isRevoked: int = 0
    isTrial: int = 0
    trialStartDate: int = 0
    trialEndDate: int = 0


class ResultComponentLicensed(object):
    code: int = 0
    message: str = ""
    data: ComponentLicensed = None

    @staticmethod
    def fromJson(jsonstr: str):
        r = ResultComponentLicensed()
        try:
            jobj = json.loads(jsonstr)
            r.code = jobj['code']
            r.message = jobj['message']
            r.data = ComponentLicensed()
            r.data.isRevoked = jobj['data']['isRevoked']
            r.data.isTrial = jobj['data']['isTrial']
            r.data.trialStartDate = jobj['data']['trialStartDate']
            r.data.trialEndDate = jobj['data']['trialEndDate']
        except json.decoder.JSONDecodeError:
            return None
        except KeyError:
            return None
        else:
            pass
        return r


class ComponentLicense(object):
    licenseName: str = ""
    licenseText: str = ""


class ResultComponentLicense(object):
    code: int = 0
    messaage: str = ""
    data: ComponentLicense = None

    @staticmethod
    def fromJson(jsonstr: str):
        r = ResultComponentLicense()
        try:
            jobj = json.loads(jsonstr)
            r.code = jobj['code']
            r.message = jobj['message']
            r.data = ComponentLicense()
            r.data.licenseName = jobj['data']['licenseName']
            r.data.licenseText = jobj['data']['licenseText']
        except json.decoder.JSONDecodeError:
            return None
        except KeyError:
            return None
        else:
            pass
        return r


class ComponentProducer(object):
    company: str = ""
    contact: str = ""
    email: str = ""
    phone: str = ""
    url: str = ""


class ResultComponentProducer(object):
    code: int = 0
    message: str = ""
    data: ComponentProducer = None

    @staticmethod
    def fromJson(jsonstr: str):
        r = ResultComponentProducer()
        try:
            jobj = json.loads(jsonstr)
            r.code = jobj['code']
            r.message = jobj['message']
            r.data = ComponentProducer()
            r.data.company = jobj['data']['company']
            r.data.contact = jobj['data']['contact']
            r.data.email = jobj['data']['email']
            r.data.phone = jobj['data']['phone']
            r.data.url = jobj['data']['url']
        except json.decoder.JSONDecodeError:
            return None
        except KeyError:
            return None
        else:
            pass
        return r


class ComponentSDK:

    __licHost: str = "isc-license-service"
    __licPort: int = 9013

    __licInfo: LicenseData = None
    __compInfo: ResultComponentRegister = None

    __componentName: str = ""
    __componentKey: str = ""

    __isvalid: bool = False
    __invalidMessage: str = ""

    @property
    def isValid(self) -> bool:
        return self.__isvalid

    @property
    def invalidMessage(self) -> str:
        return self.__invalidMessage

    @property
    def license(self) -> ComponentLicense:
        urlLic = 'http://%s:%d/api/core/license/component/license' % (self.__licHost, self.__licPort)
        param = '{"compName":"%s", "compKey":"%s"}' % (self.__componentName, self.__componentKey)
        ret = self.__httpPost(urlLic, param)
        obj = ResultComponentLicense.fromJson(ret)
        return obj.data

    @property
    def producer(self) -> ComponentProducer:
        urlLic = 'http://%s:%d/api/core/license/component/producer' % (self.__licHost, self.__licPort)
        param = '{"compName":"%s", "compKey":"%s"}' % (self.__componentName, self.__componentKey)
        ret = self.__httpPost(urlLic, param)
        obj = ResultComponentProducer.fromJson(ret)
        return obj.data

    def __init__(self, compName: str, compKey: str, host: str = "isc-license-service", port: int = 9013):
        self.__licHost = host
        self.__licPort = port
        self.__componentName = compName
        self.__componentKey = compKey
        self.__load()


    @staticmethod
    def __httpGet(url: str) -> str:
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return resp.text
            else:
                return ''
        except requests.exceptions.ConnectionError:
            return ''

    @staticmethod
    def __httpPost(url: str, param=None) -> str:
        try:
            resp = requests.post(url, data=param, headers={'Content-Type': 'application/json'})
            if resp.status_code == 200:
                return resp.text
            else:
                return resp.text
        except requests.exceptions.ConnectionError:
            return ''


    def __load(self):
        # 从 OS 内获取 OS 的授权信息
        urlLic = 'http://%s:%d/api/core/license/read' % (self.__licHost, self.__licPort)
        ret = self.__httpGet(urlLic)
        self.__licInfo = LicenseData.fromJson(ret)
        # 从云端获取组件的注册信息
        urlComp = 'http://license.isyscore.com:9990/api/license/cloud/component/one2?compName=%s&compKey=%s' % (self.__componentName, self.__componentKey)
        ret2 = self.__httpGet(urlComp)
        self.__compInfo = ResultComponentRegister.fromJson(ret2)
        if self.__compInfo is None:
            self.__isvalid = False
            self.__invalidMessage = "无法顺利请求云端服务器"
        else:
            if self.__compInfo.data is None:
                self.__isvalid = False
                self.__invalidMessage = self.__compInfo.message if self.__compInfo.message == '' else "无法从云端获取数据"
            else:
                if self.__compInfo.code == 200:
                    if self.__licInfo is not None:
                        if self.__licInfo.customer.enterpriseName == self.__compInfo.data.producerCompany and self.__licInfo.customer.contactName == self.__compInfo.data.producerContact:
                            # 直接授权给自己
                            self.__isvalid = True
                            self.__invalidMessage = ""
                        else:
                            # 查授权
                            urlCompValid = 'http://%s:%d/api/core/license/component/valid' % (self.__licHost, self.__licPort)
                            param = '{"compName":"%s", "compKey":"%s"}' % (self.__componentName, self.__componentKey)
                            ret3 = self.__httpPost(urlCompValid, param)
                            r = ResultComponentLicensed.fromJson(ret3)
                            if r.code == 200:
                                self.__isvalid = True
                                self.__invalidMessage = r.message
                            else:
                                self.__isvalid = False
                                self.__invalidMessage = r.message if r.message == '' else "未能获取到组件状态"
                    else:
                        self.__isValid = False
                        self.__invalidMessage = "OS 未授权"
                else:
                    # 云端返回的异常信息
                    self.__isValid = False
                    self.__invalidMessage = self.__compInfo.message


