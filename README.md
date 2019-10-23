# create_own_dataset
Functions to download images from internet using different methods. Additionally functions to eliminate corrupted, duplicated images are provided

## Method 01:
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

