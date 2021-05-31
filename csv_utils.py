import json
import codecs
import pandas as pd


if __name__ == "__main__":
    strings = "asndasnkdju91230-192-9410-=fospdjfosd01293=921=-4901325r0-u99sjf9dsuf9usd9fu9us9dgnxcmnva;j;lasjfojuqpoqwdep[qkfpjkqowjeiqgfu-03921847328574361-3-1dlkjasn"
    target = "wufengyu"
    strings_dict = dict()
    for i in range(len(strings)):
        strings_dict[strings[i]] = i

    print(strings_dict)


