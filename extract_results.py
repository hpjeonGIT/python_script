import os
import sys                                                          
import time
import numpy as np
import shutil
from subprocess import call


def extract_data():
    #
    # crack length results
    params = []
    with open('params.txt', 'r') as f:
        for line in f:
            params.append(line)
    i = 0
    while i < len(params):
        word = params[i].split()
        if 'sheet_thk' == word[0]:
            y0 = float(word[2])/2.0
        if 'crack_pos_x' == word[0]:
            x0 = float(word[2])
        if 'crack_length' == word[0]:
            cl_list = word[2].split(',')
        if 'crack_angle_deg' == word[0]:
            deg_list = word[2].split(',')
        i += 1
    
    cl_sum = 0; xf = x0; yf = y0
    for a,b in zip(cl_list,deg_list):
        #print(a,b)
        cl_sum += float(a)
        xf += float(a)*np.cos(float(b)*np.pi/180.)
        yf += float(a)*np.sin(float(b)*np.pi/180.)
    #
    # K1/K2/Cpd results
    Cpd_list = []; K1_list = []; K2_list = []; J_list = []; 
    K1disp_list = []; K2disp_list = []
    try:
        with open('Output-Togepi0.dat', 'r') as f:
            for line in f:
                word = line.split()
                if (len(word) > 4):
                    if (word[0]=='Cpd' and word[1]=='0' and word[3]=='1'):
                        Cpd_list.append(float(word[4]))
                    if (word[0]=='K1' and word[1]=='0' and word[3]=='1'):
                        K1_list.append(float(word[4]))
                    if (word[0]=='K2' and word[1]=='0' and word[3]=='1'):
                        K2_list.append(float(word[4]))
                    if (word[0]=='J' and word[1]=='0' and word[3]=='1'):
                        J_list.append(float(word[4]))
                    if (word[0]=='K1disp' and word[1]=='0' and word[3]=='0'):
                        K1disp_list.append(float(word[4]))
                    if (word[0]=='K2disp' and word[1]=='0' and word[3]=='0'):
                        K2disp_list.append(float(word[4]))
        return np.mean(K1_list), np.std(K1_list), np.mean(K2_list), \
            np.std(K2_list), np.mean(J_list), np.std(J_list), \
            np.mean(Cpd_list), np.std(Cpd_list), xf, yf, cl_sum,\
            np.mean(K1disp_list), np.mean(K2disp_list)
    except IOError:
        print("Error - cannot open Output-Togepi0.dat")
        print(str(os.getcwd()))
        return []

if __name__=="__main__":
    target_folder = []
    CWD = os.getcwd()
    if len(sys.argv)> 1:
        DEST = sys.argv[1]
    else:
        DEST = os.getcwd()

    print("DEST folder = ", DEST)
    f0_list = []
    for subds, dirs, files in os.walk(DEST):
        for d0 in dirs:
            if len(d0) > 3:
                if (d0[0:3] == 'rid'):
                    target_folder.append(d0)
                    
    ##
    pic_file = 'partition_crack0.png'
    pic_folder = 'GIF'
    try:
        os.makedirs(pic_folder)
    except IOError:
        print(pic_folder, " exists")
    
    target_folder.sort()
    mean_K1  = []; std_K1 = []
    mean_K2  = []; std_K2 = []
    mean_J   = []; std_J  = []
    mean_Cpd = []; std_Cpd = []
    list_rid = []
    list_xf  = []; list_yf  = []
    list_cl  = []; list_K1disp = []; list_K2disp = []
    for dirname in target_folder:
        rid = int(dirname[3:])
        os.chdir(DEST+'/'+dirname)
        try:
            shutil.copy2(pic_file,'../'+pic_folder+'/'+dirname+'.png')
        except OSError:
            print(pic_file, " doesn't exisit")
        ans = extract_data()
        if (len(ans) > 0):
            list_rid.append(rid)
            mean_K1.append(ans[0])
            std_K1.append(ans[1])
            mean_K2.append(ans[2])
            std_K2.append(ans[3])
            mean_J.append(ans[4])
            std_J.append(ans[5])
            mean_Cpd.append(ans[6])
            std_Cpd.append(ans[7])
            list_xf.append(ans[8])
            list_yf.append(ans[9])
            list_cl.append(ans[10])
            list_K1disp.append(ans[11])
            list_K2disp.append(ans[12])
    os.chdir(CWD+'/'+pic_folder)
    call_result = call("convert -delay 50 -loop 0 rid*.png ani.gif", shell=True)
    os.chdir(CWD)
    with open('harvest_results.dat','w') as f:
        f.write('# rid, K1, cov_K1, K1_disp, K2, cov_K2, K2_disp, Cpd, cov_Cpd, K1_max, crack_length\n')
        for a,k1m, k2m,cpdm,cl,k1s,k2s,cpds,k1d,k2d in zip(
            list_rid, mean_K1, mean_K2, 
            mean_Cpd, list_cl, 
            std_K1,std_K2,std_Cpd, 
            list_K1disp, list_K2disp):
            theta = cpdm*np.pi/180.
            if (abs(k1m) < 1.e-10):
                cov_k1 = -9999.
            else:
                cov_k1 = k1s/k1m
            if (abs(k2m) < 1.e-10):
                cov_k2 = -9999.
            else:
                cov_k2 = k2s/k2m
            if (abs(cpdm) < 1.e-10):
                cov_cpd = -9999.
            else:
                cov_cpd = cpds/cpdm
            K1_max = 0.5*np.cos(theta/2.)*(k1m*(1.+np.cos(theta))
                                           -3.*k2m*np.sin(theta))
            f.write("%d, %.4e, %.4e, %.4e, %.4e, %.4e, %.4e, %.3f, %.3e, %.3e, %.3e\n"
                    %(a,k1m, cov_k1, k1d, k2m, cov_k2, k2d, cpdm, cov_cpd, 
                      K1_max, cl))

