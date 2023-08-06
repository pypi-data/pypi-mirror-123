import pandas as pd
import time
import LibHanger.Library.uwLogger as Logger
import chromedriver_binary # コメントアウトしないこと
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from mercariGetter.Library.mercariConfig import mercariConfig
from LibHanger.Library.uwGlobals import *

def searchData(searchCondition):

    """
    mercariデータ検索

    Parameters
    ----------
    searchCondition : 
        検索条件

    """

    # 共通設定取得
    mc = gv.config

    # 取得したメルカリデータをpandasで返却する
    dfMercariData = getMercariDataToPandas(searchCondition, mc)

    # pandasデータをjson形式に変換する
    stringJson = dfMercariData.to_json(orient='records')

    # jsonデータを返す
    return stringJson

def getMercariDataToPandas(searchCondition, config: mercariConfig):
    
    """
    mercariデータ検索

    Parameters
    ----------
    searchCondition : 
        検索条件
    config : mercariConfig
        共通設定クラス
    """

    # 検索ワード(ここは専用の関数を用意する)
    searchWord = searchCondition
    
    # 格納用pandasカラム準備
    dfItemInfo = pd.DataFrame(columns=['itemId','itemUrl','itemName','itemPrice','itemPicUrl','soldout'])
    dictItemInfo = {}
    if searchWord == '':
        return dfItemInfo

    # 商品url
    url = config.MercariUrl + searchWord
    
    # ヘッドレスでブラウザを起動
    Logger.logging.info('Browzer Open...')
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    # ウィンドウサイズを1200x1200にする(商品名が省略される為)
    driver.set_window_size('1200', '1000')
    # url指定してページ読込
    Logger.logging.info('Page Reading...')
    driver.get(url)
    
    # 待機
    Logger.logging.info('Delay 2 Seconds...')
    time.sleep(2)

    # スクレイピング with BeautifulSoup
    Logger.logging.info('Scraping with BeautifulSoup...')
    soup = BeautifulSoup(driver.page_source, features='lxml')
    elems_items= soup.select('.ItemGrid__ItemGridCell-sc-14pfel3-1')

    # 取得した商品タグをループしてpandasデータを生成
    for index in range(len(elems_items)):
        try:
            # 商品ID
            itemUrl = elems_items[index].find_all('a')[0].get('href')
            itemId = itemUrl.split('/')[2]
            # 商品名
            itemNm = elems_items[index].find_all('mer-item-thumbnail')[0].get('item-name')
            # 商品画像URL
            itemPicUrl = elems_items[index].find_all('mer-item-thumbnail')[0].get('src')
            # 価格
            itemPrice = elems_items[index].find_all('mer-item-thumbnail')[0].get('price')
            # SoldOut
            soldOut = True if elems_items[index].find_all('mer-item-thumbnail')[0].get('sticker') else False
            # ログ出力
            Logger.logging.info('==========================================================')
            Logger.logging.info(str(index + 1) + '/' + str(len(elems_items)))
            Logger.logging.info('商品ID={}'.format(itemId))
            Logger.logging.info('商品名={}'.format(itemNm))
            Logger.logging.info('商品画像URL={}'.format(itemPicUrl))
            Logger.logging.info('価格={}'.format(itemPrice))
            Logger.logging.info('==========================================================')
            # 取得データをディクショナリにセット
            drItemInfo = pd.Series(data=['','','',0,'',False],index=dfItemInfo.columns)
            drItemInfo['itemId'] = itemId
            drItemInfo['itemUrl'] = itemUrl
            drItemInfo['itemName'] = itemNm
            drItemInfo['itemPrice'] = itemPrice
            drItemInfo['itemPicUrl'] = itemPicUrl
            drItemInfo['soldout'] = soldOut
            dictItemInfo[index] = drItemInfo
        except:
            Logger.logging.error('PandasData Create Error')
            break

    # ブラウザを閉じる
    Logger.logging.info('Browzer Closed...')
    driver.quit()

    # pandasデータ生成 
    Logger.logging.info('PandasData Create...')
    dfItemInfo = dfItemInfo.from_dict(dictItemInfo, orient='index')
    dfItemInfo = dfItemInfo.set_index(['itemId'], drop=False)

    # pandasデータを返却する
    return dfItemInfo

def returnPandasToJson(conditions):
    print(conditions)

    dfTestData = pd.DataFrame(columns=['item1','item2','item3'])
    dictTestData = {}

    for index in range(20):
        drTestData = pd.Series(data=[0,0,0], index=dfTestData.columns)
        drTestData['item1'] = index
        drTestData['item2'] = index + 100
        drTestData['item3'] = index + 200
        dictTestData[index] = drTestData

    dfTestData = dfTestData.from_dict(dictTestData, orient='index')
    dfTestData = dfTestData.set_index(['item1'], drop=False)

    stringJson = dfTestData.to_json(orient='records')

    return stringJson