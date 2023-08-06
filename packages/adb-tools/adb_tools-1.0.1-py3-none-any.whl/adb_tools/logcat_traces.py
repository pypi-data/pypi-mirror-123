import os

def get_android_crash_info(serialno, log_path):
    os.system("adb -s %s shell logcat -b crash > %s" % (serialno, log_path))


def get_anr_info(serialno, log_path):
    os.system("adb -s %s bugreport %s" % (serialno, log_path))


def clear_device_logcat_info(serialno):
    os.system("adb -s %s shell logcat -c" % serialno)


def get_app_info(serialno, package_name, log_path):
    os.system("adb -s %s shell logcat *:W | grep -i %s > %s" % (serialno, package_name, log_path))


if __name__ == "__main__":
    # clear_device_logcat_info()
    # get_android_crash_info("/Users/zhuhuiping/Desktop/脚本/crash.log")
    # get_app_info('com.shizhuang.duapp', "/Users/zhuhuiping/Desktop/脚本/app.log")
    get_anr_info('52dc62d9', '/Users/zhuhuiping/Desktop/脚本')
