# -*- coding: utf-8 -*-
import subprocess
import os
import sys
import shutil
import glob
import re
import tempfile

'''
Perform a Python equivalent of in-place `sed` substitution: e.g.,
`sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
'''
def replaceInFile(filename, pattern, replace, greedy = False):
    # For efficiency, precompile the passed regular expression.
    if greedy:
        pattern_compiled = re.compile(pattern, re.DOTALL)
    else:
        pattern_compiled = re.compile(pattern)
        
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(replace, line))

    #overwrite original file with temp file such that file attributes are preserved
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)

'''
Runs the sphinx make command with a given parameter
e.g. make json
'''
def callSphinxMake(command, makeFilePath):
    cmd = ['make']
    
    if command != None:
        cmd.append(command)
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=makeFilePath)
    for line in process.stdout:
        print line
        
    process.wait()
    return process.returncode

def copyImageFilesToSphinxSource(imageDir, dstDir):
    imageSearchPath = "%s/*" % imageDir
    imgFiles = glob.glob(imageSearchPath)
    print "Searched %s and found %s file" % (imageSearchPath, len(imgFiles))
    for img in imgFiles:
        print "Copying file %s" % img
        shutil.copy(img, dstDir)

def replaceImagePath(sphinxdocPath, docSuffix, buildDir, imgDir):
    # find all source documents
    sourceSearchPath = "%s/source/*%s" % (sphinxdocPath, docSuffix)
    srcFiles = glob.glob(sourceSearchPath)
    print "Searched source dir %s and found %s file" % (sourceSearchPath, len(srcFiles))
    for file in srcFiles:
        base = os.path.basename(file) # get file basename (e.g. something.rst)
        baseWoExt = os.path.splitext(base)[0] # remove the extension (e.g. something)
        searchInBuildDir = "%s/%s*" % (buildDir, baseWoExt)
        buildFiles = glob.glob(searchInBuildDir)
        print "Searched build dir %s and found %s" % (searchInBuildDir, buildFiles)
        
        if (len(buildFiles) > 0):
            buildFile = buildFiles[0]
            searchInBuildImageDir = "%s/%s/*" % (buildDir, imgDir)
            buildImageFiles = glob.glob(searchInBuildImageDir)
            for imageFile in buildImageFiles:
                imageBasename = os.path.basename(imageFile)
                imagePath = "images/%s" % imageBasename
                newImagePath = "%s/%s" % (imgDir, imageBasename)
                print "Replaced image path %s in file %s to new path %s" % (imagePath, buildFile, newImagePath)
                replaceInFile(buildFile, r'%s' % imagePath, '%s' % newImagePath)
        
        
def main():
    makeArg = None
    if len(sys.argv) >= 2:
        makeArg = sys.argv[1]
        
    sphinxdocPath = os.environ.get('sphinxdocPath', '/doc/sphinxdoc')
    imgDir = os.environ.get('imgDir', '_images')
    docDir = os.environ.get('docDir', '/doc')
    imageDir = "%s/images" % docDir
    docSuffix = os.environ.get('docSuffix', '.rst')
    
    result = callSphinxMake(makeArg, sphinxdocPath)
    
    if result != 0:
        # fail fast if make command failes
        sys.exit('Make command failed, exit')
        
    # e.g. /doc/sphinxdoc/build/html/_images
    imageDstDir = "%s/build/%s/%s" % (sphinxdocPath, makeArg, imgDir)
    copyImageFilesToSphinxSource(imageDir, imageDstDir)
    buildDir = "%s/build/%s" % (sphinxdocPath, makeArg)
    replaceImagePath(sphinxdocPath, docSuffix, buildDir, imgDir)
        
    
if __name__ == '__main__':
    main()