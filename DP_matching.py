###ファイルから数値データを抽出

import math
import glob
import numpy as np

def get_data(file_name):
    data=[]
    for file in glob.glob(file_name):
        with open(file,'r') as fin:
            mat=[]
            ##０フレームを入力
            mat.append([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
            content = fin.readlines()
            for line in content[3::]:
                row=[]
                toks=line.split()
                for tok in toks:
                    num=float(tok)
                    row.append(num)
                mat.append(row)
        data.append(mat)
    return data

data_tmp=[]
data_in=[]
data_tmp=get_data("city021/city021_*.txt")
data_in=get_data("city022/city022_*.txt")
##フレーム数はファイルのフレーム数＋１（０フレーム字を追加しているため）

count=0

test=1
collect=0

#テンプレート側の単語指定
for word_tmp in range(len(data_tmp)):
    t_min=10000
    t_min_word=0
    check_tmp=word_tmp
    #入力側の単語指定
    for word_in in range(len(data_in)):
        d=[]    ##局所距離を一時的に格納する
        g=[]        

##局所距離を纏めて計算する
        for word_d_tmp in range(len(data_tmp[word_tmp])):
            d_youso=[]    ##行ごとに局所距離を格納する
            for word_d_in in range(len(data_in[word_in])):    
                d_n=0
                for youso in range(15):
                    
                    e=data_tmp[word_tmp][word_d_tmp][youso]-data_in[word_in][word_d_in][youso]
                    e=e**2
                    d_n+=e
                    
                d_n=math.sqrt(d_n)
                d_youso.append(d_n)
            d.append(d_youso)
            
        check=1
##それを基に累積距離を計算する
        for word_g_tmp in range(len(data_tmp[word_tmp])):
            g_row=[]
            for word_g_in in range(len(data_in[word_in])):
                ##初期
                if word_g_in==0 and word_g_tmp==0:
                    g_now=0.0
                    g_row.append(g_now)
                ##(上辺)
                elif word_g_tmp==0 and word_g_in!=0:
                    g_now=g_row[word_g_in-1]+d[0][word_g_in]
                    g_row.append(g_now)
                ##（左端）
                elif word_g_in==0 and word_g_tmp!=0:
                    g_now=g[word_g_tmp-1][0]+d[word_g_tmp][0]
                    g_row.append(g_now)


                else:
                    ##斜め
                    if g[word_g_tmp-1][word_g_in]+d[word_g_tmp][word_g_in] > g[word_g_tmp-1][word_g_in-1]+1*d[word_g_tmp][word_g_in] and g_row[word_g_in-1]+d[word_g_tmp][word_g_in] > g[word_g_tmp-1][word_g_in-1]+1*d[word_g_tmp][word_g_in]:
                        g_now=g[word_g_tmp-1][word_g_in-1]+1*d[word_g_tmp][word_g_in]
                        g_row.append(g_now)
                    
                    ##横
                    elif g[word_g_tmp-1][word_g_in]+d[word_g_tmp][word_g_in] > g_row[word_g_in-1]+d[word_g_tmp][word_g_in] and g[word_g_tmp-1][word_g_in-1]+1*d[word_g_tmp][word_g_in] > g_row[word_g_in-1]+d[word_g_tmp][word_g_in]:
                        g_now=g_row[word_g_in-1]+d[word_g_tmp][word_g_in]
                        g_row.append(g_now)                    
                    ##縦
                    elif g[word_g_tmp-1][word_g_in-1]+1*d[word_g_tmp][word_g_in] > g[word_g_tmp-1][word_g_in]+d[word_g_tmp][word_g_in] and g_row[word_g_in-1]+d[word_g_tmp][word_g_in] > g[word_g_tmp-1][word_g_in]+d[word_g_tmp][word_g_in]:
                        g_now=g[word_g_tmp-1][word_g_in]+d[word_g_tmp][word_g_in]
                        g_row.append(g_now)

            g.append(g_row)
        t=g[len(data_tmp[word_tmp])-10][len(data_in[word_in])-10]/(len(data_tmp[word_tmp])-1+len(data_in[word_in])-1)
        if t_min > t:
            t_min=t
            t_min_word=word_in
            
    
    if t_min_word==word_tmp:
        collect+=1

    print(word_tmp)
    print(t_min_word)
    print("----------")
    test+=1

print("正解率は",collect,"%")
