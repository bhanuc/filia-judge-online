# vim:fileencoding=utf-8

Include("Page.py")


vPool['Head'] = "Login"
vPool['SectionName'] = "Member"
vPool['SectionLink'] = '#'
vPool['PageName'] = "Login"
vPool['Main'] = '''
         <form action="#" method="post" class="f-wrap-1">
         <fieldset>
         
         <!--h3>Form title here</h3-->
         
         <label for="user_id"><b>User Id:</b>
         <input id="user_id" name="user_id" type="text" class="f-name" /><br />
         </label>
         
         <label for="password"><b>Password:</b>
         <input type="password" id="password" name="password"/><br/>
         </label>
         
         <div class="f-submit-wrap">
         <input type="submit" value="Submit" class="f-submit"  /><br />
         </div>
         </fieldset>
         </form>
         <br/><br/><br/><br/><br/><br/>
'''


#always  trys to do login ,if an NameError exception is catched 
#the login page is shown to the user
try:
    from buzhug import Base
    from datetime import date
    users = Base('database/user').open()
    the_user = users.select(user_id = _user_id)[0]
    #print the_user
    if the_user.password == _password:
        vPool['Main'] = "<p>Sucesss. You have login as %s </p>" %(the_user.user_id,) + "<br/>" *11
        session=Session()
        session.user_id = _user_id
        raise HTTP_REDIRECTION, "index"
    else:
        vPool['Main'] = "<p>Failed. Please Check Your UserId and Password </p>" + "<br/>" *11
except IndexError,e:        #user not exists
    vPool['Main'] = "<p>Failed. User %s doesn't exists</p>" %(_user_id,) + "<br/>" *11
except NameError,e:
    pass


ShowPage()

