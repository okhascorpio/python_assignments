Add your postgresql credentials in .env file


install required dependencies by running 
$ pip install -r requirements.txt

Run the app
$ flask run




Useing Postman send POST request to create user:
localhost:5000/api/v1/signup
{
"email":"user1@hello.com",
"password":"one"
}

Response you receive is:
{
    "message": "User created"
}




Send signin request POST:
localhost:5000/api/v1/signin
{
"email":"user1@hello.com",
"password":"one"
}

response received JWT access token for the user:
{
 "user": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsIml
        hdCI6MTY2MjkxNTk4NSwianRpIjoiNzQ2MjhmMTktNmU3Ni00ODNiLTk0NmYtZmEwNzc5OT
        NmYTlhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjYyOTE1OTg1LCJleHAiOj
        E2NjI5MTY4ODV9.QbqiNlkrT3hyQdGQSNkJxkDaL7SwhDOC1SClmyj_MME",
        "user": "user1@hello.com"
        "user_id": "1"
    }
}




Add access token to the Auth Bearer Token field in the Postman app for all next functions

Send PUT request to change password
localhost:5000/api/v1/changePassword
{
"password":"new"
}




Send POST request to create new todo item for current user

localhost:5000/api/v1/todos
{
"name":"todo item1 user1",
"description":"is optional"
}




Send GET request to receive list of all todo items 
localhost:5000/api/v1/todos

Or add status query parameter in the url to receive list of items with specific status
localhost:5000/api/v1/todos?status=NotStarted




send PUT request to update existing todo item
by adding id of the todo item in the url, and access token of the user in the Auth Bearer token field.
localhost:5000/api/v1/todos:1
{
"name":"updated name of todo item1",
"description":"updating status to OnGoing",
"status":"OnGoing"
}

if item id is matched with the id of the bearer token sent, the item will be updated




send DELETE request to delete existing todo item
by adding id of the todo item in the url, and access token of the user in the Auth Bearer token field.
localhost:5000/api/v1/todos:1

if item id is matched with the id of the bearer token sent, the item will be deleted














