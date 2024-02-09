# To get the logos of all 100 FTSE companies in an efficient manner, we will use Wikipedia's free API. 

### The logic - Wikipedia has an article on FTSE-100 companies (https://en.wikipedia.org/wiki/FTSE_100_Index) which contains a table of the members, with links to their website. We can use Wikipedia's API (MediaWiki API) to go to each of these links, and grab the first image in them whose name contains 'logo' and the company name

### Cool! We have grabbed most images, and saved a lot of time. Now, we can go through the images manually to replace the missing logos. These are caused when the image is hosted by Wikimedia while the API only retrieves images from Wikimedia Commons.

### Not bad, 23% were incorrect/unavailable, but that means we automated 77% of our work