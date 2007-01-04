# vim:fileencoding=utf-8

Include("Page.py")

vPool['Head'] = "Running Status"
vPool['SectionName'] = "Problems"
vPool['SectionLink'] = 'browse'
vPool['PageName'] = "Runs Status"

vPool['moreMeta'] = '<META HTTP-EQUIV="REFRESH" CONTENT=20>\n'

sess = Session()

try:
    argument = THIS.path.split('?',1)[1]
    #print argument
    if argument == "pre":
        sess.page = sess.page - 1
    elif argument == "next":
        sess.page = sess.page + 1
    elif argument == "first"        :
        sess.page = 1
    else:
        sess.page   #no change
    #print sess.page
except (NameError,AttributeError,IndexError):
    sess.page = 1    
        
from database import submit_to_tr
from buzhug import Base
from datetime import date,datetime
submit = Base('database/submit').open()
num_per_page = 20 #current put it here
begin = len(submit)- num_per_page * sess.page
if begin < 0:
    begin = 0
end = begin + num_per_page
if end > len(submit):
    end = len(submit)
    
lastest_record  = list(submit)[begin:]
lastest_record.reverse()
   
vPool['Main'] = '''
        <table class="table1" >
        <!--thead>
            <tr>
                <th colspan="9">Runns Status</th>
            </tr>
        </thead-->
        <tbody>
            <tr>
            <th>ID</th>
            <th>User ID</th>
            <th>Problem ID</th>
            <th>Status</th>
            <th>Language</th>
            <th>Code</th>
            <!--<th>Time</th>-->
            <!--<th>Memory</th>-->
            <th>Submit Time</th>
            </tr>
        ''' +\
        "\n".join([submit_to_tr(rec) for rec in lastest_record]) +\
        '''
        </tbody>
        </table>
        [<a href="status?first">First Page</a>]  [<a href="status?pre">Previous Page</a>]  [<a href="status?next">Next Page</a>]
        '''


#except AttributeError,e:
#    pass
    
ShowPage()
