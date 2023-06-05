# This is the installation script that does the installation

if [ -z "$1" ]
then
	echo "No installation path specified"
	exit 69
fi

echo "Installation path found."

if [ -z "$2" ]
then
	echo "No conda environment specified"
	exit 420
fi

echo "Conda environment specified."

CONDA_ENV=$2
INSTALL_PATH=$(realpath $1)
MAIN_PATH=$INSTALL_PATH/dynamictaxes/main.py

ANACONDA3=~/anaconda3/
MINICONDA3=~/miniconda3/

if [ -d "$ANACONDA3" ]
then
	CONDAPATH=$ANACONDA3
else
	if [ -d "$MINICONDA3" ]
	then
		CONDAPATH=$MINICONDA3
	fi
fi

if [ -z "$CONDAPATH" ]
then
	echo "No conda installation found"
	exit 31
fi

echo "Found conda installation at $CONDAPATH"


cd $INSTALL_PATH
source $CONDAPATH/etc/profile.d/conda.sh
git init .
git remote add origin https://github.com/LinusBDittmer/dynamic-taxes.git
git pull origin master
conda develop -n $CONDA_ENV $INSTALL_PATH
rm -rf .git/ .github/ .gitignore requirements.txt

echo -e "\n# Dynamic taxes alias binding" >> ~/.bashrc
echo -e "alias dynamic-taxes='python $MAIN_PATH'" >> ~/.bashrc
echo -e "alias dt='python $MAIN_PATH'" >> ~/.bashrc
echo -e "alias dyntax='python $MAIN_PATH'" >> ~/.bashrc
echo -e "# End dynamic taxes" >> ~/.bashrc

echo "Installation complete."

