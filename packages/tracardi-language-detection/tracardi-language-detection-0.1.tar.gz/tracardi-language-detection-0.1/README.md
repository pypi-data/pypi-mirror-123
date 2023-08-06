# Language detection Plugin

The purpose of this plugin is  detect language from given string with meaningcloud API

# Configuration

This node requires configuration. You need have a account in meaningcloud to provide your API https://www.meaningcloud.com/

## Message configuration
* id - Enter your resource id
* message: None, - Enter your message
* key: None, - Enter your Key you can find it on https://www.meaningcloud.com/developer/account/subscriptions


## Example of action configuration

```json
        {"source": {
                "id": "55584df6-9ee3-4acd-a0ea-e555122f3dbc",
            },
                "message": {"message": """Welcome aboard
        Please pay attention as we demonstrate
        The safety features of this aircraft"""},
                "key": {"key": "YOUR KEY"
                        }}
```



# Input payload

This node does not process input payload.

# Output

This node returns json with yours datas.
