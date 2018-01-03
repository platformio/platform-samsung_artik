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

from os.path import join

from SCons.Script import (AlwaysBuild, Builder, COMMAND_LINE_TARGETS,
                          Default, DefaultEnvironment, Execute)


env = DefaultEnvironment()
platform = env.PioPlatform()


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
        "-Wp,-w",
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        "-mfpu=vfpv3"
    ],

    LINKFLAGS=[
        "-Wl,--gc-sections,--relax",
        "-mthumb",
        "-nostartfiles",
        "-nostdlib",
        "--entry=__start",
        "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
        "-mfpu=vfpv3"
    ],

    LIBS=[
        "gcc"
    ],

    PIODEBUGFLAGS=["-O0", "-g3", "-ggdb"],

    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    PROGSUFFIX=".elf",

    UPLOADER="openocd",
    UPLOADERFLAGS=[
        "-s", platform.get_package_dir("tool-artik-openocd"),
        "-f", "%s.cfg" % env.subst("$BOARD"),
        "-c", "flash_write os $BUILD_DIR/program.bin; exit"
    ],
    UPLOADCMD='"$UPLOADER" $UPLOADERFLAGS'
)

env.Append(
    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".bin"
        ),
        NS2Bin=Builder(
            action=env.VerboseAction(" ".join([
                '"$PYTHONEXE"',
                '"$HEADERTOOL"',
                "$SOURCES",
                "$TARGET"
            ]), "Adding NS2 header"),
            suffix=".bin"
        )
    )
)


#
# Target: Build executable and linkable program
#

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_prog = join("$BUILD_DIR", "${PROGNAME}.bin")
else:
    target_elf = env.BuildProgram()
    target_prog = env.NS2Bin(
        join("$BUILD_DIR", "${PROGNAME}"),
        env.ElfToBin(join("$BUILD_DIR", "interim_program"), target_elf))

AlwaysBuild(env.Alias("nobuild", target_prog))
target_buildprog = env.Alias("buildprog", target_prog, target_prog)

#
# Target: Print binary size
#

target_size = env.Alias("size", target_elf,
                        env.VerboseAction("$SIZEPRINTCMD",
                                          "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload by default .bin file
#
target_upload = env.Alias("upload", target_prog, [
    env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")
])
AlwaysBuild(target_upload)

#
# Default targets
#

Default([target_buildprog, target_size])
