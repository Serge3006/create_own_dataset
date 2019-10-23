# create_own_dataset
Functions to download images from internet using different methods. Additionally functions to eliminate corrupted, duplicated images are provided
## Create Dataset
### Method 01:
Go to google images and type the category or element you want to get images for. Scroll down until the end of the page.
In the options of your browser open the Javascript Console option. A side window will appear. You have to type the following
javascript code:

* var script = document.createElement('script');
* script.src = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js";
* document.getElementsByTagName('head')[0].appendChild(script);
* var urls = $('.rg_di .rg_meta').map(function() { return JSON.parse($(this).text()).ou; });
* var textToSave = urls.toArray().join('\n');
* var hiddenElement = document.createElement('a');
* hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
* hiddenElement.target = '_blank';
* hiddenElement.download = 'urls.txt';
* hiddenElement.click();

This will generate an urls.txt file that will contain all the image url's from your query. Use the
search_google_images.py script to download the data passing the correct arguments:

* python search_google_images.py -u --urls -o --output    
--urls: path to the urls.txt file   
--output: path to the output directory for the images

### Method 02:
Using the Microsoft Bing API is possible to download hundreds of images at once. Go to the Bing API web site: https://azure.microsoft.com/en-us/try/cognitive-services/?api=bing-image-search-api and create an account to get access to the API. After that you will receive a pair of keys that you need to save because they will serve you for the query.

Run the following code:     
* python search_bing_api.py -q --query -o --output -k --keys    
--query: term you want to search for    
--output: output directory where to save the images   
--keys: keys Bing API   

## Cleaning Dataset
Because some images could be corrupted, can have just one channel and could be duplicated we need to clean the dataset. Run the following command:

* python clean_data.py -d --data    
--data: directory where the images are    

## Manual Checking
Script to check the dataset image by image and remove the irrelevant ones.

* python check_data.py  -d --data   
--data: directory where the images are    

The script will show you every image of the dataset, you have 03 options: 1) Pass to the next image, 2) Delete the image and 3) Stop the process.
