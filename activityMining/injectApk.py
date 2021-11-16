import collections

import xmltodict
import glob
import json
import os
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import sys

# get sys args
args = sys.argv
folderName = args[1]
# folderName = 'Amazon Prime Video by Amazon Mobile LLC - com.amazon.avod.thirdpartyclient'

# get packageName
pkName = ''
xmlDir = os.path.join('data', '{}/AndroidManifest.xml'.format(folderName))

allLinks = []
with open(xmlDir, 'r') as fd:
    doc = xmltodict.parse(fd.read())
    pkName = doc['manifest']['@package']

    # get activity
    schemeName = pkName.replace('.', '_')
    if 'activity' in doc['manifest']['application'].keys():
        for activity in doc['manifest']['application']['activity']:
            # print(activity)
            activity['@android:exported'] = True
            activityName = activity['@android:name'].split('.')[-1]

            # start inject
            if 'intent-filter' in activity.keys():
                # print(activity['intent-filter'], activityName)
                if type(activity['intent-filter']) == list:
                    activity['intent-filter'].append(
                    {'action': [{'@android:name': 'android.intent.action.VIEW'}],
                     'category': [{'@android:name': 'android.intent.category.DEFAULT'},{'@android:name': 'android.intent.category.BROWSABLE'}],
                     'data': [{'@android:scheme': schemeName, '@android:host': activityName}]
                     }
                    )
                else:
                    tempdict = activity['intent-filter']
                    activity['intent-filter'] = [tempdict]
                    activity['intent-filter'].append({'action': [{'@android:name': 'android.intent.action.VIEW'}],
                     'category': [{'@android:name': 'android.intent.category.DEFAULT'},{'@android:name': 'android.intent.category.BROWSABLE'}],
                     'data': [{'@android:scheme': schemeName, '@android:host': activityName}]
                     }
                    )

                allLinks.append(f'{schemeName}://{activityName}')
            else:
                activity['intent-filter'] = {'action': [{'@android:name': 'android.intent.action.VIEW'}],
                     'category': [{'@android:name': 'android.intent.category.DEFAULT'},{'@android:name': 'android.intent.category.BROWSABLE'}],
                     'data': [{'@android:scheme': schemeName, '@android:host': activityName}]
                     },
with open(xmlDir, 'w') as fd:
    fd.write(xmltodict.unparse(doc, pretty=True))

with open('deeplinks.txt', 'a') as fd:
    fd.write(pkName + '\n')
    fd.write('\n'.join(allLinks))
    fd.write('\n\n\n')

