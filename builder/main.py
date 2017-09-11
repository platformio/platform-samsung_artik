from os.path import join
from SCons.Script import DefaultEnvironment
import os
import json
from platformio import util
import platform

env = DefaultEnvironment()

openocdPath = env.PioPlatform().get_package_dir("tool-artik-openocd")
switchPath = join(openocdPath, "switch-driver.py")
if ('Darwin' == platform.system() and os.path.exists(switchPath)):
    os.popen('sudo ' + switchPath)

BUILD_DIR_FIX = env.subst("$BUILD_DIR").replace("\\", "/")
env.Replace(
    BUILD_DIR=BUILD_DIR_FIX,
    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",
    GDB="arm-none-eabi-gdb",
    CXX="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    SIZETOOL="arm-none-eabi-size",
    STRIP="arm-none-eabi-strip",

    ASFLAGS=[
        "-D__ASSEMBLY__"
    ],

    CCFLAGS_=[
        "-g",   # include debugging info (so errors include line numbers)
        "-O0",  # optimize for size
        "-Wall",
        "-fno-builtin",
        "-Wstrict-prototypes",
        "-Wshadow",
        "-Wno-implicit-function-declaration",
        "-Wno-unused-function",
        "-Wno-unused-but-set-variable",
        "-fno-strict-aliasing",
        "-fno-strength-reduce",
        "-fomit-frame-pointer",
        "-Wp,-w"
    ],

    LINKFLAGS=[
        "-Wl,--gc-sections,--relax",
        "-mthumb",
        "-nostartfiles",
        "-nostdlib",
        "--entry=__start"
    ],

    LIBS=[
        "gcc"
    ],

    CCCOM='$CC -o $TARGET -c $CFLAGS $CCFLAGS_ $_CCCOMCOM $SOURCES',
    LINKCOM='$LINK -o $TARGET $LINKFLAGS $__RPATH $SOURCES $_LIBDIRFLAGS -Wl,--start-group $_LIBFLAGS -Wl,--end-group',
    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES'
)

env.Append(
    CCFLAGS=[
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        "-mfpu=vfpv3"
    ],
    LINKFLAGS=[
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        "-mfpu=vfpv3"
    ],
)

env.Replace(
    WORKDIR=env.PioPlatform().get_package_dir("tool-artik-openocd"),
    UPLOADER="openocd",
    UPLOADERFLAGS=[
        "-s", "$WORKDIR",
        "-f", "%s.cfg" % (env.subst("$BOARD")),
        "-c", "flash_write os $BUILD_DIR/$SOURCE; exit"
    ],

    UPLOADCMD='$UPLOADER $UPLOADERFLAGS',
)
#
# Target: Build executable and linkable firmware
#

target_elf = env.BuildProgram()

#
# Target: Generate binary firmware
#

target_bin = env.Alias(
    "program.bin", target_elf,
    env.VerboseAction("$OBJCOPY -O binary ${SOURCE} ${BUILD_DIR}/program.bin", "Generating binary"))
AlwaysBuild(target_bin)

#
# Target: Add NS2 header to executable
#

target_header = env.Alias(
    "program_head.bin", target_bin,
    env.VerboseAction("python $HEADERTOOL ${BUILD_DIR}/$SOURCE ${BUILD_DIR}/program_head.bin", "Adding NS2 header"))
AlwaysBuild(target_header)
target_buildprog = env.Alias("buildprog", target_header, target_header)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload by default .bin file
#

target_upload = env.Alias(
    "upload", target_header,
    env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE"))
AlwaysBuild(target_upload)

#
# Default targets
#

Default([target_buildprog, target_size])
