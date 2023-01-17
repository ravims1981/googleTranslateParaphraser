# googleTranslateParaphraser
There are paraphrasers on Huggingface that use the t5. it basically translates the input text into several languages before translating it back to English and the text appears to be rewritten. I just made one to work with Google Translate which is much faster. 

Youre going to have to find out how to enable your google translate cloud api, install the local cli, generate the key file and export the project id to the environment. 

Google charges $20 per million characters and gives you $10 worth of translations for free every billing cycle. 

2 hops are good 3 is great. Anything more than that only adds to your bill. 

This is indeed something you cna list on rapidapi. Just run the script and enter yourrapidapi secret and install an ssl on the server. 

run the app with :

`gunicorn -w 17 main:app --worker-class uvicorn.workers.UvicornWorker
`

requirements:
google-cloud-translate
fastapi
gunicorn
uvicorn
configparser
bcrypt


