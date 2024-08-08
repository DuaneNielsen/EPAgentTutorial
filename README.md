# EPAgentTutorial

A minimal example in python3 that creates metrics in EPAgent

### Install Steps

Download and install the infrastructure agent on your local machine using the normal worklow

```
tar xvf Infrastructure_Agent_apmia_20240807_v1.tar
cd apmia
APMIACtrl.sh install
```

In the apmia/core/config/IntroscopeAgent.profile uncomment the below line

```
# introscope.epagent.config.httpServerPort=8080
```

Restart the Infrastructure agent

```
APMIACtrl.sh restart
```

The script uses Python 3, so make sure you have python 3 installed,

You will also need requests

```
pip install requests
```

Finally run the library

```
python epagent_REST_tutorial.py
```

