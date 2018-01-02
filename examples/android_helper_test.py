#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import logging

from android_control.android_helper import AndroidHelper

logging.basicConfig(level=logging.DEBUG)


def main():
  android = AndroidHelper()

  android.is_install_adb()
  android.get_screen_width_height()
  android.get_device_info()
  android.swipe()
  android.tap()
  android.download_screenshot()
  android.record_screen_video()


if __name__ == "__main__":
  main()
