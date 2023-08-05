#!/usr/bin/python3
#************************************************************************
# Copyright 2021 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************

"""Package for Console Display Util Functions """

import datetime
import shutil


#---------------------------
# TO DO
#---------------------------
#
#---------------------------


#*************************************************
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
#*************************************************
class Colors:
    """Constant for Console Colors"""
    HEADER = '\033[5;30;47m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#*************************************************
#
#*************************************************
def GetTerminalWidth():
    """Get the width of current terminal window"""
    columns = shutil.get_terminal_size()[0]
    return columns


#*************************************************
#
#*************************************************
def ConsoleLine(left = "", center = "", right = ""):
    """Display a  titles using the full console wisth"""

    line = center.center(GetTerminalWidth(), ' ')
    line = left + line[len(left):]
    line = line[:(len(right)*(-1))] + right


    print(f"{line}")

#*************************************************
#
#*************************************************
def ConsoleTitleLine(left = "", center = "", right = ""):
    """Display a  titles using the full console wisth"""

    title = center.center(GetTerminalWidth(), ' ')
    title = left + title[len(left):]
    title = title[:(len(right)*(-1))] + right


    print(f"{Colors.HEADER}{title}{Colors.ENDC}")

#*************************************************
#
#*************************************************
def ClearDisplay():
    """Clear Console"""
    print("\033[H\033[J", end="")

#*************************************************
#
#*************************************************
def ConsoleTitle(left = "", center = "", right = ""):
    """Clear Console & add Title"""
    ClearDisplay()
    ConsoleTitleLine(left, center, right)





#*************************************************
#
#*************************************************
def FormatAWSStatus(val):
    """Return the value with the color depending on AWS Status"""
    ret = val
    val = val.upper()
    if 'FAIL' in val or 'STOP' in val or 'CANCEL' in val:
        ret = f"{Colors.FAIL}{ret}{Colors.ENDC}"
    elif 'COMPLETE' in val or 'SUCCE' in val:
        ret = f"{Colors.OKGREEN}{ret}{Colors.ENDC}"
    elif 'SUPERSED' in val:
        ret = f"{Colors.WARNING}{ret}{Colors.ENDC}"
    elif 'PROGRESS' in val:
        ret = f"{Colors.OKCYAN}{ret}{Colors.ENDC}"

    return ret

#*************************************************
#
#*************************************************
def FormatAWSDrift(val):
    """Add color to AWS Drift status string"""
    ret = val
    if 'DRIFTED' in val:
        ret = f"{Colors.FAIL}{ret}{Colors.ENDC}"
    elif 'IN_SYNC' in val:
        ret = f"{Colors.OKGREEN}{ret}{Colors.ENDC}"
    elif 'UNKNOWN' in val:
        ret = f"{Colors.OKCYAN}{ret}{Colors.ENDC}"
    elif 'NOT_CHECKED' in val:
        ret = f"{Colors.OKCYAN}{ret}{Colors.ENDC}"
    elif 'MODIFIED' in val:
        ret = f"{Colors.FAIL}{ret}{Colors.ENDC}"

    return ret


#*************************************************
#
#*************************************************
def FormatAWSState(val):
    """Add color to AWS Instance State string"""
    ret = val
    if 'shutting-down' in val:
        ret = f"{Colors.FAIL}{ret}{Colors.ENDC}"
    elif 'running' in val:
        ret = f"{Colors.OKGREEN}{ret}{Colors.ENDC}"
    elif 'pending' in val:
        ret = f"{Colors.OKCYAN}{ret}{Colors.ENDC}"
    elif 'stop' in val:
        ret = f"{Colors.FAIL}{ret}{Colors.ENDC}"
    elif 'shutting-down' in val:
        ret = f"{Colors.FAIL}{ret}{Colors.ENDC}"

    return ret


#*************************************************
#
#*************************************************
def ConvertToDatetime(value):
    """Convert possible int or float to datetime"""

    if isinstance(value, (int, float)) is False:
        return value

    if value >= 1000000000000:
        return datetime.datetime.fromtimestamp(value/1000)
    if value >= 1000000000:
        return datetime.datetime.fromtimestamp(value)

    return value

#*************************************************
#
#*************************************************
def FormatDatetime(value, format = '%Y-%m-%d %H:%M:%S'):
    """Convert a DateTime (object or unix int) into a Text Form"""

    #print(f'FormatDatetime Value Type {type(value)}')
    dtClass = None

    if value is None:
        return ''

    dtClass = ConvertToDatetime(value)

    return dtClass.strftime(format)


#*************************************************
#
#*************************************************
def FormatSince(value):
    """Convert a DateTime or Seconds (int) into Text about the elapse time (ex: 6 sec, 3.2 min)"""

    # print(f'FormatSince Value Type {type(value)} {value=}')
    timeUnits = [
        {'txt': 'sec', 'scale' : 60.0},
        {'txt': 'min', 'scale' : 60.0},
        {'txt': 'hr', 'scale' : 24.0},
        {'txt': 'day', 'scale' : 24.0},
        {'txt': 'yr', 'scale' : 365.0},
        {'txt': 'ct', 'scale' : 100.0}
    ]

    if value is None:
        return ''

    since = None
    value = ConvertToDatetime(value)

    if isinstance(value, int):
        since = value
    elif isinstance(value, float):
        since = value
    elif isinstance(value, str):
        since = float(value)
    elif isinstance(value, datetime.datetime):
        delta = datetime.datetime.utcnow() - value
        since = delta.total_seconds()
    else:
        return 'NA'

    since = float(since)
    unit = 'NA'

    # Convert and fine unit
    for timeUnit in timeUnits:
        unit = timeUnit['txt']
        if since < timeUnit['scale']:
            break
        since = since / timeUnit['scale']

    return f'{since:.1f} {unit}'


