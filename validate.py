from flask import Flask, request, jsonify
from re import search
from os import environ
import logging

webhook = Flask(__name__)

webhook.config['cpu'] = environ.get('cpu')
if search("m", webhook.config['cpu']):
    core_cpu = float(webhook.config['cpu'][:-1]) / 1000
    mcore_cpu = float(webhook.config['cpu'][:-1])
else:
    core_cpu = float(webhook.config['cpu'])
    mcore_cpu = float(webhook.config['cpu']) * 1000

webhook.logger.setLevel(logging.INFO)

if "cpu" not in environ:
    webhook.logger.error("Required environment variable for label isn't set. Exiting...")
    exit(1)


properties = open("properties.yaml", "r")
data = properties.read()
list = data.split("\n")
properties.close()

@webhook.route('/validate', methods=['POST'])
def validating_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")
    namespace = request_info["request"]["namespace"]



    if namespace in list:
        for i in range(len(request_info["request"]["object"]["spec"]["template"]["spec"]["containers"])):
            try:
                if request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][i]["resources"]["requests"]["cpu"]:
                    if search("m", request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][i]["resources"]["requests"]["cpu"]):
                        if float(request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][i]["resources"]["requests"]["cpu"][:-1]) > mcore_cpu:
                            webhook.logger.info(f'CPU Request exceeds the range!')
                            return admission_response(False, uid, f"CPU Request exceeds the range! Please set cpu request between the range 0-{mcore_cpu} milicores.")
                    else:
                        if float(request_info["request"]["object"]["spec"]["template"]["spec"]["containers"][i]["resources"]["requests"]["cpu"]) > core_cpu:
                            webhook.logger.info(f'CPU Request exceeds the range!')
                            return admission_response(False, uid, f"CPU Request exceeds the range! Please set cpu request between the range 0-{mcore_cpu} milicores.")
            except KeyError:
                webhook.logger.error(f'CPU Request is not defined!')
                return admission_response(False, uid, f"CPU Request is not defined. Please set request.cpu value for the the container")
        
        webhook.logger.info(f'CPU Request value is in the range!')
        return admission_response(True, uid, f"CPU Request value is in the range!")
    
    else:
      webhook.logger.info(f'This namespace is not restricted!')
      return admission_response(True, uid, f"This namespace is not restricted!")
    


def admission_response(allowed, uid, message):
    return jsonify({"apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response":
                        {"allowed": allowed,
                         "uid": uid,
                         "status": {"message": message}
                         }
                    })


if __name__ == '__main__':
    webhook.run(host='0.0.0.0',
                port=5000)
