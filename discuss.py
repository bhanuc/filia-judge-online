# vim:fileencoding=utf-8
from buzhug import Base
from datetime import date,datetime
from database import thread_to_tr
from database import get_max
from database import article_to_div
from database import article_to_textarea
article = Base('database/article').open()

Include("Page.py")

vPool['Head'] = "Forum"
vPool['SectionName'] = "Forum"
vPool['SectionLink'] = 'discuss'
vPool['PageName'] = "Welcome"

#vPool['Main'] = "<p>Discuss is not avaiable currently</p>"
#vPool['Main'] = ""
sess = Session()

now = datetime(1,1,1)

#always try to add new article
if hasattr(sess,'user_id'):
    uid = sess.user_id
else:
    uid = "Anonymous"
    
    
try:
    if locals().has_key('_newtopic'):
       newtid = get_max(article,'thread_id') + 1
       article.insert(problem_id = int(_problem_id),thread_id = newtid, 
                      user_id = uid, title = unicode(_title,'utf-8'),
                      content = unicode(_con,'utf-8'),reply = 0,ptime = now.today())
       vPool['Main'] = vPool['Main'] + "<div>%s</div>" %("Success Add New Topic.")
    elif locals().has_key('_newreply'):
        pid = article.select(thread_id = int(_thread_id))[0].problem_id
        #print _con
        article.insert(problem_id = pid,thread_id = int(_thread_id), 
                       user_id = uid,title = unicode("",'utf-8'),content = unicode(_con,'utf-8'),
                       reply = -1,ptime = now.today())
        
        update_article = article.select_for_update(thread_id = int(_thread_id))[0]
        article.update(update_article,reply = update_article.reply + 1)
        
except AttributeError,e:
    print e
        
    
        
if locals().has_key('_system'): #for system form  just set pid to 0
    _pid = 0
   
    
if locals().has_key('_tid'):
    articles = article.select(thread_id = int(_tid))
    articles.sort_by('+__id__')
    #print len(articles)
    vPool['Main'] = '''
        <div class="thread">
        %s
        </div>
        <h3>你的回应</h3>
        <form method="post">
          <input type="hidden" name="thread_id" value="%s"/>
          <input id="newreply" name="newreply" type="hidden" class="" value="1"/>
          <textarea id="con" name="con" wrap="off" class="f-code" rows="10" cols="40" ></textarea><br />      
          <input type="submit" value="Submit" class="f-submit" /><br />
        </form>
        ''' %('\n'.join([article_to_div(rec) for rec in articles]),_tid)
    
    vPool['moreCSS'] = vPool['moreCSS'] + '''
        <style type="text/css">
            div.thread{
                
            }
            div.thread div.topic span.authortime{
                background-color: rgb(238, 255, 238);
            }
            div.thread div.reply span.authortime{
                background-color: rgb(238, 255, 238);
            }            
            div.thread div.topic{
                padding-left:5px;
            }
            div.thread div.topic div.title{
                font-size:16px;
                font-weight:bold;
            }            
            div.thread div.reply{
                padding-left:30px;
            }            
        </style>'''
    
    
elif locals().has_key('_pid'):
    def add_last_reply(th):
        replys = article.select(thread_id = th.thread_id)
        replys.sort_by('-__id__')
        th.last_reply = replys[0].ptime
        #return th
    def get_key(th):
        return th.last_reply
    if _pid == "":
        _pid = 0
    if int(_pid) > 0:
        vPool['Head'] = "Forum For Problem %s" %_pid
    else:
        vPool['Head'] = "System Forum"
    threads = [record for record in article if record.problem_id == int(_pid) and record.reply >=0]
    #print len(threads)
    for thread in threads  :
        add_last_reply(thread)
    threads.sort(key=get_key,reverse=True)
    #print len(threads)
    #articles = article.select(problem_id = _pid,reply = 0)  
    #articles.sort_by('-thread_id')
    if len(threads) > 0:
        vPool['Main'] = '''
            <table class="table1">
            <tr>
                <th>话题</th>
                <th>作者</th>
                <th>回应</th>
                <th>最后回应</th>
            </tr>
            %s
            </table>
            <br/>
            '''%("\n".join([thread_to_tr(thread) for thread in threads]))
    else:
        vPool['Main'] = "<p>目前没有话题</p>"
    vPool['Main'] = vPool['Main'] + \
    '''<div onclick="javascript:document.getElementById('newthread').style.display='block';document.getElementById('title').focus();">开启新话题</div>
    <br/>
    <form action="#" id="newthread" name="newthread" method="post" class="f-wrap-1"  style="display:none">
    <fieldset>
        <h3>New Thread </h3>
        <label for="title"><b>Title:</b>
           <input id="title" name="title" type="text" class="f-name" /><br />
        </label>         
        <label for="con"><b>Content:</b>
          <textarea id="con" name="con" wrap="off" class="f-code" rows="10" cols="40" ></textarea><br />
        </label>          
        <div class="f-submit-wrap">
            <input type="submit" value="Submit" class="f-submit" /><br />
        </div>
    </fieldset>
    <input id="problem_id" name="problem_id" type="hidden" class="" value="%s"/>
    <input id="newtopic" name="newtopic" type="hidden" class="" value="1"/>
    </form>'''%(_pid)
else:
    vPool['Main'] = '''
    <div>
    如果您有关于题目的问题，请输入题目编号转到相关论坛.<br/>
    <form method="get">
    <input name="pid" type="text"></input> &nbsp;&nbsp;<input type="submit" value="Go">
    </form>
    如果你有网站使用的问题，或者对我们有任何的建议或意见，请点<a href="discuss?system">这里</a>.
    </div><br/><br/><br/><br/><br/><br/>
    '''
ShowPage()
