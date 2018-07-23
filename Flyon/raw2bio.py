#! /usr/bin python3
#-*-encoding:utf-8-*-
import glob
import jieba.posseg as psg
# jieba.load_userdict("result.txt")
import os
import codecs
import pickle
files1 = glob.glob("./train_data600/*.txtoriginal.txt")
files2 = glob.glob("./train_data600/*[0-9].txt")
files3 = glob.glob("./Bio_nolabel/*")
files4 = glob.glob("./Bio_label/*")
import sys
import gensim
agv = sys.argv[1]
flag=''
try:
    agv2 = sys.argv[2]
    print("Warning: 第二个参数必须是'test'!")
    flag = agv2
    files1 = glob.glob("./test_data400/*")
except Exception:
    flag = False
    pass
def cat_rawfile(file,flag):
    """
    对长文本用jiba进行分词。并标记位置和文件编号。存入nw_data文件夹。
    """
    drugs = []
    jiepou = []
    shoushu = []
    zhenzhaung = []
    with open("./CCKS_CRF/dic/drugs.txt",'r') as rf:
        for line in rf:
            line = line.strip()
            drugs.append(line)
    with open("./CCKS_CRF/dic/jiepou.txt",'r') as rf:
        for line in rf:
            line = line.strip()
            jiepou.append(line)

    with open("./CCKS_CRF/dic/shoushu.txt",'r') as rf:
        for line in rf:
            line = line.strip()
            shoushu.append(line)
    with open("./CCKS_CRF/dic/zhenzhaung.txt",'r') as rf:
        for line in rf:
            line = line.strip()
            zhenzhaung.append(line)
    n1_drug = jiepou+shoushu+zhenzhaung
    n2_jiepo = drugs+shoushu+zhenzhaung
    n3_zhengzhuang = drugs+shoushu+ jiepou
    n3_shoushu = drugs+zhenzhaung+ jiepou
    count=0
    name = os.path.basename(file)
    name_code = name.split('.')[0].split('-')[-1]
    if flag=="test":
        new_path = os.path.join("./CCKS_CRF/test_label_split/",name)
    else:
        new_path = os.path.join("./Bio_nolabel/",name)
    rf=codecs.open(file,encoding='utf8')
    wf = codecs.open(new_path,'w',encoding='utf8')
    dom = rf.read()
    result = psg.cut(dom)
    for ww in result:
        w = ww.word
        flag = ww.flag
        if w in drugs and w not in n1_drug:
            verbd = "dr"
        else:
            verbd = "Nd"
        if w in jiepou and w not in n2_jiepo:
            verbj = "jp"
        else:
            verbj = "Nj"
        if w in shoushu and w not in n3_shoushu:
            verbs = "ss"
        else:
            verbs = "Ns"
        if w in zhenzhaung and w not in n3_zhengzhuang:
            verbz = "zz"
        else:
            verbz = "Nz"

        if len(w)!=0:
            if w in ["。","?","!"]:
                wf.write(w +'\t'+flag+'\t'+verbd+'\t'+verbj+'\t'+verbs+'\t'+verbz+ '\t' +name_code+'\t'+ str(count) + '\t' + str(eval(end)+1) + '\n')
                wf.write('\n')
                count = eval(end)+1
            else:
                end=str(count+len(w))
                wf.write(w+'\t'+flag+'\t'+verbd+'\t'+verbj+'\t'+verbs+'\t'+verbz+'\t'+name_code+'\t'+str(count)+'\t'+end+'\n')
                count = eval(end)
        else:
            pass
    rf.close()
    wf.close()

def cat_labelfile(file):
    """
    对标注结果进行分词修改标签方式转成BIO格式。写入newlabel_data文件夹。
    """
    name = os.path.basename(file)
    new_path = os.path.join("./Bio_label/",name)
    rf=codecs.open(file,encoding='utf8')
    wf = codecs.open(new_path,'w',encoding='utf8')
    for line in rf:
        line_lis = line.strip().split('\t')
        word = line_lis[0]
        start = line_lis[1]
        label = line_lis[3]

        words= psg.cut(word)
        for i,w in enumerate(words):
            w = w.word
            if i==0:
                tag="B-"
                e = str(eval(start)+len(w))
            else:
                tag="I-"
                e=str(eval(start)+len(w))
            sentence=w+'\t'+start+'\t'+e+'\t'+tag+label+'\n'
            wf.write(sentence)
            start =str(eval(e))
    rf.close()
    wf.close()

def label2pickle(file4):
    """将标签与位置编码成字典的键值对，方便将标签整合到原始文件中去。"""
    basename = os.path.basename(file4)
    di = {}
    rf = codecs.open(file4, 'r', encoding='utf-8')
    wf= open("./label_pickle/"+basename+".pkl",'wb')
    for line in rf:
        line = line.strip()
        line_start = line.split('\t')[1]
        line_end = line.split('\t')[2]
        label = line.split('\t')[-1]
        end_and_label = line_end+"&"+label
        di[line_start]=end_and_label
    pickle.dump(di,wf)
    rf.close()
    wf.close()

def cat_file_label(file3,end_labeldi):
    """将原始文件与标签整合。"""
    basename = os.path.basename(file3)
    filename = basename.split('.')[0].split('-')[1]
    rf = codecs.open(file3,'r',encoding='utf-8')
    wf=codecs.open("./CCKS_CRF/BIO_ccks/"+basename,'w',encoding='utf-8')
    for line in rf:
        line_lis = line.strip().split('\t')
        try:
            word = line_lis[0]
            flag = line_lis[1]
            verbd = line_lis[2]
            verbj = line_lis[3]
            verbs = line_lis[4]
            verbz = line_lis[5]
            start = line_lis[7]
            end = line_lis[8]
            try:
                if end_labeldi[start]:
                    posible_label = end_labeldi[start]
                    trueend = posible_label.split("&")[0]
                    label = posible_label.split("&")[-1]
                    if end ==trueend:
                        wf.write(word+'\t'+flag+'\t'+verbd+'\t'+verbj+'\t'+verbs+'\t'+verbz+'\t'+filename+"\t"+start+"\t"+end+"\t"+label+"\n")
                    else:
                        wf.write(word +'\t'+flag+'\t'+verbd+'\t'+verbj+'\t'+verbs+'\t'+verbz+ '\t' +filename+"\t"+ start + "\t" + end + "\t" + "O"+"\n")
                else:
                    wf.write(word +'\t'+flag+'\t'+verbd+'\t'+verbj+'\t'+verbs+'\t'+verbz+ '\t' + filename+"\t"+start + "\t" + end + "\t" + "O"+"\n")
            except KeyError:
                wf.write(word +'\t'+flag+'\t'+verbd+'\t'+verbj+'\t'+verbs+'\t'+verbz+ '\t' +filename+"\t"+ start + "\t" + end + "\t" + "O"+"\n")
        except IndexError:
            wf.write("\n")
    wf.close()
    rf.close()

if agv == "-1":
    for file in files1:
        # cat_labelfile(file)
        cat_rawfile(file,flag)
# ###第二步(训练时候使用)
elif agv == "-2":
    for file in files2:
        cat_labelfile(file)
elif agv == "-3":
    for file in files4:
        label2pickle(file)
##第四步
elif agv == "-4":
    for file in files3:
        filename = os.path.basename(file)
        fil_ = filename.split('.')[0]+"."+filename.split('.')[2]
        ef = open("./label_pickle/"+str(fil_)+".pkl", 'rb')
        end_labeldi = pickle.load(ef, encoding='bytes')
        cat_file_label(file,end_labeldi)




