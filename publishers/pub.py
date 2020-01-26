import os
from google.cloud import pubsub_v1

project_id = "your-project-id"
topic_name = "sample-call"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your-file-path-json'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
project_path = publisher.project_path(project_id)

topic_list = []
for topic in publisher.list_topics(project_path):
    topic_list.append(topic.name.split('/')[-1])

if topic_name not in topic_list:
    topic = publisher.create_topic(topic_path)
    print("Topic created: {}".format(topic))

for n in range(1, 11):
    data = dict(
        count=n,
        message='Message %d'%n
    )
    data = str(data).encode("utf-8")
    future = publisher.publish(
        topic_path, data
    )
    print(future.result())

print("Published messages with custom attributes.")


