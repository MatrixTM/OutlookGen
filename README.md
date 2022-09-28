<p align="center"><img src="https://arvanloud.io/dl_16062215/icon.ico" alt="outlook"></p>
<div align="center" style="margin-top: 0;">
   <h1>Outlook Generator</h1>
   <p>Dont Skid 👀</p>
</div>
<em><h5 align="center">(Programming Language - Python 3)</h5></em>
<p align="center">
<a href="#"><img alt="OutlookGen forks" src="https://img.shields.io/github/forks/MatrixTM/OutlookGen?style=for-the-badge"></a>
<a href="#"><img alt="Repo stars" src="https://img.shields.io/github/stars/MatrixTM/OutlookGen?style=for-the-badge&color=yellow"></a>
<a href="#"><img alt="OutlookGen License" src="https://img.shields.io/github/license/MatrixTM/OutlookGen?color=orange&style=for-the-badge"></a>
<a href="https://github.com/MatrixTM/OutlookGen/issues"><img alt="issues" src="https://img.shields.io/github/issues/MatrixTM/OutlookGen?color=purple&style=for-the-badge"></a>
<p align="center"><img src="https://views.whatilearened.today/views/github/MatrixTM/OutlookGen.svg" width="80px" height="28px" alt="View"></p>

---

<p align="center"><img src="https://user-images.githubusercontent.com/95581741/192341106-89bf0a97-d974-4e41-866e-8e334a0b6ed5.png" width="570" alt="outlook"></p>

## 📝 Document

**Install Requirements**

```
pip3 install -r requirements.txt
```

**Install Chrome Driver**

##### Windows

###### Alos You Can Watch [This Video](https://youtube.com)

- Go [Here](https://chromedriver.chromium.org/downloads) And Download chromedriver Windows Version
- Put chromedriver.exe into Script folder

##### Linux

*Run This Command*

```shell script
sudo apt install chromium-chromedriver
```

- Go [Here](https://chromedriver.chromium.org/downloads) And Download chromedriver Linux Version
- Put chromedriver into Script folder

---

## ⚙️ Config Document

| Name  | Descripton |
| ------------- | ------------- |
| Prefix  | Log Prefix (Default: &beGen&5>> )  |
| ProxyFile  | proxy file path (Default: proxy.txt)  |
| OutputFile  | output file path (Default: account.txt)  |
| Timer  | Generate Timer (Default: true)  |
| driverPath  | path of chromedriver (Default: ./chromedriver)  |
| providers  | Captcha Providers (Default: anycaptcha/twocaptcha)  |
| api_key  | Your Api Key (Default: )  |
| site_key  | outlook site key (Default: B7D8911C-5CC8-A9A3-35B0-554ACEE604DA)  |
| Domain  | Email Domain (Default: @hotmail.com/@outlook.com)  |
| minBirthDate  | Minimum BirthDate (Default: 1980)  |
| maxBirthDate  | Maximum BirthDate (Default: 1999)  |
| PasswordLength  | Password Length (Default: 10)  |
| FirstNameLength  | First Name Length (Default: 5)  |
| LastNameLength  | Last Name Length (Default: 5)  |
| DriverArguments  | driver argument list (Default: ...)  |

#### Change this configs

- driverPath
- providers
- api_key
- Domain

**`config.json` Example**

```json
{
  "Common": {
    "Prefix": "&beGen&5>> ",
    "ProxyFile": "proxy.txt",
    "OutputFile": "account.txt",
    "Timer": true,
    "driverPath": "./chromedriver"
  },
  "Captcha": {
    "providers": "anycaptcha",
    "api_key": "0dv3a5b276b347bxxxx12a6x8a9m862",
    "site_key": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA"
  },
  "EmailInfo": {
    "Domain": "@outlook.com",
    "minBirthDate": 1980,
    "maxBirthDate": 1999,
    "PasswordLength": 10,
    "FirstNameLength": 5,
    "LastNameLength": 5
  },
  "DriverArguments": [
    "--disable-logging",
    "--disable-login-animations",
    "--disable-notifications",
    "--incognito",
    "--ignore-certificate-errors",
    "--disable-blink-features=AutomationControlled",
    "--disable-gpu",
    "--headless",
    "--no-sandbox"
  ]
}
```
