# Copyright 2014-present PlatformIO <contact@platformio.org>
# Copyright 2017 Samsung Electronics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from base64 import b64decode
from os import listdir
from os.path import isdir, isfile, join

from SCons.Script import ARGUMENTS, DefaultEnvironment

from platformio import util

env = DefaultEnvironment()

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-tizenrt")
assert isdir(FRAMEWORK_DIR)


def getPreConfig():
    pre_config = "typical"
    if ARGUMENTS.get("CUSTOM_PRE_CONFIG", ""):
        pre_config = b64decode(ARGUMENTS.get("CUSTOM_PRE_CONFIG"))
    if pre_config and not isdir(join(FRAMEWORK_DIR, "libsdk", pre_config)):
        sys.stderr.write(
            "Error: Wrong `custom_pre_config`, please check it in "
            "platformio.ini. Use 'typical' as default.\n")
        env.Exit(1)
    return pre_config


def getLibsName(path):
    ret = []
    elelist = listdir(path)
    for element in elelist:
        filepath = join(path, element)
        if isfile(filepath) and element.endswith('.a'):
            ret.append(element[3:-2])
    return ret


def parseSdkConfigsJson(basepath, filepath, pre_config):
    ret = {}
    data = util.load_json(filepath)
    prelist = data['preBuildConfigs']
    for element in prelist:
        key = element['id']
        valueList = element['includePaths']
        for index in range(len(valueList)):
            valueList[index] = join(basepath, valueList[index])
        ret[key] = valueList
    return ret[pre_config]


pre_config = getPreConfig()
configdir = join(FRAMEWORK_DIR, "libsdk", pre_config)

libdir = join(configdir, "libs")

entry_lib = env.Library(
    join("$BUILD_DIR", "entry"), [
        join(FRAMEWORK_DIR, "examples", "hello", "._main.c"),
        join(libdir, "arm_vectortab.o")
    ])

env.Append(
    LIBS=[getLibsName(libdir), entry_lib],
    LIBPATH=[libdir],
    LDSCRIPT_PATH=join(FRAMEWORK_DIR, "common", "scripts", "flash.ld"),
    CPPPATH=parseSdkConfigsJson(configdir,
                                join(FRAMEWORK_DIR, ".metadata",
                                     "configs.json"), pre_config))

env.Replace(HEADERTOOL=join(FRAMEWORK_DIR, "common", "tools", "s5jchksum.py"))
