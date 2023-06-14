*** Settings ***
Library    AppiumLibrary
*** Variables ***
${APPIUM_SERVER}    http://127.0.0.1:4750/wd/hub
*** Keywords ***
Open Device
    ${androiddriver}=    Open Application
    ...    ${APPIUM_SERVER}
    ...    platformName=android
    ...    udid=emulator-5554
    ...    platformVersion=13
    ...    deviceName=Galaxy Nexus API 33
    ...    automationName=uiautomator2
    ...    newCommandTimeout=2500
    ...    appPackage=com.android.camera2
    ...    appActivity=com.android.camera.CameraLauncher
    Capture Page Screenshot
    Set Suite Variable    ${androiddriver}
*** Test Cases ***
Simple Test Open Device Cam
    Open Device
    Capture Page Screenshot
