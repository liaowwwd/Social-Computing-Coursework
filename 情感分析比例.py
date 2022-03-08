from snownlp import SnowNLP
import csv
movielst = [
    "何以为家",
    "哪吒之魔童降世",
    "流浪地球",
    "寄生虫",
    "爱尔兰人",
    "阳光姐妹淘",
    "绿皮书",
    "婚姻故事",
    "复仇者联盟4：终局之战",
    "谁先爱上他的",
    "人生七年9",
    ]
with open('情感比snownlp.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["名称", "正面", "中性", "负面"])
           
for moviename in movielst:
    with open(moviename+'粉丝属性.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        cnt = 0
        neg = 0
        mid = 0
        pos = 0
        for row in spamreader:
            cnt+=1
            if cnt == 1 :
                continue
            s = SnowNLP(row[2]).sentiments
            try:
                star = int(row[1])*0.2
                ave = (s + star) / 2
            except:
                star = 0
                ave = s
            if ave <= 0.5:
                neg+=1
            elif ave <= 0.7:
                mid+=1
            else:
                pos+=1
        sum = pos+mid+neg
        with open('情感比snownlp.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([moviename,str(pos/sum*100)+'%'
                             ,str(mid/sum*100)+'%'
                             ,str(neg/sum*100)+'%'])
            
 
    '''
        list = row[0].split(',')
        print(list)
        for i in list:
            print(i,end="/")
    '''