#*************************************************
#
#*************************************************
def Table(params, datas):
    """
    Print a Table on Screen from parameters and a data array.

    Args:
        params (dict):
            title (string): Table Tile
            columns (list): Each elements defines a column
                [{
                    type: Data type, options
                        i = index
                        str = string
                        date = datetime displayed in format YYYY-MM-DD
                        datetime =  datetime displayed in format YYYY-MM-DD HH:MM:SS
                        since =  Duration between value and now (must be a datetime)
                    dataName : Key name in the data list
                    title : Column name to display

                    maxWidth : Maximum Width for a column
                    minWidth : Minimum Width for a column
                    fixWidth : Column is for a to a specific width

                    format : Special formating for this column, options
                        aws-status
                        aws-state  (EC2 States)
                        aws-drift
                }...]

        datas (list): Each element is a Row (or Data)


    """

    columns = params.get('columns', [])
    tableWidth = 0
    consoleWidth = GetTerminalWidth()

    #----------------------------
    # Loop to prepare data
    #----------------------------
    for col in columns :

        dataType = col.get('type', 'str')
        if dataType == 'i':
            col['dataName'] = 'i'

        dataName = col.get('dataName', 'not set')

        maxW = col.get('maxWidth', None)
        minW = col.get('minWidth', None)
        fixW = col.get('fixWidth', None)

        width = len(col.get('title', ''))

        index = 0
        for data in datas:
            index += 1
            value = data.get(dataName, None)

            if dataType == 'i':
                value = str(index)
            elif value is None:
                value = ''
            elif dataType == 'date':
                value = FormatDatetime(data.get(dataName, None), '%Y-%m-%d')
            elif dataType == 'datetime' and value is not None:
                value = FormatDatetime(data.get(dataName, None), '%Y-%m-%d %H:%M:%S')
            elif dataType == 'since':
                value = FormatSince(value)
            else: value = str(value)

            data[dataName] = value

            width = max(width, len(value))

        if maxW is not None:
            width = min(width, maxW)
        if minW is not None:
            width = max(width, minW)
        if fixW is not None:
            width = fixW

        # make sure we dont overflow terminal
        width = min(width, consoleWidth - (tableWidth + 3))
        if width <= 3:
            width = 0
        else:
            tableWidth += width + 3

        col['width'] = width

    #----------------------------
    # Loop to build top tow
    #----------------------------
    topRow = ''
    for col in columns :
        colWidth = col.get('width')
        if colWidth < 1:
            continue
        title = col.get('title', '')[0:colWidth]
        title = title.center(colWidth, ' ')
        topRow += f" {title} |"

    #----------------------------
    # Print Title and Top Row
    #----------------------------
    title = params.get('title', None)
    if title is not None:
        title = title.center(tableWidth, ' ')
        print(f"{Colors.HEADER}{title}{Colors.ENDC}")

    print(f"{Colors.HEADER}{topRow}{Colors.ENDC}")

    #----------------------------
    # Loop to print all data Rows
    #----------------------------
    for data in datas:
        dataRow = ''
        for col in columns :
            dataName = col.get('dataName', 'not set')
            colWidth = col.get('width')
            colFormat = col.get('format', '')

            if colWidth < 1:
                continue

            val = data.get(dataName, '')
            val = val[0:colWidth].ljust(colWidth, ' ')

            if colFormat == 'aws-status':
                val = FormatAWSStatus(val)
            elif colFormat == 'aws-drift':
                val = FormatAWSDrift(val)
            elif colFormat == 'aws-state':
                val = FormatAWSState(val)

            dataRow += f" {val} |"

        print(dataRow)

    bottomRow = " " * tableWidth
    print(f"{Colors.HEADER}{bottomRow}{Colors.ENDC}")



#*************************************************
# To Test Class
#*************************************************
if __name__ == "__main__":

    theParams = {
            'title' : "Cloudformation Stacks for region: TBD",
            'columns' : [
                {'title' : 'id'      , 'type': 'i',       'width' : 4  },
                {'title' : 'Name'    , 'type': 'str',     'width' : 40, 'dataName': 'StackName'},
                {'title' : 'Creation', 'type': 'date',    'width' : 10, 'dataName': 'CreationTime', 'format': '%Y-%m-%d'},
                {'title' : 'Status'  , 'type': 'str',     'width' : 15, 'dataName': 'StackStatus'}
            ]
    }
    theDatas = [
        {'StackName' : 'first-stack', 'CreationTime': datetime.datetime(2021, 8, 23), 'StackStatus': 'COMPLETE'},
        {'StackName' : 'second-stack', 'CreationTime': datetime.datetime(2021, 8, 23), 'StackStatus': 'UPDATING'},
    ]

    Table(theParams, theDatas)
