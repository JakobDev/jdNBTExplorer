<h1 align="center">jdNBTExplorer</h1>

<h3 align="center">An Editor for Minecraft NBT files</h3>

<p align="center">
    <img alt="jdNBTExplorer" src="screenshots/MainWindow.png"/>
</p>

jdNBTExplorer allows you to edit NBT files.
NBT is a custom file format used in Minecraft to store data related to your worlds.
With jdNBTExplorer, you can view and edit these files directly.

jdNBTExplore supports the following file formats:

- .dat
- .dat_old
- .mca
- .mcc

## Install

### Flatpak
You can get jdNBTExplorer from [Flathub](https://flathub.org/apps/page.codeberg.JakobDev.jdNBTExplorer)

### AUR
Arch Users can get jdNBTExplorer from the [AUR](https://aur.archlinux.org/packages/jdnbtexplorer)

### Sourceforge
You can get Windows and AppImage Builds from [Sourceforge](https://sourceforge.net/projects/jdnbtexplorer)

### Winget
You can install jdNBTExplorer using winget:
```
winget install JakobDev.jdNBTExplorer
```

### pip
You can install jdNBTExplorer from [PyPI](https://pypi.org/project/jdNBTExplorer) using `pip`:
```shell
pip install jdNBTExplorer
```
Using this Method, it will not include a Desktop Entry or any other Data file, so you need to run jdNBTExplorer from the Command Line.
Use this only, when nothing else works.

### From source
This is only for experienced Users and someone, who wants to package jdNBTExplorer for a Distro.
jdNBTExplorershould be installed as a Python package.
You can use `pip` or any other tool that can handle Python packages.
You need to have `lrelease` installed to build the Package.
After that, you should run `install-unix-datafiles.py` which wil install things like the Desktop Entry or the Icon in the correct place.
It defaults to `/usr`, but you can change it with the `--prefix` argument.
It also applies the translation to this files.
You need gettext installed to run `install-unix-datafiles.py`.

Here's a example of installing jdNBTExplorer into `/usr/local`:
```shell
sudo pip install --prefix /usr/local .
sudo ./install-unix-datafiles.py --prefix /usr/local
```

## Translate
You can help translating jdNBTExplorer on [Codeberg Translate](https://translate.codeberg.org/projects/jdNBTExplorer)

![Translation status](https://translate.codeberg.org/widget/jdNBTExplorer/jdNBTExplorer/multi-auto.svg)

## Develop
jdNBTExploreris written in Python and uses PyQt6 as GUI toolkit. You should have some experience in both.
You can run `jdNBTExplorer.py`to start jdNBTExplorer from source and test your local changes.
It ships with a few scripts in the tools directory that you need to develop.

#### CompileUI.py
This is the most important script. It will take all `.ui` files in `jdNBTExplorer/ui` and compiles it to a Python class
and stores it in `jdNBTExplorer/ui_compiled`. Without running this script first, you can't start jdNBTExplorer.
You need to rerun it every time you changed or added a `.ui` file.

#### BuildTranslations.py
This script takes all `.ts` files and compiles it to `.qm` files.
The `.ts` files are containing the translation source and are being used during the translation process.
The `.qm` contains the compiled translation and are being used by the Program.
You need to compile a `.ts` file to a `.qm` file to see the translations in the Program.

#### UpdateTranslations.py
This regenerates the `.ts` files. You need to run it, when you changed something in the source code.
The `.ts` files are contains the line in the source, where the string to translate appears,
so make sure you run it even when you don't changed a translatable string, so the location is correct.

####  UpdateUnixDataTranslations.py
This regenerates the translation files in `deploy/translations`. these files contains the translations for the Desktop Entry and the AppStream File.
It uses gettext, as it is hard to translate this using Qt.
These files just exists to integrate the translation with Weblate, because Weblate can't translate the Desktop Entry and the AppStream file.
Make sure you run this when you edited one of these files.
You need to have gettext installed to use it.

#### UpdateTranslators.py
This uses git to get a list of all Translators and writes it to `jdNBTExplorer/data/translators.json`.
This is used to display the translators in the About Dialog.
You need git to run this script.

#### WriteChangelogHtml.py
This read the Changelog from `deploy/page.codeberg.JakobDev.jdNBTExplorer.metainfo.xml`, converts it to HTML and writes it to `jdNBTExplorer/data/changelog.html`.
This is used to display the Changelog in the About Dialog.
You need [appstream-python](https://pypi.org/project/appstream-python) to be installed to use this script.