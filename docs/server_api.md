# Output format
``` 
    { 
        "status" : "following status",
        "comment" : "supplementing comment"
    }

```

# Valid statuses with output
 - `ok` : Your request is seccussfully processed
 - `error`: One of the processes failed

 Login valid statuses:
 ```
    {
        "status" : "ok",
        "comment": "You are seccussfully logged in"
    }
 ```
 ```
    {
        "status" : "error",
        "comment": "Please check your login or sign up by following link [sign_up]"
    }
```
```
    {
        "status" : "error",
        "comment" : "Invalid format, check your input and try again"
    }
```