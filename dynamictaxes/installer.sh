# This is the installation script that does the installation

if [ -z "$1" ]
then
	echo "No installation path specified"
	exit 69
fi
if [ -z "$2" ]
then
	echo "No conda environment specified"
	exit 420
fi

CONDA_ENV=$2
INSTALL_PATH=$1

git init $INSTALL_PATH
git remote add origin https://github.com/LinusBDittmer/dynamic-taxes.git
git pull origin master
conda develop -n $CONDA_ENV $INSTALL_PATH

