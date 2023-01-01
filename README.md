# [Fitness Wrapped](https://fitness-wrapped-app-fp3nk5sylq-ue.a.run.app/)

Ever since I bought an Apple Watch in 2020, I took data collection to the next level. I've always been a health and fitness enthusiast, but I started tracking every walk, bike ride, gym workout, body measurements, nutrition, and more. Especially being a type-1 diabetic, it's important for me to stay active, eat the right foods, and stay consistent to help manage this disease. 

## Inspiration

After my T1 diabetes diagnosis in May 2021, I realized how my personal data could improve diabetes management. I began analyzing nutrition data that I had logged in 2020 in MyFitnessPal, blood glucose data from the continous glucose monitor I wear every day, step counts from Apple Health, and body mass from my bluetooth weighing scale. I produced various charts and models but lost motivation in June after realizing the complexity of integrating data from these disjoint sources.

November came along, and I had an epiphany: winter break was coming soon and I wanted a rush of fulfillment for the new year, since I would have 3 weeks of free time. Around the time, Spotify also released Spotify Wrapped, which enabled users to view and share their top artists throughout the year in the form of a vibrant, interactive visualization. This inspired me to build my own version, but using health and fitness data instead. Similar to Spotify Wrapped, I was driven to create visuals to share aggregate statistics from my workouts and nutrition throughout the year. Version 1 came out by December, but there were many bugs, and I was only able to deploy it on a local flask server. 

For most of 2022, the project was on pause as I started my MS at Columbia University and joined Ford as an ML Engineer. In December, I saw Spotify Wrapped again and was driven to pick the project back up. I added various feature improvements which are described below.

## Project Management

Inspired by Kanban boards in the agile workflow, I used Trello to management timelines, issues, and the workflow. 

<img width="568" height=500 alt="Screen Shot 2021-12-28 at 5 41 03 PM" src="https://user-images.githubusercontent.com/42814002/147619493-a8ad10ff-0ff3-415c-8438-578d1bf06714.png">

As shown above, these were some of the initial features I added to my board. I utilized 3 buckets: todo, in-progress, and complete. I updated the features daily, as new ideas came to my head.

## Methodology

1. Extract, transform, and load data.
2. Conduct EDA.
3. Build backend.
4. Build frontend.
4. Deploy the app.

### ETL (Extract, Transform, Load)

With data coming from various sources (Apple Health, MyFitnessPal (MFP), Renpho Weighing Scale, Apple Watch, Dexcom CGM, Strong Workout App), I had to develop a robust pipeline to combine all these datasets and standardize them. I wrote a script to parse the large (~2.5gb) XML from Apple Health/Watch; used APIs to pull data from MFP, Dexcom, and Renpho; and parsed CSVs from Strong. After extraction, I applied various transformations to standardize the data, create consistent sampling periods, and downsample. Finally, I loaded the data into local tables on GCP's BigQuery.

### EDA

This was the most exciting part: exploring my data! I produced dozens of plots and statistics like heart rate plots, wordclouds of favorite food items, macronutrient distributions, blood glucose patterns, daily TDEE, caloric intake, step count distributions, and much more. Ultimately, I narrowed down a list of 10 plots and statistics that really stuck with me. These were hard to choose, but given that the goal of this project was to "wrap up" the year, I had to be selective in what I included. These plots are implemented in the app.

### Backend/Front-End

This is where I learned the most, as I don't have prior back-end or front-end experience with desigining websites or UIs. I learned about various languages, frameworks, and tools like Flask, Node, and Django. Ultimately, I settled on Flask as I'm most proficient in Python. I learned about advanced callbacks, compressing responses, and designing layouts.

### Frontend

For the front-end, I used HTML (in addition to Flask) for structuring the homepage, CSS for styling, and JS to handle client-side interactivitiy.

### Deployment

The last step involved deploying the web app onto a remote server. This step was important to me, as I wanted to make this public and available for anyone to see. I explored various cloud PaaS and SaaS solutions like Pythonanywhere, Heroku, AWS EC2, Digital Ocean, GCP App Engine, and GCP Cloud Run. In version 1, I decided to go with Heroku, as there were many tutorials and resources for deploying Flask/Dash apps. In 2022, I transitioned to GCP's Cloud Run, as I began working on deploying the ETL pipeline on GCP Dataproc and thought it would make the most sense to centralize around one cloud provider.

This step involved containerizing the app, pushing the image to a registry, and deploying the service. 

Deployment had its own set of issues. My builds kept failing due to the storage, RAM, and response size limits being exceeded. My initial app loading several large datasets into memory and conducted expensive data transformations. Since my datasets were static and only portraying statistics from 2022, I decided to only load the final, processed versions of the data and plots. Heroku's free plan only allowed for 512mb of RAM and storage, so this was very beneficial. Another issue I ran into was Git's file storage limit being exceeded. GitHub has its own quotas, so I had to incorporate Git LFS and connect it to Heroku for successful deployment.

After deployment, the app was functional but slow in loading. The walking visualizer map with 900+ walks and 1 million coordinates from the year was a 150mb file causing the app to crash or load slowly. This is why the webpage takes a while to load.

## Next Steps

This was originally just a winter break project, but now having built this full-stack system, I'm inspired to make this grow. Here are some of the new tasks in the pipeline:

- Implement the Ramer–Douglas–Peucker algorithm to downsample the GPX files being loaded into the map. The goal is to reduce file size to below 100mb for faster rendering and so I can prevent using Git LFS.
- Deploy the walking visualizer map as its own standalone app. Instead of embedding the HTML for the map directly in the dashboard, add a hyperlink redirecting to the standalone. Since I'm using Heroku's free service, this would help improve load time by distributing the load across two sites rather than one.
- Train and deploy an ML model that will predict what workout someone should do if they want to burn a target number of calories, only have a certain amount of time, and are only willing to exert a specified amount of intensity. This is really functional to me personally, since I am always looking for the most efficient workout when I am in a rush. This step will also involve collecting data from other Apple Health/Watch users.
- Incorporate more diabetes-related metrics.
- Schedule tasks for ETL. I've done this with my Dexcom CGM data before using cron jobs on my local system, but with this scale of data, local storage is no longer an option. I will probably have to look into cloud options like Amazon's EBS, RDS, or S3.
- Add CI/CD for updates to the app code.
- Leverage pyspark for initial processing of raw data. Although the app assumes the data is processed already, if I wanted to scale the app to allow users to upload their Apple Health exports (XML), I would need to trigger an ETL pipeline (perhaps using a service like Dataproc on GCP) to do the heavy procesing. These XMLs are over 2GB!

**If you're interested in seeing your Fitness Wrapped, send me an email at amanichopra@gmail.com!**
