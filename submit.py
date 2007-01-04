# vim:fileencoding=utf-8

Include("Page.py")
try:
    problem_id = _pid
except (NameError):
    problem_id = ""

vPool['Head'] = "Submit Your Answer"
vPool['SectionName'] = "Problems"
vPool['SectionLink'] = 'browse'
vPool['PageName'] = "Submit"
vPool['Main'] = '''
         <form action="#" method="post" class="f-wrap-1">
         
         <div class="req"><b>*</b> Indicates required field</div>
         
         <fieldset>
         
         <!--h3>Form title here</h3-->
         
         <label for="problem_id"><b><span class="req">*</span>Problem Id:</b>
         <input id="problem_id" name="problem_id" type="text" class="f-name" value="%s"/><br />
         </label>
         
         <label for="lang"><b><span class="req">*</span>Programming Language:</b>
         <select id="lang" name="lang" >
         <option>Select...</option>
         <option>C</option>
         <option>C++</option>
         <option>Java</option>
         </select>
         <br />
         </label>
         
         
         <label for="code"><b><span class="req">*</span>Code:</b>
         <textarea id="code" name="code" wrap="off" class="f-code" rows="20" cols="50" ></textarea>
         <br />
         </label>
         
         <div class="f-submit-wrap">
         <input type="submit" value="Submit" class="f-submit"  /><br />
         </div>
         </fieldset>
         </form>
''' %(problem_id,)

sess = Session()

try:
    from buzhug import Base
    from datetime import date,datetime
    submit = Base('database/submit').open()
    now = datetime(1,1,1)
    record_id = submit.insert(user_id = sess.user_id, problem_id = int(_problem_id),lang = _lang, code = unicode(_code,'utf-8'),stime = now.today(), status=6)
    vPool['Main'] = \
        '''<p>Success! Your Submit Record Id is %d</p>
           <p>You will be notified when the result comes out.<br>
              You can also get the result in <a href="status">status page</a></p>
        '''%(record_id,) + "<br/>" * 9
    if not hasattr(sess,'just_submit'):
        sess.just_submit = [(record_id,_problem_id,'Waiting')]
    else:
        sess.just_submit.append((record_id,_problem_id,'Waiting'))
except AttributeError,e:
    vPool['Main'] = "<p>Not Login</p>" + "<br/>" *11
except NameError,e:
   pass


ShowPage()
