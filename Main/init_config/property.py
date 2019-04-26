
DATA_DIR = '/Users/Rambo/Downloads/highschool_data/'
DATA_OUTPUT_DIR = "/Users/Rambo/Documents/GZ_output/"

SUBJECT = ['yuwen','shuxue','yingyu','tongyongjishu','wuli','huaxue','shengwu','zhengzhi','lishi','dili']

COLUMNS = {"试题编号","参考学生数","得分人数","得分率","平均分","难度","标准差","斯皮尔曼区分度","皮尔顺区分度","A等平均分","B等平均分","C等平均分","D等平均分"}

RANK_MAP = {"dili":"Dlfd","yuwen":"Ywfd","huaxue":"Hxfd","lishi":"Lsfd","shengwu":"Swfd","wuli":"Wlfd",
            "zhengzhi":"Zzfd","tiyu":"Tyfd","shuxue":"Sxfd","yingyu":"Yyfd","xxjs":"xxjsfd"}

SUBJECT_MAP = {"dili":"地理","yuwen":"语文","huaxue":"化学","lishi":"历史","shengwu":"生物","wuli":"物理",
            "zhengzhi":"政治","tiyu":"体育","shuxue":"数学","yingyu":"英语","xxjs":"信息技术"}

CITY_MAP = {1:"贵阳",2:"遵义",3:"安顺",4:"毕节",5:"铜仁",6:"六盘水",7:"黔南州",8:"黔东南",9:"黔西南"}

def dirToString(subject,type):
    typeToDir={
        "item":DATA_DIR+subject+'ItemInfor.csv',
        "score":DATA_DIR+subject+'Score.txt',
        "rank":DATA_DIR+"等级数据.txt",
        "option":DATA_DIR+subject+"Options.txt"
    }
    return typeToDir.get(type)
