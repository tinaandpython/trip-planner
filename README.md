![Custom Logo](trip_planner/itinerary_generator/static/images/brand_logo.png)

Trip Planner is a web application built on Django framework that utilizes an integrated AI API to generate personalized travel itineraries based on user-provided destination and number of days. It allows users to store generated itineraries and delete them as needed.

# Features: 

* Itinerary Generation: Users can input a destination and the number of days they plan to stay, and the application generates a detailed travel itinerary using an AI-powered API.

* User Authentication: Secure user authentication system ensures that only registered users can access and store their itineraries.

* Session Management: Utilizes Django sessions to temporarily store generated itineraries before they are saved to the database upon user request.

* CRUD Operations: Users can save generated itineraries to their profile and delete them if they no longer need them.

* Responsive Design: The application is designed to be responsive, ensuring optimal user experience across devices of different screen sizes.

# Technologies Used:

* Django: Python-based web framework for rapid development and clean design.
* Bootstrap: Front-end framework for responsive and mobile-first design.
* RapidAPI: Integrated API service used for generating travel itineraries based on AI algorithms.
* Docker: The application is containerized using Docker, ensuring a consistent environment across different systems. However, the database backend is configured to use SQLite, which is stored locally within the container rather than using a separate Docker image for the database.


## Icons and Logos:

- **Bootstrap Icons**: Used for navigation menu icons.
  - [Bootstrap Icons](https://icons.getbootstrap.com/)
  
- **Akar Icons**: Used for toggle menu icon in mobile view and buttons.
  - [Akar Icons](https://akaricons.com/)

- **Custom Logo**: Used on the homepage. Created by Me :) on:
  - [Canva](https://shorturl.at/i00PF)

# To-be-Done:

* User Profile: A possibility for the users to change their username, email, password and add a profile picture.
  
* Custom Itinerary: Allows users to create personalized travel itineraries based on their preferences. Users can specify destinations, number of days and fill in each day with the desired activities.
  
* Media: Possibly integrate another API that would return a photo of a selected destination.

* Database: Migrate the data from SQLite to PostgreSQL or MongoDB database to make the project more scalabale and suitable for deployment and dockerization.
