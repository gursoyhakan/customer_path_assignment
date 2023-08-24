# -*- coding: utf-8 -*-
#kodun amaci kisisellestirilmis harita uretip bunu k-shortest path ile cozmektir.
import copy
import time
import math
mustsay=10
k_num=1
BIGNUM=9999999
nodenum=721
#bu fonksiyon edgelerin uzunluklarini hesapliyor
def hesapla(mustnum,basact,basday,sonact,sonday):
    pjk=copy.deepcopy(pjikdata[mustnum][:])
    chrn=copy.deepcopy(churndata[mustnum][:])
    pj=constantpjik
    ch=constantchurn
    a=b=c=d=e=0
    if pjk[4]=="" or pjk[4]==" ":
        a=-0.6197
    elif pjk[4]<=2:
        a=-0.6169
    elif pjk[4]<=19:
        a=-0.3316
    elif pjk[4]<=36:
        a=-0.1382
    if pjk[5]==0:
        b=1.087
    elif pjk[5]<=16:
        b=1.049
    elif pjk[5]<=18:
        b=0.8145
    elif pjk[5]<=20:
        b=0.5527
    elif pjk[5]<=21:
        b=0.4382
    elif pjk[5]<=22:
        b=0.3136
    elif pjk[5]<=23:
        b=0.2088
    elif pjk[5]<=24:
        b=0.1033
    if pjk[6]<=0:
        c=0.2552
    elif pjk[6]<=1:
        c=0.2151
    elif pjk[6]<=2:
        c=0.0611
    if pjk[7]==0:
        d=-0.7335
    elif pjk[7]<=0.25:
        d=-0.4973
    elif pjk[7]<=0.6:
        d=-0.37
    elif pjk[7]<=0.75:
        d=-0.2916
    elif pjk[7]<=0.83:
        d=-0.101
    else: d=-0.2605
    if pjk[8]==1:
        d=-3.37091
    elif pjk[8]==2:
        e=1.486384
    elif pjk[8]==3:
        e=0.643362
    elif pjk[8]==4:
        e=0.37012
    elif pjk[8]==5:
        e=-0.1508
    elif pjk[8]==6:
        e=-0.41893
    elif pjk[8]==7:
        e=-0.74992
    elif pjk[8]==8:
        e=-0.93868
    elif pjk[8]==9:
        e=-1.27795
    elif pjk[8]==10:
        e=-1.4673
    elif pjk[8]==11:
        e=-2.00688
    pj+=-0.1407*sonday-1.313*pjk[1]+5.641*pjk[2]+0.2386*actions[sonact][1]+a+b+c+d+e
    pj=math.exp(pj)
    pj=pj/(1+pj)
    pj=1-pj
    #pj=math.log(pj)
    if chrn[2]==0:
        a=4.974
    elif chrn[2]==2:
        a=3.583
    elif chrn[2]==3:
        a=2.938
    elif chrn[2]==4:
        a=2.291
    elif chrn[2]==6:
        a=1.361
    if chrn[3]<=1:
        b=0.4236
    if chrn[4]<=0.016:
        c=0.4387
    elif chrn[4]<=0.026:
        c=0.3608
    elif chrn[4]<=0.037:
        c=0.3130
    elif chrn[4]<=0.084:
        c=0.1438
    else:
        c=0.6738
    if chrn[6]<=407:
        d=1.4820
    elif chrn[6]<=552:
        d=1.1360
    elif chrn[6]<=1214:
        d=1.0110
    elif chrn[6]<=2471:
        d=0.6365
    elif chrn[6]<=4385:
        d=0.3936
    if chrn[7]=="KK":
        e=-2.118
    elif chrn[7]=="KMH":
        e=-1.766
    else:
        e=0
        
    ch+=0.02829*chrn[0]+0.000305*chrn[1]+a+b+c+d+e
    ch=math.exp(ch)
    ch=ch/(1+ch)

    return [pj,ch]
time1=time.gmtime()

