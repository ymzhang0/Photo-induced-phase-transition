def get_vbm_cbm(nele, nk, nband, eigen, ibzkt): 
    kinfo = []
    V = []
    C = []
    for i in range(nk):
        kinfo.append(eigen[7+i*(nband+2)].split())
        V.append(float(eigen[7+int(nele/2)+i*(nband+2)].split()[1]))
        C.append(float(eigen[7+1+int(nele/2)+i*(nband+2)].split()[1]))

    vbm = max(V)
    k_vbm = kinfo[V.index(max(V))]
    cbm = min(C)
    k_cbm = kinfo[C.index(min(C))]
    return [vbm ,cbm]

def get_weight(nk, ibzkt):
    weight = []
    for i in range(nk):
        weight.append(int(ibzkt[3+i].split()[3]))
    return weight

def str2int(list_):
    list1 = []
    for i in list_:
        list1.append(float(i))
    list_ = list1
    return list_

def eigen_normalize(nk, nband, eigen):
    eigen_normalize = []
    for i in range(nk):
        value_temp = [] 
        for j in range(nband):
            value_temp.append(eigen[8+j+i*(nband+2)].split()[1])
            value_temp = str2int(value_temp)
        eigen_normalize.append(value_temp)
    return eigen_normalize

def eigen_merge(eigen_normalize,nele):
    eigen_merge_v = []
    eigen_merge_c = []
    for i in eigen_normalize:
        for j in i[0 : int(nele/2)]:
            eigen_merge_v.append(j)
    for i in eigen_normalize:        
        for j in i[int(nele/2) : len(i)]:
            eigen_merge_c.append(j)
    return [eigen_merge_v, eigen_merge_c]

def find_k(nband, nele, nele_ex, eigen_merge_v, eigen_merge_c):
    k_ex_index_c = []
    k_ex_index_v = []
    if nele_ex == 0:
        print('no excitation')
    else:
        for i in range(nele_ex):
            index_v = eigen_merge_v.index(max(eigen_merge_v))
            eigen_merge_v[index_v] = min(eigen_merge_v)
            index_v = index_v // int(nele/2)
            k_ex_index_v.append(index_v)
            

            index_c = eigen_merge_c.index(min(eigen_merge_c))
            eigen_merge_c[index_c] = max(eigen_merge_c)
            index_c = index_c // int(nband-nele/2)
            k_ex_index_c.append(index_c)
            
            
    return [k_ex_index_c, k_ex_index_v]        


def FERWE(k_c, k_v, weight, nband, nele, nele_ex, nk):     
    k_v1 = []
    k_c1 = []
    count = 0
    for i in k_v:
        if count < nele_ex:
            k_v1.append(i)
        else:
            break
        count = count + weight[i]

    count = 0
    for i in k_c:
        if count < nele_ex:
            k_c1.append(i)
        else:
            break
        count = count + weight[i]
        
    k_v1_la = k_v1[-1]
    k_v1.pop()
    k_v1.sort()
    k_c1_la = k_c1[-1]
    k_c1.pop()
    k_c1.sort()

    FERWE = list(range(nk))
    count_v = 0
    count_c = 0
    for i in k_v1:
        count_v = count_v + weight[i]
    for i in k_c1:
        count_c = count_c + weight[i]
        
    for i in range(nk):
        if i != k_v1_la:
            if i in k_v1:
                FERWE[i] = str(int((nele/2)-k_v1.count(i)))+'*'+'1'+' '+str(k_v1.count(i))+'*'+'0'
            else:
                FERWE[i] = str(int(nele/2))+'*'+'1'
        else:
            FERWE[i] = str(int(nele/2)-k_v1.count(i)-1)+'*'+'1'+' '+'1'+'*'+str(1-(nele_ex-count_v)/weight[i])+' '+str(k_v1.count(i))+'*'+'0'
            
     

    for i in range(nk):
        if i != k_c1_la:
            if i in k_c1:
                 FERWE[i] = FERWE[i] +' '+str(k_c1.count(i))+'*'+'1'+' '+str(int(nband-nele/2-k_c1.count(i)))+'*'+'0'
            else:
                 FERWE[i] = FERWE[i] +' '+str(int(nband-nele/2))+'*'+'0'
        else:
            FERWE[i] = FERWE[i]+ ' '+str(k_c1.count(i))+'*'+'1'+' ' +'1'+'*'+str((nele_ex-count_c)/weight[i])+' '+ str(nband-(nele/2)-k_c1.count(i)-1)+'*'+'0'
    
    return [FERWE, k_v1_la, k_c1_la, k_v1, k_c1,count]
        

def fermi_find(k_v1_la, k_c1_la, k_v1, k_c1, eigen_normalize, nele):
    num_v = k_v1.count(k_v1_la)
    num_c = k_c1.count(k_c1_la) 
    ef_v = eigen_normalize[k_v1_la][int(nele/2 - num_v - 1)]
    ef_c = eigen_normalize[k_c1_la][int(nele/2 + num_c )]
    quasi_fermi = abs(ef_v-ef_c)
    return [ef_v, ef_c, quasi_fermi]
        
        
if __name__=='__main__':            
    print('tools')
