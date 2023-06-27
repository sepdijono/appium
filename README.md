# Appium
Appium Device Connection Setup
How to install appium in robot framework project please read this : [Appium Tutorial](https://github.com/sepdijono/appium/blob/main/appium-tutorial.pdf)

# Burp Suite 
Burp Suite Certificate Setup
How to download & install Burp Suite certificate please read this : [Burp Suite Certificate Installation](https://github.com/sepdijono/appium/blob/main/perform_test_avd_using_burpsuite.pdf)

# Implementation
* Create Virtualenv
```
python3 -m venv ~/venvs/automation
```
* Activate Virtualenv
```
source ~/your-venv-directory/bin/activate
```
* Deactivate Virtualenv : Run this in activated virtualenv
```
deactivate
```
* Install requirements.txt
```
pip install -r requirements.txt
```
After that you'll be okay to run the code

# Running a .robot file
```
robot --outputdir /home/yourhomename/Android/testcases/output open-cam-activity.robot
```



Regards
pyy
