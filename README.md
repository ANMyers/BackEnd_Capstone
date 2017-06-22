# About
   Hi, my name is Adam Myers and I'm a student at Nashville Software School.
This repository is my second capstone from attending the school. This is my attempt at building a machine learning application from a user choosen dataset. I utilize the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets.html) for retrieving datasets to iterate over. This site is being built to allow users to upload a dataset then run an alogorithm on that dataset.

# Why?
   The reason I went with this project is because over the course of my 
lifetime I've come across names of different algorithms that I had no idea how they worked or what they did. I wanted to see for myself how much I could learn and what I could do with different algorithms. Although the term 'algorithm' can be intimidating at first if you don't have a mathematical background I've learned that it can be quite fun and amazing to see what they can be used for and how they actually work.

# How It Works
   All a user visiting the site needs to do is first create an account by
registering. If you want information about the implemented algorithms or what format is available to upload visit the 'About' page. Once you have a grasp on the operation of the site click on 'Try It' page. You will be shown a method to name a new project, select an algorithm, upload your .txt file that contains your dataset, then click 'Continue'. Once your dataset has loaded you will be shown a view to remove variables you don't want to include and rename ones that will be the foundation for the algorithm later. You will also need to select how many sets to train on and how many to predict on (train against). Once everything is set click 'Run Algorithm'. The next view will display the results of the operation and show you predictions on what you selected to train against. You will then be allowed to go back and change things up for another go. Have fun!

# What To Expect
   First and formost the splash page should look like this:
![image](https://user-images.githubusercontent.com/24867879/27454642-3b6abfcc-5760-11e7-9e88-725178a2576b.png)

   From here you can go to About page by clicking on the link in the top right which will bring you to a page looking like this:
![image](https://user-images.githubusercontent.com/24867879/27454685-656db3ce-5760-11e7-85a4-fbaaee073e56.png)

   This page has a 'How It Works' section for explaining how to operate the site from there you can Register a new user from the link in the top right of 'Register'.

   Once Registered now you can build a project, click on 'Try It' to get started:
![image](https://user-images.githubusercontent.com/24867879/27454809-def7c248-5760-11e7-86f9-9eccd976a826.png)

   Fill out a project name, select an algorithm, upload a dataset (.txt file only), from there you can click 'Continue to step 2':
![image](https://user-images.githubusercontent.com/24867879/27454875-0edb8a76-5761-11e7-987e-8c7bcaa2511f.png)

   And the fun begins, here is your area to tinker, choose what you would like to train on and predict on, select variables to exclude and name the ones provided (for SVC you need to select an variable to predict on). Once you're all set click 'Run Algorithm':
![image](https://user-images.githubusercontent.com/24867879/27454951-548015f6-5761-11e7-9edb-9104549f243a.png)

   Now you get your results! Happy Tinkering!


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
