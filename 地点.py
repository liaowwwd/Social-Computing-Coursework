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
for movie in movielst:
    loc_dic = {}
    print(loc_dic)
    with open(movie+'粉丝属性.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        cnt = 0
        for row in spamreader:
            if cnt == 0 :
                cnt += 1
                continue
            cnt+=1
            if (row[3] in loc_dic) == False:
                loc_dic[row[3]] = 1
            else:
                loc_dic[row[3]] += 1
            #中性 0.45~0.55
            #中性 0.45~0.55
        print("cnt",cnt)
    with open(movie+'粉丝地址.csv', "w", newline='') as f:
        writer = csv.writer(f)
        for key in loc_dic:
            writer.writerow([key,loc_dic[key]])
    '''
        list = row[0].split(',')
        print(list)
        for i in list:
            print(i,end="/")
    '''
