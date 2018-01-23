# Docker Sphinx

Docker image for [Sphinx](http://www.sphinx-doc.org/en/stable/).
Cheatsheet for reStructuredText can be [found here](https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst)

This image contains:

- [Sphinx](http://www.sphinx-doc.org/en/stable/)
- A theme:
  - [sphinx_rtd_theme](https://github.com/rtfd/sphinx_rtd_theme)
- A variety of plugins:
  - [sphinxcontrib-plantuml](https://pypi.python.org/pypi/sphinxcontrib-plantuml)
  - [sphinxcontrib-httpdomain](https://pypi.python.org/pypi/sphinxcontrib-httpdomain)
- [Confluence Publisher](https://github.com/Arello-Mobile/confluence-publisher)

## Build

```sh
git clone git@github.com:jimmikristensen/docker-sphinx.git
cd docker-sphinx
docker build --force-rm -t jkris/docker-sphinx .
```

## Install

```sh
docker pull jkris/docker-sphinx
```

## Basic Usage

```sh
docker run --rm -i -t -v "${PWD}:/doc" -u "$(id -u):$(id -g)" jkris/docker-sphinx <cmd>
```

The volume mount ${PWD} should point to the dir containing the .rst files. You can execute any commands <cmd> within the docker container - read on to see some examples.

To __automate the process__, please look at the [Advanced Usage](https://github.com/jimmikristensen/docker-sphinx#advanced-usage) section or the [example directory](https://github.com/jimmikristensen/docker-sphinx/tree/master/examples).

### Docker Compose

It is recommended to use [Docker Compose](https://docs.docker.com/compose/). An example `docker-compose.yml` is seen as:

```yaml
version: "2"
services:
  sphinx:
    image: "jkris/docker-sphinx"
    volumes:
      - "${PWD}:/doc"
    user: "1000:1000"
```

Now you can run:

```sh
docker-compose run --rm sphinx <cmd>
```

Basic examples using docker-compose:

```sh
# create a new sphinx documentation project structure
docker-compose run --rm sphinx sphinx-quickstart
# or using the quiet flag (without interactive wizard)
docker-compose run --rm sphinx sphinx-quickstart  -p 'Project' -a 'Author' --sep --dot=. -v 1.0 --suffix=.rst --master=index --extensions=sphinxcontrib.plantuml --quiet /doc
```

To see the full list of arguments of the quickstart command, see [Invocation of sphinx-quickstart](http://www.sphinx-doc.org/en/stable/invocation.html).

After the documentation structure has been setup, you can generate documentation in different formats.

```sh
# to generate html
docker-compose run --rm sphinx make html
# to generate json (will be used later in this readme to push to confluence)
docker-compose run --rm sphinx make json
```

This image contains the _sphinx-confluence_ which means it can be used for pushing documentation to a confluence server.
Before this can be done, you need to create a config.yml containing confluence specific information. Read more about [confluence-publisher](https://github.com/Arello-Mobile/confluence-publisher).
An example could look like this:

```sh
docker-compose run --rm sphinx conf_publisher config.yml --verbose --url <confluence url>/wiki --auth <confluence auth> --force)

```

## Advanced Usage

To make the automation process easier for use in a deployment pipeline, I have created three python scripts.

Please look at the [example](https://github.com/jimmikristensen/docker-sphinx/tree/master/examples) directory for further details.

### sphinx_init.py

This script will run the _sphinx-quickstart_ with the arguments necessary for setting up the sphinx project in quiet mode. 
If run multiple times, it will cleanup before running again. It modifies the conf.py used by sphinx to use environment variables instead of configured values, 
which enables you to set (and change) the values when the container is started.
It will also add any .rst files you have in your directory to the master document (usually index.rst).

### sphinx_make.py
This script has two purposes: 1) To copy any images that are stored in _assets/images_ directory into the sphinx build directory and change the path for the image
in the generated document, and 2) to run the sphinx make command.

### sphinx_confluence_publish.py

This script generates the config.yml file based on the environemtn variables
you pass to it and the .rst documents in your directory. If you are using plantuml in your documents or have images or
downloads in your sphinx project, these files will be added to the config.yml and attached the confluence page.
Furthermore, the plantuml and images referenced in your .rst documents will be converted to confluence image references
to the attachments, which means that they will be visible in confluence.

### Sphinx Environment Variables