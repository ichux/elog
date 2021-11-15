#!/bin/bash

# Run the command to ignore the files listed
# echo -e "oprint.txt\ndid-these.txt"" >> .git/info/exclude

BRANCH_NAME=`git branch | grep \* | tr -d '* '`

# clean up if found
rm -f oprint.txt

### push code section
echo -e "\n"

git status

echo -e "\n"
read -e -p "HAVE YOU MANUALLY COMMITTED YOUR FILES? - *carefully study the above statements*: " choice

#cat <<EOF > oprint.txt
cat > oprint.txt << EOF
$BRANCH_NAME

$(cat did-these.txt)

$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

if [[ "$choice" == [Nn]* ]]; then
	echo -e "\n"
	echo "You need to manually add the necessary files"
else
	if [[ "$choice" == [Yy]* ]]; then
		# git commit --verbose --file=oprint.txt
		git commit --verbose --message="$( cat oprint.txt )"
		rm -f oprint.txt
		echo "code was COMMITTED"
	fi
	if [[ "$choice" == [Yy]* ]]; then
		git push origin -f $BRANCH_NAME
		echo "code was PUSHED"
	fi
	echo -e "\n"
fi