f=open("pjik.csv","r")
i=0
pjikdata=[]
for line in f:
    k=line.split(";")
    if i<mustsay+1 and i>0:
        if(k[5]==""):k[5]=0;
        if(k[4]==""):k[4]=0;
        if(k[3]==""):k[3]=0;
        if(k[7]==""):k[7]=0;
        if(k[19]==""):k[19]=0;
        if(k[9]==""):k[9]=0;
        pjikdata.append([float(k[1]),float(k[2]),float(k[6]),float(k[9]),float(k[3]),float(k[4]),float(k[5]),float(k[7]),float(k[19])])
        '''yukaridaki siralama kisisel veri olarak, 
        CAD_LAST_ACTION_DELAY_DAY, 
        CAD_LAD_COLLECTION_PERIODS_3MONTHS
        TOPLAM_ODEME_ORANI_3M
        TOTAL_SEVERITY_NEW
        CAD_CUST_DELAY_DAY_FROM_PREV_EXIT
        BEFORE_LAST_ACTION_DATE_RATING_TTC
        SE_MEMZUC_ACCRUAL_OF_INTEREST_TERM_NUM_LAST_3
        CAD_CUST_FIRST_20D_EXIT_RATE_6M
        DUAL_SUCCESS_FAIL_ACTION_NUM_7D
'''

    i+=1
f.close()
f=open("churn.csv","r")
i=0
churndata=[]
for line in f:
    k=line.split(";")
    if i<mustsay+1 and i>0: 
        if(k[29]==""):k[29]=0;
        if(k[25]==""):k[25]=0;
        if(k[24]==""):k[24]=0;
        if(k[10]==""):k[10]=0;
        if(k[22]==""):k[22]=0;
        if(k[2]==""):k[2]=0;
        if(k[16]==""):k[16]=0;
        for j in ([2,10,16,22,24,25,29]):
            k[j]=float(k[j])
        churndata.append([k[29],k[25],k[24],k[10],k[22],k[2],k[16],k[82][:-2 ]])
        '''yukaridaki siralama kisisel veri olarak, 
        SUCCESS_ACTION_NUM_14D, 
        TOTAL_SEVERITY_NEW,
        URUN_AKTIF_ADET,
        CAD_LAD_DELAYED_PRODUCTS_COUNT,
        BEFORE_LAST_ACTION_DATE_SCORE_TTC,
        CAD_LAST_ACTION_DELAY_DAY, 
        CAD_LAD_CUST_DELAY_RISK_AMOUNT,
        CAD_PRODUCT,
'''
    i+=1
f.close()
constantchurn=-4.679
constantpjik=-4.201    
actions=[[0,0],['SMS1',3],['IVN1',6.5],['SMS2',8.5],['IVN2',10.5],['SMS3',12],['IVN3',13.25],['SMS4',14.5],['CCT4',16],['SMS5',15.5],['CCT5',19],['SMS6',16.25],['CCT6',20.5]]
mustpaths=[[[]]for i in range(mustsay)]
f=open("kshortestpathsonuc.txt","w")                    
#buradan itibaren her musteri icin k-shortest path yapiliyor.
#oncelikle harita hesaplaniyor musteri icin
print(time1)
for musteri in range(mustsay):
    edges={}
    for i in range(1,13):
        for j in range(1,61):
            edges[0,0,i,j]=hesapla(musteri,0,0,i,j)
            edges[i,j,0,61]=hesapla(musteri,i,j,0,61)
            for k in range(1,13):
                    for t in range(1,61):
                        if (k>=i)and (t-j>=3):
                            edges[i,j,k,t]=hesapla(musteri,i,j,k,t)
                        else:
                            edges[i,j,k,t]=(BIGNUM,0)
    edges[0,0,0,61]=hesapla(musteri,0,0,0,61)
    time2=time.gmtime()
    print(time2,musteri)
