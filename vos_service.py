import pandas as pd

workbook = pd.ExcelFile("finance.xlsx")
krx100_stock = workbook.parse("업종명")
krx100 = workbook.parse("재무")
krx100.iloc[2:, 1:] = krx100.iloc[2:, 1:].apply(pd.to_numeric)  # 문자열 => 숫자
print("Excel 전처리 완료")


# 입력한 종목의 업종명 구하는 함수
def get_sector(stock: str):
    for i in range(2541):
        if (stock == krx100_stock.iloc[i, 1]):
            return krx100_stock.iloc[i, 3]


# 입력한 종목의 매출액 증가율 구하는 함수 (2011-12-31 ~ 2021-12-31)
def sales(stock: str):  # , year: int):
    col = 3
    count = 0
    sales = []
    while (col < 1601):
        if (stock == krx100.iloc[0, col]):
            count += 1
            for i in range(11):
                lastSale = float(krx100.iloc[i+2, col])
                sale = float(krx100.iloc[i+3, col])
                if (sale != 0 and lastSale != 0):
                    result = (sale-lastSale)/lastSale*100
                    sales.append(result)
                else:
                    sales.append(0)
        col += 16
    if (count != 0):
        return sales
    else:
        return 0


# ======================= ROE
# 입력한 종목(stock)의 ROE 구하는 함수 (2010-12-31 ~ 2021-12-31)
def ROE_stock(stock: str):
    col = 15
    ROE = []
    while (col < 1601):
        if (stock == krx100.iloc[0, col]):
            for i in range(12):
                ROE.append(krx100.iloc[i+2, col])
        col += 16
    return ROE


# 입력한 종목(stock)의 최근 (year)년 평균 ROE 구하는 함수
def ROE_avg_stock(stock: str, year: int):
    ROE_sum = 0
    ROE_avg = 0
    col = 15
    count = 0
    while (col < 1601):
        if (stock == krx100.iloc[0, col]):
            for i in range(year):
                if (krx100.iloc[13-i, col] != 0):
                    count += 1
                ROE_sum += krx100.iloc[13-i, col]
            ROE_avg = ROE_sum/count
        col += 16
    return ROE_avg


# 입력한 종목(stock) 업종의 최근 (year)년 평균 ROE 구하는 함수
def ROE_avg_sector(sector: str, year: int):
    ROE_sum = 0
    col = 15
    count = 0
    while (col < 1601):
        if (sector == get_sector(krx100.iloc[0, col])):
            count += 1
            ROE_sum += ROE_avg_stock(krx100.iloc[0, col], year)
        col += 16
    if (count != 0):
        return ROE_sum / count
    else:
        return 0
# ======================= ROE


# ======================= 부채 비율
# 입력한 종목(stock)의 부채 비율 구하는 함수 (2010-12-31 ~ 2021-12-31)
def debt_stock(stock: str):
    col = 8
    debt = []
    while (col < 1601):
        if (stock == krx100.iloc[0, col]):
            for i in range(12):
                debt.append(krx100.iloc[i+2, col])
        col += 16
    return debt


# 입력한 종목(stock)의 최근 (year)년 평균 부채 비율 구하는 함수
def debt_avg_stock(stock: str, year: int):
    debt_sum = 0
    debt_avg = 0
    col = 8
    count = 0
    while (col < 1601):
        if (stock == krx100.iloc[0, col]):
            for i in range(year):
                if (krx100.iloc[13-i, col] != 0):
                    count += 1
                debt_sum += krx100.iloc[13-i, col]
            debt_avg = debt_sum/count
        col += 16
    return debt_avg


# 입력한 종목(stock) 업종의 최근 (year)년 평균 부채 비율 구하는 함수
def debt_avg_sector(sector: str, year: int):
    debt_sum = 0
    col = 8
    count = 0
    while (col < 1601):
        if (sector == get_sector(krx100.iloc[0, col])):
            count += 1
            debt_sum += debt_avg_stock(krx100.iloc[0, col], year)
        col += 16
    if (count != 0):
        return debt_sum / count
    else:
        return 0
