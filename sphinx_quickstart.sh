#!/bin/bash

DOC_DIR=/doc/sphinxdoc

# clean up sphinxdoc dir before initializing
rm -fr $DOC_DIR/build
rm -fr $DOC_DIR/source
rm $DOC_DIR/make.bat
rm $DOC_DIR/Makefile

sphinx-quickstart  -p $projectName -a 'me' --sep --dot=. -v 1.0 --suffix=.rst --master=index --extensions=sphinxcontrib.plantuml -q $DOC_DIR

# edit config file to use environment variables and sphinx_rtd_theme theme for HTML
sed -i "s/# import os/import os/g" $DOC_DIR/source/conf.py
sed -i "s/project = .*/project = os.environ[\'projectName\']/g" $DOC_DIR/source/conf.py
sed -i "s/copyright = .*/copyright = os.environ[\'owner\']/g" $DOC_DIR/source/conf.py
sed -i "s/author = .*/author = os.environ[\'owner\']/g" $DOC_DIR/source/conf.py
sed -i "s/version = .*/version = os.environ[\'major\']\+\".\"\+os.environ[\'minor\']/g" $DOC_DIR/source/conf.py
sed -i "s/release = .*/release = os.environ[\'major\']\+\".\"\+os.environ[\'minor\']/g" $DOC_DIR/source/conf.py
sed -i "s/html_theme = \'.*\'/html_theme = \'sphinx_rtd_theme\'/g" $DOC_DIR/source/conf.py

# remove indices and tables from the master document (index.rst)
sed -i '/^Indices and tables/,/* :ref:`search`/ d' $DOC_DIR/source/index.rst

# find all rst files and copy them to source dir and append to master doc
find . -iname "*.rst" -maxdepth 1 | \
    while read F; do
	echo "Copy rst file to source dir"
	cp $F $DOC_DIR/source/
	echo "Appending rst files to master doc"
	sed -i "/:caption: Contents:/ a \\\n\ \ \ $F" $DOC_DIR/source/index.rst
    done
