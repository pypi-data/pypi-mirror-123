#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

import json
from sys import version_info
from datetime import timedelta
import logging
import requests
import base64, codecs

MIN_PYTHON_VERSION = (3, 5, 3)

_ = version_info >= MIN_PYTHON_VERSION or exit(
    "Python %d.%d.%d required" % MIN_PYTHON_VERSION
)

__version__ = "1.0.1"

_LOGGER = logging.getLogger(__name__)

# Date format for url
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

TIMEOUT = timedelta(seconds=30)


'''
#nguyen ban
bac1 = 1678 # 0 - 50
bac2 = 1734 # 51 - 100
bac3 = 2014 # 101 - 200
bac4 = 2536 # 201 - 300
bac5 = 2834 # 301 - 400
bac6 = 2927 # 401 tro len
'''
#giam gia covid19
bac1 = 1510 # 0 - 50
bac2 = 1561 # 51 - 100
bac3 = 1813 # 101 - 200
bac4 = 2282 # 201 - 300
bac5 = 2834 # 301 - 400
bac6 = 2927 # 401 tro len

###################################
magic = 'IyEvdXNyL2Jpbi9lbnYgcHl0aG9uDQojDQojIFRoaXMgcHJvZ3JhbSBpcyBmcmVlIHNvZnR3YXJlOiB5b3UgY2FuIHJlZGlzdHJpYnV0ZSBpdCBhbmQvb3IgbW9kaWZ5DQojIGl0IHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgR05VIExlc3NlciBQdWJsaWMgTGljZW5zZSBhcyBwdWJsaXNoZWQgYnkNCiMgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbiwgZWl0aGVyIHZlcnNpb24gMyBvZiB0aGUgTGljZW5zZSwgb3INCiMgKGF0IHlvdXIgb3B0aW9uKSBhbnkgbGF0ZXIgdmVyc2lvbi4NCiMNCiMgVGhpcyBwcm9ncmFtIGlzIGRpc3RyaWJ1dGVkIGluIHRoZSBob3BlIHRoYXQgaXQgd2lsbCBiZSB1c2VmdWwsDQojIGJ1dCBXSVRIT1VUIEFOWSBXQVJSQU5UWTsgd2l0aG91dCBldmVuIHRoZSBpbXBsaWVkIHdhcnJhbnR5I'
love = 'T9zQDbwVR1SHxAVDH5HDHWWGRyHJFOipvOTFIEBEIAGVRMCHvOOVSOOHyEWD1IZDIVtHSIFHR9GEF4tVSAyMFO0nTHAPvZtE05IVRkyp3AypvODqJWfnJZtGTywMJ5mMFOzo3VtoJ9lMFOxMKEunJkmYt0XVj0XVlOMo3Htp2uiqJkxVTuuqzHtpzIwMJy2MJDtLFOwo3O5VT9zVUEbMFOUGyHtGTImp2IlVSO1LzkcLlOZnJAyoaAyQDbwVTSfo25aVUqcqTttqTucplOjpz9apzSgYvNtFJLtoz90YPOmMJHtJ2u0qUN6Yl93q3phM251Yz9lMl9fnJAyoaAypl9qYt0XQDccoKOipaDtnaAiot0XnJ1jo3W0VUWypKIyp3EmQDbAPt0XL2kup3ZtDyOWBt0XVPNtVTEyMvOsK2yhnKEsKlumMJkzYPOhLJ1yCH5iozHfVUO3CH5iozHcBt0XVPNtVPNtVPOmMJkzYy9mMKAmnJ9hVQ0tpzIkqJImqUZhH2Imp2yiovtcQDbtVPNtVPNtVUAyoT'
god = 'YuX25hbWUgPSBuYW1lDQogICAgICAgIHNlbGYuX3B3ID0gcHcNCg0KDQogICAgZGVmIF9hdXRoZW50aWMoc2VsZik6DQogICAgICAgIFVSTF9UT0tFTiA9ICdodHRwczovL2FwaWNza2guZXZuaGFub2kuY29tLnZuL2Nvbm5lY3QvdG9rZW4nDQogICAgICAgIGRhdGEgPSB7DQogICAgICAgICd1c2VybmFtZSc6IHNlbGYuX25hbWUsDQogICAgICAgICdwYXNzd29yZCc6IHNlbGYuX3B3LA0KICAgICAgICAnZ3JhbnRfdHlwZSc6ICdwYXNzd29yZCcsDQogICAgICAgICdjbGllbnRfaWQnOiAnaHR0cGxvY2FsaG9zdDQ1MDAnLA0KICAgICAgICAnY2xpZW50X3NlY3JldCc6ICdzZWNyZXQnDQogICAgICAgIH0NCg0KICAgICAgICB7DQogICAgICAgICJrZXkxIjoidmFsdWUiLA0KICAgICAgICAia2V5MiI6InZhbHVlIg0KICA'
destiny = 'tVPNtVPO9QDbAPvNtVPNtVPNtrj0XVPNtVPNtVPNvn2I5ZlV6VaMuoUIyVvjAPvNtVPNtVPNtVzgyrGDvBvW2LJk1MFVAPvNtVPNtVPNtsD0XVPNtVPNtVPO0o2gyovN9WlpAPvNtVPNtVPNtqUW5Bt0XVPNtVPNtVPNtVPNtpzImpT9hp2HtCFOlMKS1MKA0pl5jo3A0XSIFGS9HG0gSGvjtMTS0LG1xLKEuXF50MKu0QDbtVPNtVPNtVPNtVPNwpUWcoaDbpzImpT9hp2HhqTI4qPxAPvNtVPNtVPNtVPNtVTEuqTRtCFOdp29hYzkiLJEmXUWyp3OioaAyXD0XVPNtVPNtVPNtVPNtqT9eMJ4tCFOxLKEuJlquL2Ayp3AsqT9eMJ4aKD0XVPNtVPNtVPOyrTAypUDtEKuwMKO0nJ9hVTSmVTI4Bt0XVPNtVPNtVPNtVPNtpUWcoaDbMKtcQDbtVPNtVPNtVPNtVPO0o2gyovN9VPqypaWsqT9eMJ4aQDbAPvNtVPNtVPNtpzI0qKWhVUEin2Ih'
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))
###################################

