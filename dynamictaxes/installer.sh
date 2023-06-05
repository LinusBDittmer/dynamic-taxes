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
INSTALL_PATH=$(realpath $1)
MAIN_PATH=$INSTALL_PATH/dynamictaxes/main.py

cd $INSTALL_PATH
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

