# unloader_from_exel

# .env
You must provide .env file as lists in env.sample or cli args (base_uri, cabinet_uri, access_token, developer_email, folder_path)

## Usage
``` shell
$ pip3 install -r ./requirements.txt
$ python3 ./main.py # if using only .env. Or:
$ python3 ./main.py --base_uri=<base uri> --cabinet_uri=<cabinet uri> --access_token=<access token> --developer_email=<developer email> --folder_path=<folder path>
```

## How we parse configuration parameters
``` python
arg_parser.add_argument('--base_uri', default=os.getenv('BASE_URI'))
arg_parser.add_argument('--cabinet_uri', default=os.getenv('CABINET_URI'))
arg_parser.add_argument('--access_token', default=os.getenv('ACCESS_TOKEN'))
arg_parser.add_argument('--developer_email', default=os.getenv('DEVELOPER_EMAIL'))
arg_parser.add_argument('--folder_path', default=os.getenv('FOLDER_PATH'))

```

### Additional info
Data recovery is not implemented as not required task (Плюсом будет умение скрипта запускать заливку с места последнего запуска (на случай сетевых проблем или прерывании выполнения), например, с определенной строки.)