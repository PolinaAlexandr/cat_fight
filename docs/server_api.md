# Visual fuild output example
``` 
        ______________________________
        |     |     |     |     |=^.^=|
       5|_____|_____|_____|_____|__()/|
        |     |     |     |     |     |
       4|_____|_____|_____|_____|_____|
        |     |     |     |     |     |
       3|_____|_____|_____|_____|_____|
        |     |     |     |     |     |
       2|_____|_____|_____|_____|_____|
        |=^.^=|     |     |     |\ V /|
       1|\()__|_____|_____|_____|/_^_\|
        1     2     3     4     5

```
 - `=^.^=` : Players avatar 
 - `X`  : Crossed points (this course is not available)


# Output format
``` 
    { 
        "result" : "operation result",
        "comment" : "supplementing comment"
    }

```

# Valid responses with output
 - `ok` : Your request is seccussfully processed
 - `error`: One of the processes failed

Registration valid responses:
```
    {
        "result" : "ok",
        "comment": "You are successfully registered"
    }
```
```
    {
        "result" : "error",
        "comment" :  "Please follow the current template 
        {"login": "John", "password" : "*****"}"
    }
```
```
    {
        "result" : "error",
        "comment" : "This login already exists, please choose the new one"
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid format, check your input and try again"
    }
```
 Login valid responses:
 ```
    {
        "result" : "ok",
        "comment": "You are successfully logged in"
        "token" : "your_token"
    }
 ```
 ```
    {
        "result" : "error",
        "comment": "Please check your login/password or sign up by following link [sign_up]"
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid format, check your input and try again"
    }
```
```
    {
        "result" : "error",
        "comment" :  "Please follow the current template 
        {"login": "John", "password" : "*****"}"
    }
```

Logout valid responses:
```
    {
        "result" : "ok",
        "comment": "You are successfully logged out"
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid format, check your input and try again"
    }
```
```
    {"""
        "result" : "error",
        "comment" : "Please follow the current template {"token" : "*************"}"
        """
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid token, try again"
    }
```

Statistics valid responses:
```
    {
        "result" : "ok"
        "statistics": {
            "registration_date": "26/26/2019 18/26/28", 
            "status": "logged out", 
            "user_name": "Jack"
        }, 

    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid format, check your input and try again"
    }
```
```
    {"""
        "result" : "error",
        "comment" : "Please follow the current template {"user_name" : "John",
        "token" : "*****"}"
        """
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid token"
    }
```
```
    {
        "result" : "error",
        "comment" : "Cannot check statistics, user does not exists"
    }
```
 
Battle/join valid responses:
```
    {
        "result" : "ok",
        "comment" : "Your enemy is: user's enemy name" 
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid format, check your input and try again"
    }
```
```
    {"""
        "result" : "error",
        "comment" : "Please follow the current template {"token" : "*****"}"
        """
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid token"
    }
```
```
    {
        "result" : "error",
        "comment" : "Cannot find battle partner"
    }
```

Battle/status valid responses:
```
    {
        "result" : "ok",
        "status" : "You are not in the battle"
    }
```
```
    {
        "result" : "ok",
        "status" : "You are fighting against user_enemy_name" 
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid format, check your input and try again"
    }
```
```
    {"""
        "result" : "error",
        "comment" : "Please follow the current template {"token" : "*****"}"
        """
    }
```
```
    {
        "result" : "error",
        "comment" : "Invalid token"
    }
```
