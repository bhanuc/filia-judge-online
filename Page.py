# vim:fileencoding=utf-8

#简化引用对象名
from Cheetah.Template import Template as ctTpl
vPool = {}
vPool['moreMeta'] = ""
vPool['moreJS'] = ""
vPool['moreCSS'] = ""
vPool['Head'] = "Welcome To Filia's Judge Online"
vPool['status'] = '''
    Click Here to <a href="login">Login</a> or <a href="register">register</a>
'''
vPool['SubmitStatus'] = ""
vPool['SectionName'] = "Main"
vPool['PageName'] = "Welcome"
vPool['SectionLink'] = '#'
vPool['Main'] = '''
            <p>
                这个站点是一个在线裁判系统.<br/>
                采用Python开发,基于<a target="_blank" href="http://karrigell.sourceforge.net/">Karrigell</a>框架.<br/>
                页面基于HTML/CSS模板系统<a target="_blank" href="http://www.mollio.org">mollio</a>.<br/>
                更对信息请点击<a href="ppt/">这里</a><br/>
            </p><br/><br/><br/><br/><br/><br/><br/><br/><br/>
'''

def ShowPage():
    sess = Session()
    try:
        vPool['status'] = '''Welcome %s.<a href="logout">[logout]</a>&nbsp;<a href="member">[member]</a>''' %(sess.user_id,)
#        vPool['SubmitStatus'] = '\n'.join(['''<li>Problem ID:%s&nbsp;<span class="result" id="result_%d">%s</span></li>''' %(item[1],item[0],item[2]) for item in sess.just_submit])
#        vPool['SubmitStatus'] = vPool['SubmitStatus'] + \
#            '''
#            <script type="text/javascript" src="js/utils.js"></script>
#            <script type="text/javascript"> 
#            function update_all()
#            {
#                update = [];
#                %s
#                update.each( function(id){
#                   fetch_result(id,"result_"+id); 
#                });
#            }
#            Event.observe(window, 'load',update_all, false);
#            </script>
#            ''' %('\n'.join(["update.push(%d);" %(item[0]) for item in sess.just_submit]))
    except Exception,e:
        #print e
        pass
    page = open("template/index.html","r").read()
    txp = ctTpl(page, searchList=[vPool])
    print txp    
    
def check_problem():
    #just if the problem exsits
    return True
    