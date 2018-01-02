#!/bin/ash

# check if env vars are set
: "${confluenceAuth?ENV var missing, confluence auth base64 key is not set}"
: "${confluencePageId?ENV var missing, confluence page ID is not set}"
: "${confluencePublishFile?ENV var missing, doc file to publish to confluence not set}"

DOC_DIR=/doc/sphinxdoc
CONFIG_FILE=$DOC_DIR/config.yml
TMP_IMAGE_FILE=/tmp/images.tmp

# remove existing config if present
rm $CONFIG_FILE
rm $TMP_IMAGE_FILE

images=""

find $DOC_DIR/build/json/_images -iname "*.png" -maxdepth 1 | \
    while read F; do
	echo "   - $F" >> $TMP_IMAGE_FILE
    done

attachedImages=`cat $TMP_IMAGE_FILE`

if [ ! -z "$attachedImages" ]; then
    attachedImages=" - attachments:
   images:
$attachedImages"
fi

# create config for confluence publisher
touch $CONFIG_FILE
/bin/cat <<EOF >$CONFIG_FILE
version: 2
url: https://tv2cms.atlassian.net/wiki
base_dir: $DOC_DIR/build/json
downloads_dir: _images
source_ext: .fjson
pages:
 - id: $confluencePageId
   source: $confluencePublishFile
$attachedImages
EOF

conf_publisher -F $DOC_DIR/config.yml --auth $confluenceAuth

