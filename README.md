# ofxstatement-hype

![badge](https://github.com/lorenzogiudici5/ofxstatement-hype/actions/workflows/build-and-publish.yml/badge.svg)

This is a plugin for [ofxstatement](https://github.com/kedder/ofxstatement).

Hype (Banca Sella) allows to export movements from mobile app: the only format available is PDF.

This plugin converts PDF statement to OFX format, suitable for importing into GnuCash.

## Installation

### From PyPI repositories
```
pip3 install ofxstatement-hype
```

### From source
```
git clone https://github.com/lorenzogiudici5/ofxstatement-hype.git
python3 setup.py install
```

## Configuration
Add plugin config, running the following command:

```bash
$ ofxstatement edit-config
```

Edit the file:
```
[hype]
plugin = hype
currency = EUR
account = hype
```

Save and exit the text editor.

## Usage
Export your movements from Hype mobile app following the instructions [here](https://support.hype.it/hc/it/articles/360005910553-Come-salvare-e-condividere-la-lista-movimenti-di-HYPE).

Run the followning command:
```bash
$ ofxstatement convert -t hype ec_01_12_2023_30_12_2023.pdf ec_2023_12.ofx
```
