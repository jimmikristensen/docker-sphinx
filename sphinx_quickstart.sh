#!/bin/bash

sphinx-quickstart  -p 'myproject' -a 'me' --sep --dot=. -v 1.0 --suffix=.rst --master=index --extensions=sphinxcontrib.plantuml -q /doc
