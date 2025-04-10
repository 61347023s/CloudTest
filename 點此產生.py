#1 引入套件
from time import sleep
from function import coding,tomorrow,read_file,get_info
print('done')
print('pull')
try:
    #2 讀取當日課表
    all=[]
    short=['國','數','英','社','自','生','理','化','物','科']
    form=['國文','數學','英文','社會','自然','生物','理化','化學','物理','地科']
    cla=dict(zip(short,form))

    with open('課表複製貼上區.csv','r') as f:
        for line in f.readlines():
            line=line.strip().split(',')
            all.append(line)
        f.close()
    all.remove(all[0])
    for i in range(len(all)):
        all[i][3]=cla[all[i][3][len(all[i][3])-1]]

    #2.1 刪除調課、順延、隔週無、XX起、分X堂、拆X堂
    s=[i[4] for i in all]
    for i in range(len(s)):
        if(s[i]!=''):
            if(s[i][0]=='調' or s[i][0]=='順' or s[i]=='隔週無' or '起' in s[i] or '分' in s[i] or '拆' in s[i]):
                all[i][4]='del'
    #2.2 亂碼處理
    coding(all)

    #3 取得資料
    #3.1 取得學生資料
    stu=get_info(all,1)

    #3.2 取得老師資料
    tea=get_info(all,2)

    #4 讀取例外
    #4.1 爸爸
    father=read_file('爸爸.txt')

    #4.2 本人
    self=read_file('本人.txt')

    #4.3 其他家長
    with open('其他家長.txt','r',encoding='UTF-8') as f:
        other={}
        for line in f.readlines():
            line=line.strip()
            name=line.split()[0]
            call=line.split()[1]
            other[name]=call
        f.close()

    #4.4 兄弟姊妹
    with open('兄弟姊妹.txt','r',encoding='UTF-8') as f:
        brother=[]
        for line in f.readlines():
            line=line.strip().split()
            brother.append(line)
        f.close()
    
    #5 產生提醒簡訊
    date=tomorrow()
    f=open('提醒簡訊.txt','w',encoding='UTF-8')
    #5.1 老師
    for i in tea:
        online=False;school=False
        tea[i]=sorted(tea[i])
        f.write('%s老師您好! 提醒您%s\n'%(i,date))
        for j in range(len(tea[i])):
            if(tea[i][j][-2:]=='線上'):
                online=True
                f.write('%s\t有一堂%s課(線上)\n'%(tea[i][j][:9],tea[i][j][-4:-2]))
            else:
                school=True
                f.write('%s\t有一堂%s課\n'%(tea[i][j][:9],tea[i][j][-4:-2]))
        if(online and not school):  #線上
            f.write('請您備妥相關教材、並準時上線!\n文山個別指導中心 課務組 關心您。\n\n')
        elif(school and not online):  #實體
            f.write('請您備妥相關教材、並準時出席、路上小心!\n文山個別指導中心 課務組 關心您。\n\n')            
        elif(school and online):  #線上或實體
            f.write('請您備妥相關教材、並準時出席!\n文山個別指導中心 課務組 關心您。\n\n')
    f.write('\n\n\n\n')

    #5.2 本人
    for i in stu:
        if(i in self):
            f.write('%s您好! 提醒您%s\n'%(i,date))
            for j in range(len(stu[i])):
                if(stu[i][j][-2:]=='線上'):
                    online=True;school=False
                    f.write('%s\t有一堂%s課(線上)\n'%(stu[i][j][:9],stu[i][j][-4:-2]))
                else:
                    school=True
                    f.write('%s\t有一堂%s課\n'%(stu[i][j][:9],stu[i][j][-4:-2]))
            if(online and not school):  #線上
                f.write('請記得備妥相關教材、並準時上線!\n文山個別指導中心 課務組 關心您。\n\n')
            elif(school and not online):  #實體
                f.write('請記得備妥相關教材、並準時出席、路上小心!\n文山個別指導中心 課務組 關心您。\n\n')            
            elif(school and online):  #線上或實體
                f.write('請記得備妥相關教材、並準時出席!\n文山個別指導中心 課務組 關心您。\n\n')

    #5.3 兄弟姊妹
    for i in brother:
        count=0
        for j in i:
            for k in stu:
                if(j==k):
                    count+=1
        if(count==len(i)):
            online=False;school=False
            if(i[0] in father):
                f.write('爸爸您好! 提醒您%s\n'%date)
            elif(i[0] in other):
                f.write('%s您好! 提醒您%s\n'%(other[i[0]],date))
            else:
                f.write('媽媽您好! 提醒您%s\n'%date)
            for j in i:
                f.write(j+'\n')
                for k in range(len(stu[j])):
                    if(stu[j][k][-2:]=='線上'):
                        online=True
                        f.write('%s\t有一堂%s課(線上)\n'%(stu[j][k][:9],stu[j][k][-4:-2]))
                    else:
                        school=True
                        f.write('%s\t有一堂%s課\n'%(stu[j][k][:9],stu[j][k][-4:-2]))
                del stu[j]
            if(online and not school):  #線上
                f.write('請記得提醒孩子備妥相關教材、並準時上線!\n文山個別指導中心 課務組 關心您。\n\n')
            elif(school and not online):  #實體
                f.write('請記得提醒孩子備妥相關教材、並準時出席、路上小心!\n文山個別指導中心 課務組 關心您。\n\n')            
            elif(school and online):  #線上或實體
                f.write('請記得提醒孩子備妥相關教材、並準時出席!\n文山個別指導中心 課務組 關心您。\n\n')

    #5.4 學生家長
    for i in stu:   
        online=False;school=False 
        stu[i]=sorted(stu[i])
        if(i in father):
            f.write('%s爸爸您好! 提醒您%s\n'%(i,date))
        elif(i in other):
            f.write('%s%s您好! 提醒您%s\n'%(i,other[i],date))
        else:
            f.write('%s媽媽您好! 提醒您%s\n'%(i,date))
        for j in range(len(stu[i])):
            if(stu[i][j][-2:]=='線上'):
                online=True
                f.write('%s\t有一堂%s課(線上)\n'%(stu[i][j][:9],stu[i][j][-4:-2]))
            else:
                school=True
                f.write('%s\t有一堂%s課\n'%(stu[i][j][:9],stu[i][j][-4:-2]))
        if(online and not school):  #線上
            f.write('請記得提醒孩子備妥相關教材、並準時上線!\n文山個別指導中心 課務組 關心您。\n\n')
        elif(school and not online):  #實體
            f.write('請記得提醒孩子備妥相關教材、並準時出席、路上小心!\n文山個別指導中心 課務組 關心您。\n\n')            
        elif(school and online):  #線上或實體
            f.write('請記得提醒孩子備妥相關教材、並準時出席!\n文山個別指導中心 課務組 關心您。\n\n')
    f.close()
    
#6 例外處理
except Exception as e:
    print('\n\n\n\n\n\n\n\n\n錯誤:',e)
    print('\n\n無法產生提醒簡訊。')
    print('\n\n可能是在課表複製貼上時留下空行或空格。')
    print('\n\n請再檢查一遍。')
    sleep(10)
else:
    print('\n\n\n\n\n\n\n\n\n\n\n提醒簡訊寫入完成。')
    print('\n\n請打開「提醒簡訊.txt」進行複製。')
    sleep(2)
