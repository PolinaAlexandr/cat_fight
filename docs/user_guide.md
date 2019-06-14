# User_guide!
## cURL examples :

 Lets start with the registratin:
```
    $ curl -X POST -H "Content-Type:application/json" -d '{"user_name" : "your_user_name", "password" : "your_password"}' http://host:port/registration
```

After registration you should login. Just replace `registration` endpoint with `login`. Do not forget to copy your output token for the future operations:

```
    $ curl -X POST -H "Content-Type:application/json" -d '{"user_name" : "your_user_name", "password" : "your_password"}' http://host:port/login
```

For logging out(`/logout`) use the current form: 
```
    $ curl -X POST -H "Content-Type:application/json" -d '{ "token" : "your_valid_token"}' http://host:port/logout
```
Statistics endpoint(`/stats`) shows information about chosen user, it is avalible only for logined users:
```
    $ curl -X POST -H "Content-Type:application/json" -d '{"user_name" : "chosen_user_name", "token" : "your_valid_token"}' http://host:port/stats
```
Time to join the battle and meet your enemy! Searching for the partner starts here `battle/join`: 
```
    $ curl -X POST -H "Content-Type:application/json" -d '{"token" : "your_valid_token"}' http://host:port/battle/join

```
To know your battle status try `/battle/status`:
```
    $ curl -X POST -H "Content-Type:application/json" -d '{"token" : "your_valid_token"}' http://host:port/battle/status

```
For starting action after joining the battle use `battle/action`. To learn available actions see [battle-guide]:
```
    $ curl -X POST -H "Content-Type:application/json" -d '{"token" : "your_valid_token", "action" : "up"}' http://host:port/battle/action

```