import requests
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import datetime

fruit_id_box = ["45", "G49", "469", "T6", "W2", "I2", "E1", "F1", "H2", "X09", "M1", "O2", "Y1", "N9", "839", "B2", "A1", "Q1"]

def craw_fruit(fruit_id):
    today = datetime.datetime.now()
    today_year = today.year-1
    fruit_avg_price = []
    fruit_date = []
    return_value = []

    try:
        url = "https://www.twfood.cc/api/FarmTradeSums?filter={%22order%22:%22day%20asc%22,%22where%22:{%22itemCode%22:%22"+fruit_id_box[fruit_id]+"%22,%22day%22:{%22gte%22:%22"+str(today_year)+"/"+str(today.month)+"/"+str(today.day)+"%22}}}"
        r=requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})
    except:
        return_value.append(-1)
        return return_value
      
    script=r.text
    data=json.loads(script)

    for i in range(0,len(data)):
        fruit_avg_price.append(data[i]["avgPrice"])
        fruit_date.append(data[i]["day"])
        last_price=data[i]["avgPrice"]
        last_date=data[i]["day"]

    year_price_avg = np.mean(fruit_avg_price)
        
    plt.plot(fruit_date,fruit_avg_price,"r")
    plt.title("whole year price")
    plt.xlabel('date')
    plt.ylabel('price')
    x_locator=MultipleLocator(50)
    y_locator=MultipleLocator(20)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_locator)
    ax.yaxis.set_major_locator(y_locator)
    plt.savefig('price_chart.png', bbox_inches='tight')
    plt.close()

    return_value.append(last_price)
    return_value.append(last_date)

    if last_price >= year_price_avg:
        return_value.append("最後價格高於平均價格，推薦販售，不推薦買入")
    else: 
        return_value.append("最後價格低於平均價格，不推薦販售，推薦買入")

    return return_value