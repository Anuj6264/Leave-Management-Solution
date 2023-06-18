# Leave-Management-Solution
A leave management solution is an application that allows an employee to request for leaves and a manager to accept or reject the leaves using Python Flask Application on Backend and Vue JS on Frontend. For the purpose of storing data, PostgreSQL database is used.  

## Getting Started

To get started with Leave-Management-Solution, follow the instructions below:-

### Prerequisites

Make sure you have the following prerequisites installed on your machine:

- Python (version 3.11.4)
- node (version 18.16.0)
- npm (version 9.5.1)
- PostgreSQL (version 15.3)
- pgAdmin 4 (version 7.3)

### Clone the Repository

Clone the Leave-Management-Solution repository to your local machine using the following command:

```shell
git clone https://github.com/Anuj6264/Leave-Management-Solution.git 
```

## Install Dependencies
Navigate to the cloned repository directory and install the project dependencies by running the following commands:

### Backend
```shell
cd backend
pip3 install -r requirements.txt
```
For connecting to database, create a profile on pgAdmin 4 , creating username and password while installing it. Create a new Database in the dashboard. 
Now use these credentials in the ``backendApp.py`` file.

```shell
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<your-username>:<your-password>@localhost:5432/<your-database-name>'
```
Save the file and run the ``backendApp.py`` file. This will connect the backend server with the PostgreSQL database and will create tables in this database.

### Frontend
```shell
cd frontend
cd frontend
npm init
npm install
```

## Running the App

Execute the following commands to run the application:

### Backend
```shell
python backendApp.py
```
### Frontend
```shell
npm run serve
```
This will start backend and frontend applications at different ports. The frontend port will be possibly ``http://localhost:8080/`` or ``http://localhost:8081/`` and backend port should be ``http://127.0.0.1:5000``. 

Your app should be running by now, please check the port ``http://localhost:8080/`` to see the application running!

## Demo 

To see the demo of the application running, headout to this [link](https://drive.google.com/file/d/1iNUOux9Vi0jSKI2IntLe__zWVQmYa3wj/view?usp=sharing) where the different features of the application are shown.
