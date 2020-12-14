from class_creator import MyMQTTClass
import subprocess, unittest, time, traceback, warnings
from multiprocessing import Process


class TestClassCreator(unittest.TestCase):

    def setUp(self):
        subprocess.call('mosquitto -d', shell=True)
        self.client1 = MyMQTTClass('test_client1')
        self.client2 = MyMQTTClass('test_client2')

    def test_push_message(self):
        succeeded = True
        try:
            self.client1.push_message(host, port, topics[0], 0, b"qos 0")
            self.client1.push_message(host, port, topics[0], 1, b"qos 1")
            self.client1.push_message(host, port, topics[0], 2, b"qos 2")
            assert len(self.client1.publisheds) == 3
        except:
            traceback.print_exc()
            succeeded = False

        # check client1 is publishing messages and client2 recieves it
        try:
            def subscribe():
                self.client2.connect(host, port)
                self.client2.subscribe(topics[0], 0)
                self.client2.loop_start()

            def pushing():
                self.client1.push_message(host, port, topics[0], 0, b"qos 0")
                self.client1.push_message(host, port, topics[0], 1, b"qos 1")
                self.client1.push_message(host, port, topics[0], 2, b"qos 2")

            Process(target=subscribe()).start()
            Process(target=pushing()).start()
            assert len(self.client2.messages) == 3
        except:
            traceback.print_exc()
            succeeded = False
        self.assertEqual(succeeded, True)


    def test_zero_length_clientid(self):
        succeeded = False
        try:
            client0 = MyMQTTClass('')
        except:
            warnings.simplefilter('ignore')
            succeeded = True
        self.assertEqual(succeeded, True)

    def test_dollar_topics(self):
        succeeded = True
        try:
            self.client1.connect(host, port)
            self.client1.subscribe(wildtopics[2])
            self.client1.loop_start()
            self.client1.publish("$" + topics[1], b"", 1)
            self.client1.loop_stop()
            assert len(self.client1.messages) == 0
        except:
            traceback.print_exc()
            succeeded = False
        self.assertEqual(succeeded, True)

    def tearDown(self):
        subprocess.call('pkill mosquitto', shell=True)
        time.sleep(1)


if __name__ == '__main__':
    topics = ("TopicA", "TopicA/B", "Topic/C", "TopicA/C", "/TopicA")
    wildtopics = ("TopicA/+", "+/C", "#", "/#", "/+", "+/+", "TopicA/#")
    host = "localhost"
    port = 1883
    unittest.main()
