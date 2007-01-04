# vim:fileencoding=utf-8
from buzhug import Base
from datetime import date,datetime
from database import contest_to_tr
from database import contest_detail_to_div
contests = Base('database/contest').open()

Include("Page.py")

vPool['Head'] = "Contests"
vPool['SectionName'] = "Contests"
vPool['SectionLink'] = '#'
vPool['PageName'] = "Contests"

if locals().has_key('_cid'):
    #print contests[int(_cid)]
    vPool['Main'] = contest_detail_to_div(contests[int(_cid)])
    vPool['moreCSS'] = '''
        <style type="text/css">
        div.contest h2.name {text-align:center}
        div.contest div.time {text-align:center}
        div.contest div.status {text-align:center}
        div.contest div.problems {text-align:center;padding-left:30%}
        div.contest div.problems ol li {text-align:left;}
        </style>
        '''
else:
    vPool['Main'] = '''
    <table class="table1">
    <tr>
    <th>Name</th><th>Start Time</th><th>End Time</th><th>Status</th>
    </tr>
    %s
    </table>
    ''' %"\n".join([contest_to_tr(rec) for rec in contests])


        
ShowPage()
