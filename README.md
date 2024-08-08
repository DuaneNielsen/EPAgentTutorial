# EPAgentTutorial

A minimal example in python3 that creates metrics in EPAgent

### Install Steps

Download and install the infrastructure agent on your local machine using the normal worklow

```
tar xvf Infrastructure_Agent_apmia_20240807_v1.tar
cd apmia
APMIACtrl.sh install
```

open the IntroscopeAgent.profile (use whatever text editor you like)

```
cd ..
vi apmia/core/config/IntroscopeAgent.profile
```

search and uncomment the below line

```
# introscope.epagent.config.httpServerPort=8080
```

Restart the Infrastructure agent

```
cd apmia
APMIACtrl.sh restart
```

The script uses Python 3, so make sure you have python 3 installed,

You will also need requests

```
pip install requests
```

Finally run the script

```
python epagent_REST_tutorial.py  --verbose
```

It will write output like so..

```
jsonDump:
{
    "metrics": [
        {
            "type": "IntAverage",
            "name": "Example|Metrics:IntAverageMetric",
            "value": "22"
        },
        {
            "type": "IntCounter",
            "name": "Example|Metrics:IntCounterMetric",
            "value": "22"
        },
        {
            "type": "LongCounter",
            "name": "Example|Metrics:LongCounterMetric",
            "value": "22"
        },
        {
            "type": "StringEvent",
            "name": "Example|Metrics:StringEvent",
            "value": "Hi I am a string value"
        }
    ]
}
Response:
{
    "validCount": 4
}
StatusCode: 200
```

Run it for a while... on DX SaaS instance, you should see output like so...

![image](https://github.com/user-attachments/assets/d3a1f111-ab81-4ecb-99bf-faf40ef27422)



