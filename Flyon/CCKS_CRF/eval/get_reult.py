#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
AUTHOR:zhoukaiyin
Tiime:2018年7月3号
"""
import glob
import os

def del_file(dirname):
    files = os.listdir(dirname)
    for file in files:
        f_path = os.path.join("CCKS_result",file)
        if os.path.isfile:
            os.remove(f_path)

def split_result(openfile):
    with open(openfile,'r') as rf:
        for line in rf:
            lis = line.split('\t')
            long = len(lis)
            if long >2:
                # print(line)
                filename = "入院记录现病史-"+lis[-4]+".txt"
                word = lis[0]
                start = lis[-3]
                end = lis[-2]
                label = lis[-1]
                # if label == "O\n":
                #     # print(label)
                #     pass
                # else:
                #     print(label)
                wf = open("./CCKS_result/"+filename,'a') 
                wf.write("{}\t{}\t{}\t{}".format(word,start,end,label))

def change_format(base_path):
    files = glob.glob(base_path+"/*")
    # print(files)
    # files = ["./CCKS_result//入院记录现病史-32.txt"]
    for file in files:
        all=[]
        words = []
        base_name = os.path.basename(file)
        with open(file,'r') as rf,open("./finall/"+base_name,'w') as wf:
            lines = rf.readlines()
            for i, line in enumerate(lines):
                line = line.rstrip()
                lis = line.split('\t')

                label = lis[-1]
                if label!="O":
                    label_1 = label.split('-')[0]
                    label_2 = label.split('-')[1]
                else:
                    label_1="O"
                    label_2="O"
                # words.append(lis)
                before = lines[i-1].strip().split('\t')[-1]
                words.append(lis)
                # print(words)
                
                if label_1=="B":
                    # print(lis)
                    words.pop()
                    all.append(words)
                    words=[]
                    words.append(lis)
                elif before=="O" and label_1=="I":
                    words=[]
            all.append(words)
            # print(all)
            for needs in all:
                w=[]
                offset = []
                end = []
                if len(needs)!=0:
                    label=needs[0][-1].split('-')[-1]
                
                    for ww in needs:
                        if ww[-1]=="O":
                            break
                        w.append(ww[0])
                        offset.append(ww[1])
                        end.append(ww[2])    
                    if len(w)!=0:
                        # print(''.join(w),offset[0],end[-1],label)
                        wf.write("{}\t{}\t{}\t{}\n".format(''.join(w),offset[0],end[-1],label))
def main():
    base_path = "CCKS_result"
    files = glob.glob("bio_ccks/*.tab")
    openfile = files[0]
    finall_files = glob.glob("CCKS_result/*.txt")
    # del_file(base_path)
    split_result(openfile)
    change_format(base_path)

if __name__=="__main__":
    main()
