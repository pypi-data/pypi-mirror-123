
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
import os
import boto3
import json
import pprint

#*************************************************
# Reformat SNS Message to a SMS consumable texte
#*************************************************
def ReformatForSMS(snsMessage):

    theMsg = ""

    # ----------------------------
    # ALARM Event - Rewrite for clear SMS
    # ----------------------------
    if 'AlarmDescription' in snsMessage :
        theMsg = snsMessage['AlarmDescription'] + "\n"
        theMsg += 'State: ' + snsMessage['NewStateValue'] + "\n"
        theMsg += 'Since: ' + snsMessage['StateChangeTime']

    # ----------------------------
    # Guard duty Event
    # ----------------------------
    if snsMessage['source'] == "aws.guardduty":

        theType = snsMessage["detail-type"]

        if theType == 'GuardDuty Finding' :
            theMsg = theType + '\n'
            theMsg += snsMessage['detail']['description']
        
        elif theType == 'AWS API Call via CloudTrail' :
            theMsg = 'GuardDuty API' + '\n'
            theMsg += snsMessage['detail']['eventName'] + '\n'
            theMsg += 'By ' + snsMessage['detail']['userIdentity']['userName']
        else:
            theMsg = theType + '\n'
            theMsg = 'New Guarduty Type'
    
    return theMsg

#*************************************************
# Function that can transmit a Event to another region that can send SMS.  
#*************************************************
def TransmitToSmsTopic (snsEvent, arnSmsTopic):

    #print(f'TransmitToSms snsEvent: {snsEvent}')
    rawSnsMessage = snsEvent["Message"]
    jsonSnsMessage = json.loads(rawSnsMessage)

    #print(f'Complete Sns Message:')       
    #pprint.pprint(jsonSnsMessage)

    theMsg = ReformatForSMS(jsonSnsMessage)        
    print(f'Reformat Sms Message: {theMsg}')

    sns = boto3.client(service_name='sns', region_name='us-east-1')

    params = {
        'Message': theMsg,
        'Subject': snsEvent['Subject'],
        'TopicArn': arnSmsTopic
    }
    if params['Subject'] is None: params['Subject'] = 'No Subject'
    #pprint.pprint(params)

    resp = sns.publish(**params)
    print(f'sns.publish response: {resp}')

#*************************************************
#
#*************************************************
def TransmitToSms_handler(event, context):

    arnSmsTopic = os.environ.get('ARN_SMS_TOPIC', None)
    if arnSmsTopic is None:
        print(f'[ERROR] Environement Variable ARN_SMS_TOPIC is missing')
        return {'statusCode': 401,'body': json.dumps('Environement Variable ARN_SMS_TOPIC is missing')}


    #print(f'Handler Event {event}')
    theSns = event['Records'][0]['Sns']
    TransmitToSmsTopic(theSns, arnSmsTopic = arnSmsTopic)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }


