#!/bin/bash

# Bootstrap BlackBox with needed Operating System
# and initial packages

CLUSTER_ID='0'
ENDPOINT_URL='https://endpoint.domain'
USERNAME='barograph'
PROVIDER_IP="$(ifconfig | grep -A 1 'ens3' | \
		   tail -1 | cut -d ':' -f 2 | \
		   cut -d ' ' -f 1)"

apt get install -y curl openssl python3.5-minimal \
	python3-minimal python2.7-minimal \
	python-minimal

# Create the '$USERNAME' user and allow sudo
useradd --groups sudo --create-home --user-group $USERNAME \
	--shell /bin/bash
echo "$USERNAME       ALL= NOPASSWD: ALL" >> /etc/sudoers
USER_HOME_DIR=`getent passwd $USERNAME | cut -d: -f 6`

su - $USERNAME <<- EOSU
	# Generate Private Key and add the Public Key to the
	# authorized keys
	mkdir -p ~/.ssh/
	echo "y" | ssh-keygen -f ~/.ssh/id_rsa -b 2048 -t rsa \
			   -q -N ""
	cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

	# Generate POST data
	PRIVATE_KEY=\`cat ~/.ssh/id_rsa\`
	POST_DATA=\`cat <<- EOF
	{
	    "cluster_id": "$CLUSTER_ID",
	    "node_info": {
	        "ip": "$PROVIDER_IP",
	        "user": "$USERNAME",
	        "user_home_dir": "$USER_HOME_DIR",
	        "ssh_key": "\$PRIVATE_KEY"
	    }
	}
	EOF\`

	curl -X POST -H "Content-Type: application/json" \
		-d "\$POST_DATA" $ENDPOINT_URL --insecure

	exit
EOSU
