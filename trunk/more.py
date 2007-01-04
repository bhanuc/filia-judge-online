# vim:fileencoding=utf-8

from buzhug import Base
if not locals().has_key('_sid'):
    print "Tell Me Which Submission You Want to see."
else:
    submit = Base('database/submit').open()
    record = submit[int(_sid)]
    lang = ["unknow","shBrushUnknow.js"]
    if record.lang in ['C','C++']:
        lang = ["cpp","shBrushCpp.js"]
    #print record.lang
    if record.lang in ['Java']:
        lang = ['java',"shBrushJava.js"]
        
    print '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<!--
Copyright: Filia Tao (gudu2005@gmail.com) Chengjian (@)
License: Released Under the GPL 2
         http://www.gnu.org/copyleft/gpl.html
-->
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>View Source And Complier Error</title>
<link type="text/css" rel="stylesheet" href="js/highlighter/SyntaxHighlighter.css"></link>
<script type="text/javascript" src="js/highlighter/shCore.js"></script>
<script type="text/javascript" src="js/highlighter/%s"></script>
</head>
<body>
<h2>The Source Code </h2><br/>
<textarea id="sourcecode" name="sourcecode" class="%s">
%s
</textarea>
<script type="text/javascript">
dp.SyntaxHighlighter.HighlightAll('sourcecode');
</script>
<h3 name="error">Complier Error Infomation</h3><br/>
<pre>
%s
</pre>
</body>
</html>
''' %(lang[1],lang[0],record.code.encode('utf-8'),record.more.encode('utf-8'))


    