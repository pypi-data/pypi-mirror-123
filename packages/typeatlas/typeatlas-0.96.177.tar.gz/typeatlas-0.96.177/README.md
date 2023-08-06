# TypeAtlas font explorer

TypeAtlas is a featureful graphical font explorer targeting GNU/Linux, without
disregarding cross-platform compatibility.
See [Screenshots](https://imgur.com/a/uoaN94p).

TypeAtlas provides:

* Complete list of system fonts.
    * Limited listing of fonts on remote fontconfig systems, including servers.
    * Browsing and preview of font files that have yet to be installed.
* Per-font preview and information:
    * Multi-language font previews, with three preview styles for individual
      fonts, and two preview styles for multiple fonts.
    * Complete character map display for the individual fonts, and
      limited multi-font character map display.
    * Extended information, include language support; classification by
      font's PANOSE properties; and font license preview (fontTools only).
* Font searching and filtering:
    * Search by font name.
    * Search by file name using the `file:` keyword, or file path
      using the `path:` keyword
    * Search for supported characters using the `charset:` keyword (slow)
      or the dedicated Font Sampler comparison utility (very slow)
    * Search by supported languages (fontconfig only) and writing systems
    * Search by font class: by guessed generic family (Serif or Sans Serif),
      by the PANOSE properties of the fonts when available, and by
      various other font attributes.
    * Saveable and restorable searches and filters.
* Manual categorization using manual tags and categories, and searching by
  them.
* Multiple interface modes, including simpler and more complex ones.
* Additional tools:
    * GlyphAtlas - a basic standalone character map (less mature than kcharmap
      or gucharmap), with support for legacy encodings, including modes of
      interpretation of their unicode translation for ambiguous
      encodings (including graphical characters).
    * A graphical character selector that can be invoked from other utilties or
      script
    * The `typefind` command line search utility, whose `typefind --chars abc`
      search is easier to use than `fc-match :charset=0061`.
* Small helpful facilities, such as getting the fontspec code for XeLaTeX or
  LuaLaTeX for the selected font.

TypeAtlas can be used as a feature-heavy GUI frontend for fontconfig's `fc-list` and
`fc-match` utilities.

## Installation

### GNU/Linux: Manual installation

Before you install TypeAtlas, you need to install **PyQt** and **fontTools**:

On Ubuntu, Debian or other Debian-based, this can be done with:

    sudo apt-get install python3-pyqt5 python3-fonttools python3-pip

On Fedora, this can be done with

    sudo dnf install python3 PyQt5 fonttools

You can install it in your home directory using pip:

    pip3 install --user typeatlas

If you have downloaded the source, you can run TypeAtlas directly from
the source tree:

    ./typeatlas-qt

...or install it in your user's home directory from there, too:

    ./setup.py install --user

On the first run, TypeAtlas will perform a slow scan the fonts on your
system, and generate a database of additional information. On non-fontconfig
systems, this can take a significant amount of time.

### Requirements

* Operating system support
    * TypeAtlas targets and is tested on **GNU/Linux**, which is the only
      officially supported platform.
    * Unix-like systems that rely on fontconfig are expected to
      work with no or minor adjustments.
    * Provided are OS-agnostic fallbacks for operation on e.g. macOS and
      Windows with some loss of functionality, but no testing is being
      done on such platforms.
* **Python 3.7** or later. Python 3.5 or even 3.4 may work, but have not been
  tested, and any effort to preserve compatibility with them is not expected to
  last.
* **PyQt5** or **PySide2**, along with Qt 5. Qt 6 support has not been added
  yet.
* **Fontconfig 2.13** or later. Version 2.11 breaks font character set
  functionality. Operation without fontconfig is possible, but at the expense
  of worse performance and lack of font language detection.
* *fontTools 3.35* or later. Older versions have not been tested.
  It is optional on fontconfig systems, where it provides mostly cosmetic
  features. On non-fontconfig systems or systems with fontconfig 2.11,
  lack of fontTools will severely degrade performance.
* An awful lot of RAM if you have a lot of fonts.

## Known issues

TypeAtlas is in development, and as such it is expected to contain a non-trivial
quantity of known and unknown bugs. At the moment, the most significant issues
that can be faced are as follows:

* First run takes a significant amount of time, some spent on things not
  critically necessary.
* With multiple fonts are selected, copying characters or selecting blocks in the
  character map only acknowledges the first font. The multiple font mode is
  otherwise incomplete.
* When saving tags, TypeAtlas can helpfully erase the icon and colour choice
  you just made.
* When configuring choice for multiple languages, automated inferences about
  font support can be wrong.
* Significant memory footprint. This is mostly as a result of the memory consumed
  by loading and displaying a large font list, but can be alleviated in the future
  by disabling display of features, or delaying the load of parts of the information,
  or providing a non-Qt interface.
* Very slow handling of CJK fonts, in particular when loading more than one of them
  in the character map.
* Character map filtering can also be faster.
* Many of the advanced features are not well tested, particularly involving the loading
  or management of complex filters, and may malfunction or crash.

The following bugs have been experienced in the past during the development:

* Sudden hang with 100% CPU consumption. Report if this still hapens.
* Crashes on strange fonts due to Qt bugs (this is workarounded).
