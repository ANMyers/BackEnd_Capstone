# About
   Hi, my name is Adam Myers and I'm a student at Nashville Software School.
This repository is my second capstone from attending the school. This is my attempt at building a machine learning application from a user choosen dataset. I utilize the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets.html) for retrieving datasets to iterate over. This site is being built to allow users to upload a dataset then run an alogorithm on that dataset.

# Why?
   The reason I went with this project is because over the course of my 
lifetime I've come across names of different algorithms that I had no idea how they worked or what they did. I wanted to see for myself how much I could learn and what I could do with different algorithms. Although the term 'algorithm' can be intimidating at first if you don't have a mathematical background I've learned that it can be quite fun and amazing to see what they can be used for and how they actually work.

# How It Works
   All a user visiting the site needs to do is first create an account by
registering. If you want information about the implemented algorithms or what format is available to upload visit the 'About' page. Once you have a grasp on the operation of the site click on 'Try It' page. You will be shown a method to name a new project, select an algorithm, upload your .txt file that contains your dataset, then click 'Continue'. Once your dataset has loaded you will be shown a view to remove variables you don't want to include and rename ones that will be the foundation for the algorithm later. You will also need to select how many sets to train on and how many to predict on (train against). Once everything is set click 'Run Algorithm'. The next view will display the results of the operation and show you predictions on what you selected to train against. You will then be allowed to go back and change things up for another go. Have fun!

# Installing BackEnd
   If you so fancy to download or clone this site here is what you will need 
to make sure you have installed for the backend:

### Prerequisites

Install [pip](https://packaging.python.org/installing/)

Install [Python 3.6](https://www.python.org/downloads/)

From your terminal you can now use the following commands:
```
pip install django
```
```
pip install scipy
```
```
pip install numpy
```
```
pip install sklearn
```

Setting up the database:
```
python manage.py builddb 
```

Run the server:
```
python manage.py runserver
```

Now you have the backend built and running. Time for the frontend.

# Installing FrontEnd
From CapstoneClient/ directory
```
cd CapstoneClient
```
go ahead and npm install those packages
```npm install```

from there you can go ahead and run your httpserver
```
http-server
```

route to http://localhost:8080/ and you should be set. Enjoy :)


## Built With

* [Python](http://www.dropwizard.io/1.0.2/docs/) - Main Backend Language
* [Django](http://www.dropwizard.io/1.0.2/docs/) - The Backend Framework Used
* [pip](https://maven.apache.org/) - Dependency Management
* [grunt](https://gruntjs.com/) - Javascript Task Runner
