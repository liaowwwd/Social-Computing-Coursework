import wordcloud
import jieba
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

for moviename in movielst:
    with open(moviename+'粉丝属性.csv', newline='') as csvfile:
        w = wordcloud.WordCloud(width=1000,
                                height=700,
                                background_color='white',
                                font_path='simsun.ttf')
        spamreader = csv.reader(csvfile, delimiter=',')
        cnt = 0
        c =''
        for row in spamreader:
            cnt+=1
            if cnt == 1 :
                continue
            s = jieba.lcut(row[2])
            # 创建词云对象，赋值给w，现在w就表示了一个词云对象
            c = c + " ".join(s)
            # 调用词云对象的generate方法，将文本传入
        w.generate(c)
        # 将生成的词云保存为output1.png图片文件，保存出到当前文件夹中
        w.to_file(moviename+'.png')