#*************************************************
#
#*************************************************
if __name__ == "__main__":
 

    GuardDutyEvent1 =  {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:ca-central-1:303697492861:phil-pager:e4a6578e-8b89-4220-9936-686197ba386f', 'Sns': {'Type': 'Notification', 'MessageId': '85e6d543-6da0-57f3-9388-8dfd4d63dc7d', 'TopicArn': 'arn:aws:sns:ca-central-1:303697492861:phil-pager', 'Subject': None, 'Message': '{"version":"0","id":"9f0a1529-b909-c3dc-e0c0-3cc988be73a6","detail-type":"AWS API Call via CloudTrail","source":"aws.guardduty","account":"303697492861","time":"2021-03-07T00:29:35Z","region":"ca-central-1","resources":[],"detail":{"eventVersion":"1.08","userIdentity":{"type":"IAMUser","principalId":"AIDAIN6CTTAXW7PC3RIGS","arn":"arn:aws:iam::303697492861:user/phil","accountId":"303697492861","accessKeyId":"AKIAUNNOH7N6ZJM7336Y","userName":"phil"},"eventTime":"2021-03-07T00:29:35Z","eventSource":"guardduty.amazonaws.com","eventName":"CreateSampleFindings","sourceIPAddress":"162.244.45.96","userAgent":"aws-cli/2.1.24 Python/3.7.3 Linux/4.19.121-linuxkit exe/x86_64.debian.10 prompt/off command/guardduty.create-sample-findings","requestParameters":{"findingTypes":["Backdoor:EC2/Spambot"],"detectorId":"e8b2d11eace51dd009880267917bb379"},"responseElements":null,"requestID":"fecc958f-1236-41fd-97a8-ca0d04c86fe4","eventID":"f4842151-d501-4c15-94bd-ddcec3f3acc5","readOnly":false,"eventType":"AwsApiCall","managementEvent":true,"eventCategory":"Management"}}', 'Timestamp': '2021-03-07T00:29:55.065Z', 'SignatureVersion': '1', 'Signature': 'r79rBp8VcEloebZoDjwdIqbgImuZ5Q2mqdu1EZJFX9xbGBPW6iCsdVbd1F1YqBYb5rqFjiizzWKxJ05P/CGpxt6mXadEczAmDxL0/whBqNPdSLdSLrOisWkeBiijuIkSLsLFZibZqsfTPY2yV614qBhSiodXGmP6SeFF6xbdYNn+Fs7cDBoikK/EALuwCPofOCU+acsEIJBXoqVyVYB6IXjUEcmo7JsCtaAsBr4maPKcv3q6QltpdWdj5JtbGJyIBksxOmJ2vXVKNMzA7cUhwts0llPB3p9AZ9qSLrZGm7HGcBy9AMShkzXtrcsQPz4XBgAor5Mu44I1djAL79QF4Q==', 'SigningCertUrl': 'https://sns.ca-central-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem', 'UnsubscribeUrl': 'https://sns.ca-central-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:ca-central-1:303697492861:phil-pager:e4a6578e-8b89-4220-9936-686197ba386f', 'MessageAttributes': {}}}]}
    # GuardDutyEvent2 = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:ca-central-1:303697492861:phil-pager:e4a6578e-8b89-4220-9936-686197ba386f', 'Sns': {'Type': 'Notification', 'MessageId': 'f041e509-0fa7-5c39-af20-bdb72e802e09', 'TopicArn': 'arn:aws:sns:ca-central-1:303697492861:phil-pager', 'Subject': None, 'Message': '{"version":"0","id":"860d8fdd-3d43-d844-370b-0fb08d1b661d","detail-type":"GuardDuty Finding","source":"aws.guardduty","account":"303697492861","time":"2021-03-07T00:30:34Z","region":"ca-central-1","resources":[],"detail":{"schemaVersion":"2.0","accountId":"303697492861","region":"ca-central-1","partition":"aws","id":"7ebc050b71c556086b524045c9067feb","arn":"arn:aws:guardduty:ca-central-1:303697492861:detector/e8b2d11eace51dd009880267917bb379/finding/7ebc050b71c556086b524045c9067feb","type":"Backdoor:EC2/Spambot","resource":{"resourceType":"Instance","instanceDetails":{"instanceId":"i-99999999","instanceType":"m3.xlarge","outpostArn":"arn:aws:outposts:us-west-2:123456789000:outpost/op-0fbc006e9abbc73c3","launchTime":"2016-08-02T02:05:06Z","platform":null,"productCodes":[{"productCodeId":"GeneratedFindingProductCodeId","productCodeType":"GeneratedFindingProductCodeType"}],"iamInstanceProfile":{"arn":"arn:aws:iam::303697492861:example/instance/profile","id":"GeneratedFindingInstanceProfileId"},"networkInterfaces":[{"ipv6Addresses":[],"networkInterfaceId":"eni-bfcffe88","privateDnsName":"GeneratedFindingPrivateDnsName","privateIpAddress":"10.0.0.1","privateIpAddresses":[{"privateDnsName":"GeneratedFindingPrivateName","privateIpAddress":"10.0.0.1"}],"subnetId":"GeneratedFindingSubnetId","vpcId":"GeneratedFindingVPCId","securityGroups":[{"groupName":"GeneratedFindingSecurityGroupName","groupId":"GeneratedFindingSecurityId"}],"publicDnsName":"GeneratedFindingPublicDNSName","publicIp":"198.51.100.0"}],"tags":[{"key":"GeneratedFindingInstaceTag1","value":"GeneratedFindingInstaceValue1"},{"key":"GeneratedFindingInstaceTag2","value":"GeneratedFindingInstaceTagValue2"},{"key":"GeneratedFindingInstaceTag3","value":"GeneratedFindingInstaceTagValue3"},{"key":"GeneratedFindingInstaceTag4","value":"GeneratedFindingInstaceTagValue4"},{"key":"GeneratedFindingInstaceTag5","value":"GeneratedFindingInstaceTagValue5"},{"key":"GeneratedFindingInstaceTag6","value":"GeneratedFindingInstaceTagValue6"},{"key":"GeneratedFindingInstaceTag7","value":"GeneratedFindingInstaceTagValue7"},{"key":"GeneratedFindingInstaceTag8","value":"GeneratedFindingInstaceTagValue8"},{"key":"GeneratedFindingInstaceTag9","value":"GeneratedFindingInstaceTagValue9"}],"instanceState":"running","availabilityZone":"GeneratedFindingInstaceAvailabilityZone","imageId":"ami-99999999","imageDescription":"GeneratedFindingInstaceImageDescription"}},"service":{"serviceName":"guardduty","detectorId":"e8b2d11eace51dd009880267917bb379","action":{"actionType":"NETWORK_CONNECTION","networkConnectionAction":{"connectionDirection":"OUTBOUND","localIpDetails":{"ipAddressV4":"10.0.0.23"},"remoteIpDetails":{"ipAddressV4":"198.51.100.0","organization":{"asn":"-1","asnOrg":"GeneratedFindingASNOrg","isp":"GeneratedFindingISP","org":"GeneratedFindingORG"},"country":{"countryName":"GeneratedFindingCountryName"},"city":{"cityName":"GeneratedFindingCityName"},"geoLocation":{"lat":0,"lon":0}},"remotePortDetails":{"port":25,"portName":"SMTP"},"localPortDetails":{"port":2000,"portName":"Unknown"},"protocol":"TCP","blocked":false}},"resourceRole":"TARGET","additionalInfo":{"unusualProtocol":"UDP","threatListName":"GeneratedFindingThreatListName","unusual":25,"sample":true},"eventFirstSeen":"2021-03-07T00:29:35.498Z","eventLastSeen":"2021-03-07T00:29:35.498Z","archived":false,"count":1},"severity":5,"createdAt":"2021-03-07T00:29:35.498Z","updatedAt":"2021-03-07T00:29:35.498Z","title":"Unusual outbound communication on port 25 from EC2 instance i-99999999.","description":"EC2 instance i-99999999 is communicating on an unusual port 25 with a remote host. This port is commonly used to send email."}}', 'Timestamp': '2021-03-07T00:31:35.840Z', 'SignatureVersion': '1', 'Signature': 'UPoPMP0kXdy27TNpuCYluNvOfIm+sbW4c9pv7XRXUuU/TIoHWQUUQiNSSD/C3rWSd/xhfx0H/x/dXXTKRMIEnJAgxnK8UE653atC92XbQqU4PcJrwxPKpzF4t6hicRrMDQdlBpjkJcHXLjGvJUcnB44Pui1R/tfY+Wp9J2jBwKnK8HiukWBhaiaHtEJP55OJnQn9FXtdAbC0jwl/v0ayHWes3wBomqtO38mHKjuYdIZlCCiyCg2kCOGYvXacO6JFWrVSNgZu1UuFFpo9UxI3jne/z5efLsGnh5lgySuuHTNmp1ZACVxX5MaDpZY0nm7uxkfp+qqavdEODpP8+REl2w==', 'SigningCertUrl': 'https://sns.ca-central-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem', 'UnsubscribeUrl': 'https://sns.ca-central-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:ca-central-1:303697492861:phil-pager:e4a6578e-8b89-4220-9936-686197ba386f', 'MessageAttributes': {}}}]}

    # TransmitToSms_handler(GuardDutyEvent2, None)
