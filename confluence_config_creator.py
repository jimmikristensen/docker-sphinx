import os
import sys
import glob

confluenceAuthPages='README:160465230,index:235012393'

def createPageString():
    pagesStr=''
    pages=confluenceAuthPages.split(',')

    for page in pages:
        pageParts = page.split(':');
        pageFile = pageParts[0]
        pageConfluenceId = pageParts[1]

        pageStr = "- id: %s\n  source: %s" % (pageConfluenceId, pageFile)
        if pagesStr != '':
            pagesStr = "%s\n%s" % (pagesStr, pageStr)
        else:
            pagesStr = pageStr

    return pagesStr

def createImagesString(imageDir):
    imagesStr = ''
    imageFiles = glob.glob(imageDir+'/*')
        
    if (len(imageFiles) > 0):
        imagesStr = "  attachments:"
        
    for imageFile in imageFiles:
        imagesStr = "%s\n  - %s" % (imagesStr, imageFile)

    return imagesStr

print createPageString()
print createImagesString('/Users/jikr/IdeaProjects/play-template-app/doc/sphinxdoc/build/json/_images')
if 'confluenceAuth' not in os.environ:
    sys.exit('Environment variable confluenceAuth is missing')

if 'confluenceAuthPages' not in os.environ:
    sys.exit('Environment variable confluencePages is missing')
