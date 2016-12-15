#EasyFuelTracker

Code Institute stream 3 project.

View here:
[https://stream3.jamcoy.com](https://stream3.jamcoy.com).

##About
EasyFuelTracker has two primary goals:
* To enable people to calculate and track their car’s true fuel economy.
* To enable potential purchasers of cars to browse collated data from all the users to ascertain true fuel economy performance (rather than manufacturers' figures).
 
##Main features

###User accounts with credit card payments for subscriptions
When registering at EasyFuelTracker, the user is required to sign-up for a monthly subscription.  This is handled by the
 stripe online credit card payment platform.  Once registered, the user will be able to add cars to their account and post
 messages in the forums.

###Car fuel economy tracker 'My cars'

This is the main component of EasyFuelTracker.  Demo account details have been provided to the Code Institute.  Without these, you
 will need to input a lot of data to see anything interesting.

Users can add their cars to their account by entering their registration number.
 This is posted to an API which responds with all the details about the car.  The user must confirm it's the correct vehicle, which
 enables any collected fuel economy data to be collated and contributed to the community.
 
 Insert ppitcure confirming details.
 
 Once a vehicle has been added, the user can start logging their refueling events.  The data is processed to show various statistics to the user:
 
[[https://github.com/jamcoy/stream3/master/README_images/chart.png|alt=chart]]
 
 The interactive charts show the following data over time:
 * Fuel economy
 * Mileage
 * Fuel price per litre
 * Cost to refuel the vehicle
 * Mileage
 
 The chart uses Chart.js with Chart.Scatter.
 
  Additionally, the user can:
 * Add additional cars
 * View each car's details
 * View each car's refueling history
 * Delete a car
 
 [[https://github.com/jamcoy/stream3/master/README_images/Confirm_car.png|alt=add_car]]
 [[https://github.com/jamcoy/stream3/master/README_images/Refuel_history.png|alt=Refuel_history]]

###Car economy statistics 'Economy stats'
All the collated data from all the users vehicles can be explored by a user.  By using a series of ajax-enabled select
 menus, the user can progressively drill down to a specific vehicle type to see it's average fuel economy.  Once the three key
 fields (manufacturer, model and year) have been entered, results will be displayed.  The user can continue to drill down further using
 sub-modal, engine size, transmission and fuel type.
  
  For this to be truly useful a large number of users will need to log their refueling activities over a period of time.
 
###Forum (with poll feature)
Anyone can view the forum.  Only logged in members can post.  The forum is fully responsive and supports posting of remotely hosted images and emoticons.

###Blog with commenting via Disqus
The list of blog entries are displayed to the user as a series of cards.  Clicking any of the cards will take the user to the blog.  Users can 
 leave comments using the Disqus commenting platform.

###Complementary pages
Standard 'about' and 'terms' pages are provided with 'Lorem Ipsum' content.  A contact form is provided which will send an email to admin staff. 

##Design aspects
EasyFuelTracker has been developed to be fully responsive and has been tested across a range of devices.  This has been achieved by using bootstrap and media queries.

##Technology stack and third party libraries and packages
**[Django](http://flask.pocoo.org/)** - Web application framework.
* Python for the backend
* HTML and CSS for the frontend
* JavaScript and jQuery for ajax functionality between server and client
* MySQL for the production database (SQLite was used while in development) 

###Django / python package highlights:
**[Django-stdimage](https://github.com/codingjoe/django-stdimage)** - Django Standardized Image Field.  Resizes images when uploaded by a user.  Requires Pillow to be compiled with support for jpeg encoding and decoding.
**[Pillow](http://python-pillow.org/)** - Python Imaging Library
**[Arrow](http://crsmithdev.com/arrow/)** - A Python library that offers a human-friendly approach to creating, manipulating, formatting and converting dates, times, and timestamps.
**[Django-Disqus](https://github.com/arthurk/django-disqus/)** - Facilitates using the Disqus commenting platform in Django applications.

For the full list of python packages, please refer to the requirements in the repository.

##Third party libraries
**[Bootstrap](http://getbootstrap.com/)** provides a responsive framework to the application.  This was enhanced with media queries and additional code to resize some of the dc.js charts, which are not natively responsive.
**[TinyMCE](https://www.tinymce.com/)** - JavaScript HTML WYSIWYG editor used in the blog and forum applications.  In the forums, it's configured to enable users to include emoticons and externally hosted images. 
**[Stripe](https://stripe.com)** - Online credit card payment platform.  When registering at EasyFuelTracker, users are required to make a monthly payment by subscription.
**[Date range picker](http://www.daterangepicker.com/)** - A JavaScript library for choosing date ranges and designed to work with the Bootstrap CSS framework.  Used for entering refueling dates.
**[Moment.js](http://momentjs.com/)** - A JavaScript library for parsing, validating, manipulating and displaying dates in JavaScript. Required by Date Range Picker.
**[Chart.js](http://www.chartjs.org/)** - A JavaScript charting library.
**[Scatter chart](http://dima117.github.io/Chart.Scatter/)** - A scatter chart is a graph in which the values of two variables are plotted along two axes.  In the case of EasyFuelTracker, Chart.Scatter enables the displaying of data that does not have a set 
time frequency, which is usually the case for refueling a vehicle.  Chart.Scatter is an addon for the Chart.js library. 
**[Bootstrap Select](https://silviomoreto.github.io/bootstrap-select/)** - Provides bootstrap styling to standard select elements.

##Testing
A suite of unit tests were developed for the 'Cars' application to ensure that the templates render correctly and show the correct information.  This includes checking the calculated statistics (in 'My cars') and a number of unit tests for the refueling form. 

##Fuel economy calculations
EasyFuelTracker calculates a vehicle's fuel economy using the brim-to-brim method (one full tank to the next full tank).
Partial tanks are included in the calculations if they meet the following conditions:
* Single partial tanks must be preceded by and followed by a full tank, with no missed refuels reported.
* Sequential partial tanks must be preceded by a full tank and must end with a full tank, with no missed refuels anywhere in the sequence.

If a uses misses logging any refuels, their latest refuel and all preceding refuels to the previous full tank are excluded. However, the latest full tank becomes a valid start point for the next brim-to-brim calculation, but cannot be included in the previous brim-to-brim calculation.

Users are encouraged in several places to fill their tank when refueling and not to miss logging anything.  Messages are shown when tracking is suspended or resumed when they report that they have missed logging something.

##Hosting
The website is hosted on a virtual private server (Debian) using Gunicorn as the webserver, with Nginx acting as a reverse proxy server.  Nginx is configured to use gzip compression and TLS encryption.

##Notes
If you clone the repository and run the code locally, you will need to specify which of the settings files you wish to use.
For example: python manage.py runserver --settings=settings.dev

