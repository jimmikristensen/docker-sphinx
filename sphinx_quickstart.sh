#!/bin/bash

sphinx-quickstart  -p 'myproject' -a 'me' --sep --dot=. -v 1.0 --suffix=.rst --master=index --extensions=sphinxcontrib.plantuml -q /doc

sed -i "s/# import os/import os/g" /doc/conf.py
sed -i "s/project = .*/project = os.environ[\'projectName\']/g" /doc/conf.py
sed -i "s/copyright = .*/copyright = os.environ[\'owner\']/g" /doc/conf.py
sed -i "s/author = .*/author = os.environ[\'owner\']/g" /doc/conf.py
sed -i "s/version = .*/version = os.environ[\'major\']\+\".\"\+os.environ[\'minor\']/g" /doc/conf.py
sed -i "s/release = .*/release = os.environ[\'major\']\+\".\"\+os.environ[\'minor\']/g" /doc/conf.py
sed -i "s/html_theme = \'.*\'/html_theme = \'sphinx_rtd_theme\'/g" /doc/conf.py

