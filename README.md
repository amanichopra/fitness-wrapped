# [2021 Wrapped](https://fitness-wrapped.herokuapp.com/)

Ever since I bought an Apple Watch in 2020, I took data collection to the next level. I've always been a health and fitness enthusiast, but I started tracking every walk, bike ride, gym workout, body measurements, nutrition, and more. Especially being a type-1 diabetic, it's important for me to stay active, eat the right foods, and stay consistent to help manage this disease. 

## Inspiration

After my T1 diabetes diagnosis in May 2021, I realized how my own personal data could impact more than just diabetes management. I began analyzing nutrition data that I had logged in 2020 in MyFitnessPal, blood glucose data from the continous glucose monitor I wear every day, step counts from Apple Health, and body mass from my bluetooth weighing scale. I produced various charts and models but lost motivation in June after realizing the complexity of integrating data from these disjoint sources.

November came along, and I had an epiphany: winter break was coming soon and I needed to come up with a game plan to feel fulfilled and do something productive and exciting, since I would have 3 weeks of free time. Around the time, Spotify also released "Spotify Wrapped", which leveraged data science to portray fun, competitive statistics for users to view and share. This inspired me to build my own version, but using health and fitness data instead. Similar to Spotify Wrapped, I was driven to create high-level visuals to share aggregate statistics from my workouts and nutrition through the year.

## Managing Goals, Workflows, and Timelines

After this epiphany, I began brainstorming how I could execute this vision and build something deliverable. I've always had ideas in my head, but this one was different. I couldn't waste all the data that I've been tracking so consistently. I learned about Trello and the agile workflow to help manage my project workflow. 

<img width="568" height=500 alt="Screen Shot 2021-12-28 at 5 41 03 PM" src="https://user-images.githubusercontent.com/42814002/147619493-a8ad10ff-0ff3-415c-8438-578d1bf06714.png">

As shown above, these were some of the initial features I added to my kanban boards. I utilized 3 buckets: todo, in-progress, and complete. I updated the features daily throughout November, as new ideas came to my head.

## Methodology

Finally, winter break came along. I had 3 weeks to get this project to a deliverable state. At this point, my workflow boards had 4 main items:
1. Extract, transform, and load data.
2. Design meaningful visuals portraying my walking routes, activity levels, aggregate statistics, and nutrition.
3. Create a web application.
4. Deploy the app.

### ETL (Extract, Transform, Load)

This part of the project resulting in the most bugs. With data coming from various sources (Apple Health, MyFitnessPal (MFP), Renpho Weighing Scale, Apple Watch, Dexcom CGM, Strong Workout App), I had to develop a robust pipeline to combine all these datasets and standardize them. I wrote a script to parse the large (~1.5gb) XML from Apple Health/Watch; I used APIs to pull data from MFP, Dexcom, and Renpho; and I parsed CSVs from Strong. After extraction, I applied various transformation to standardize the data and create consistent sampling periods (mostly downsampling). Finally, I loaded the data into local SQL tables.

### EDA and Designing Visuals

This was the most exciting part: exploring my data! I produced dozens of plots and statistics like heart rate distributions, favorite food items, macronutrient distributions, blood glucose patterns, daily TDEE, caloric intake, step count distributions, and much more. Ultimately, I narrowed down a list of 10 plots and statistics that really stuck with me. These were hard to choose, but given that the goal of this project was to "wrap up" the year, I had to be selective in what I included. These plots are implemented in the app.

### Creating the Web App

Creating the web app was definitely the most difficult part. At the same time though, this is where I learned the most. I don't have prior front-end experience with desigining websites or UIs. I learned about various languages, frameworks, and tools like Flask, Django, HTML, CSS, JS, Bootstrap, and React. Ultimately, I decided to use HTML for structuring the site, Boostrap CSS to style it, JS for the interactivity, and Flask in Python to implement the dashboard. 

Designing the layout for the site was the fun part. In fact, it felt more like art than programming. I spent days drawing layouts on my iPad, planning where to position each of the plots and statistics. After coming up with a satisfying layout, I went about writing the HTML, CSS, and JS. After this, I wrote the Flask app and tested locally.

### Deployment

The last step involved deploying the web app onto a remote server. This step was important to me, as I wanted to make this public and available for anyone to see. I explored various cloud Platform as a Service (PaaS) solutions like Pythonanywhere, Heroku, AWS Elastic Beanstalk, Digital Ocean, and Amazon EC2. Ultimately, I decided to go with Heroku, as there were many tutorials and resources for deploying Flask/Dash apps.

This step was all about containerizing the app. Heroku runs on dyno, which is its own container, but also includes support for docker. I explored both these options but settled on dynos due to its low overhead. 

Deployment had its own set of issues. My builds kept failing due to the storage and RAM limits being exceeded. My initial app loading several large datasets into memory and conducted expensive data transformations. Since my datasets were static and only portraying statistics from 2021, I decided to only load the final, processed versions of the data and plots. Heroku's free plan only allowed for 512mb of RAM and storage, so this was very beneficial. Another issue I ran into was Git's file storage limit being exceeded. GitHub has its own quotas, so I had to incorporate Git LFS and connect it to Heroku for successful deployment.

After deployment, the app was functional but slow in loading. The walking visualizer map with 900+ walks and 1 million coordinates from the year was a 150mb file causing the app to crash or load slowly. This is why the webpage takes a while to load.

## Next Steps

This was originally just a winter break project, but now having built this full-stack system, I'm inspired to make this grow. Here are some of the new tasks in the pipeline:

- Implement the Ramer–Douglas–Peucker algorithm to downsample the GPX files being loaded into the map. The goal is to reduce file size to below 100mb for faster rendering and so I can prevent using Git LFS.
- Deploy the walking visualizer map as its own standalone app. Instead of embedding the HTML for the map directly in the dashboard, add a hyperlink redirecting to the standalone. Since I'm using Heroku's free service, this would help improve load time by distributing the load across two sites rather than one.
- Deploy an ML model that will predict what workout someone should do if they want to burn a target number of calories, only have a certain amount of time, and are only willing to exert a specified amount of intensity. This is really functional to me personally, since I am always looking for the most efficient workout when I am in a rush. This step will also involve collecting data from other Apple Health/Watch users.
- Incorporate more diabetes-related metrics.
- Schedule tasks for ETL. I've done this with my Dexcom CGM data before using cron jobs on my local system, but with this scale of data, local storage is no longer an option. I will probably have to look into cloud options like Amazon's EBS, RDS, or S3.

**If you're interested in seeing your 2021 Wrapped, send me an email at amanichopra@gmail.com!**
