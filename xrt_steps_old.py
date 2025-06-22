import os as os

#os.system("export HEADASNOQUERY= \nexport HEADASPROMPT=/dev/null")
startpath="/Users/kdn5172/Desktop/"
startpath=os.getcwd()+"/"#"/Users/kdn5172/Desktop/"
#print("CWD: "+os.getcwd())
os.chdir(startpath)

os.system("ls -d */")

specpath=input("Enter data directory: ")
totpath=startpath+specpath
os.chdir(totpath)
os.chdir(startpath)

# xrt_path = startpath+"xrt_code/"
xrt_path = startpath+"code_xrt/"

choice1 = input("Overwrite all files? [y/n]: ")

if choice1 == "Y" or choice1 == "y":
    choice1 = "y"
    choiceREG = input("Overwrite region files too? [y/n]: ")
    if choiceREG == "Y" or choiceREG == "y":
        choiceREG = "y"
    else:
        choiceREG = "n"
else:
    # choice1 = input("Overwrite some files? [y/n]: ")
    # if choice1 == "Y" or choice1 == "y":
    #     choice1 = "manual"
    # else:
    choice1 = "n"

# choice2 = input("Manual value entry? [y/n]: ")
choice2 = input("What signal-to-noise limit would you like? [0 - n]: ")

try:
    choice2 = abs(int(choice2))
except:
    choice2 = 3

choice3 = input("Are these 4FGL objects? [y/n]: ")
if choice3 == "y" or choice3 == "Y":
    choice3 = "y"
else:
    choice3 = "n"
     

# if choice2 == "Y" or choice2 == "y":
#     choice2 = "y"
# else:
#     choice2 = "n"

# cmd = "python "+xrt_path+"evt_merger.py "+specpath+" y \n"
# print(cmd)
# os.system(cmd)

if choice1 == "y":
    cmd  = "python "+xrt_path+"evt_merger.py "+specpath+" y \n"
    cmd += "python "+xrt_path+"img_merger.py "+specpath+" n n \n"
    cmd += "python "+xrt_path+"obs_time.py "+specpath+" \n"
    cmd += "python "+xrt_path+"ximage_detect.py y y "+specpath+" \n"
    cmd += "python "+xrt_path+"det_analysis.py "+choice3+" y "+specpath+" \n"
    print(cmd)
    os.system(cmd)
    # raise ValueError("STOP2")
    cmd = "python "+xrt_path+"find_sig_dets.py "+specpath+" "+str(choice2)+"\n"
    # print(cmd)
    # os.system(cmd)
    # if choice2 == "y":
    #     cmd = "python "+xrt_path+"find_sig_dets.py\n"
    # else:
    #     cmd = "python "+xrt_path+"find_sig_dets.py "+specpath+" 6\n"
    cmd += "python "+xrt_path+"region_gen.py "+choiceREG+" y "+specpath+" \n"
    cmd += "python "+xrt_path+"xsel_step.py y "+specpath+" \n"
    cmd += "python "+xrt_path+"xspec_step.py y y n "+specpath+" \n"
    cmd += "python "+xrt_path+"xspec_reader.py y "+specpath+" \n"
    print(cmd)
    os.system(cmd)

else:
    # cmd  = "python "+xrt_path+"evt_merger.py "+specpath+" n \n"
    # cmd += "python "+xrt_path+"img_merger.py "+specpath+" n n \n"
    # cmd += "python "+xrt_path+"obs_time.py "+specpath+" \n"
    # cmd += "python "+xrt_path+"ximage_detect.py n y "+specpath+" \n"
    # cmd += "python "+xrt_path+"det_analysis.py n "+specpath+" \n"
    # cmd += "python "+xrt_path+"find_sig_dets.py "+specpath+" \n"
    # if choice2 == "y":
    #     os.system(cmd)
    # else:
    #     os.system(cmd+"6 \n")
    # cmd  = "python "+xrt_path+"region_gen.py n y "+specpath+" \n"
    # cmd += "python "+xrt_path+"xsel_step.py n "+specpath+" \n"
    # cmd += "python "+xrt_path+"xspec_step.py n y n "+specpath+" \n"
    # cmd += "python "+xrt_path+"xspec_reader.py y "+specpath+" \n"

    # os.system(cmd)

    cmd  = "python "+xrt_path+"evt_merger.py "+specpath+" n \n"
    cmd += "python "+xrt_path+"img_merger.py "+specpath+" n n \n"
    cmd += "python "+xrt_path+"obs_time.py "+specpath+" \n"
    cmd += "python "+xrt_path+"ximage_detect.py n y "+specpath+" \n"
    cmd += "python "+xrt_path+"det_analysis.py "+choice3+" n "+specpath+" \n"
    print(cmd)
    os.system(cmd)

    cmd = "python "+xrt_path+"find_sig_dets.py "+specpath+" "+str(choice2)+"\n"
    # print(cmd)
    # os.system(cmd)
    # if choice2 == "y":
    #     cmd = "python "+xrt_path+"find_sig_dets.py\n"
    # else:
    #     cmd = "python "+xrt_path+"find_sig_dets.py "+specpath+" 6\n"
    cmd += "python "+xrt_path+"region_gen.py n n "+specpath+" \n"
    cmd += "python "+xrt_path+"xsel_step.py n "+specpath+" \n"
    cmd += "python "+xrt_path+"xspec_step.py n y n "+specpath+" \n"
    cmd += "python "+xrt_path+"xspec_reader.py y "+specpath+" \n"
    print(cmd)
    os.system(cmd)
