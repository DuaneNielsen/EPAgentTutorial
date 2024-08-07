#!/usr/bin/env python3

import json
import optparse
import requests
import sys
import time
from datetime import datetime
import math


def time_to_sine_wave(period_minutes=2, min_value=0, max_value=100):
    # Get the current time
    now = datetime.now()

    # Calculate the number of seconds since the start of the current period
    period_seconds = period_minutes * 60
    seconds_in_period = (now.minute * 60 + now.second) % period_seconds

    # Convert seconds to radians (2π radians = 1 full period)
    radians = (seconds_in_period / period_seconds) * 2 * math.pi

    # Calculate the sine value (-1 to 1)
    sine_value = math.sin(radians)

    # Scale and shift the sine value to our desired range
    amplitude = (max_value - min_value) / 2
    midpoint = (max_value + min_value) / 2
    scaled_value = sine_value * amplitude + midpoint

    return scaled_value

def main(argv):
    parser = optparse.OptionParser()
    parser.add_option("-v", "--verbose", help="verbose output",
                      dest="verbose", default=False, action="store_true")
    parser.add_option("-H", "--hostname", default="localhost",
                      help="hostname EPAgent is running on", dest="hostname")
    parser.add_option("-p", "--port",
                      help="port EPAgent is listening on, "
                           "from apmia core config IntroscopeAgent.profile : introscope.epagent.config.httpServerPort",
                      type="int", default=8080, dest="port")
    options, args = parser.parse_args()

    if options.verbose:
        print("Verbose enabled")

    url = f"http://{options.hostname}:{options.port}/apm/metricFeed"
    headers = {'content-type': 'application/json'}

    if options.verbose:
        print(f"Submitting to: {url}")

    submissionCount = 0

    while True:
        start = datetime.now()
        value = time_to_sine_wave()

        """
        There are 4 types of metrics in APM
        
        IntAverage: A time series of integer values that when aggregated over time, will report the average values
        IntCounter: A time series of integer values that will SUM the values when aggregated over time
        LongCounter: A time series of long values that will SUM the values when aggregated over time
        StringEvent: A string value that is reported only in the current moment.  Useful to report configuration values
                    to the operator
        
        The metric name path separator is '|', and ':' signifies the start of the metric name
        
        eg : "Example|Metrics:IntAverageMetric" will create a metric called IntAverageMetric 
        under the folder Example / Metrics
        
        the value should be an integer
        """

        metricDict = {
            'metrics': [
                {
                    'type': 'IntAverage',
                    'name': f"Example|Metrics:IntAverageMetric",
                    'value': f"{int(value)}"
                },
                {
                    'type': 'IntCounter',
                    'name': f"Example|Metrics:IntCounterMetric",
                    'value': f"{int(value)}"
                },
                {
                    'type': 'LongCounter',
                    'name': f"Example|Metrics:LongCounterMetric",
                    'value': f"{int(value)}"
                },
                {
                    'type': 'StringEvent',
                    'name': f"Example|Metrics:StringEvent",
                    'value': f"Hi I am a string value"
                },
            ]
        }


        try:
            r = requests.post(url, data=json.dumps(metricDict), headers=headers)
        except requests.ConnectionError as err:
            print(
                f"Unable to connect to EPAgent via URL \"{url}\": {err}\n check file: apmia/core/config/IntroscopeAgent.profile property: introscope.epagent.config.httpServerPort  Did you forget to comment it in?")
            sys.exit(1)

        if options.verbose:
            print("jsonDump:")
            print(json.dumps(metricDict, indent=4))

            print("Response:")
            response = json.loads(r.text)
            print(json.dumps(response, indent=4))

            print(f"StatusCode: {r.status_code}")

        submissionCount += 1

        end = datetime.now()
        delta = end - start
        howlong = 15.0 - delta.total_seconds()
        time.sleep(max(0, howlong))


if __name__ == "__main__":
    main(sys.argv)