# ======================= 부채 비율


# # 업계 평균 PER, PBR 반환
# def getAvgPerPbr(sector: str, num: int, allInfo):
#     PER_sum = 0
#     PBR_sum = 0
#     PER_avg = 0
#     PBR_avg = 0
#     count_PER = 0
#     count_PBR = 0

#     for i in range(num):  # 모든 종목에 대해서
#         other = get_sector(allInfo.iloc[i, 1].strip())  # 각 종목의 업종을 구함
#         if (sector == other):  # 입력한 종목의 업종과 특정 종목의 업종이 같으면
#             PER = float(allInfo.iloc[i, 6])
#             PBR = float(allInfo.iloc[i, 10])
#             if not (pd.isna(PER)):  # 값이 Nan이 아니면
#                 count_PER += 1
#                 PER_sum += PER
#             if not (pd.isna(PBR)):  # 값이 Nan이 아니면
#                 count_PBR += 1
#                 PBR_sum += PBR
#     PER_avg = PER_sum/count_PER
#     PBR_avg = PBR_sum/count_PBR

#     return PER_avg, PBR_avg


# # 종목의 단축코드 입력하면 표준코드 반환하는 함수
# def stdCode(stock_num: str):
#     gen_otp_url = "https://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
#     gen_otp_data = {
#         "locale": "ko_KR",
#         "mktId": "ALL",
#         "share": "1",
#         "csvxls_isNo": "false",
#         "name": "fileDown",
#         "url": "dbms/MDC/STAT/standard/MDCSTAT01901"
#     }
#     headers = {"Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader"}
#     otp = rq.post(gen_otp_url, gen_otp_data, headers=headers).text
#     down_url = "https://data.krx.co.kr/comm/fileDn/download_csv/download.cmd"
#     down_sector_KS = rq.post(down_url, {"code": otp}, headers=headers)
#     sector_KS = pd.read_csv(BytesIO(down_sector_KS.content), encoding="CP949")
#     # 크롤링 완료

#     standardCode = tuple(sector_KS["표준코드"])
#     code = tuple(sector_KS["단축코드"])
#     for i in range(len(code)):
#         if (stock_num == code[i]):
#             return standardCode[i]


# # 종목 입력하면 입력한 날짜부터 오늘까지의 PER, PBR
# def getInfo(sector_num: str, name: str, stdCode: str, date: str):
#     print("today", today)
#     print("stdCode", stdCode)
#     print("date", date)
#     gen_otp_url = "https://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
#     gen_otp_data = {
#         "locale": "ko_KR",
#         "searchType": "2",
#         "mktId": "ALL",
#         "trdDd": today,
#         "tboxisuCd_finder_stkisu0_0": sector_num+"/"+name,
#         "isuCd": stdCode,
#         "isuCd2": "KR7005930003",
#         "codeNmisuCd_finder_stkisu0_0": name,
#         "param1isuCd_finder_stkisu0_0": "ALL",
#         "strtDd": date,
#         "endDd": today,  # 오늘 날짜 써야함
#         "csvxls_isNo": "false",
#         "name": "fileDown",
#         "url": "dbms/MDC/STAT/standard/MDCSTAT03502"
#     }
#     headers = {"Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader"}
#     otp = rq.post(gen_otp_url, gen_otp_data, headers=headers).text
#     down_url = "https://data.krx.co.kr/comm/fileDn/download_csv/download.cmd"
#     down_sector_KS = rq.post(down_url, {"code": otp}, headers=headers)
#     sector_KS = pd.read_csv(BytesIO(down_sector_KS.content), encoding="CP949")
#     PER = tuple(sector_KS["PER"])
#     PBR = tuple(sector_KS["PBR"])
#     print(len(PER))
#     print(len(PBR))
#     # print("PER", PER[::-1])
#     return PER[::-1], PBR[::-1]
