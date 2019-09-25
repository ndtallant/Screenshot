# Screenshot Webpages

- To use, have firefox and its [webdriver](https://github.com/mozilla/geckodriver/releases) installed.
- To run with defaults, simply run `python screenshot.py`


### Command Line Arguments
```
usage: screenshot.py [-h] [--start_position START_POSITION]
                     [--max_time MAX_TIME] [--ads ADS]
                     [--fullscreen FULLSCREEN]

optional arguments:
  -h, --help            show this help message and exit
  --start_position START_POSITION
                        The line in the urls file to start on. Default is 0.
  --max_time MAX_TIME   The max timeout rate for a url in seconds. Default is
                        10.
  --ads ADS             True for ads, False for no ads. Defualt is False.
  --fullscreen FULLSCREEN
                        True for fullscreen, False for no fullscreen. Defualt
                        is False.
```
