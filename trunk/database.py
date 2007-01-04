# vim:fileencoding=utf-8
from buzhug import Base
from datetime import date,datetime

def build_problem():
    try:
        print "Build the problem Database........"
        problem = Base('database/problem')
        problem.create(('problem_id',str),('title',unicode),('time_limit',int),('memory_limit',int),("source",unicode))
        print "Done." 
    except IOError:
        print "Error. problem Database  Already Exists"
    problem = Base('database/problem').open()
    print "Data in problem "
    for record in problem :
        print record.title.encode('utf-8')
    print "Done"
        
    
def build_relation():    #problem and contest relationship
    try:
        contest = Base('database/contest')
        problem = Base('database/problem')
        print "Build the relation Database........"
        relation = Base('database/relation')
        relation.create(('contest',contest),('problem',problem))
        print "Done." 
    except IOError:
        print "Error. relation Database  Already Exists"
        print "OR contest ,problem database not exists"
    relation = Base('database/relation').open()
    print "Data in relation "
    for record in relation :
        print record.contest.name.encode('utf-8'),record.problem.title.encode('utf-8')
    print "Done"

def build_contest():
    try:
        print "Build the Contest Database........"
        contest = Base('database/contest')
        contest.create(('name',unicode),('start',datetime),('end',datetime),('status',int),('holder',str))
        print "Done." 
    except IOError:
        print "Error. Contest Database  Already Exists"
    print "Set String Format"
    contest.set_string_format(unicode,'utf-8')
    print "Done"
    contest = Base('database/contest').open()
    print "Data in contest "
    #print len(users)
    for record in contest :
        print record.name.encode('utf-8')
    print "Done"

def build_user():
    try:
        print "Build the User Database........"
        users = Base('database/user')
        users.create(('user_id',str),('password',str),('nick_name',unicode),('email',str))
        print "Done." 
    except IOError:
        print "Error. User Database  Already Exists"
    print "Set String Format"
    users.set_string_format(unicode,'utf-8')
    print "Done"
    users = Base('database/user').open()
    print "Data in user "
    print len(users)
    for record in users :
       #print "id:" + record.id,
       print "user_id:" + record.user_id
       print "nick_name:" + record.nick_name.encode('gb2312')   # why gb2312
       #users.delete(record)
    print "Done"
    
def build_submit():
    try:
        print "Build the Submit Record Database........"
        submit = Base('database/submit')
        submit.create(('user_id',str),('problem_id',int),('lang',str),('code',unicode),('status',int),('more',unicode),('codelen',int),('time',int),('memory',int),('stime',datetime))
        print "Done." 
    except IOError:
        print "Error. Submit Database  Already Exists"
    print "Set String Format"
    submit.set_string_format(unicode,'utf-8')
    submit.set_string_format(date,'%Y-%m-%d')
    submit.set_string_format(datetime,'%Y-%m-%d %H:%M:%S')    
    print "Done"
    print "Data in submit "
    submit = Base('database/submit').open()
    for record in submit :
       print record.__id__,record.problem_id,record.lang,record.status
    print "Done"         
    
def build_article():
    try:
        print "Build the Article Database........"
        article = Base('database/article')
        article.create(('problem_id',int),('thread_id',int),('user_id',str),('reply',int),('title',unicode),('content',unicode),('ptime',datetime))
        print "Done." 
    except IOError:
        print "Error. Article Database  Already Exists"
    print "Set String Format"
    article.set_string_format(unicode,'utf-8')
    article.set_string_format(date,'%Y-%m-%d')
    article.set_string_format(datetime,'%Y-%m-%d %H:%M:%S')    
    print "Done"
    print "Data in article "
    article = Base('database/article').open()
    for record in article :
       print record.problem_id,record.thread_id,record.reply
    print "Done"       
     
def get_max(db,field):
    fs = [getattr(record,field) for record in db]
    if len(fs) == 0:
        return 0
    else:
        return max(fs)
        
    
