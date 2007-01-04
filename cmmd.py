# vim:fileencoding=utf-8
from buzhug import Base
from datetime import date,datetime

import string,os,time
import filecmp

subcode = Base('database/submit').open()
sleep_time = 5
ret =""
while True:
    unjudged = subcode.select_for_update(status = 6)
    if len(unjudged) == 0:
        print "No Unjudged Submit in database, sleep for %d second" %sleep_time
        time.sleep(sleep_time)
        continue
    for record in unjudged :
        try:
            print "Begin Test For SubmitId:%d ProblemID:%d " %(record.__id__,record.problem_id)
            temp=record.code
            type=record.lang    
            if(type=="C"):
                dealing=open('dealCode.c','w')
                dealing.write(temp.decode('utf-8'))
                dealing.close()        
                cmd='gcc dealCode.c -o result.exe -O  -ansi -fno-asm -Wall -lm -static '
            else:
                if(type=="C++"):#c++
                    dealing=open('dealCode.cpp','w')
                    dealing.write(temp.encode('utf-8'))
                    dealing.close()
                    cmd='g++ dealCode.cpp -o result.exe -O  -ansi -fno-asm -Wall -lm -static '
                        
            if(type=="Java"):#java
                dealing=open('Main.java','w')
                dealing.write(temp.decode('utf-8'))
                dealing.close()    
                cmd='javac -g:none Main.java '    
                
            print cmd
            #f = os.system(cmd,)
            #print f.read()
            compile_ret = os.system(cmd + " 2>error 1>tmp")
            if compile_ret != 0:
                compile_output =  file("error").read()
                ret={"ExitCode":1,"Desc":"COMPLIER ERROR","More":compile_output}
                print ret 
            else:       
                if type=="JAVA":
                    cmd="java Main <ProblemSet/%d/data.in 1>b.out 2>error "  %record.problem_id
                    #subcode.update(record,codelen=len(file("deal/Main.class").read()))
                else:
                    cmd='result.exe <ProblemSet/%d/data.in 1>b.out 2>error'  %record.problem_id
                    #subcode.update(record,codelen=len(file("result.exe").read()))
                    #print len(file("result.exe").read())
                print cmd
                
                run_ret = os.system(cmd)
                print run_ret 
                #if run_ret != 0:
                #    ret={"ExitCode":2,"Desc":"INNER ERROR"}
                #    print ret
                #else:
                if filecmp.cmp("b.out","ProblemSet/%d/data.out" %(record.problem_id)):
                    ret={"ExitCode":0,"Desc":"ACCEPT"}
                else:
                    ret={"ExitCode":4,"Desc":"WRONG ANSWER"}
                print ret
            print "End Test For SubmitId:%d ProblemID:%d " %(record.__id__,record.problem_id)
            print "**********************************************************"
            if not ret.has_key("More"):
                subcode.update(record,status=ret['ExitCode'])
            else:
                subcode.update(record,status=ret['ExitCode'],more = unicode(ret['More'],"utf-8"))
        except Exception,e:
            subcode.update(record,status=5)
            print e
            
        
                
        
                
        
                
        
                
        
        






                    