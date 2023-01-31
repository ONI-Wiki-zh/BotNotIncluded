# BotNotIncluded
Pywikibot and other scripts for [zh ONI wiki](https://oxygennotincluded.fandom.com/zh) (and other wikis sometimes).

- Make sure to run with Python 3.7+ as some new features are used. (e.g. Insertion-order preservation nature of dict)

# Configure
You can configure the script with these environment variables:
| Name           | Notes                            | Default                                                                                 |
| -------------- | -------------------------------- | --------------------------------------------------------------------------------------- |
| `BNI_ONI_ROOT` | Root path of the ONI game        | `C:\Program Files (x86)\Steam\steamapps\common\OxygenNotIncluded`                       |
| `BNI_PO_HANT`  | Root path of the zh-hant po file | `C:\Users\%USERNAME%\Documents\Klei\OxygenNotIncluded\mods\Steam\2906930548\strings.po` |

## Run
```sh
python -m venv venv --clear
pip install -r requirements.txt

# Preparing necessary data

python game_update.py
```
