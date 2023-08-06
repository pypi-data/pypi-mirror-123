from sys import version_info
from datetime import timedelta, datetime
import logging
import json , time
import requests
import urllib3
urllib3.disable_warnings()

MIN_PYTHON_VERSION = (3, 5, 3)

_ = version_info >= MIN_PYTHON_VERSION or exit(
    "Python %d.%d.%d required" % MIN_PYTHON_VERSION
)

__version__ = "0.0.2"

# Date format for url
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

TIMEOUT = timedelta(seconds=30)


class API:

    def __init__(self, name=None, pw=None):
        self.name = name
        self.pw = pw
        self._session = self.loginevn()
  
    def loginevn(self):
        headers = {
          'sec-ch-ua': '"Chromium";v="91", " Not A;Brand";v="99", "Google Chrome";v="91"',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Referer': 'https://cskh.evnhcmc.vn/Taikhoan/lienKetDiemDungDien',
          'X-Requested-With': 'XMLHttpRequest',
          'sec-ch-ua-mobile': '?0',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        sessionlogin = requests.Session()
        data = {
          'u': self.name,
          'p': self.pw,
          'remember': '1',
          'token': ''
        }

        response = sessionlogin.post('https://cskh.evnhcmc.vn/Dangnhap/checkLG', headers=headers, data=data, verify=False)
        print(response.status_code)

        return sessionlogin

    def _request_data(self, makh=''):
        date = self.kc_date(8)
        data = {
          'token': '',
          'input_makh': makh,
          'input_tungay': date['kc_date'],
          'input_denngay': date['tomorow_date']
        }
        data_hoadon = {
          'input_makh': makh,
          'input_thang': 'tatca',
          'input_nam': '2021',
          'page': 1
        }
        print(data)
        res_dien_su_dung = self._session.post('https://cskh.evnhcmc.vn/Tracuu/ajax_dienNangTieuThuTheoNgay',  data=data, verify=False).text
        time.sleep(1)
        res_hoa_don = self._session.post('https://cskh.evnhcmc.vn/Tracuu/ajax_ds_hoadon',  data=data_hoadon, verify=False).text
        time.sleep(1)
        json_dien_su_dung = json.loads(res_dien_su_dung)
        json_hoa_don = json.loads(res_hoa_don)
        state = json_dien_su_dung['state']
        data_dien_su_dung = json_dien_su_dung['data']
        data_hoa_don = json_hoa_don['data']['ds_hoadon']
        alert = json_dien_su_dung['alert']
        sanluong_tungngay = data_dien_su_dung['sanluong_tungngay']
        lendata = len(sanluong_tungngay)
        datajson = {
          'state':state,
          'alert':alert,
          'soNgay':data_dien_su_dung['soNgay'],
          'tieude':data_dien_su_dung['tieude'],
          'ngay': sanluong_tungngay[lendata-2]['ngay'],
          'thoidiemdo': sanluong_tungngay[lendata-2]['thoidiemdo'],
          'sanluong_tong':sanluong_tungngay[lendata-2]['sanluong_tong'],
          'tong_p_giao':sanluong_tungngay[lendata-2]['tong_p_giao'],
          'data_dien_su_dung': data_dien_su_dung,
          'data_hoa_don': data_hoa_don
        }

        return datajson

    def kc_date(self, kc=4):
        import datetime 
        today = datetime.date.today()
        tomorow_date = today + datetime.timedelta(days = 2)
        kc_date = today - datetime.timedelta(days = kc)

        return {"kc_date":kc_date.strftime("05/%m/%Y"), "tomorow_date":tomorow_date.strftime("%d/%m/%Y")}

    def get_evn_hcm(self, makhx):
        return self._request_data(makhx)

