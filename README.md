# unloader_from_exel

# .env
You must provide .env file as lists in env.sample or cli args (base_uri, cabinet_uri, access_token, developer_email, folder_path)

## How we parse configuration parameters
``` python
arg_parser.add_argument('--base_uri', default=os.getenv('BASE_URI'))
arg_parser.add_argument('--cabinet_uri', default=os.getenv('CABINET_URI'))
arg_parser.add_argument('--access_token', default=os.getenv('ACCESS_TOKEN'))
arg_parser.add_argument('--developer_email', default=os.getenv('DEVELOPER_EMAIL'))
arg_parser.add_argument('--folder_path', default=os.getenv('FOLDER_PATH'))

```
