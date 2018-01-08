import os
import sys
import glob

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
    imagesStr = createImagesString(imagesPath)
    downloadStr = createDownloadsString(downloadsPath)
    
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
            

def createConfigYaml(confluencePages, confluenceUrl, basePath, downloadDir, imgDir, srcExt):
    imagesPath = "%s/%s" % (basePath, imgDir)
    downloadsPath = "%s/%s" % (basePath, downloadDir)
    pageStr = createPageString(confluencePages, imagesPath, downloadsPath)
    
    yamlStr = (
        "version: 2\n"
        "url: %s\n"
        "base_dir: %s\n"
        "downloads_dir: %s\n"
        "images_dir: %s\n"
        "source_ext: %s\n"
        "%s"
        % (confluenceUrl, basePath, downloadDir, imgDir, srcExt, pageStr)
    )

    return yamlStr

def saveConfigYaml(configFilePath, configStr):
    fh = open(configFilePath)
    fh.write(configStr)
    fh.close()

if 'confluenceAuth' not in os.environ:
    sys.exit('Environment variable confluenceAuth is missing')

if 'confluencePages' not in os.environ:
    sys.exit('Environment variable confluencePages is missing')

if 'confluenceUrl' not in os.environ:
    sys.exit('Environment variable confluenceUrl is missing')

confluencePages = os.environ.get('confluencePages')
confluenceUrl = os.environ.get('confluenceUrl')
basePath = os.environ.get('basePath', '/doc/sphinxdoc/build/json')
configPath = os.environ.get('configPath', '/doc/sphinxdoc')
downloadDir = os.environ.get('downloadDir', '_downloads')
imgDir = os.environ.get('imgDir', '_images')
srcExt = os.environ.get('srcExt', '.fjson')

configYamlStr = createConfigYaml(confluencePages, confluenceUrl, basePath, downloadDir, imgDir, srcExt)
saveConfigYaml(configPath, configYamlStr)
