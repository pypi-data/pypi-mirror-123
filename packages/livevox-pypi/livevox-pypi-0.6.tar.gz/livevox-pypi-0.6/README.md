# livevox-pypi

livevox-pypi is a Python library for dealing with not supported livevox API functions.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install livevox-pypi.

```bash
pip install livevox-pypi
```

## Usage

```python
from livevox_api import livevox_pypi as lv

# Set selenium options
options = lv.setting_selenium_options(headless=False)

#Initialize webdriver object
driver = webdriver.Chrome('./chromedriver', options = options)

# Login Into Livevox 
lv.login_livevox(driver,username='javier',password='ilovepython',client_code='Python_client')


```

## Contributing
Only the Data Science Team of Teleperformance will pull requests in this project.

## License
[MIT](https://choosealicense.com/licenses/mit/)