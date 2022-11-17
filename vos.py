import pandas as pd
import requests as rq
from io import BytesIO
from datetime import date
from vos_service import get_sector

today = date.today().strftime("%Y%m%d")
gen_otp_url = "https://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
gen_otp_data = {
    "locale": "ko_KR",
    "searchType": "1",
    "mktId": "ALL",
    "trdDd": today,  # 기준 날짜
    "tboxisuCd_finder_stkisu0_0": "005930/삼성전자",
    "isuCd": "KR7005930003",
    "isuCd2": "KR7005930003",
    "codeNmisuCd_finder_stkisu0_0": "삼성전자",
    "param1isuCd_finder_stkisu0_0": "ALL",
    "strtDd": today,
    "endDd": today,
    "csvxls_isNo": "false",
    "name": "fileDown",
    "url": "dbms/MDC/STAT/standard/MDCSTAT03501"
}
headers = {"Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader"}
otp = rq.post(gen_otp_url, gen_otp_data, headers=headers).text
down_url = "https://data.krx.co.kr/comm/fileDn/download_csv/download.cmd"
down_allInfo = rq.post(down_url, {"code": otp}, headers=headers)
allInfo = pd.read_csv(BytesIO(down_allInfo.content), encoding="CP949")
allInfo = allInfo.fillna(0)
stock = tuple(allInfo["종목명"])
print("크롤링 완료")

dictPER = {}
dictPBR = {}

# PER
for i in range(len(stock)):  # 모든 종목에 대해서
    sector = get_sector(allInfo.iloc[i, 1].strip())  # 각 종목의 업종을 구함
    if not sector in dictPER:
        dictPER[sector] = []
    PER = float(allInfo.iloc[i, 6])
    if not (pd.isna(PER)):
        dictPER[sector].append(PER)


# PBR
for i in range(len(stock)):  # 모든 종목에 대해서
    sector = get_sector(allInfo.iloc[i, 1].strip())  # 각 종목의 업종을 구함
    if not sector in dictPBR:
        dictPBR[sector] = []
    PBR = float(allInfo.iloc[i, 10])
    if not (pd.isna(PBR)):
        dictPBR[sector].append(PBR)


# PER
for i in dictPER:
    sum = 0
    avg = 0
    length = len(dictPER[i])
    for j in dictPER[i]:
        sum += j
    avg = sum/length
    # print(i, dictPER[i], avg)
    dictPER[i] = avg


# PBR
for i in dictPBR:
    sum = 0
    avg = 0
    length = len(dictPBR[i])
    for j in dictPBR[i]:
        sum += j
    avg = sum/length
    # print(i, dictPBR[i], avg)
    dictPBR[i] = avg
