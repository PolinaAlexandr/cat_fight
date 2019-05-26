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
