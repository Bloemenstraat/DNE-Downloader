# "This person does not exist" Downloader

Scraper for the [this person doesn not exist website](https://this-person-does-not-exist.com/) . Helps you automatically download batch of files from the website and sort them by gender.

##Dependencies
The following dependencies are required to operate this script:

```
pip install requests bs4 tqdm opencv-python
```

## CLI arguments
```
-n, --number
```
Specify the number of images you would like to download.

```
-j, --jsonify
```
If selected, creates a file named "pictures.json" in the current directory that lists the images' filenames and their gender.
