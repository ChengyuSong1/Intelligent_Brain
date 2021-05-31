import time
import random
import decimal
import datetime


def getdate(num):
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-num)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date


def get_random_color():
    color_list = ["c1", "c2", "c3"]
    return random.choice(color_list)


def get_ryb():
    color_list = ["red", "yellow", "blue"]
    return random.choice(color_list)


def get_random_num(a=1, b=100):
    x = random.uniform(a, b)
    y = round(x, 2)
    return y


def get_one_num(a=1, b=100):
    x = random.randint(a, b)
    return x


def get_random_bool():
    x = ["true", "false"]
    return random.choice(x)


def get_five_year():
    year = int(time.strftime('%Y', time.localtime(time.time())))
    res = list()
    for i in range(year-4, year+1):
        res.append(i)
    return res


def get_color(thedict, key, units=None):
    """
    :param thedict:
    :param key:
    :param units:
    :return:
    """
    value = get_dict_key(thedict, key, units=None)
    color_dict = {"c1": "c1", "c2": "c2", "c3": "c3"}
    value = color_dict.get(value, get_random_color())
    return value


def get_dict_key(thedict, key, units=None, num=None):
    """
    :param thedict:
    :param key:
    :param units:
    :return:
    """
    value = thedict.get(key, "NaN")
    if isinstance(value, float):
        # if units is not None:
        #     value = value/units
        # value = round(value, 2)
        if value == 0:
            value = "NaN"

    elif isinstance(value, int):
        # if units is not None:
        #     value = value/units
        if value == 0:
            value = "NaN"

    elif isinstance(value, decimal.Decimal):
        value = float(value)
        # if units is not None:
        #     value = value/units

        if value == 0:
            value = "NaN"

    elif isinstance(value, str):
        if value == "0000-00-00":
            value = "NaN"
        if not value:
            value = "NaN"
        value = value.strip()
        # if "9999999999" in value:
        #     value = "NaN"

    # v1 = value
    try:
        if int(value) == 9999999999:
            value = "NaN"
    except:
        pass

    try:
        if float(value) == 9999999999:
            value = "NaN"
    except:
        pass

    try:
        if int(value) == 999999999:
            value = "NaN"
    except:
        pass

    try:
        if units is not None:
            value = value/units
        value = round(value, 2)
    except:
        pass

    if num is not None:
        if value == "NaN":
            value = num
    # print(key, value, v1)

    return value


def get_unit_num(thedict, key, unit="元"):
    value = thedict.get(key, "NaN")

    try:
        value = int(value)
    except:
        value = "NaN"

    try:
        if int(value) == 9999999999:
            value = "NaN"
    except:
        pass

    try:
        if int(value) == 999999999:
            value = "NaN"
    except:
        pass

    unit_dict = {
        "元": {1: "亿元", 2: "万元"},
        "万": {1: "万亿元", 2: "亿元"},
    }

    if isinstance(value, int):
        if value >= (10000*10000):
            value = value/(10000*10000)
            value = round(value, 2)
            unit = unit_dict[unit][1]
        elif value >= 10000:
            value = value / 10000
            value = round(value, 2)
            unit = unit_dict[unit][2]

    if unit == "万":
        unit = "万元"

    return value, unit


def get_unit_value(value, unit="元"):

    try:
        value = int(value)
    except:
        value = "NaN"

    try:
        if int(value) == 9999999999:
            value = "NaN"
    except:
        pass

    try:
        if int(value) == 999999999:
            value = "NaN"
    except:
        pass

    unit_dict = {
        "元": {1: "亿元", 2: "万元"},
        "万": {1: "万亿元", 2: "亿元"},
    }

    if isinstance(value, int):
        if value >= (10000*10000):
            value = value/(10000*10000)
            value = round(value, 2)
            unit = unit_dict[unit][1]
        elif value >= 10000:
            value = value / 10000
            value = round(value, 2)
            unit = unit_dict[unit][2]

    if unit == "万":
        unit = "万元"

    return value, unit



