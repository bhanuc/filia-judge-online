# vim:fileencoding=utf-8
from buzhug import Base
from datetime import date,datetime
from database import problem_to_tr
Include("Page.py")
def show_all():
    '''show all problem sets'''
    problem = Base('database/problem').open()
    vPool['Main'] = '''
            <p>Currently, we only have a few test problems.</p>
            <table class="table1" >
            <!--thead>
                <tr>
                    <th colspan="9">Problems</th>
                </tr>
            </thead-->
            <tbody>
                <tr>
                <th>Problem ID</th>
                <th>Title</th>
                <th>Ratio (AC/SUBMIT)</th>
                <!--<th>Added Date</th>-->
                </tr>
                %s
            </tbody>
            </table>
            <!--[<a href="browse?first">First Page</a>]  [<a href="browse?pre">Previous Page</a>]  [<a href="browse?next">Next Page</a>]-->
            ''' % '\n'.join([problem_to_tr(rec) for rec in problem])
            
vPool['Head'] = "Browse The Problem Sets"
vPool['SectionName'] = "Problems"
vPool['SectionLink'] = 'browse'
vPool['PageName'] = "Browse"

try:

    desc = file("ProblemSet/%s/desc.txt" %_pid).read()
    vPool['Main'] = '''
                <pre>%s</pre>
                <br/>
                <div><a href="submit?pid=%s">Submit Your Answer</a>
                &nbsp;&nbsp;&nbsp;<a href="discuss?pid=%s">Discuss This Problem</a></div>
                ''' %(desc,_pid,_pid)
except (TypeError,ValueError,IndexError,NameError):
    #print "TYPE ERROR"
    show_all()
except IOError:
    vPool['Main'] = '''
                <p>No Such Problem.</p>
                '''
    
ShowPage()






