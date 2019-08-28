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
* Open terminal and create a virtual enviroment for the project by typing "python -m venv venv" to the terminal.
* Activate the virtual enviroment by typing "source venv/scripts/activate" into the terminal. 
* Install project requirements defined in application/requirements.txt by typing: "pip install requirements.txt" into the terminal.
* Now you are set
* Start the program by typing: "Python run.py"
* Open web browser and go to address: http://127.0.0.1:5000/
* The application is usable there, for further instruction, go to the [user guide](./userguide.md)

### Cloud eg. Heroku use
* In order to use the application as heroku app you need to have working Heroku-account. You can create a own heroku account [here](https://signup.heroku.com/)
* You also need Heroku command line tool. You can install them [here](https://devcenter.heroku.com/articles/heroku-cli)
* Follow instructions there to configure your heroku account to work with command line.

