# Output format
``` 
    { 
        "status" : "following status",
        "comment" : "supplementing comment"
    }

```

# Valid statuses with outputs

 - `ok` : Your request is seccussfully processed:
 ```
    {
        "status" : "ok",
        "comment": "You are seccussfully logged in"
    }
 ```
- `error`: One of the processes failed:
```
    {
        "status" : "error",
        "comment": "Please check your login or sign up by following link [sign_up]"
    }
```