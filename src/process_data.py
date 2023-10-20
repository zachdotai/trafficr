import json
from collections import OrderedDict

import pandas as pd


with open('/data/traffic_flow.json') as json_data:
    traffic_info = json.load(json_data, object_pairs_hook=OrderedDict)

    days_label = ''
    hours_label = ''

    for day in traffic_info['hours']:
        for hour in traffic_info['hours'][day]:
            days_label += '\t' + day
            hours_label += '\t' + hour + ':00'

    print(days_label)
    print(hours_label)
    print('\n')

    for road in traffic_info['results']:
        line1 = road + '\nDistance from (km)\t' + str(traffic_info['distance'][road]['from']) + '\nDistance to (km)\t' + str(traffic_info['distance'][road]['from'])
        print(line1)

        line2 = road + ' (from)'
        line3 = road + ' (to)'

        for day in traffic_info['results'][road]['from']:
            for hour in traffic_info['results'][road]['from'][day]:
                average_speed = traffic_info['results'][road]['from'][day][hour]
                line2 += '\t' + str(average_speed)
        print(line2)

        for day in traffic_info['results'][road]['to']:
            for hour in traffic_info['results'][road]['to'][day]:
                average_speed = traffic_info['results'][road]['to'][day][hour]
                line3 += '\t' + str(average_speed)
        print(line3)
        print('\n')

