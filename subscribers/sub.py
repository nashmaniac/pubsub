from google.cloud import pubsub_v1
import os

project_id = "your-project-id"
topic_name = "sample-call"
subscription_name = "sample_subscription"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your-file-path-json'

subscriber = pubsub_v1.SubscriberClient()
topic_path = subscriber.topic_path(project_id, topic_name)
project_path = subscriber.project_path(project_id)
subscription_path = subscriber.subscription_path(
    project_id, subscription_name
)

subscription_list = []
for sub in subscriber.list_subscriptions(project_path):
    subscription_list.append(sub.name.split('/')[-1])

if subscription_name not in subscription_list:
    subscription = subscriber.create_subscription(
        subscription_path, topic_path
    )

    print("Subscription created: {}".format(subscription))


import ast
def callback(data):
    received_dict = ast.literal_eval(data.data.decode('utf-8'))
    print("Received message from (producer): {}".format(received_dict))

    data.ack()

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback
)
print("Listening for messages on {}..\n".format(subscription_path))

# result() in a future will block indefinitely if `timeout` is not set,
# unless an exception is encountered first.
try:
    streaming_pull_future.result()
except:  # noqa
    streaming_pull_future.cancel()