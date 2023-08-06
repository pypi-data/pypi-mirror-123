# 📀 LabCAS Downloader

This is a simple downloader script for [LabCAS](https://edrn.nci.nih.gov/data-and-resources/informatics/labcas), the Laboratory Catalog and Archive System. This script enables you to "bulk download" data from a LabCAS installation such as

-   [Early Detection Research Network's LabCAS](https://edrn-labcas.jpl.nasa.gov/)
-   The [Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions's LabCAS](https://mcl-labcas.jpl.nasa.gov/)
-   Or any other LabCAS installation that supports the LabCAS API.


## 🖥 Prerequisites

This software works with Python 3.8, 3.9, or 3.10. Other versions may work but have not been tested.


## 💿 Installation

To install the LabCAS downloader, simply use the Python package installer, `pip`, i.e.:

    pip install jpl.labcas.downloader

You'll probably want to do this in a virtual environment so the package doesn't conflict with other Python usage on your system. For example, on a typical Unix (or macOS) system, you'd run (where `$` is the command-line prompt):
```console
$ python3 -m venv venv
$ cd venv
$ bin/pip install jpl.labcas.downloader
```
Then use the `bin/jpl-labcas-downloader` program out of the `venv` directory.


## 💁‍♀️ Usage

To use the LabCAS Downloader, you'll need to have the following information at the ready:

-   The **collection ID** or the **collection/dataset ID** of the data you want to download. For example, if you're after the entire Automated Quantitative Measures of Breast Density Data, use the collection ID `Automated_Quantitative_Measures_of_Breast_Density_Data`. However, if you want just the `C0250` dataset from that collection, use `Automated_Quantitative_Measures_of_Breast_Density_Data/C02520`. You can append more `/`s for nested datasets as needed.
-   Your assigned LabCAS **username and the password** that authenticates your account.
-   Lastly, the **API endpoint** you want to use:
    -   For EDRN, that's `https://edrn-labcas.jpl.nasa.gov/data-access-api/`
    -   For the Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions, it's `https://edrn-labcas.jpl.nasa.gov/data-access-api/`

Then, run the `jpl-labcas-downloader` as follows:

    jpl-labcas-downloader --username USERNAME --api URL DATA-ID

For example, to download the `Automated_Quantitative_Measures_of_Breast_Density_Data` from the API at `https://edrn-labcas.jpl.nasa.gov/data-access-api/` using username `jane`, run:

    jpl-labcas-downloader --username jane --api https://edrn-labcas.jpl.nasa.gov/data-access-api/ Automated_Quantitative_Measures_of_Breast_Density_Data

You'll be prompted for your password, and files will be written to the current directory.


👉 **Note:** Any existing files will be overwritten.


### 🎨 Customization

The `jpl-labcas-downloader` supports several options as well as environment variables to customize its behavior.

-   `--username USERNAME` tells the username to use to authenticate to the API. You can set the `LABCAS_USERNAME` environment variable to serve as a default. Leave this out to use no authentication.
-   `--password PASSWORD` indicates the password to use, but **this is insecure** as password should not be put on command-lines. The `LABCAS_PASSWORD` can provide the default password. However, if neither the option nor the environment variable is given, you will be prompted for a password.
-   `--api URL` tells the URL of the LabCAS API to query. It defaults to the `LABCAS_API_URL` environment variable. If neither is given, `https://edrn-labcas.jpl.nasa.gov/data-access-api/` is the fallback value.
-   `--TARGET DIR` tells in what directory to write output files. It defaults to the current directory.

You can see all the options at a glance by running `jpl-labcas-downloader --help`.


## 👥 Contributing

Within the JPL Informatics Center, we value the health of our community as much as the code, and that includes participation in creating and refining this software. Towards that end, we ask that you read and practice what's described in these documents:

-   Our [contributor's guide](https://github.com/EDRN/.github/blob/main/CONTRIBUTING.md) delineates the kinds of contributions we accept.
-   Our [code of conduct](https://github.com/EDRN/.github/blob/main/CODE_OF_CONDUCT.md) outlines the standards of behavior we practice and expect by everyone who participates with our software.

### 🔧 Development

If you're a developer of this package, you'll probably do something like the following:
```console
$ git clone https://github.com/EDRN/labcas-downloader.git
$ cd labcas-downloader
$ python3 -m venv venv
$ venv/bin/pip install --quiet --upgrade pip setuptools
$ venv/bin/pip install --editable '.[dev]'
```
Then, changes you make to files under `src` will be immediately reflected in `venv/bin/jpl-labcas-downloader` when run. `venv/bin` will also contain supporting development tools.


### 🔢 Versioning

We use the [SemVer](https://semver.org/) philosophy for versioning this software.


## 📃 License

The project is licensed under the [Apache version 2](LICENSE.md) license.
