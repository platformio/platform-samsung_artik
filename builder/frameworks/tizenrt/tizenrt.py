from os.path import join
from SCons.Script import DefaultEnvironment
from platformio import util
import os
import json

env = DefaultEnvironment()


def getPreConfig(sdkdir):

    if util.load_project_config().has_option("env:%s" % (env.subst("$BOARD")), "pre_config"):
        pre_config = util.load_project_config().get("env:%s" % (env.subst("$BOARD")), "pre_config")
        if os.path.exists(join(sdkdir, "libsdk", pre_config)):
            pass
        else:
            print 'Wrong pre_config, please check it in platform.ini. Use "typical" as default.'
            pre_config = "typical"
        configdir = join(sdkdir, "libsdk", pre_config)
    else:
        pre_config = "typical"
        configdir = join(sdkdir, "libsdk", pre_config)
    return (pre_config, configdir)


def getLibsName(path):
    ret = []
    elelist = os.listdir(path)
    for element in elelist:
        filepath = os.path.join(path, element)
        if (os.path.isfile(filepath) and element.endswith('.a')):
            ret.append(element[3: -2])
    return ret


def parseSdkConfigsJson(basepath, filepath, pre_config):
    ret = {}
    jsonfile = open(filepath)
    data = json.load(jsonfile)
    prelist = data['preBuildConfigs']
    for element in prelist:
        key = element['id']
        valueList = element['includePaths']
        for index in range(len(valueList)):
            valueList[index] = os.path.join(basepath, valueList[index])
        ret[key] = valueList
    return ret[pre_config]

sdkdir = env.PioPlatform().get_package_dir("framework-tizenrt")

(pre_config, configdir) = getPreConfig(sdkdir)

libdir = join(configdir, "libs")

entry_lib = (env.Library(join("$BUILD_DIR", "entry"), [join(sdkdir, "examples/hello/._main.c"), join(libdir, "arm_vectortab.o")]))

env.Append(
    LIBS=[
        getLibsName(libdir),
        entry_lib
    ],
    LIBPATH=[
        libdir
    ],
    LDSCRIPT_PATH=join(sdkdir, "common", "scripts", "flash.ld"),
    CPPPATH=parseSdkConfigsJson(configdir, join(sdkdir, ".metadata", "configs.json"), pre_config)
)

env.Replace(
    HEADERTOOL=join(env.PioPlatform().get_package_dir("framework-tizenrt") or "",
                    "common/tools/s5jchksum.py")
)
