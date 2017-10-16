import glob
import os
from dominate import document
from dominate.tags import *

def writeWebPage(fullpath):
    images = [os.path.basename(x) for x in reversed(glob.glob(fullpath + '/*.svg'))]

    with document(title='') as doc:
        h1('')
        for path in images:
            span(img(src=path), _class='image')

    with open(fullpath +'/index.html', 'w') as f:
        f.write(doc.render())
