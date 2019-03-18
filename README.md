### Automated search & download images from google search result. 

The Script take the image query, number of images to be scraped, and the preffered size of images.
For example an input of 'cat' 23 L return 23 large google images of cats.
The download directory created in the script folder and named as the query.
So a query for 'cats' download the image files to a folder called 'cats'

Script written in Python 3.7 utilizing Selenium WebDriver library
tested in Windows

### Installation guide
[Clone repo](https://github.com/Av1chem/HW/archive/master.zip) and run command in terminal at the repo folder:
```
py -m pip install -r requirements.txt
```
After that you should be able to execute
```
python gImagesSearch.py
```
NOTE: You need Python3 & pip installed first. (Check https://www.python.org/downloads/release/python-372/ for installation instruction).

