import glob
import os
# files = glob.glob("./finall/*")
# files = sorted(files)
# print(files)
import codecs
with open("result.txt",'w') as wf:
    for num in range(1,401):
        file = "./finall/入院记录现病史-"+str(num)+".txt"
        with codecs.open(file,'r',encoding='utf-8') as rf:
            for i,line in enumerate(rf):
                result = []
                name = os.path.basename(file)
                name1 = name.split('.')[0]
                name2 = name1.split('-')[-1]
                line = line.strip()
                if i == 0:
                    wf.write("{},{};".format(int(name2),line))
                else:
                    wf.write("{};".format(line))
            wf.write('\n')