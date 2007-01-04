# vim:fileencoding=utf-8

Include("Page.py")


vPool['Head'] = "个人信息"
vPool['SectionName'] = "Member"
vPool['SectionLink'] = '#'
vPool['PageName'] = "个人信息"

sess = Session()
    
 

try:
    try:
        uid = THIS.path.split('?',1)[1]
        other  = True
    except (ValueError,IndexError):
        other = False
        uid = sess.user_id
    from buzhug import Base
    from datetime import date
    users = Base('database/user').open()
    the_user = users.select(user_id = uid)[0]
    if other:
        vPool['Main'] = "He/She is " + the_user.nick_name  + "<br/>" *11 
    else:
        vPool['Main'] = "You are " + the_user.nick_name + "<br/>" *11
except IndexError,e:        #user not exists
    vPool['Main'] = "<p>User %s doesn't exists</p>" %(uid,) + "<br/>" *11
except (AttributeError,NameError):
    vPool['Main'] = "<p>Tell Me Who you Want to see</p>" + "<br/>" *11


ShowPage()


    