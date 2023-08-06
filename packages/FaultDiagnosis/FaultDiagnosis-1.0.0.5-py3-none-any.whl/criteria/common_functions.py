#common_functions.py

# 한글 폰트 설정
from matplotlib import font_manager, rc

rc('font', family=font_manager.FontProperties(fname="\c:/Windows/Fonts/malgun.ttf").get_name())
fontprop = font_manager.FontProperties(fname="\c:/Windows/Fonts/malgunbd.ttf", size=12)

from sklearn import ensemble
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, roc_curve
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from scipy.stats import wasserstein_distance, energy_distance
from scipy.spatial import distance
from math import sqrt, fabs, exp
import matplotlib.pyplot as plt
import pylab as plot
import numpy as np
import pandas as pd
import joblib
import datetime as dt
import csv
import sys
import warnings
import pymssql
import pandas.io.sql as psql
import pandas as pd
import pyodbc
warnings.filterwarnings(action='ignore')


class Common:
    __host = "192.168.11.54"
    __user = "sunghan"
    __password = "Sunghan!2345"
    __database = 'sunghan'
    SiteCode = ""

    def __init__(self, Sitecode):
        self.SiteCode = Sitecode
        Common.SiteCode = Sitecode

    # MSSQL 접속
    @classmethod
    def conn(cls):
       return pymssql.connect(cls.__host, cls.__user, cls.__password, cls.__database, charset='UTF8')

    # 냉방, 난방 구분 (T_OPERATING_CONFIG)
    def sitecode(self):
        db = Common.conn()
        cursor = db.cursor()
        cursor.execute("SELECT top 1 ltrim(SiteCode) FROM T_SITE_INFORMATION WHERE OperationYN = 'Y'")

        all_row = cursor.fetchall()
        SiteCode = all_row[0][0]
        cursor.close()
        db.close()

        Common.SiteCode = SiteCode
        #print("Common.SiteCode:", Common.SiteCode)
        #print("SiteCode:", SiteCode)
        return SiteCode


    # 냉방, 난방 구분 (T_OPERATING_CONFIG)
    def air_condition(self):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  ltrim(ColdStartDate), ltrim(HeatingStartDate), ColdStartHour, ColdEndHour, HeatingStartHour, HeatingEndHour \
                 FROM T_OPERATING_CONFIG \
                WHERE SiteCode = %s "
        val = (Common.SiteCode)
        cursor.execute(sql, val)

        # 실행문 조회
        all_row = cursor.fetchall()
        # print("all_row:",all_row)

        ColdStartDate = all_row[0][0]
        HeatingStartDate = all_row[0][1]
        ColdStartHour = all_row[0][2]
        ColdEndHour = all_row[0][3]
        HeatingStartHour = all_row[0][4]
        HeatingEndHour = all_row[0][5]

        cursor.close()
        db.close()

        if (ColdStartDate != None and ColdStartDate != ''):
            AirCondition = '1'
        if (HeatingStartDate != None and HeatingStartDate != ''):
            AirCondition = '2'
        if (ColdStartDate != None and ColdStartDate != '' and HeatingStartDate != None and HeatingStartDate != ''):
            print("냉방, 난방 일자 모두 유효합니다. 해당 진단 일자만 입력하십시오")
            AirCondition = '0'
        #print("AirCondition:",AirCondition)
        return AirCondition

    # 냉/난방 시작 날짜 (T_OPERATING_CONFIG)
    def start_date(self):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  ColdStartDate, HeatingStartDate FROM T_OPERATING_CONFIG WHERE SiteCode = %s"
        val = (Common.SiteCode)
        cursor.execute(sql, val)

        # 실행문 조회
        all_row = cursor.fetchall()

        ColdStartDate = all_row[0][0]
        HeatingStartDate = all_row[0][1]

        cursor.close()
        db.close()

        if (ColdStartDate != None and ColdStartDate != ''):
            startdate = ColdStartDate
        if (HeatingStartDate != None and HeatingStartDate != ''):
            startdate = HeatingStartDate
        if (ColdStartDate != None and ColdStartDate != '' and HeatingStartDate != None and HeatingStartDate != ''):
            print("냉방, 난방 일자 모두 유효합니다. 한가지 진단 일자만 입력하십시오")
        #print("startdate:", startdate)
        return startdate

    # 장비기본 정보 조회 (T_AHU_INFO)
    def ahu_info(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  ColdSupplySetupTemp, HeatSupplySetupTemp, SupplyAirVolume, OutdoorAirVolume, ExhaustAirVolume \
                FROM T_AHU_INFO \
                WHERE EquipmentClassCode = %s \
                  AND EquipmentNo = %d \
                  AND SiteCode = %s \
                  AND BuildingNo = %s AND ZoneNo = %d"
        val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo)
        cursor.execute(sql, val)

        # 실행문 조회
        all_row = cursor.fetchall()
        ColdSupplySetupTemp = all_row[0][0]
        HeatSupplySetupTemp = all_row[0][1]
        SupplyAirVolume = all_row[0][2]
        OutdoorAirVolume = all_row[0][3]
        ExhaustAirVolume = all_row[0][4]

        #print("all_row:",all_row)
        cursor.close()
        db.close()
        return ColdSupplySetupTemp, HeatSupplySetupTemp, SupplyAirVolume, OutdoorAirVolume, ExhaustAirVolume

    # 공조기 유사도 기준 정보 조회 (T_AHU_CRITERIA_SIMILARITY_INFO)
    def T_AHU_CRITERIA_SIMILARITY_INFO(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatingIndication):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  CvRMSE, WassersteinDistance, EnergyDistance, PolyDegree \
                 FROM T_AHU_CRITERIA_SIMILARITY_INFO \
                WHERE EquipmentClassCode = %s \
                  AND EquipmentNo = %d \
                  AND SiteCode = %s \
                  AND BuildingNo = %s \
                  AND ZoneNo = %d \
                  AND CoolHeatingIndication = %s"
        val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatingIndication)
        cursor.execute(sql, val)

        # 실행문 조회
        all_row = cursor.fetchall()

        if (cursor.rowcount > 0):
            CvRMSE = all_row[0][0]
            WassersteinDistance = all_row[0][1]
            EnergyDistance = all_row[0][2]
            PolyDegree = all_row[0][3]

        # print("all_row:", cursor.rowcount)
        if (cursor.rowcount == 0):
            print("찾는 데이터가 없습니다!")
        # else:
        #print("all_row:",all_row, CvRMSE, WassersteinDistance, EnergyDistance, PolyDegree)
        cursor.close()
        db.close()
        return CvRMSE, WassersteinDistance, EnergyDistance, PolyDegree

    # AHU 센싱정보 조회 (T_AHU_SENSING_INFO)
    def T_AHU_SENSING_INFO(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  SensingTime, OATemp, SATemp, RATemp, MATemp, SAFlow, OAFlow, RAFlow, SAReh, RAReh, \
                       OADamper, RADamper, EADamper, CoolCVlv, HeatCVlv, SFPower, RFPower \
                 FROM T_AHU_SENSING_INFO \
                WHERE EquipmentClassCode = '" + EquipmentClassCode + "' AND EquipmentNo = EquipmentNo  \
                  AND SiteCode = '" + SiteCode + "' AND BuildingNo = '" + BuildingNo + "' AND ZoneNo = ZoneNo "

        # print("sql:", sql)
        df = pd.read_sql(sql, db)
        #print("df len:", len(df))
        #print("df:", df)

        cursor.close()
        db.close()
        return df

    # STD 센싱정보 조회
    def T_STD_SENSING_INFO(CoolHeatingIndication):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  OATemp, SATemp, RATemp, MATemp, CoilVlv, SAFlow, OAFlow, OADamper, SFPower, FaultType \
                 FROM T_STD_SENSING_INFO \
                WHERE CoolHeatingIndication = '" + CoolHeatingIndication + "'"
        df = pd.read_sql(sql, db)
        #print("len(df):", len(df))

        cursor.close()
        db.close()
        return df

"""
SiteCode = Common.sitecode(Common.SiteCode)
print("SiteCode:",SiteCode)
aircondition = Common.air_condition(Common.SiteCode)
print("aircondition:",aircondition)
startdate = Common.start_date(Common.SiteCode)
print("startdate:",startdate)
ColdSupplySetupTemp, HeatSupplySetupTemp, SupplyAirVolume, OutdoorAirVolume, ExhaustAirVolume = Common.ahu_info("AHU", 1, Common.SiteCode, "M", 11)
print(ColdSupplySetupTemp, HeatSupplySetupTemp, SupplyAirVolume, OutdoorAirVolume, ExhaustAirVolume)

print(Common.T_AHU_CRITERIA_SIMILARITY_INFO("AHU", 1, Common.SiteCode, "M", 11, 1))
print(Common.T_AHU_SENSING_INFO("AHU", 1, Common.SiteCode, "M", 11))
print(Common.T_STD_SENSING_INFO("1"))
"""