#!/usr/bin/env python

#  Raymond Kirk (Tunstill) Copyright (c) 2019
#  Email: ray.tunstill@gmail.com

# Script to run and collect data from a scenario.yaml file.


from __future__ import absolute_import, division, print_function

import datetime
import json
import os
from collections import defaultdict
from threading import Event

import actionlib
import pathlib
import rospy

from topic_store.file_parsers import ScenarioFileParser
from topic_store.load_balancer import LoadBalancer, FPSCounter
from topic_store.msg import CollectDataAction, CollectDataResult, \
    CollectDataFeedback
from topic_store.store import SubscriberTree, AutoSubscriber
from topic_store.utils import best_logger, DefaultLogger, get_size, size_to_human_readable


class ScenarioRunner:
    def __init__(self, scenario_file, stabilise_time, verbose=True, queue_size=100, n_io_threads=1, threads_auto=False,
                 use_grid_fs=False):
        self.saved_n = 0

        self.scenario_file = scenario_file
        self.stabilise_time = stabilise_time
        self.verbose = verbose
        self.thread_queue_size = queue_size
        self.n_threads = n_io_threads
        self.auto_threads = threads_auto
        self.use_grid_fs = use_grid_fs
        self.events = {}

        # Load Scenario
        rospy.loginfo("Loading scenario: '{}'".format(scenario_file))
        self.scenario = ScenarioFileParser(scenario_file)

        # Create publisher for topic_store scenario logs
        self.logger = best_logger(verbose=verbose)
        self.info_logger = DefaultLogger(verbose=verbose)

        # Create subscriber tree for getting all the data
        self.subscriber_tree = SubscriberTree(self.scenario.data)
        if self.stabilise_time:
            self.info_logger("Waiting for {}s before starting (stabilise_time)".format(self.stabilise_time))
            rospy.sleep(self.stabilise_time)

        # Choose appropriate methods
        # Setting up the scenario runner this way means it's easily extendable by inheriting from Scenario runner
        # and declaring custom behaviours
        save_init_function_name = "init_save_" + self.scenario.storage["method"]
        self.save_method_init_function = getattr(self, save_init_function_name, None)
        if not callable(self.save_method_init_function):
            raise Exception("Invalid storage value ('{}()' does not exist)".format(save_init_function_name))
        self.save_method_init_function()

        save_function_name = "save_" + self.scenario.storage["method"]
        self.save_method_function = getattr(self, save_function_name, None)
        if not callable(self.save_method_function):
            raise Exception("Invalid storage value ('{}()' does not exist)".format(save_function_name))

        collection_method_init_name = "init_way_point_" + self.scenario.collection["method"]
        self.collection_method_init_function = getattr(self, collection_method_init_name, None)
        if not callable(self.collection_method_init_function):
            raise Exception("Invalid way point value ('{}()' does not exist)".format(collection_method_init_name))

        self.save_callback_rate = FPSCounter()
        self.event_callback_rate = FPSCounter()
        self.extra_logs = {}
        if self.n_threads > 0:
            self.jobs_worker = LoadBalancer(maxsize=self.thread_queue_size, threads=self.n_threads,
                                            auto=self.auto_threads)
            self.save_callback_rate = FPSCounter(self.jobs_worker.maxsize)
        self.collection_method_init_function()

    def init_way_point_action_server(self):
        def __request(goal_msg):
            success, save_msg = True, "Success!"
            # TODO: self.save() no longer returns values of self.__save() because jobs are handled in a load_balancer
            # TODO: for now action_server will return success no matter what
            self.save()
            result = CollectDataResult(success)
            feedback = CollectDataFeedback(save_msg)
            self.service_server.publish_feedback(feedback)
            (self.service_server.set_succeeded if success else self.service_server.set_aborted)(result)

        action_lib_server_name = self.scenario.collection["action_server_name"]
        self.info_logger("Starting '{}' actionlib server".format(action_lib_server_name))
        self.service_server = actionlib.SimpleActionServer(action_lib_server_name, CollectDataAction, __request, False)
        self.service_server.start()

    def init_way_point_action_server_video(self):
        event_name = "action_lib_start_stop"
        topic_to_watch = self.scenario.collection["watch_topic"]

        self.events[event_name] = {"event": Event(), "data": False}
        self.events[topic_to_watch] = {"event": Event(), "data": ""}

        def __request(goal_msg):
            should_start = str(goal_msg.message).lower() in ["true", "t", "start"]
            starting_string = "Starting" if should_start else "Stopping"
            self.info_logger("{} data collection from '{}'".format(starting_string, action_lib_server_name))
            self.set_event_msg_callback(should_start, event_name)

            result = CollectDataResult(should_start)
            feedback = CollectDataFeedback("{} data capture".format(starting_string))
            self.service_server.publish_feedback(feedback)
            self.service_server.set_succeeded(result)

        action_lib_server_name = self.scenario.collection["action_server_name"]
        self.info_logger("Starting '{}' actionlib server".format(action_lib_server_name))
        self.service_server = actionlib.SimpleActionServer(action_lib_server_name, CollectDataAction, __request, False)
        self.service_server.start()

        AutoSubscriber(topic_to_watch, callback=self.set_event_msg_callback, callback_args=topic_to_watch)

        while not rospy.is_shutdown():
            self.events[topic_to_watch]["event"].wait()
            self.events[topic_to_watch]["event"].clear()
            if self.events[event_name]["data"]:
                self.save()
                # self.log("Waiting for event on '{}' topic before next data cycle".format(topic_to_watch))

    def set_event_msg_callback(self, data, event_id):
        if event_id in self.events:
            self.event_callback_rate.toc()
            self.event_callback_rate.tic()
            self.extra_logs["event_callback_rate"] = "{:.2f}".format(self.save_callback_rate.get_fps())
            self.events[event_id]["data"] = data
            self.events[event_id]["event"].set()

    def init_way_point_timer(self):
        delay = self.scenario.collection["timer_delay"]
        while not rospy.is_shutdown():
            self.save()
            # self.log("Waiting for {}s before next data cycle".format(delay))
            rospy.sleep(delay)

    def init_way_point_event(self):
        event_name = "topic_update"
        topic_to_watch = self.scenario.collection["watch_topic"]
        self.events[event_name] = {"event": Event(), "data": ""}
        AutoSubscriber(topic_to_watch, callback=self.set_event_msg_callback, callback_args=event_name)
        while not rospy.is_shutdown():
            self.events[event_name]["event"].wait()
            self.events[event_name]["event"].clear()
            self.save()
            # self.log("Waiting for event on '{}' topic before next data cycle".format(topic_to_watch))

    def init_save_database(self):
        from topic_store.database import MongoStorage
        self.db_client = MongoStorage(config=self.scenario.storage["config"], collection=self.scenario.context,
                                      use_grid_fs=self.use_grid_fs)
        self.info_logger("Initialised saving to database {} @ '{}/{}'".format(self.db_client.uri,
                                                                              self.db_client.name,
                                                                              self.scenario.context))

    def init_save_filesystem(self):
        from topic_store.filesystem import TopicStorage
        formatted_datetime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        save_location = self.scenario.storage["location"]
        if not save_location or save_location in ["default", "auto", "topic_store"]:
            save_location = pathlib.Path(os.path.expanduser("~/.ros/topic_store/filesystem"))
        elif save_location.startswith("pkg="):
            package_name = save_location.split('=')[-1]
            save_location = pathlib.Path(os.path.expanduser("~/.ros/topic_store/filesystem/{}/".format(package_name)))
        else:
            save_location = pathlib.Path(os.path.expanduser(save_location))
        save_folder = save_location / self.scenario.context
        self.info_logger("Configured save_location as '{}'".format(save_folder))
        try:
            save_folder.mkdir(parents=True)
        except OSError as e:
            if e.errno != 17:  # File exists is okay
                raise

        save_file = save_folder / "{}{}".format(formatted_datetime, TopicStorage.suffix)
        self.filesystem_storage = TopicStorage(save_file)
        self.info_logger("Initialised saving to the filesystem at '{}'".format(self.filesystem_storage.path))

    def save_database(self, message_tree):
        insert_result = self.db_client.insert_one(message_tree)
        self.saved_n += 1
        # self.log("Inserted document to database result='acknowledged={}, inserted_id={}'".format(
        #     insert_result.acknowledged, insert_result.inserted_id))
        return insert_result.inserted_id

    def save_filesystem(self, message_tree):
        # self.log("Saving documents to file system n={}".format(self.saved_n))
        self.saved_n += 1
        self.filesystem_storage.insert_one(message_tree)
        return self.saved_n

    def __save(self, data, job_meta=None, **kwargs):
        try:
            saved_data_id = self.save_method_function(data)
        except Exception as e:
            self.info_logger("Exception raised when saving! '{}'".format(e.message))
            return False, e.message
        if job_meta is not None:
            worker_id = job_meta.pop("worker_id", None)
            # Pretty print some variables
            info_str = {k.replace("worker_", ""): "{:.2f}".format(v) for k, v in job_meta.items()}
            self.extra_logs["save_callback_rate"] = "{:.2f}".format(self.save_callback_rate.get_fps())
            for k, v in self.extra_logs.items():
                info_str[k] = v
            self.logger("Worker {} successfully saved data id='{}'".format(worker_id, saved_data_id), **info_str)
        else:
            self.logger("Successfully saved data id='{}'".format(saved_data_id), **self.extra_logs)
        return True, "Success!"

    def save(self):
        """Collates data from the scenario topic structure and saves. Returns SaveSuccess, SaveMessage"""
        self.save_callback_rate.toc()
        self.save_callback_rate.tic()
        data_hierarchy = self.subscriber_tree.get_message_tree()
        if self.n_threads == 0:  # don't use a threading model
            self.__save(data_hierarchy)
        else:
            added_task = self.jobs_worker.add_task(self.__save, [data_hierarchy], {}, wait=False)
            if not added_task:
                self.info_logger("IO Queue Full, cannot add jobs to the queue, please wait.", verbose=True)
                self.jobs_worker.add_task(self.__save, [data_hierarchy], {}, wait=True)


