# [Fitness Wrapped](https://fitness-wrapped-app-fp3nk5sylq-ue.a.run.app/)

Ever since I bought an Apple Watch in 2020, I took data collection to the next level. I've always been a health and fitness enthusiast, but I started tracking every walk, bike ride, gym workout, body measurements, nutrition, and more. Especially being a type-1 diabetic, it's important for me to stay active, eat the right foods, and stay consistent to help manage this disease. 

## Inspiration

After my T1 diabetes diagnosis in May 2021, I realized how my personal data could improve diabetes management. I began analyzing nutrition data that I had logged in 2020 in MyFitnessPal, blood glucose data from the continous glucose monitor I wear every day, step counts from Apple Health, and body mass from my bluetooth weighing scale. I produced various charts and models but lost motivation in June after realizing the complexity of integrating data from these disjoint sources.

November came along, and I had an epiphany: winter break was coming soon and I wanted a rush of fulfillment for the new year, since I would have 3 weeks of free time. Around the time, Spotify also released Spotify Wrapped, which enabled users to view and share their top artists throughout the year in the form of a vibrant, interactive visualization. This inspired me to build my own version, but using health and fitness data instead. Similar to Spotify Wrapped, I was driven to create visuals to share aggregate statistics from my workouts and nutrition throughout the year. Version 1 came out by December, but there were many bugs, and I was only able to deploy it on a local flask server. 

For most of 2022, the project was on pause as I started my MS at Columbia University and joined Ford as an ML Engineer. In December, I saw Spotify Wrapped again and was driven to pick the project back up. I added various feature improvements which are described later.

## Project Management

Inspired by Kanban boards in the agile workflow, I first used Trello to management timelines, issues, and the workflow. In 2022, I migrated to projects on GitHub to allow for linking issues and PRs.

<img width="600" height=400 alt="Screen Shot 2021-12-28 at 5 41 03 PM" src="https://user-images.githubusercontent.com/42814002/210306329-c97ed56b-7d12-4247-9c29-9a82c4495ccf.png">

As shown above, these were some of the initial features I added to my board. I utilized 3 buckets: todo, in-progress, and complete. I updated the features daily, as new ideas came to my head.

## Methodology

1. Extract, transform, and load data.
2. Conduct EDA.
3. Build backend.
4. Build frontend.
4. Deploy the app.

### ETL (Extract, Transform, Load)

With data coming from various sources (Apple Health, MyFitnessPal (MFP), Renpho Weighing Scale, Apple Watch, Dexcom CGM, Strong Workout App), I had to develop a robust pipeline to combine all these datasets and standardize them. I wrote a script to parse the large (~2.5gb) XML from Apple Health/Watch; used APIs to pull data from MFP, Dexcom, and Renpho; and parsed CSVs from Strong. After extraction, I applied various transformations to standardize the data, create consistent sampling periods, and downsample. There was extensive preprocessing/standardization needed, especially with the unstructured formats from Apple Health (XML) and Myfitnesspal's recipe/ingredient data. For example, I had to filter out many words like brand names, proper names, and adjectives to certain ingredients like Greek Yogurt vs. Yogurt or Bob Mill's Steel Cut Oats vs. Oats. Finally, I loaded the data into local tables on GCP's BigQuery. At first, I ran the ETL scripts locally on my Mac, but later I started experimenting with CRON jobs to schedule each of the tasks. Currently, I'm working on migrating the ETL to Cloud Composer on GCP to allow for setting up triggers like file uploads to GCS, utilizing a higher performance cluster on Dataproc, leveraging pyspark, and enabling more robust orchestration. 

### EDA

This was the most exciting part: exploring my data! I produced dozens of plots and statistics like heart rate plots, wordclouds of favorite food items, macronutrient distributions, blood glucose patterns, daily TDEE, caloric intake, step count distributions, and much more. Ultimately, I narrowed down a list of 10 plots and statistics that really stuck with me. These were hard to choose, but given that the goal of this project was to "wrap up" the year, I had to be selective in what I included. These plots are implemented in the app.

My favorite visualization is the "Walking Visualizer", which highlights all my walking, cycling, running, and hiking routes throughout the world. Along with each route, various aggregate statistics (calories burned, duration, avg. heart rate, etc.) are displayed. Due to the high sampling rate of the original GPX files, I experimented with using downsampling algorithms like Ramer–Douglas–Peucker (RDP) to reduce to size of the visual. RDP hasn't proved to be too effective as it only drops the map size by ~20%. I am still experimenting with it though.

I hope to incorporate more stats/visuals related to my diabetes data in the next version. I also hope to train and deploy an ML model that will predict what workout someone should do if they want to burn a target number of calories, only have a certain amount of time, and are only willing to exert a specified amount of intensity. This is really functional to me personally, since I am always looking for the most efficient workout when I am in a rush. This step will also involve collecting data from other Apple Health/Watch users.

### Backend

This is where I learned the most, as I have no prior experience with desigining web servers. I learned about various languages, frameworks, and tools like Flask, Node, and Django. Ultimately, I settled on Flask as I'm most proficient in Python. I learned about advanced callbacks, compressing responses, and designing layouts. There are probably many optimization issues that I'm oblivious to, but I hope to incorporate tactics like caching in future versions.

### Frontend

For the front-end, I used HTML (in addition to Flask) for structuring the homepage, CSS for styling, and JS to handle client-side interactivitiy. Once again, I have no experience in front-end development besides making simple HTML webpages. I learned about the power of CSS for customizing the design of webpages and found it tricky to develop a template from scratch. I started exploring bootstrapping and hope to use more fault-tolerant templates that are friendly on all browsers and devices.

### Deployment

The last step involved deploying the web app onto a remote server. This step was important to me, as I wanted to make this public and available for anyone to see. I explored various cloud PaaS and SaaS solutions like Pythonanywhere, Heroku, AWS EC2, Digital Ocean, GCP App Engine, and GCP Cloud Run. In version 1, I decided to go with Heroku, as there were many tutorials and resources for deploying Flask/Dash apps. In 2022, I transitioned to GCP's Cloud Run, as I began working on deploying the ETL pipeline on GCP Dataproc and thought it would make the most sense to centralize around one cloud provider.

Deployment had its own set of issues. My builds kept failing due to the storage, RAM, and response size limits being exceeded. My initial app loading several large datasets into memory and conducted expensive data transformations. Since my datasets were static and only portraying statistics from 2022, I decided to only load the final, processed versions of the data and plots. 

I hope to implement CI/CD using Cloud Build on GCP for deploying new versions of the app with Github triggers; implement caching to prevent reloading the large visuals from json; and possibly load balancing and a CDN for more reachability.

**If you're interested in seeing your Fitness Wrapped, send me an email at aman.chopra@columbia.edu!**
