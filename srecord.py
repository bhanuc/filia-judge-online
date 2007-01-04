# vim:fileencoding=utf-8

Include("Page.py")

vPool['Head'] = "Solve Problems"
vPool['SectionName'] = "Problems"
vPool['SectionLink'] = 'browse'
vPool['PageName'] = "Solve Record"



sess = Session();
try:
    uid = sess.user_id
except AttributeError:
    uid = ""
try:
    uid = uid = THIS.path.split('?',1)[1]
except (ValueError,IndexError):
    pass

if uid == "":
    vPool['Main'] = "<p>Tell Me Who's Solve Record you Want to see</p>" + "<br/>" *11
else:         
    from database import submit_to_tr
    from buzhug import Base
    from datetime import date,datetime
    submit = Base('database/submit').open()
    rs = [item.problem_id for item in submit.select(['problem_id'],user_id = uid,status = 0)]
    rs = set(rs)
    if len(rs) == 0:
        vPool['Main'] = "<div>No Resolved Problems for this user <b>%s</b></div>" %uid
    else:
        vPool['Head'] = "Solved Problems For %s" %uid
        group_records = [[]] * ((len(rs)-1)/8 + 1)
        i = 0
        for record in rs :
            group_records[i/8].append(record)
            i = i + 1
        vPool['Main'] = "<br/> \n".join(["&nbsp;&nbsp;".join(["<a href='browse?pid=%d'>%d</a>" %(item,item) for item in gitem]) for gitem in group_records])
        vPool['Main'] = "<div>" + vPool['Main'] + "</div>"
    
ShowPage()