class API:
    """ API class for EVN Online API  """
    INTERVAL_6MIN = "6min"
    INTERVAL_DAY = "day"

    def __init__(self, name=None, pw=None, makh=None):
        self._name = name
        self._pw = pw
        self._makh=makh
        self._token = self._authen(self._name, self._pw)

    def _authen(self, name, pw):
        authen = BPI(name, pw)
        token = authen._authentic()
        #print(token)
        return token

    def _get_home_detail(self):
        json_data = {
                "ten_kh":'ten_kh',
                "makh":'makh',
                "tienthangtruoc":'tienthangtruoc',
                "sanluong":'sanluong',
                "chiso":'chiso',
                "socongto":'sosongto',
                "thoidiem":'thoidiem',
                "copyright": 'trumxuquang@gmail.com'
        }

        return json_data

    def get_evn_hn(self):
        return self._request_data()

    def kc_date(self, kc=4):
        import datetime 
        today = datetime.date.today()
        tomorow_date = today + datetime.timedelta(days = 2)
        kc_date = today - datetime.timedelta(days = kc)

        return {"kc_date":kc_date.strftime("%d/%m/%Y"), "tomorow_date":tomorow_date.strftime("%d/%m/%Y")}

    def _request_data(self):
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'Authorization': 'Bearer '+self._token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://evnhanoi.vn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://evnhanoi.vn/search/tracuu-chiso-congto',
            'Accept-Language': 'vi-VN,vi;q=0.9',
        }
        date = self.kc_date(4)
        data = {"maDonVi":self._makh[0:6],"maDiemDo":self._makh+'1',"ngayDau":date['kc_date'],"ngayCuoi":date['tomorow_date'],"maXacThuc":"EVNHN"}
        data = json.dumps(data)
        response = requests.post('https://evnhanoi.vn/api/TraCuu/LayChiSoDoXa', headers=headers, data=data).text
        #print(response)

        rsp = json.loads(response)
        #isError
        isError = rsp['isError']
        #data -> chisongay
        datavn = rsp['data']


        sanluong_tungngay = datavn['chiSoNgay']
        lendata = len(sanluong_tungngay)
        datajson = {
          'isError':isError,

          'maDiemDo':sanluong_tungngay[lendata-2]['maDiemDo'],
          'soCto': sanluong_tungngay[lendata-2]['soCto'],
          'time_p_giao':sanluong_tungngay[lendata-2]['ngay'],
          'loaiBcs':sanluong_tungngay[lendata-2]['loaiBcs'],
          'tong_p_giao':sanluong_tungngay[lendata-2]['sg'],

          'time_p_chot':sanluong_tungngay[lendata-1]['ngay'],
          'tong_p_chot':sanluong_tungngay[lendata-1]['sg']
        }
        #print(datajson)

        return datajson
    ##########
    def gettheogio(self,token='xx', makhx='PE04000011000'):
        import requests
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'Authorization': 'Bearer '+token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://evnhanoi.vn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://evnhanoi.vn/search/tracuu-chiso-congto',
            'Accept-Language': 'vi-VN,vi;q=0.9',
        }
        date = self.kc_date(4)
        data = {"maDonVi":makhx[0:6],"maDiemDo":makhx+'1',"ngayDau":date['kc_date'],"ngayCuoi":date['tomorow_date'],"maXacThuc":"EVNHN"}
        data = json.dumps(data)
        response = requests.post('https://evnhanoi.vn/api/TraCuu/LayChiSoDoXa', headers=headers, data=data)
        print(response.text)

    def hass_chisohientai(self, jsondata):

        sanluong = jsondata['sanluong']
        makh = jsondata['makh']
        tienthangtruoc = jsondata['tienthangtruoc']
        chiso = jsondata['chiso']
        socongto = jsondata['socongto']
        thoidiem = jsondata['thoidiem']

        intx = sanluong.find(".")
        sanLuong1 = 0
        if intx == -1:
            sanLuong1 = sanluong
        else:
            sanLuong1 = sanluong[: intx]
        
        sanLuong1 = sanLuong1.strip()

        tienhientai = self.tinhtien(float(sanLuong1))

        json_data = {
            "ten_kh":jsondata['ten_kh'],
            "ma_khachhang":makh,
            "sanLuong_thangnay":sanLuong1,
            "tien_thangnay":tienhientai,
            "chiso_congto":chiso.replace(" ",""),
            "thoidiemdo":thoidiem,
            "tienthangtruoc":tienthangtruoc,
            "socongto":socongto,
            "chiso_date":thoidiem[:10],
            "chiso_time":thoidiem[-8:],
            "copyright":'trumxuquang@gmail.com'
        }

        return json_data


    def _50k(self, xyz):
        result = xyz*bac1
        return result

    def _100k(self, xyz):
        result = self._50k(50) + (xyz -50) * bac2
        return result

    def _200k(self, xyz):
        result = self._100k(100) + (xyz -100) * bac3
        return result

    def _300k(self, xyz):
        result = self._200k(200) + (xyz -200) * bac4
        return result

    def _400k(self, xyz):
        result = self._300k(300) + (xyz -300) * bac5
        return result

    def _500k(self, xyz):
        result = self._400k(400) + (xyz -400) * bac6
        return result

    def _thue10(self, x):
        return x * 10 /100

    def tinhtien(self, x):
        b1 = 0 < x < 51
        b2 = 50 < x < 101
        b3 = 100 < x < 201
        b4 = 200 < x < 301
        b5 = 300 < x < 401
        b6 = 400 < x < 3009

        if b1:
            tiengoc = self._50k(x)
            tienthue = self._thue10(tiengoc)
            sumd = tiengoc + tienthue
            return round(sumd)
        if b2:
            tiengoc = self._100k(x)
            tienthue = self._thue10(tiengoc)
            sumd = tiengoc + tienthue
            return round(sumd)
        if b3:
            tiengoc = self._200k(x)
            tienthue = self._thue10(tiengoc)
            sumd = tiengoc + tienthue
            return round(sumd)
        if b4:
            tiengoc = self._300k(x)
            tienthue = self._thue10(tiengoc)
            sumd = tiengoc + tienthue
            return round(sumd)
        if b5:
            tiengoc = self._400k(x)
            tienthue = self._thue10(tiengoc)
            sumd = tiengoc + tienthue
            return round(sumd)
        if b6:
            tiengoc = self._500k(x)
            tienthue = self._thue10(tiengoc)
            sumd = tiengoc + tienthue
            return round(sumd)

########################################