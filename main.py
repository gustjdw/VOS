import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from vos import allInfo, stock, dictPER, dictPBR
from vos_service import get_sector, sales, ROE_stock, ROE_avg_stock, ROE_avg_sector, debt_stock, debt_avg_stock, debt_avg_sector


class req(BaseModel):
    name: str
    date: str
    year: int


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/vos", status_code=200)
def vos(req: req):
    print("요청 들어옴")
    name = req.name  # 종목명
    date = req.date.replace("-", "")[0:8]  # 매수 날짜
    year = req.year  # 평균 낼 년 수

    if (0 < year < 12):

        for i in range(len(stock)):  # 모든 종목에 대해서
            if (name == allInfo.iloc[i, 1].strip()):  # 종목명이 동일하면
                # stock_num = allInfo.iloc[i, 0]  # 종목의 단축코드
                PER = allInfo.iloc[i, 6]  # 당일 기준 PER
                PBR = allInfo.iloc[i, 10]  # 당일 기준 PBR

        sector = get_sector(name)  # 업종명
        sale = sales(name)  # 매출액 증가율
        ROEStock = ROE_stock(name)  # ROE 변화
        ROEAvgStock = ROE_avg_stock(name, year)  # N년 평균 ROE
        ROEAvgSector = ROE_avg_sector(sector, year)  # 업계 N년 평균 ROE
        debtStock = debt_stock(name)  # 부채 비율
        debtAvgStock = debt_avg_stock(name, year)  # N년 평균 부채 비율
        debtAvgSector = debt_avg_sector(sector, year)  # 업계 N년 평균 부채 비율
        PER_avg = dictPER[sector]  # 당일 기준 업계 평균 PER
        PBR_avg = dictPBR[sector]  # 당일 기준 업계 평균 PBR

        if (sale == 0):  # KRX100에 속하지 않은 종목일 때
            ROEAvgSector = 0
            debtAvgSector = 0

        result = {
            "sector": sector,
            "sale": sale,
            "ROE_stock": ROEStock,
            "ROE_avg_stock": ROEAvgStock,
            "ROE_avg_sector": ROEAvgSector,
            "debt_stock": debtStock,
            "debt_avg_stock": debtAvgStock,
            "debt_avg_sector": debtAvgSector,
            "PER": PER,
            "PER_avg": PER_avg,
            "PBR": PBR,
            "PBR_avg": PBR_avg
        }
        with open("output.json", "w") as f:
            json.dump(result, f, indent=2)
        return result

    else:
        return "12 미만의 수를 입력하쇼"


@app.post("/test", status_code=200)
def test(req: req):
    print("요청 들어옴")
    name = req.name  # 종목명
    date = req.date.replace("-", "")[0:8]  # 매수 날짜
    year = req.year  # 평균 낼 년 수

    if (year < 12):

        # for i in range(len(stock)):  # 모든 종목에 대해서
        # if (name == allInfo.iloc[i, 1].strip()):  # 종목명이 동일하면
        # stock_num = allInfo.iloc[i, 0]  # 종목의 단축코드
        # PER = allInfo.iloc[i, 6]  # PER
        # PBR = allInfo.iloc[i, 10]  # PBR

        sector = get_sector(name)  # 종목의 업종명
        print("sector = Vget_sector(name)")

        sale = sales(name, year)
        print("sale = sales(name, year)")

        # result = getAvgPerPbr(sector, len(stock), allInfo)
        # print("result = getAvgPerPbr(sector, stock, allInfo)")

        # PER_avg = result[0]
        # PBR_avg = result[1]

        result = {
            "sector": sector,
            "sale": sale,
            "ROE_stock": ROE_stock(name),
            "ROE_avg_stock": ROE_avg_stock(name, year),
            "ROE_avg_sector": ROE_avg_sector(sector, year),
            "debt_stock": debt_stock(name),
            "debt_avg_stock": debt_avg_stock(name, year),
            "debt_avg_sector": debt_avg_sector(sector, year),
            "PER": 0.5,  # PER,
            "PER_avg": 1.5,  # PER_avg,
            "PBR": 2.5,  # PBR,
            "PBR_avg": 3.5,  # PBR_avg
        }
        with open("output.json", "w") as f:
            json.dump(result, f, indent=2)
        return result

    else:
        return "12 미만의 수를 입력하쇼"


@app.get("/")
async def root():
    return "Welcome"


# start server
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=3000, reload=True)