class SameNameError(Exception):
    '''Raise This Exception Where try to insert to database with a same name'''
    def __init__(self,dict):
        Exception.__init__(self)
        self.field = dict['field']
        self.value = dict['value']
        self.message = "Already Exisits an Entry with %s = %s " %(self.field,self.value)


def problem_to_tr(rec):
    '''Convert an problem record to a tr'''
    ret = ['<tr>']
    ret.append('<td>%s</td>' %rec.problem_id)
    ret.append('<td><a href="browse?pid=%s">%s</a></td>' %(rec.problem_id,rec.title.encode('utf-8')))
    submit = Base('database/submit').open()
    submit_num = len(submit.select(problem_id= int(rec.problem_id)))
    ac_num = len(submit.select(problem_id= int(rec.problem_id),status = 0))
    try:
        rat = ac_num*100.0/submit_num
    except ZeroDivisionError:
        rat = 0.00
        
    ret.append('<td>%2.2f (%d/%d)</td>' %(rat,ac_num,submit_num))
    ret.append('</tr>\n')
    return '\n'.join(ret)


#SUBMIT_STATUS.
status_desc = ["ACCEPT","COMPLIER ERROR","RUNTIME ERROR","TIME OUT","WRONG ANSWER","INNER ERROR","WAIT FOR JUDGE"]

def submit_to_tr(rec):
    '''Convert an submit record to a tr '''
    # @param rec submit record 
    # @return a string contains an <tr> with the infomation of the record
    #
    ret = ["<tr>"]
    ret.append("<td>%d</td>" % rec.__id__)
    ret.append("<td><a href='member?%s'>%s</a></td>" % (rec.user_id,rec.user_id))
    ret.append("<td><a href='browse?pid=%d'>%d</a></td>" % (rec.problem_id,rec.problem_id))
    if rec.status == 1:
        ret.append("<td><a href='more?sid=%d' target='_blank'>%s</a></td>" % (rec.__id__,status_desc[rec.status]))
    else:
        ret.append("<td>%s</td>" % status_desc[rec.status])
    ret.append("<td>%s</td>" % rec.lang)
    ret.append("<td>%dB</td>" % len(rec.code))  #or rec.codelen
    #ret.append("<td>%s</td>" % rec.time)
    #ret.append("<td>%s</td>" % rec.memory)
    ret.append("<td>%s</td>" % str(rec.stime))  
    ret.append("</tr>")
    return "\n".join(ret)

def thread_to_tr(rec):
    '''Convert the information about an thread into a tr'''
    ret = ["<tr>"]
    ret.append("<td><a href='discuss?tid=%d'>%s</a></td>" % (rec.thread_id,rec.title.encode('utf-8')))
    ret.append("<td>%s</td>" % rec.user_id)
    ret.append("<td>%d</td>" % rec.reply)
    ret.append("<td>%s</td>" % str(rec.last_reply))
    ret.append("</tr>")
    return "\n".join(ret)

def article_to_div(rec):
    '''Convert the information about an thread into a tr'''
    if rec.reply < 0:
        atype = "reply"
    else:
        atype = "topic"
    ret = ["<div class='%s'>" %atype]
    ret.append("<div class='title'>%s</div>" % rec.title.encode('utf-8'))
    ret.append("<span class='authortime'><a href='member?%s'>%s</a>&nbsp;&nbsp;%s</span><br/>" % (rec.user_id,rec.user_id,str(rec.ptime)))
    ret.append("<pre>%s</pre><br/>" % rec.content.encode('utf-8'))
    ret.append("</div>")
    return "\n".join(ret)   
 
def article_to_textarea(rec):
    '''Convert the information about an thread into a tr'''
    if rec.reply < 0:
        atype = "reply"
    else:
        atype = "topic"
    ret = ["<div class='%s'>" %atype]
    ret.append("<div class='title'>%s</div>" % rec.title.encode('utf-8'))
    ret.append("%s&nbsp;&nbsp;" % rec.user_id)
    ret.append("%s<br/>" % str(rec.ptime))
    ret.append("<textarea readonly wrap=off rows='20' cols='100'>%s</textarea><br/>" % rec.content.encode('utf-8'))
    ret.append("</div>")
    return "\n".join(ret)  

