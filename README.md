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
git clone https://github.com/OSC/docker-sphinx.git
cd docker-sphinx
docker build --force-rm -t ohiosupercomputer/docker-sphinx .
```

## Install

```sh
docker pull ohiosupercomputer/docker-sphinx
```

## Usage

```sh
docker run --rm -i -t -v "${PWD}:/doc" -u "$(id -u):$(id -g)" ohiosupercomputer/docker-sphinx <cmd>
```

### Docker Compose

It is recommended to use [Docker Compose](https://docs.docker.com/compose/). An
example `docker-compose.yml` is seen as:

```yaml
version: "2"
services:
  sphinx:
    image: "ohiosupercomputer/docker-sphinx"
    volumes:
      - "${PWD}:/doc"
    user: "1000:1000"
```

Then run:

```sh
docker-compose run --rm sphinx <cmd>
```

Examples:

```sh
docker-compose run --rm sphinx sphinx-quickstart
# or without interactive wizard
docker-compose run --rm sphinx sphinx-quickstart  -p 'Template Project' -a 'TV 2 PLAY Backend' --sep --dot=. -v 1.0 --suffix=.rst --master=index --extensions=sphinxcontrib.plantuml -q /doc
docker-compose run --rm sphinx make html
docker-compose run --rm sphinx conf_publisher config.yml --verbose --url <confluence url>/wiki --auth <confluence auth> --force
```
