#!/bin/bash

# Bootstrap BlackBox with needed Operating System
# and initial packages
set -x -e

ENDPOINT_URL='http://endpoint.domain/path'
USERNAME='barograph'
PROVIDER_IP=$(ip -o route get to 8.8.8.8 | \
              sed -n 's/.*src \([0-9.]\+\).*/\1/p')

apt install -y curl openssl python3.5-minimal \
    python3-minimal python2.7-minimal \
    python-minimal

# Create the '$USERNAME' user and allow sudo
useradd --groups sudo --create-home --user-group $USERNAME \
        --shell /bin/bash
echo "$USERNAME       ALL= NOPASSWD: ALL" >> /etc/sudoers

su - $USERNAME <<- EOSU
    # Generate Private Key and add the Public Key to the
    # authorized keys
    mkdir -p ~/.ssh/
    echo "y" | ssh-keygen -f ~/.ssh/id_rsa -b 2048 -t rsa \
               -q -N ""
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

    # Generate POST data
    PRIVATE_KEY=\$(base64 -w 0 ~/.ssh/id_rsa)
    POST_DATA=\`cat <<- EOF
{
    "ip": "$PROVIDER_IP",
    "user": "$USERNAME",
    "ssh_key": "\$PRIVATE_KEY"
}
EOF\`

    curl -X POST -H "Content-Type: application/json" \
         -d "\$POST_DATA" $ENDPOINT_URL --insecure

    exit
EOSU
