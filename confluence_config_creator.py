import os
import sys
import glob
'''
confluencePages='README:160465230,index:235012393'
confluenceUrl='https://tv2cms.atlassian.net/wiki'
baseDir='/doc/sphinxdoc/build/json'
configDir='/doc/sphinxdoc'
downloadDir='_downloads'
imgDir='_images'
srcExt='.fjson'
'''



def createPageString(confluencePages, imagesPath, downloadsPath):
    pagesStr=''
    pages=confluencePages.split(',')

    for page in pages:
        pageParts = page.split(':');
        pageFile = pageParts[0]
        pageConfluenceId = pageParts[1]
        attachmentsStr = createAttachmentsString(imagesPath, downloadsPath)

        pageStr = "- id: %s\n  source: %s" % (pageConfluenceId, pageFile)
        if pagesStr != '':
            pagesStr = "%s\n%s%s" % (pagesStr, pageStr, attachmentsStr)
        else:
            pagesStr = "%s%s" % (pageStr, attachmentsStr)

    if pageStr == '':
        raise ValueError('Unable to parse confluencePages - is empty or malformed')

    pagesStr = "pages:\n%s" % pagesStr
    return pagesStr

def createAttachmentsString(imagesPath, downloadsPath):
    attachmentsStr = ''
    imagesStr = createImagesString('/home/jimmi/IdeaProjects/play-template/doc/sphinxdoc/build/json/_images')
    downloadStr = createDownloadsString('/home/jimmi/IdeaProjects/play-template/doc/sphinxdoc/build/json/_downloads')
    
    if downloadStr != '' or imagesStr != '':
        attachmentsStr = "%s\n  attachments:" % attachmentsStr
        if imagesStr != '':
            attachmentsStr = "%s\n%s" % (attachmentsStr, imagesStr)
        if downloadStr != '':
            attachmentsStr = "%s\n%s" % (attachmentsStr, downloadStr)
    return attachmentsStr

def createImagesString(imageDir):
    imagesStr = ''
    imageFiles = glob.glob(imageDir+'/*')
        
    if (len(imageFiles) > 0):
        imagesStr = '    images:'
        for imageFile in imageFiles:
            imagesStr = "%s\n    - %s" % (imagesStr, imageFile)
    return imagesStr

def createDownloadsString(downloadDir):
    downloadStr = ''
    downloadFiles = glob.glob(downloadDir+'/*')

    if (len(downloadFiles) > 0):
        downloadStr = '    downloads:'
        for downloadFile in downloadFiles:
            downloadStr = "%s\n    - %s" % (downloadStr, downloadFile)
    return downloadStr
            

def createConfigYaml(confluencePages, confluenceUrl, baseDir, downloadDir, imgDir, srcExt):
    imagesPath = "%s/%s" % (baseDir, imgDir)
    downloadsPath = "%s/%s" % (baseDir, downloadDir)
    pageStr = createPageString(confluencePages)
    
    yamlStr = (
        "version: 2\n"
        "url: %s\n"
        "base_dir: %s\n"
        "downloads_dir: %s\n"
        "images_dir: %s\n"
        "source_ext: %s\n"
        "%s"
        % (confluenceUrl, baseDir, downloadDir, imgDir, srcExt, pageStr)
    )

    return yamlStr

print createConfigYaml(confluencePages, confluenceUrl, baseDir, downloadDir, imgDir, srcExt)
if 'confluenceAuth' not in os.environ:
    sys.exit('Environment variable confluenceAuth is missing')

if 'confluencePages' not in os.environ:
    sys.exit('Environment variable confluencePages is missing')
