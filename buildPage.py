import glob
import os
from dominate import document
from dominate.tags import *

def writeWebPage(fullpath):
    images = [os.path.basename(x) for x in reversed(glob.glob(fullpath + '/*.svg'))]
    data = [name.strip('.svg') + '.dat' for name in images]

    with document(title='') as doc:
        h1('')
        for path in images:
            item = span(_class='plot', style="border:1px solid gray; display:inline-block;")
            item.add(img(src=path))
            item.add(pre(path.strip('.svg')))

    with open(fullpath +'/index.html', 'w') as f:
        f.write(doc.render())