class ScenarioMonitor:
    def __init__(self, scenario_file, verbose=True, no_log=False):
        self.saved_n = 0

        self.scenario_file = scenario_file
        self.verbose = verbose
        self.events = {}

        # Load Scenario
        rospy.loginfo("Loading scenario: '{}'".format(scenario_file))
        self.scenario = ScenarioFileParser(scenario_file)

        # Create publisher for topic_store scenario logs
        self.logger = best_logger(verbose=verbose, topic="monitor")
        self.info_logger = DefaultLogger(verbose=verbose, topic="monitor")

        # Create subscriber tree for getting all the data
        self.hz = defaultdict(FPSCounter)
        self.size = defaultdict(str)
        self.no_log = no_log
        self.subscriber_tree = SubscriberTree(self.scenario.data, callback=self.topic_info_callback, pass_ref=True)

        self.run()

    def run(self):
        rate = rospy.Rate(5)
        while not rospy.is_shutdown():
            rate.sleep()
            topic_info = [(k, self.hz[k].get_fps(), size_to_human_readable(self.size[k])) for k in self.hz.keys()]
            topic_info_dict = {name: "{:.2f}hz ({})".format(hz, size) for name, hz, size in topic_info}
            total_size = sum([size for size in self.size.values()])
            if total_size:
                topic_info_dict["total_size"] = "~{}".format(size_to_human_readable(total_size))
            self.logger(message=json.dumps(topic_info_dict, indent=4), only_publish=self.no_log)

    def topic_info_callback(self, auto_logger, data, *args, **kwargs):
        topic_name = auto_logger.subscriber.subscriber.name
        self.hz[topic_name].toc()
        self.hz[topic_name].tic()
        self.size[topic_name] = get_size(data, human_readable=False)
