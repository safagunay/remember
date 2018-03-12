#-*- coding:utf-8 -*-
import sys
import os
from pathlib import Path
def parseargs(arglist):
    lines_to_del = []
    try:
        for e in arglist:
            if "-" in e:
                bounds = [ int(x) for x in e.split("-") ]
                if(len(bounds)>2): raise Exception
                bounds.sort()
                for i in range(bounds[0],bounds[1]+1):
                    lines_to_del.append(i)
            elif int(e) > 0:
                lines_to_del.append(int(e))
            else: raise Exception
    except:
        sys.stderr.write("err: invalid arguments\n")
        sys.exit(-1)
    lines_to_del.sort()
    return lines_to_del

if(__name__=="__main__"):
    
    PATH = "{}/remember.txt".format(str(Path.home()))
    opt = ""
    infile = 0
    line_number = 0
    if(len(sys.argv)>1):
        opt = sys.argv[1]
    else:
        sys.exit(0)
    if(opt=="-p"):
        if(os.path.exists(PATH)):
            try:
                with open(PATH,"r") as f:
                    lines = f.readlines()
                    line_number = int ( lines[len(lines) - 1].split()[0] ) + 1
                infile = open(PATH,"a")
            except:
                sys.stderr.write("err: cannot access the file: %s\n" %PATH)
            else:
                if(len(sys.argv[2:])>0):
                    infile.write("%d %s\n" %
                    (line_number, " ".join(sys.argv[2:]) )
                    )
                    print ("successfuly written to %s" %PATH)
                else:
                    sys.stderr.write("err: no arguments spesified\n")
            finally:
                if infile:
                    infile.close()
        else: 
            sys.stderr.write("err: no such path exists: %s\n" %PATH)
    
    elif(opt=="-a"):
        infile = open(PATH,"r")
        print (infile.read())
        infile.close()
    
    elif(opt=="-r"):
        if(len(sys.argv[2:])>0):
            lines = []
            lines_to_del = parseargs(sys.argv[2:])
            with open(PATH,"r") as f:
                lines = f.readlines()
            if lines_to_del[len(lines_to_del)-1] > len(lines):
                sys.stderr.write("err : line number exceeds the max\n")
                sys.exit(-1)
            infile = open(PATH,"w")
            count = 1
            for line in lines:
                line_elements = line.split()
                if(len(line_elements)==0):
                    continue
                try:
                    if int(line_elements[0]) in lines_to_del:
                        print (" ".join(line_elements[0:]))
                    else:
                        infile.write("%d %s\n" %(count, " ".join(line_elements[1:])))
                        count += 1
                except:
                    infile.write("%s\n" %(" ".join(line_elements)))
                    
            infile.close()
        else: 
            sys.stderr.write("err: no arguments spesified\n")

    elif(opt=="-e"):
        os.system("xed {}".format(PATH))
        
    else:
        if(os.system("grep -i '{}' {}".format(opt,PATH)) != 0):
            print ("no value found in %s" %PATH)

