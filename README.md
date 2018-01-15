# Docker Sphinx

Docker image for [Sphinx](http://www.sphinx-doc.org/en/stable/).

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

## Usage

```sh
docker run --rm -i -t -v "${PWD}:/doc" -u "$(id -u):$(id -g)" jkris/docker-sphinx <cmd>
```

The volume mount ${PWD} should point to the dir containing the .rst files. You can execute any commands <cmd> within the docker container, read on to see some examples.

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

To see the full list of arguments of the quickstart command, see [Invocation of sphinx-quickstart](http://www.sphinx-doc.org/en/stable/invocation.html)

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
