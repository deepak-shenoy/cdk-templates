#
# Test Lambda Handler Script
# Deepak Shenoy
# May 2nd, 2026
#
import json

def handler(event, context):
    http_method = event.get("httpMethod", "")
    path        = event.get("path","")
    body        = event.get("body", "")

    if path == "/test1" and http_method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Context-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "test completed"})
        }

    if path == "/test2" and http_method == "POST":
        return {
            "statusCode": 200,
            "headers": {
                "Context-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"body": json.loads(body or {})})
        }
    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Route not found"})
    }