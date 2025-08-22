# Baseline repo with following branches and environments
[Architecture DoD (Definition of Done)](https://bxpress.atlassian.net/wiki/spaces/ARCHBX/pages/619118694/Architecture+DoD+Definition+of+Done#Python)

Dockerfile `FROM python:3.12-alpine`

## development
## staging
## production

### Secrets
```
GCP_PROJECT_<CAPABILITY>
GCP_SA_<CAPABILITY>
```

### Example Message from 'queue-cmkin-mover'
```
{
  "Type": "Notification",
  "MessageId": "9510a403-8361-563d-aadd-fb899f41f873",
  "TopicArn": "arn:aws:sns:us-east-1:772932014686:topic-intcus-cmkin-tracking-xb-payload",
  "Message": "{\"_id\":\"6671b6d5465c601b584800d1\",\"timestamp\":\"2024-06-18T16:33:25.657+00:00\",\"service\":\"notify\",\"stepDetail\":\"Data Processing Started\",\"isProcessed\":true,\"eventDate\":\"2024-06-18T11:34:58.000Z\",\"error\":\"\",\"eventObservation\":\"CONSERJE 1-9\",\"orderId\":\"4500008774\",\"observationPublish\":\"Retransmitted\",\"eventCode\":\"DL\",\"media\":\"string\",\"endpointCliente\":\"http://bx-srv-intcus-tracking-utils.prod-ns-clientes-intcus/api/intcus/bx-srv-intcus-tracking-utils/v1/zara/tracking\",\"payload\":\"{\\\"orderTrackingNumber\\\":\\\"4500008774\\\",\\\"orderNumber\\\":\\\"[412697828465]\\\",\\\"statusDate\\\":\\\"2024-06-18T11:34:58.000Z\\\",\\\"remarks\\\":\\\"CONSERJE 1-9\\\",\\\"itxCode\\\":\\\"76309346-1-8\\\",\\\"courierCode\\\":\\\"923758\\\",\\\"courierDesc\\\":\\\"Blue Express Chile\\\",\\\"url\\\":\\\"http://www.bluex.cl/nacional?documentos=\\\",\\\"courierStatus\\\":\\\"DL\\\",\\\"statusRecord\\\":\\\"not_processed\\\",\\\"type\\\":\\\"dayana trujillo\\\",\\\"account\\\":\\\"76309346-1-8\\\"}\",\"segment\":\"ecommerce\",\"trackingId\":1733868223,\"messageId\":\"fbe3a2f2-eb3a-4c9b-9b05-cff192440331\",\"codeResponse\":\"200 OK\",\"responseMessage\":\"{\\\"success\\\":\\\"true\\\"}\",\"messageJson\":\"{\\\"Type\\\":\\\"Notification\\\",\\\"MessageId\\\":\\\"b72260a7-046c-5dd2-839d-3e4cbc9b0212\\\"}\",\"sellerAccount\":\"200200012-1-19\"}",
  "Timestamp": "2024-10-16T19:54:08.676Z",
  "SignatureVersion": "1",
  "Signature": "WQzZYe4nwb2cRTUOfGBNY9r9NVoXyNvaqeKtOLwKtSRTbq2ANp+oxMfDfQbrwzVuaM/ymT5nRt5uuCbYnL6NNoxbrKXpcWsa0DzMRsLY4qQB96pXzxEjEOKqAKGkGrQG3BjwBG4f2XnPIft+8Ye4MAdEKutH+FOpqlcIUXe7ye/2wpsi/sZNwMNSmJhGRjtnFiEP61qokjkGXNyPm9KB2hahpwIZ44rk2csjGXJH8Vok1Z1tbmiG6iC3bJnhwQZd5bl5nF1Xyck0mC3mJ5xbYCnxI3oi1aLvh/2w6Wudakdn+Z3pE6lARaWjkE5Js2TDHYME56a/IpshGhKL/4rxKg==",
  "SigningCertURL": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-60eadc530605d63b8e62a523676ef735.pem",
  "UnsubscribeURL": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:772932014686:topic-intcus-cmkin-tracking-xb-payload:700f7f4e-0f50-4ce9-9192-9cc3447b2069",
  "MessageAttributes": {
    "traceId": {
      "Type": "String",
      "Value": "62373033353463312d393630652d346339352d386634642d663838613539663139346466"
    },
    "eventId": {
      "Type": "String",
      "Value": "b70354c1-960e-4c95-8f4d-f88a59f194df"
    },
    "businessCapacity": { "Type": "String", "Value": "cmkin" },
    "entityType": { "Type": "String", "Value": "Events" },
    "channel": { "Type": "String", "Value": "Legacy" },
    "entityId": { "Type": "String", "Value": "9154786841" },
    "eventType": { "Type": "String", "Value": "created" },
    "version": { "Type": "String", "Value": "1.0" },
    "parentSpanId": {
      "Type": "String",
      "Value": "71756575652d696e746375732d636d6b696e2d747261636b696e672d78622d656e726963686d656e74"
    },
    "spanId": {
      "Type": "String",
      "Value": "61726e3a6177733a736e733a75732d656173742d313a3737323933323031343638363a746f7069632d696e746375732d636d6b696e2d747261636b696e672d78622d7061796c6f6164"
    },
    "datetime": { "Type": "String", "Value": "2024-10-16T19:54:08Z" },
    "domain": { "Type": "String", "Value": "clientes" },
    "subdomain": { "Type": "String", "Value": "intcus" },
    "timestamp": { "Type": "String", "Value": "1729108448" }
  }
}