def user_to_html(user,option = {}):
    '''Convert an user record to an form (for update info) or an table (for view info)'''
    # @param user an record of user
    # @param option an dictionary with possible key-value ['update':true/false,'showemail':true/false]
    if not option.has_key('update'):
        option['update'] = False
    if not option.has_key('showemail'):
        option['showemail'] = False
    from Cheetah.Template import Template as ctTpl
    if option['update']:
        ret = '''<form>
        
        </form>
        '''
    page = open("template/index.html","r").read()
    txp = ctTpl(page, searchList=[vPool])         

contest_status = ["Running","Scheduled","Ended"]
def contest_to_tr(rec):
    ret = ["<tr>"]
    ret.append("<td><a href='contest?cid=%d'>%s</td>" %(rec.__id__,rec.name.encode('utf-8')))
    ret.append("<td>%s</td>" %rec.start)
    ret.append("<td>%s</td>" %rec.end)
    ret.append("<td>%s</td>" %contest_status[rec.status])
    ret.append("</tr>")
    return "\n".join(ret)

def contest_detail_to_div(rec):
    curr = datetime(1,1,1).now()
    if curr > rec.end:
        status = contest_status[2]
    elif curr <rec.start:
        status = contest_status[1]
    else:
        status = contest_status[0]

    ret = ["<div class='contest'>"]
    ret.append("<h2 class='name'>%s</h2>" %rec.name.encode('utf-8'))
    ret.append("<div class='time'>Start:%s &nbsp; End:%s</div>" %(rec.start,rec.end))
    ret.append("<div class='status'>Current:%s &nbsp; Status:%s</div> " %(datetime(1,1,1).now(),status))
    ret.append("<div class='problems'>")
    ret.append("<ol>")
    relation = Base('database/relation').open()
    problems = [item.problem for item in relation if item.contest.__id__ == rec.__id__]
    for problem in problems:
        ret.append("<li><a href='browse?pid=%s'>%s</a></li>" %(problem.problem_id,problem.title.encode('utf-8')))
    ret.append("</ol>")
    ret.append("</div>")
    ret.append("</div>")    
    return '\n'.join(ret)



def add_problems_contest():
    problems = Base('database/problem').open()
    relation = Base('database/relation').open()
    cont= Base('database/contest').open()[0]
    #relation.insert(problem=problems[0],contest=cont)
    relation.insert(problem=problems[1],contest=cont)
    relation.insert(problem=problems[2],contest=cont)
    relation.insert(problem=problems[3],contest=cont)
    relation.insert(problem=problems[4],contest=cont)
    relation.insert(problem=problems[5],contest=cont)
    
def add_problems():
    problem = Base('database/problem').open()
    problem.insert(problem_id = "1002",title=unicode("Dividing","utf-8"),time_limit=1000,memory_limit=10000)
    problem.insert(problem_id = "1003",title=unicode("Simple Addition","utf-8"),time_limit=1000,memory_limit=10000)
    problem.insert(problem_id = "1004",title=unicode("Is There Any Prefix ?","utf-8"),time_limit=1000,memory_limit=10000)
    problem.insert(problem_id = "1005",title=unicode("Smith Number","utf-8"),time_limit=1000,memory_limit=10000)
    problem.insert(problem_id = "1006",title=unicode("洗牌","utf-8"),time_limit=1000,memory_limit=10000)
    
#   contest = Base('database/contest').open()
#   current = datetime(1,1,1).now()
#   end_time = datetime(current.year,current.month,current.day,current.hour+2,current.minute)
#   contest.insert(name=unicode("My First Contest",'utf-8'),start=current,end = end_time,status=0)

if __name__ == "__main__":
    #add_problems()
    add_problems_contest()
    #build_problem()
    build_relation()
    #problem = Base('database/problem').open()
    #problem.insert(problem_id = "1001",title=unicode("A+B Problem","utf-8"),time_limit=1000,memory_limit=10000)
    #build_contest()
    pass