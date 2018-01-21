# -*- coding: utf-8 -*-
import re
import sys
import os
import shutil
import tempfile
import glob
from sphinx import quickstart as sphinx_quickstart

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
Clean up sphinx directory
'''
def cleanUp(docPath):
    try:
        shutil.rmtree(docPath+"/build")
        shutil.rmtree(docPath+"/source")
        os.remove(docPath+"/make.bat")
        os.remove(docPath+"/Makefile")
    except OSError as err:
        print("Unable to clean up", err)

'''
Replace hardcoded config params with params from environment
'''
def setupConfig(configPath):
    replaceInFile(configPath, r'# import os', 'import os')
    replaceInFile(configPath, r'project = .*', 'project = os.environ[\'projectName\']')
    replaceInFile(configPath, r'copyright = .*', 'copyright = os.environ[\'owner\']')
    replaceInFile(configPath, r'author = .*', 'author = os.environ[\'owner\']')
    replaceInFile(configPath, r'version = .*', 'version = os.environ[\'major\']+\".\"+os.environ[\'minor\']')
    replaceInFile(configPath, r'release = .*', 'release = os.environ[\'major\']+\".\"+os.environ[\'minor\']')
    replaceInFile(configPath, r'html_theme = \'.*\'', 'html_theme = \'sphinx_rtd_theme\'')
        
'''
Iterates through all markdown (usually .rst) file, sopies 
them to the source dir and finally adds the files to the 
master doc (usually index.rst) file under the line containing 
":caption: Contents:" 
'''
def copyMarkdownFilesAndAppendToMaster(searchDir, fileSuffix, dstPath, masterDoc):
    # Find all markdown files
    docFiles = glob.glob("%s/*%s" % (searchDir, fileSuffix))
    masterDocument = dstPath+'/'+masterDoc+fileSuffix
    for file in docFiles:
        # copy all markdown files to source dir
        shutil.copy(file, dstPath)
        # add the markdown files to the mast
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            with open(masterDocument) as src_file:
                for line in src_file:
                    if line.startswith('   :caption: Contents:'):
                        line = '   ' + line.strip() + '\n\n   ' + os.path.basename(file)
                    tmp_file.write(line)

        shutil.copystat(masterDocument, tmp_file.name)
        shutil.move(tmp_file.name, masterDocument)
    
def main():
    if 'projectName' not in os.environ:
        sys.exit('Environment variable projectName is missing')

    projectName = os.environ.get('projectName');
    sphinxdocPath = os.environ.get('sphinxdocPath', '/doc/sphinxdoc')
    docDir = os.environ.get('docDir', '/doc')
    masterDoc = os.environ.get('masterDoc', 'index')
    docVersion = os.environ.get('docVersion', '1.0')
    docSuffix = os.environ.get('docSuffix', '.rst')
    docAuthor = os.environ.get('docAuthor', 'me')

    # clean up sphinxdoc dir before initializing
    cleanUp(sphinxdocPath)

    # Initialize the sphinx doc
    quickstartArgs = [sys.argv[0], '-p', projectName, '-a', docAuthor, '--sep', '--dot=.', '-v', docVersion, '--suffix='+docSuffix, '--master='+masterDoc, '--extensions=sphinxcontrib.plantuml', '-q', sphinxdocPath]
    print "Running sphinx-quickstart with the following arguments:"
    print quickstartArgs
    sphinx_quickstart.main(quickstartArgs)

    # edit config file to use environment variables and sphinx_rtd_theme theme for HTML
    setupConfig(sphinxdocPath+'/source/conf.py')

    # find all rst files and copy them to source dir and append to master doc
    copyMarkdownFilesAndAppendToMaster(docDir, docSuffix, sphinxdocPath+'/source', masterDoc)
    
if __name__ == '__main__':
    main()
