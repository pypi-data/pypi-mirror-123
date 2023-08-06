With Data Scraper you can scrape any website without the need of inspecting web elements or parsing HTML using Beautiful Soup etc.  
With just URLs as input you get JSON data as output.  
First you need to train the scraper for particular website & then run it.

![Data Scraper Explanation](https://firebasestorage.googleapis.com/v0/b/datakund-studio.appspot.com/o/Pypi%20data%20scraper.png?alt=media&token=8da8dc2e-3d88-45e2-a300-b60cfc68d8e2)


### Youtube Video Link
[![Youtube Video Link](https://img.youtube.com/vi/z35Fq9nRE2k/0.jpg)](https://www.youtube.com/watch?v=z35Fq9nRE2k)

### Train Scraper
```sh
from data_scraper import *
URL1='https://pypi.org/search/?q=request'
URL2='https://pypi.org/search/?q=datakund'
response=scraper.train(URL1,URL2)
print(response)
#{'id':'QJP4LW2EBTQM45N',success:true}
open('PyPi Scraper.txt', 'w').write(response['id'])
```

### Run Scraper
```sh
from data_scraper import *
Id=open('PyPi Scraper.txt', 'r').read()
#This is id of scraper we got in training above
URL3='https://pypi.org/search/?q=scraper'
response=scraper.run(URL3,id=Id)
with open('./data.json','w') as data:
	data.write(json.dumps(response,indent=4))
```


### How it works?
* It takes two URLs of 2 similiar pages to train the scraper.
* It learns from the HTML structure of those pages and builds a scraper.
* In the response you get ID of the scraper.
* That ID can be used to run the scraper for the URLs of pages simililar to the above used in training.


### Examples
Below are some of the examples of URLs using which you can train the scraper:-
1. Pypi packages scraper [https://pypi.org/search/?q=firebase](https://pypi.org/search/?q=firebase)  [https://pypi.org/search/?q=datakund](https://pypi.org/search/?q=datakund)
2. Wordpress theme scraper [https://wordpress.org/themes/search/green/](https://wordpress.org/themes/search/green/)   [https://wordpress.org/themes/search/red/](https://wordpress.org/themes/search/red/)
3. Cryptocurrency details scraper [https://coinmarketcap.com/](https://coinmarketcap.com/)  [https://coinmarketcap.com/?page=2](https://coinmarketcap.com/?page=2)
4. PlayStore app details scraper[https://play.google.com/store/apps/details?id=com.whatsapp](https://play.google.com/store/apps/details?id=com.whatsapp)   [https://play.google.com/store/apps/details?id=org.telegram.messenger](https://play.google.com/store/apps/details?id=org.telegram.messenger)

### Queries/ Feedback
If you have some queries or feedback please contact us at following    
[Telegram](https://t.me/datakund)  
[Email](abhishek@datakund.com)