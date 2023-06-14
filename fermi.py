import math
from tools import get_vbm_cbm, get_weight, str2int, eigen_normalize, eigen_merge, find_k, FERWE, fermi_find

nele_ex = input('number of exciting electrons: ')
nele_ex = int(nele_ex)
EIGENVAL = open('EIGENVAL','r')
IBZKT = open('IBZKPT','r')
eigen = EIGENVAL.readlines()
ibzkt = IBZKT.readlines()
[nele, nk, nband] = eigen[5].split()
[nele, nk, nband] = [int(nele), int (nk), int(nband)]

[vbm, cbm] = get_vbm_cbm(nele,nk,nband,eigen,ibzkt) 
weight = get_weight(nk, ibzkt) 
eigen_normalize = eigen_normalize(nk, nband, eigen) 
[eigen_merge_v, eigen_merge_c] = eigen_merge(eigen_normalize, nele)
[k_c, k_v] = find_k(nband, nele, nele_ex, eigen_merge_v, eigen_merge_c)
[FERWE, k_v1_la, k_c1_la, k_v1, k_c1,count] = FERWE(k_c, k_v, weight, nband, nele, nele_ex, nk)
[ef_v, ef_c, quasi_fermi] = fermi_find(k_v1_la, k_c1_la, k_v1, k_c1, eigen_normalize, nele)

print('\nFERWE_SETTING:')
count = 0
for i in FERWE:
        print(i,'   weight=', weight[count])
        count = count + 1

print('\nvbm = ', vbm, '  cbm = ', cbm, 'band gap = ', abs(vbm-cbm))
print('quasi_ef_v = ', ef_v, '  quasi_ef_c = ', ef_c, 'photon energy = ', quasi_fermi)

file=open('FERWE','w')
file.write(str(FERWE))
file.close()
