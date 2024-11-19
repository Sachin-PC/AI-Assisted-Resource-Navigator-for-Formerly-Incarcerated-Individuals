# AI-Assisted-Resource-Navigator-for-Formerly-Incarcerated-Individuals

Backend:
In the backend of the Project, what we have implemented So far:
1. We have implemented the Scraping of 10,000 legal documents from some of the reliable sites for information regarding legal information and also from the websites which work cloesly on providong legal support to Formerly Incarcerated people.
We have used Scrapy library to scrape the data from web concurrently following the politness policy and also by following the robot.txt of each website. We have used a priority queue in order to scrape the urls with high priority first. The priority is calculated based on the wave number(depth of the fetched url) and also the number of inlinks of the website.We will scrape more documents by the end of completing this project. The scraped files are stored locally as html files with each craweld data is stored in individual files
2. The scraped files are then batch processed to get the content and is split and stored in a vector database. We have used chroma as vector database.
3. We have worked on using different retreival strategies to getting the related documents from the vector database for a given input. In future alos, we will work on analyzing different documenbt ranking strategies and document retreival strategies like self query retreival, reranker retreival, ensembel retreival strategies.
3. In model inference, we have used Langchian's LCEL for creating a chain for multiple stages of the model inference starting from taking input query from the user to getting conversation history and passing it to the model. The model we have used here is gpt-3.5. By the completion of this project, our aim is to analyze different models along with open source models. 

To-Do(Backend)
As of now, we have implemented the end to end flow of getting the data from the vector database to have a conversational chat model. But we need to extend this to sclae for multiple users and also for a single user to have multiple sessions independednt of each other.
1. Scraping more data(50,000 - 100,000 files based on the capacity and the availability)
2. Extending the simple flow to have a database to persist the conversations w.r.t different users and different sessions. We are currently working on this and have chosen to use postgresql database(We are going with postgresql instead of SQLLite because postgresql is better at handl;ing concurrent requests and also good for scalability. As of now, we have confined our data to be of text format and hence, we have not chosen no sql database. In the future, we can look into having nosql database when we focus on different datatypes like images in the response)
3. We need to evaluate the results and if time permits, analyze different models.
4. Integrating backend with the frontend.(Front end is being developed paralelly )

The links for the backend work done till now: 
1. https://github.com/Sachin-PC/RAG_Scraper
2. https://github.com/Sachin-PC/AI-Assisted-Resource-Navigator-for-Formerly-Incarcerated-Individuals