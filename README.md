# Calibrated Recommendation Fairness with the Users Genres Preferences  
Some introdutory text

## Install and Run  

### Intall
1. Update and upgrade the OS: `sudo apt upgrade && sudo apt upgrade -y`  
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
  
### Config  
1. Git:  
.1. Reload bash: `source ~/.bashrc`  
.2. Generate ssh key: `ssh-keygen`  
.3. Copy the key: `cat ~/.ssh/id_rsa.pub`    
.4. Paste in the git(lab-hub)  
.5. Clone the repository: `git clone git@github.com:DiegoCorrea/Calibrated-Recommendations-Fairness-with-the-Users-Genres-Preferences.git`    
1. Go to the project root path: `cd Calibrated-Recommendations-Fairness-with-the-Users-Genres-Preferences/`  
1. Load the conda environment: `conda env create -f environment.yml`  
1. Active the environment: `conda activate calibrated_recommendation`  
1. Get the dataset  
.1. `import gdown`  
.2. `output = 'dataset.zip' `  
.3. `url = 'https://drive.google.com/uc?id=1mc7ZsI5HEeLwbDRJ3f8JHUWl2tjlljKh' `  
.4. `gdown.download(url, output, quiet=False) `  
6. Unzip the dataset: `unzip dataset.zip`
  
### Run  
1. Extract language: `sh extract_language.sh`
1. Code on background: `python main.py > log/output_terminal.log 2>&1 & disown`  