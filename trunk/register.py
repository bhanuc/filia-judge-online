# vim:fileencoding=utf-8
#
from database import SameNameError

Include('Page.py')

vPool['moreJS'] ='''<script type="text/javascript" src="js/validation.js"></script>
                    <script type="text/javascript">
                        // 密码两此相同  ( from http://ajaxcn.org/comments/start/2006-05-22/1 ,thanks macrochen
                        Validation.add("validate-identical", "The value must be same as password filed.", function(v){
                            return !Validation.get('IsEmpty').test(v) && v == $F("password");
                        });
                        
                        //长度 4-15 
                        Validation.add('validate-length','Your input is too long or too short.',function (v){
                                    return !Validation.get('IsEmpty').test(v) && v.length>=4 && v.length<=15;
                        });      
                        Event.observe(window,'load',function(ev){var valid = new Validation('register', {immediate : true});});
                    </script>          
                  '''
vPool['moreCSS'] = '''  <style>
                        .validation-advice {
                            font-size: 8pt;
                            color : #3366FF;
                        }
                        </style>
                    '''
vPool['Head'] = "Register"
vPool['SectionName'] = "Member"
vPool['SectionLink'] = '#'
vPool['PageName'] = "Register"
vPool['Main'] = '''
        <form action="#" id="register" name="register" method="post" class="f-wrap-1">
        <fieldset>
        
        <!--h3>Form title here</h3-->
        
        <label for="user_id" ><b>User Id:</b>
           <input id="user_id" name="user_id" type="text" class="f-name required validate-alphpnum" /><br />
        </label>
        <label for="nick_name"><b>Nick Name:</b>
           <input id="nick_name" name="nick_name" type="text" class="f-name" /><br />
        </label>         
        <label for="password"><b>Password:</b>
           <input type="password" id="password" name="password" class="required validate-length"/><br/>
        </label>
        <label for="con_password"><b>Confirm Password:</b>
           <input type="password" id="con_password" name="con_password" class="required validate-identical"/><br/>
        </label>    
        <label for="email"><b>E-Mail:</b>
           <input id="email" name="email" class="required validate-email"/><br/>
        </label>             
        <div class="f-submit-wrap">
        <input type="submit" value="Submit" class="f-submit"  /><br />
        </div>
        </fieldset>
        </form>

'''
        
try:
    from buzhug import Base
    from datetime import date
    users = Base('database/user').open()
    result_set = users.select(['user_id'],user_id=_user_id)
    if len(result_set) > 0:
        raise SameNameError,{'field':'user_id','value':_user_id}
    new_user = users.insert(user_id=_user_id,password=_password,nick_name=unicode(_nick_name,'utf-8'),email=_email)
    vPool['Main'] =  "<p>Success, Thank you for register.</p>" + "<br/>"*11
except IndexError,e:
     vPool['Main'] =  "<p>Failed. " + e.message + "</p>"+ "<br/>"*11
except SameNameError,e:
    vPool['Main'] =  "<p>Failed. " + e.message + "</p>"+ "<br/>"*11
except NameError,e:
    pass
    #print type(e)
    #print e.message


ShowPage()