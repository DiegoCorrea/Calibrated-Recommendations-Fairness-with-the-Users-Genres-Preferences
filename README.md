# Exploiting Personalized Calibration and Metrics for Fairness Recommendation  
Code from the paper published on Journal Expert Systems With Applications.  

Exploiting Personalized Calibration and Metrics for Fairness Recommendation  
  - Docker Container on Code Ocean: [https://doi.org/10.24433/CO.6790880.v1](https://doi.org/10.24433/CO.6790880.v1)  
  - Paper: [https://doi.org/10.1016/j.eswa.2021.115112](https://doi.org/10.1016/j.eswa.2021.115112)

This paper is the first part of two belonged to my master dissertation.
  - Master dissertation (portuguese and with more information than this article): [Incoming]()
  - Second paper: [Incoming]()

# Abstract  
Recommendation systems are used to suggest items that users can be interested in. These systems are based on the user preference historic to create a recommendation list with items that have the higher similarity with the user's interests, in order to achieve the best possible user's satisfaction, which is usually measured as recommendation precision. However, the search for the best precision can cause some side effects such as overspecialization, few diversity and miscalibration of genres, classes and niches. Calibration provides fairer recommendations, which respect the genre proportionality on the user's preferences, avoiding overspecialization. This article aims to explore ways to balance the trade-off weight between precision and calibration based on divergence measures, as well as to propose metrics to evaluate the calibration in the suggested list. The proposed system works in a post-processing step and does not depend on a specific recommender algorithm or workflow. For this purpose, we evaluate six recommender algorithms applied in the movie domain, analyzing variations of three fairness measures, two personalized trade-off weights and eleven constant weights. To understand the results we use the precision, the reciprocal rank and two proposed metrics. The results indicate that the trade-off formulation of personalized weights obtains better results when used to compare the recommendation lists using matrix factorization-based approaches on Movielens dataset. In addition, the calibration also impacts the precision and fairness of all considered algorithms used in evaluation.  

# PS  
PS 1: Be care with the path names and repositories.  
PS 2: If you want run before clone the repository, visit the docker container on code ocean.   
PS 3: If your research will use the code or part of the paper, verify the correct citation.    
PS 4: For question and contribution, please, send to the email in the paper.  

# To Ubuntu/Debian  

## Install
1. Update and upgrade the OS: `sudo apt update && sudo apt upgrade -y`  
1. Git: `sudo apt install git`  
1. Python: `sudo apt install python3.7` 
1. Unzip: `sudo apt install unzip`  
1. htop: `sudo apt install htop`  
1. gcc: `sudo apt install gcc`
1. g++: `sudo apt install g++`
1. text: `sudo apt install gettext libgettextpo-dev`
1. Conda [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)-[All O.S.](https://docs.anaconda.com/anaconda/install/linux/)  
1.1. Download: `curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh`   
1.1. Install: `bash Anaconda3-2019.10-Linux-x86_64.sh -yes`  
1. PyCharm (Optional: for better development)  
  
## Config  
1. Git:  
.1. Reload bash: `source ~/.bashrc`  
.2. Generate ssh key: `ssh-keygen`  
.3. Copy the key: `cat ~/.ssh/id_rsa.pub`    
.4. Paste in the git(lab-hub)  
.5. Clone the repository: `git clone git@github.com:DiegoCorrea/Calibrated-Recommendations-Fairness-with-the-Users-Genres-Preferences.git`    
1. Go to the project root path: `cd Calibrated-Recommendations-Fairness-with-the-Users-Genres-Preferences/`  
1. Load the conda environment: `conda env create -f environment.yml`  
1. Active the environment: `conda activate calibrated_recommendation_preferences`  
1. Get the dataset  
.1. `import gdown`  
.2. `output = 'dataset.zip' `  
.3. `url = 'https://drive.google.com/uc?id=1mc7ZsI5HEeLwbDRJ3f8JHUWl2tjlljKh' `  
.4. `gdown.download(url, output, quiet=False) `  
6. Unzip the dataset: `unzip dataset.zip`
  
## Run  
1. Extract language: `sh extract_language.sh`
1. Code on background: `python main.py > log/output_terminal.log 2>&1 & disown`

# To RedHat/CentOS  

## Install
1. Update and upgrade the OS: `sudo yum update -y`  
1. Git: `sudo yum install git -y`  
1. Softwares de apoio: `sudo yum install openssl-devel bzip2-devel libffi-devel -y` 
1. Unzip: `sudo yum install unzip -y`  
1. htop: `sudo yum install htop -y`  
1. gcc e g++: `sudo yum install gcc gcc-c++ -y`
1. text: `sudo yum install gettext -y`
1. Python:  
.1. Download Python: `wget https://www.python.org/ftp/python/3.8.1/Python-3.8.1.tgz`  
.2. Descompactar e ir para a pasta: `tar xzf Python-3.8.1.tgz && cd Python-3.8.1`  
.3. Configurar: `sudo ./configure --enable-optimizations`    
.4. Instalar: `sudo make altinstall`  
.5. Remove: `cd .. && sudo rm Python-3.8.1.tgz && sudo rm -rf Python-3.8.1`  
1. Conda [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)-[All O.S.](https://docs.anaconda.com/anaconda/install/linux/):  
.1. Pre-instalação: `sudo yum install libXcomposite libXcursor libXi libXtst libXrandr alsa-lib mesa-libEGL libXdamage mesa-libGL libXScrnSaver`    
.2. Download: `curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh`   
.3. Install: `bash Anaconda3-2019.10-Linux-x86_64.sh -yes`  
.4. Reload bash: `source ~/.bashrc` 
1. PyCharm (Optional: for better development)  
  
## Config  
1. Git:   
.1. Generate ssh key: `ssh-keygen`  
.2. Copy the key: `cat ~/.ssh/id_rsa.pub`    
.3. Paste in the git(lab-hub)  
.4. Clone the repository: `git clone git@github.com:DiegoCorrea/Calibrated-Recommendations-Fairness-with-the-Users-Genres-Preferences.git`    
1. Go to the project root path: `cd Calibrated-Recommendations-Fairness-with-the-Users-Genres-Preferences/`  
1. Load the conda environment: `conda env create -f environment.yml`  
1. Active the environment: `conda activate calibrated_recommendation_preferences`  

## Get Dataset
Execute the script `sh datasets.sh > log/output_terminal.log 2>&1 & disown`   
or follows the commands bellow:
1. Get the dataset: `python`  
.1. `import gdown`  
.2. `output = 'dataset.zip' `  
.3. `url = 'https://drive.google.com/uc?id=1mc7ZsI5HEeLwbDRJ3f8JHUWl2tjlljKh' `  
.4. `gdown.download(url, output, quiet=False) `  
6. Unzip the dataset: `unzip dataset.zip`  
  
## Run  
1. Extract language: `sh extract_language.sh`
1. Code on background: `python main.py > log/output_terminal.log 2>&1 & disown`    