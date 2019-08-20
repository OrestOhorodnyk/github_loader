# GttHub Loader

This application will create a new repository in a user's GitHub account and commits its code to the
repository.


## Requirements:
* This application can be deployed to any OS with docker installed
* To create a new repository a user should have valid GitHub username and password

## Getting Started
```
git clone https://github.com/OrestOhorodnyk/github_loader.git
```

### Prerequisites

You need to build application with docker so install it and run:

```
cd github_loader
sudo docker build -t github_app .
```

### Installation

Wait until docker install all dependencies(it may take 5 min)

Then docker run all a container
To use default configuration (default secret key and disabled debug mode) run i terminal:
```
sudo docker run -d -p 5000:5000 --name github_loader github_app
```
If you want to set you own secret key use this command:
```
docker run -d -p 5000:5000 -e SECRET_KEY='new_key' -e --name github_loader github_app
```

## Usage
1.  Open a browser and navigate to
```
http://localhost:5000/login
```

2. Enter your GitHub **username** and **password**

3. Click the **'Create new repository'**  button in the top right corner
4. Enter name and description (name should not be used in your Github account)
5. Click the **'Create repository'**

Creation of new repository may take some time, after it dane you'll see
confirmation  message.

6. After successful repository creation you can logout by clicking on the
'Logout' button in top left corner

## Debugging in Docker container
To run the app in debug mode use
```
docker run --rm -d -p 5000:5000 DEBUG_MODE=True --name github_loader github_app
```
You may view the container logs running this command:
```
docker docker logs -f github_loader
```
Also you may find log file using the following commands:
```
docker exec -it github_loader bash
```
then navigate to the log directory
```
cd /app/logs
```

# Running the app without docker

## Requirments
- python 3.7
- virtualenv
- pip

### Installation

1. Clone the project, cd to the project
```
git clone https://github.com/OrestOhorodnyk/github_loader.git
```
2. Create and activate virtualenv with python 3.7
3. Install required packages
```
pip install -r github_loader/requirements.txt
```
4. Run the app
```
python run.py
```

#Enjoy!