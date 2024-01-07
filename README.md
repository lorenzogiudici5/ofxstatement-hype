# ofxstatement-hype

![badge](https://github.com/lorenzogiudici5/ofxstatement-hype/actions/workflows/build-and-publish.yml/badge.svg)

This is a plugin for [ofxstatement](https://github.com/kedder/ofxstatement).

Hype allow to export movements in PDF format only from mobile app. Check instructions [here](https://support.hype.it/hc/it/articles/360005910553-Come-salvare-e-condividere-la-lista-movimenti-di-HYPE
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

## Usage
Export your movements from Hype app and then run
```bash
$ ofxstatement convert -t hype ec_2023_12.pdf ec_2023_12.ofx
```