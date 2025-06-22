import os as os
import subprocess
import logging
logging.basicConfig(level=logging.INFO)

print("\n",20*"%")
print("This code will merge and analyze observations \n" \
      "of X-ray sources. This code cannot work in \n" \
      "parallel, so consider manually running img_merger \n" \
      "to allow for parallelization. This code will not \n" \
      "overwrite merged exposure maps.")
print(20*"%","\n")

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
    choiceREG = "n"

mode = input("Which mode do you want to process? [pc/wt/both]: ")

# choice2 = input("Manual value entry? [y/n]: ")
choice2 = input("What signal-to-noise limit would you like? [0 - n]: ")

try:
    choice2 = abs(int(choice2))
except:
    choice2 = 3

choice3 = input("Are these 4FGL objects? [y/n]: ")
if choice3 == "y" or choice3 == "Y":
    choice3 = "y"
    choice4 = "y"
else:
    choice3 = "n"
    choice4 = input("Do you want to use TestWithin to locate specfic sources? [y/n]: ").lower()
    if choice4 != "y": choice4 = "n"

cmd  =f"python {xrt_path}evt_merger.py {specpath} {choice1} {mode} \n"
cmd += f"python {xrt_path}img_merger.py {specpath} n n \n"
cmd += f"python {xrt_path}ximage_detect.py {specpath} {choice1} \n"
cmd += f"python {xrt_path}det_analysis.py {specpath} {choice3} {choice4} {choice1} {choice2} \n"
cmd += f"python {xrt_path}region_gen.py {specpath} {choiceREG} {choiceREG} \n"
cmd += f"python {xrt_path}xsel_step.py {specpath} {choice1} 1 \n"
cmd += f"python {xrt_path}xspec_step.py {specpath} {choice1} y n"

os.system(cmd)


# if choice1 == "y":
#     cmd  =f"python {xrt_path}evt_merger.py {specpath} y \n"
#     cmd += "python "+xrt_path+"img_merger.py "+specpath+" n n \n"
#     cmd += "python "+xrt_path+"obs_time.py "+specpath+" \n"
#     cmd += "python "+xrt_path+"ximage_detect.py y y "+specpath+" \n"
#     cmd += "python "+xrt_path+"det_analysis.py "+choice3+" y "+specpath+" \n"
#     print(cmd)
#     os.system(cmd)
#     # raise ValueError("STOP2")
#     cmd = "python "+xrt_path+"find_sig_dets.py "+specpath+" "+str(choice2)+"\n"
#     # print(cmd)
#     # os.system(cmd)
#     # if choice2 == "y":
#     #     cmd = "python "+xrt_path+"find_sig_dets.py\n"
#     # else:
#     #     cmd = "python "+xrt_path+"find_sig_dets.py "+specpath+" 6\n"
#     cmd += "python "+xrt_path+"region_gen.py "+choiceREG+" y "+specpath+" \n"
#     cmd += "python "+xrt_path+"xsel_step.py y "+specpath+" \n"
#     cmd += "python "+xrt_path+"xspec_step.py y y n "+specpath+" \n"
#     cmd += "python "+xrt_path+"xspec_reader.py y "+specpath+" \n"
#     print(cmd)
#     os.system(cmd)

# else:
#     # cmd  = "python "+xrt_path+"evt_merger.py "+specpath+" n \n"
#     # cmd += "python "+xrt_path+"img_merger.py "+specpath+" n n \n"
#     # cmd += "python "+xrt_path+"obs_time.py "+specpath+" \n"
#     # cmd += "python "+xrt_path+"ximage_detect.py n y "+specpath+" \n"
#     # cmd += "python "+xrt_path+"det_analysis.py n "+specpath+" \n"
#     # cmd += "python "+xrt_path+"find_sig_dets.py "+specpath+" \n"
#     # if choice2 == "y":
#     #     os.system(cmd)
#     # else:
#     #     os.system(cmd+"6 \n")
#     # cmd  = "python "+xrt_path+"region_gen.py n y "+specpath+" \n"
#     # cmd += "python "+xrt_path+"xsel_step.py n "+specpath+" \n"
#     # cmd += "python "+xrt_path+"xspec_step.py n y n "+specpath+" \n"
#     # cmd += "python "+xrt_path+"xspec_reader.py y "+specpath+" \n"

#     # os.system(cmd)

#     cmd  = "python "+xrt_path+"evt_merger.py "+specpath+" n \n"
#     cmd += "python "+xrt_path+"img_merger.py "+specpath+" n n \n"
#     cmd += "python "+xrt_path+"obs_time.py "+specpath+" \n"
#     cmd += "python "+xrt_path+"ximage_detect.py n y "+specpath+" \n"
#     cmd += "python "+xrt_path+"det_analysis.py "+choice3+" n "+specpath+" \n"
#     print(cmd)
#     os.system(cmd)

#     cmd = "python "+xrt_path+"find_sig_dets.py "+specpath+" "+str(choice2)+"\n"
#     # print(cmd)
#     # os.system(cmd)
#     # if choice2 == "y":
#     #     cmd = "python "+xrt_path+"find_sig_dets.py\n"
#     # else:
#     #     cmd = "python "+xrt_path+"find_sig_dets.py "+specpath+" 6\n"
#     cmd += "python "+xrt_path+"region_gen.py n n "+specpath+" \n"
#     cmd += "python "+xrt_path+"xsel_step.py n "+specpath+" \n"
#     cmd += "python "+xrt_path+"xspec_step.py n y n "+specpath+" \n"
#     cmd += "python "+xrt_path+"xspec_reader.py y "+specpath+" \n"
#     print(cmd)
#     os.system(cmd)
