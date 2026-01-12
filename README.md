# metazooa_pro

## Installation instructions
```
git clone https://github.com/etd530/metazooa_pro && cd metazooa_pro
conda create -n metazooa && conda activate metazooa
conda install -c conda-forge -c bioconda taxopy
wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip && unzip taxdmp.zip && rm taxdmp.zip
```

## How to play
Simply run:
```
./metazooa_pro.py
```

Then follow the instructions :)

DISCLAIMER: only tested on Ubuntu systems.

## Possible issues
Sometimes you have to deactivate conda and then activate the environemnt again for it to detect the newly installed taxopy library.
