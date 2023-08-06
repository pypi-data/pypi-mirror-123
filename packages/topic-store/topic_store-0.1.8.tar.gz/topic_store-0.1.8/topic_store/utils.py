#  Raymond Kirk (Tunstill) Copyright (c) 2019
#  Email: ray.tunstill@gmail.com

# Suite of utilities for topic_store package

from __future__ import absolute_import, division, print_function

from datetime import datetime

import rospy
import numpy as np

__all__ = ["time_as_ms", "ros_time_as_ms", "DefaultLogger", "best_logger", "get_topic_info", "get_partial", "get_size",
           "size_to_human_readable", "idx_of_instance"]

from std_msgs.msg import String

_numpy_types = {
    "rgb8": (np.uint8, 3), "rgba8": (np.uint8, 4), "rgb16": (np.uint16, 3), "rgba16": (np.uint16, 4),
    "bgr8": (np.uint8, 3), "bgra8": (np.uint8, 4), "bgr16": (np.uint16, 3), "bgra16": (np.uint16, 4),
    "mono8": (np.uint8, 1), "mono16": (np.uint16, 1), "bayer_rggb8": (np.uint8, 1),
    "bayer_bggr8": (np.uint8, 1), "bayer_gbrg8": (np.uint8, 1), "bayer_grbg8": (np.uint8, 1),
    "bayer_rggb16": (np.uint16, 1), "bayer_bggr16": (np.uint16, 1), "bayer_gbrg16": (np.uint16, 1),
    "bayer_grbg16": (np.uint16, 1), "8UC1": (np.uint8, 1), "8UC2": (np.uint8, 2), "8UC3": (np.uint8, 3),
    "8UC4": (np.uint8, 4), "8SC1": (np.int8, 1), "8SC2": (np.int8, 2), "8SC3": (np.int8, 3),
    "8SC4": (np.int8, 4), "16UC1": (np.uint16, 1), "16UC2": (np.uint16, 2), "16UC3": (np.uint16, 3),
    "16UC4": (np.uint16, 4), "16SC1": (np.int16, 1), "16SC2": (np.int16, 2), "16SC3": (np.int16, 3),
    "16SC4": (np.int16, 4), "32SC1": (np.int32, 1), "32SC2": (np.int32, 2), "32SC3": (np.int32, 3),
    "32SC4": (np.int32, 4), "32FC1": (np.float32, 1), "32FC2": (np.float32, 2), "32FC3": (np.float32, 3),
    "32FC4": (np.float32, 4), "64FC1": (np.float64, 1), "64FC2": (np.float64, 2), "64FC3": (np.float64, 3),
    "64FC4": (np.float64, 4)
}

def idx_of_instance(obj, instance_checks):
    if isinstance(instance_checks, tuple):
        instance_checks = (instance_checks,)
    for idx, _type in enumerate(instance_checks):
        if isinstance(obj, _type):
            return idx
    return -1


def time_as_ms(timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()
    return (timestamp - datetime.fromtimestamp(0)).total_seconds()


def ros_time_as_ms(timestamp=None):
    if timestamp is None:
        try:
            timestamp = rospy.Time.now()
        except rospy.exceptions.ROSInitException:
            import warnings
            warnings.warn("Warning can't set ros time (node not initialised ROSInitException) so using system time.")
            return time_as_ms()
    return timestamp.to_sec()


class DefaultLogger:
    def __init__(self, verbose=True, topic=None, **kwargs):
        self._verbose = verbose
        self._logger = print
        # Create publisher for topic_store scenario logs
        if topic is None:
            topic = "logs"
        self._log_publisher = rospy.Publisher("/topic_store/{}".format(topic), String, queue_size=1)
        self._base_description = "\033[93mTopic Store\033[0m: "

    def __call__(self, message, only_publish=False, **kwargs):
        self._log_publisher.publish(String(message))
        if only_publish:
            return
        verbose = kwargs.pop("verbose", False) or self._verbose
        if verbose:
            kwarg_str = " " + ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
            self._logger("{}{}{}".format(self._base_description, message, kwarg_str))


class TQDMInfiniteLogger(DefaultLogger, object):
    def __init__(self, verbose=True, topic=None, **kwargs):
        super(TQDMInfiniteLogger, self).__init__(verbose=verbose, topic=topic)
        try:
            from tqdm import tqdm
        except ImportError:
            raise

        tqdm_args = {
            "total": 0,
            "bar_format": "{desc} {n_fmt}/{total_fmt} [{elapsed}, '{rate_fmt}{postfix}']",
            "desc": self._base_description,
        }

        tqdm_args.update(kwargs)
        self._progress_bar = tqdm(**tqdm_args)
        self._progress_bar.clear()

    def __call__(self, message, only_publish=False, **kwargs):
        self._log_publisher.publish(String(message))
        if only_publish:
            return
        verbose = kwargs.pop("verbose", False) or self._verbose
        if verbose:
            if kwargs:
                self._progress_bar.set_postfix(kwargs)
            self._progress_bar.set_description_str(self._base_description + message)
            self._progress_bar.total += 1
            self._progress_bar.update(1)


def best_logger(verbose, topic=None, **kwargs):
    """Return the best logger available"""
    try:
        return TQDMInfiniteLogger(verbose=verbose, topic=topic, **kwargs)
    except ImportError:
        return DefaultLogger(verbose=verbose, topic=topic, **kwargs)


def get_size(obj, recurse=True, human_readable=True):
    """Sum size of object & members. Utility function for printing document size, used in __repr__."""
    from types import ModuleType, FunctionType
    from gc import get_referents
    import sys
    blacklisted_types = (type, ModuleType, FunctionType)

    if isinstance(obj, blacklisted_types):
        raise TypeError('getsize() does not take argument of type: ' + str(type(obj)))
    size = 0

    if recurse:
        seen_ids = set()
        objects = [obj]
        while objects:
            need_referents = []
            for obj in objects:
                if not isinstance(obj, blacklisted_types) and id(obj) not in seen_ids:
                    seen_ids.add(id(obj))
                    size += sys.getsizeof(obj)
                    need_referents.append(obj)
            objects = get_referents(*need_referents)
    else:
        size = sys.getsizeof(obj)

    if not human_readable:
        return size

    return size_to_human_readable(size)


def size_to_human_readable(size):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if size < 1024.0:
            break
        size /= 1024.0
    return "{:.2f}{}B".format(size, unit)


def get_partial(func, *part_args):
    def wrapper(*extra_args):
        args = list(part_args)
        args.extend(extra_args)
        return func(*args)

    return wrapper


def get_topic_info(topic):
    """Returns topic_class, topic_type tuple"""
    import rostopic  # No python package so here to enable some non-ros functionality
    return rostopic.get_topic_class(topic)[0], rostopic.get_topic_type(topic)[0]
