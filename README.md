# user_insights

![Platform](https://img.shields.io/badge/platform-Qlik%20Sense%20Hub-lightgrey.svg)
![Qlik Sense Version](https://img.shields.io/badge/Qlik%20Sense%20Version-November%202018-brightgreen.svg)

- [User Insights](#user-insights)
- [Description](#description)
- [Reload-and-distribution-schedule](#reload-and-distribution-schedule)
- [IDE](#IDE)
- [Usage](#usage)
- [Deployment](#deployment)
- [Distribution](#distribution)
- [Hub-Customization](#Hub-customization)
- [Changelog](#changelog)

<br><br>
***

## Description
- User insights is an internal user monitoring application that provide visualization in a self-serve hub, it reports user activities based on data provider - [Heap Analytics](https://heapanalytics.com/app/report).

<br><br>
***

## Reload and distribution schedule

<br><br>
***

## IDE
Before continuing, make sure that you have these tools installed:
- [Sublime Text Editor](https://www.sublimetext.com/)
- [Visual Studio Code](https://code.visualstudio.com/)(*optional*)
- [Visual Studio - Python extension](https://code.visualstudio.com/)
<br><br>
***

## Usage

<br><br>
***

## Deployment
1. make sure the pyModule in the server is up-to-date, double check the codes here: https://bitbucket.com/
2. CI/CD pipeline is in place, the deployment on dev-us-qss is fully automated.  New commits on `master` will be automatically copied over to `DEV-US-QSS` and execute `autodeploy.py` script to upload qvf, replace target app, reload replaced app and delete imported app.
3. Import the .qvf files to QMC.
4. Rename the files with the client acronym, e.g. `Morri_User_Insights` or `Jm_User_Insights`. Be careful to not replace the existing app, if it's case, add another suffix to appname.
5. The app will be placed on your workstream folder.
6. Reload the app on your workstream.
7. Replace/Publish the app to the properly stream.

<br><br>

## Distribution

<br><br>
***

## Hub-customization

<br><br>
***

## Changelog

### **1.0.4alpha - CI/CD pipeline enabled**
- _auto_deploy/autodeploy.py will work with Bamboo auto build.

### **1.0.2 - Hide fields, reveal master items in Hub**
- Hide all fields except master items.
- [username] fields has to be untagged $hidden after renaming master item fields and hide other fields.

### **1.0.0 - MVP**
- Initial Release

<br><br>
***
