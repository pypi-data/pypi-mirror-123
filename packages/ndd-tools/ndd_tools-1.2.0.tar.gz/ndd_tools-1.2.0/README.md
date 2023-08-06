# LoggerMixin
## usage
```
from ndd_tools import LoggerConfig, LoggerMixin
class A(LoggerMixin):
    def __init__(self, logger_config: LoggerConfig, *args, **kwargs):
        self.set_logger_up(logger_config)

        # to enable debug mode: log message send to console
        self.set_logger_debug_mode(True)

        # to disable debug mode:
        self.set_logger_debug_mode(False)

        # to change log level, change in config or method
        self.set_logger_level(loggingLevel)

        # to add file handler
        self.add_logger_file_handler(file_path: str, file_name: str, [formatter])

        # get current logger config
        self.get_logger_config()

        # incase you want create new logger
        # recreate new logger_config then use
        self.set_logger_up(new_logger_config)



    def run(self):
        self.debug('this is debug log message')
        self.info('this is info log message')
        self.warn('this is warn log message')
        self.error('this is error log message')
        self.critical('this is critical log message')

```
## example

# ApiClient
## usage
```
json_config_file_path = "/path/to/file/json"  
client = ApiClient(json_config_file_path)  
data = client.make_request('example1', header_dict, body_dict)  
```

# json format example
```yaml
{  
  "name": "api endpoints",  
  "description": "hello",  
  "config": {  
    "example1": {  
      "method": "GET",  
      "url": "https://gorest.co.in/public/v1/users",  
      "header": {  
        "Content-Type": "application/json"  
      },  
      "parameters": {  
        "hello": "world"  
      },  
      "save_response": false  
    }  
  }  
}  