#bu noktadan itibaren ilgili musteri icin k-shortest path yapiliyor
    weight1={}
    weight2={}
    for i in range(1,13):
      for j in range(1,61):
        weight1[0,(i-1)*60+j]=edges[0,0,i,j][0]  
        weight1[(i-1)*60+j,nodenum]=edges[i,j,0,61][0]
        weight2[0,(i-1)*60+j]=edges[0,0,i,j][1]  
        weight2[(i-1)*60+j,nodenum]=edges[i,j,0,61][1]
        for k in range(1,13):
           for t in range(1,61): 
               weight1[(i-1)*60+j,(k-1)*60+t]=edges[i,j,k,t][0]
               weight2[(i-1)*60+j,(k-1)*60+t]=edges[i,j,k,t][1]
    weight1[0,nodenum]=edges[0,0,0,61][0]
    weight2[0,nodenum]=edges[0,0,0,61][1]  
    outs=[[] for i in range(nodenum+1)]
    for i in range(nodenum):
       for j in range(1,nodenum+1):
           if (weight1[i,j]<BIGNUM):
               outs[i].append(j)
    priorityQ=[0]
    distances=[BIGNUM for i in range(nodenum+1)]
    distances[0]=0
    visited=[0 for i in range(nodenum+1)]
    parent=[i for i in range(nodenum+1)]
    while priorityQ!=[]:
        pivot=priorityQ[0]
        priorityQ.remove(pivot)
        visited[pivot]=1
        for i in outs[pivot]:
            if visited[i]!=1:
                if i not in priorityQ:
                    priorityQ.append(i)
            if distances[i]>distances[pivot]+weight1[pivot,i]:
                distances[i]=distances[pivot]+weight1[pivot,i]
                parent[i]=pivot
        if priorityQ!=[]:
                i=0
                while i<len(priorityQ):
                    if distances[priorityQ[0]]>distances[priorityQ[i]]:
                        priorityQ[0],priorityQ[i]=priorityQ[i],priorityQ[0]
                    i+=1    
    i=nodenum
    mainpath=[]
    while i!=0:
        mainpath.append(i)
        i=parent[i]
    mainpath.append(0)
    mainpath.reverse()
    mainedge=[]
    for i in range(len(mainpath)-1):
      mainedge.append([copy.deepcopy(weight1[mainpath[i],mainpath[i+1]]),mainpath[i],mainpath[i+1]])
    mainedge.sort()
    k=0
    mainedges=[]
    mainedges.append(copy.deepcopy(mainedge))
    time2=time.gmtime()
    print(time2,musteri,"-disjktras over")
    for k in range(k_num-1):
        newpaths="a"
        newpaths=[]
        mainedge1=copy.deepcopy(mainedges[k])
        for edge in mainedge1:
            originalweight=weight1[edge[1],edge[2]]
            weight1[edge[1],edge[2]]=BIGNUM
            priorityQ1=[0]
            distances1=[BIGNUM for i in range(nodenum+1)]
            distances1[0]=0
            visited1=[0 for i in range(nodenum+1)]
            parent1=[i for i in range(nodenum+1)]
            while priorityQ1!=[]:
                pivot1=priorityQ1[0]
                priorityQ1.remove(pivot1)
                visited[pivot1]=1
                for i in outs[pivot1]:
                    if visited1[i]!=1:
                        if i not in priorityQ1:
                            priorityQ1.append(i)
                    if distances1[i]>distances1[pivot1]+weight1[pivot1,i]:
                        distances1[i]=distances1[pivot1]+weight1[pivot1,i]
                        parent1[i]=pivot1
                if priorityQ1!=[]:
                        i=0
                        while i<len(priorityQ1):
                            if distances1[priorityQ1[0]]>distances1[priorityQ1[i]]:
                                priorityQ1[0],priorityQ1[i]=priorityQ1[i],priorityQ1[0]
                            i+=1    
            i=nodenum
            newpath=[]
            while i!=0:
                newpath.append(i)
                i=parent1[i]
            newpath.append(0)
            newpath.reverse()
            newpaths.append([distances1[-1],copy.deepcopy(newpath),edge])
            weight1[edge[1],edge[2]]=originalweight
        newbest="b"
        newbest=[]
        ind=newpaths.index(min(newpaths))
        for i in range(len(newpaths[ind][1])-1):
          newbest.append([copy.deepcopy(weight1[newpaths[ind][1][i],newpaths[ind][1][i+1]]),newpaths[ind][1][i],newpaths[ind][1][i+1]])
        newbest.sort()
        weight1[mainedge1[ind][1],mainedge1[ind][2]]=BIGNUM
        mainedges.append(copy.deepcopy(newbest))
        time2=time.gmtime()
        print(time2,musteri," k part over" )

    for i in mainedges:
      top=0
      for j in i:
          top+=j[0]
      f.write(str(musteri))
      f.write("-")
      f.writelines(str(top))
      
f.close()