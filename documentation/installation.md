# How to install application

## Download the project
* Go to the grocerylist appcalition github folder. Link [here](https://github.com/MiikaProject/Ostoslista)
* Download the project by clicking on "clone or download" button, then choose "Download ZIP" option
* Unzip the downloaded ZIP-file
* Follow instructions in subheading "Local use" or "Cloud use".

### Local use
* You should have project downloaded to your computer now
* In order to run project locally you need to have Python installed. You can download and install from the Python website: (https://www.python.org/)
* Navigate to the project folder with command line or open the project in editor such as [Visual Studio Code](https://code.visualstudio.com/)
* Open terminal and create a virtual enviroment for the project by typing "py -m venv venv" to the terminal. This command can be different depending on the operating system you are using and the version of python you have installed. Above is for Windows 10.
* Activate the virtual enviroment by typing "source venv/scripts/activate" into the terminal. This command also varies between operating systems. The example is for Windows 10.
* Install project requirements defined in application/requirements.txt by typing: "pip install requirements.txt" into the terminal.
* Now you are set
* Start the program by typing: "Python run.py"
* Open web browser and go to address: http://127.0.0.1:5000/
* The application is usable there, for further instruction, go to the [user guide](./userguide.md)

### Cloud eg. Heroku use
* In order to use the application as heroku app you need to have working Heroku-account. You can create a own heroku account [here](https://signup.heroku.com/)
* You also need Heroku command line tool. You can install them [here](https://devcenter.heroku.com/articles/heroku-cli)
* Follow instructions there to configure your heroku account to work with command line.
* Type "heroku create 'name of your application'" into the terminal
* Your heroku projects git repository is : https://git.heroku.com/yourprojectname.git
* Add heroku to your git remote by typing: git remote add heroku 'your repository url'
* Send project to heroku by typing:  
git add .  
git commit -m "commit to heroku"  
git push heroku master  
* You can see the url of your application website in the end
* You still need to add PostGreSQL into Heroku to be able to use database in the online application. This is done by following commands:  
heroku config:set HEROKU=1  
heroku addons:add heroku-postgresql:hobby-dev
* Now the application is fully working in Heroku!


