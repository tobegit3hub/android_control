#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging
import os
import subprocess
import sys

logging.basicConfig(level=logging.DEBUG)


class AndroidHelper(object):
  """
  The helper class to access Android devices.
  """

  def __init__(self):
    pass

  def is_install_adb(self):
    """
    Check if install adb or not.

    Args:

    Return:
      True if it installed adb and False if not.
    """

    command = "adb devices"
    if os.system(command) == 0:
      logging.debug("The adb command has installed")
      return True
    else:
      logging.debug("The adb command has not installed")
      return False

  def get_device_info(self):
    """
    Get the information of the device.

    Args:

    Return:
      The dictionary of the information of the device.
    """

    # Example: "MIX 2"
    device_adb_command = "adb shell getprop ro.product.model"
    device_result = os.popen(device_adb_command).read()
    # Example: "Physical density: 440"
    density_adb_command = "adb shell wm density"
    density_result = os.popen(density_adb_command).read()

    device_info = {"device": device_result, "density": density_result}
    logging.debug("The deivce info: {}".format(device_info))
    return device_info

  def get_screen_width_height(self):
    """
    Get the width and height of the screen.

    Args:

    Return:
      width: The width of the screen.
      height: The height of the screen.
    """

    # Example is "Physical size: 1080x2160"
    adb_command = "adb shell wm size"
    adb_command_output = os.popen(adb_command).read()
    if adb_command_output.startswith("Physical size: "):
      # Example is "1080x2160"
      width_height_string = adb_command_output[len("Physical size: "):]
      width_height_array = width_height_string.split("x")
      width = width_height_array[0]
      height = width_height_array[1]
      logging.debug(
          "The screen width: {} and height: {}".format(width, height))
      return width, height

  def download_screenshot(self, filename="./screenshot.png"):
    """
    Download the screenshot of the device.

    Args:
     filename: The filename of the screenshot image to save.

    Return:
    """

    adb_command = "adb shell screencap -p"
    screenshot_content = subprocess.Popen(
        adb_command, shell=True, stdout=subprocess.PIPE).stdout.read()

    if sys.platform == "win32":
      screenshot_content = screenshot_content.replace(b'\r\n', b'\n')

    logging.debug("Try to save the screenshot in path: {}".format(filename))
    f = open(filename, "wb")
    f.write(screenshot_content)
    f.close()

  def download_file(self, phone_file, local_file):
    adb_command = "adb pull {} {}".format(phone_file, local_file)
    logging.debug("Try to execute command: {}".format(adb_command))
    os.system(adb_command)

  def upload_file(self, local_file, phone_file):
    adb_command = "adb push {} {}".format(local_file, phone_file)
    logging.debug("Try to execute command: {}".format(adb_command))
    os.system(adb_command)

  def delete_phone_file(self, phone_file, recursive=False):
    adb_command = "adb pull /sdcard/screen_video.mp4 ./screen_video.mp4"
    if recursive:
      adb_command = "adb shell rm -r {}".format(phone_file)
    else:
      adb_command = "adb shell rm {}".format(phone_file)

    logging.debug("Try to execute command: {}".format(adb_command))
    os.system(adb_command)

  def record_screen_video(self,
                          duration=5,
                          local_filename="./screen_video.mp4",
                          phone_filename="/sdcard/screen_video.mp4",
                          delete_phone_file=True):
    """
    Record the screen video and download.

    Args:
     duration: The duration the video to record.
     local_filename: The filename of the screen video in local.
     phone_filename: The filename of the screen video in the phone.
     delete_phone_file: If delete the video after copying to local.

    Return:
    """

    adb_command = "adb shell screenrecord --time-limit {} {}".format(
        duration, phone_filename)
    logging.debug("Try to execute command: {}".format(adb_command))
    os.system(adb_command)

    adb_command = "adb pull /sdcard/screen_video.mp./screen_video.mp4"
    self.download_file(phone_filename, local_filename)

    if delete_phone_file:
      self.delete_phone_file(phone_filename)

  def swipe(self, x1=100, y1=100, x2=100, y2=200, swipe_time=200):
    """
    Swipe the device.

    Args:
     x1: The x of start point.
     y1: The y of start point.
     x2: The x of end point.
     y2: The y of end point.
     swipe_time: The duration to press.

    Return:
    """
    adb_command = "adb shell input swipe {} {} {} {} {}".format(
        x1, y1, x2, y2, swipe_time)
    logging.debug("Try to execute command: {}".format(adb_command))
    os.system(adb_command)

  def tap(self, x=100, y=100):
    """
    Tap the screen.

    Args:
      x: The x of point.
      y: The y of point.

    Return:
    """
    adb_command = "adb shell input tap {} {}".format(x, y)
    logging.debug("Try to execute command: {}".format(adb_command))
    os.system(adb_command)
