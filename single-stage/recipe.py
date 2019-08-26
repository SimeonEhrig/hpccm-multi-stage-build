import argparse
import hpccm

from hpccm.primitives import baseimage, copy, shell, runscript
from hpccm.building_blocks.cmake import cmake
from hpccm.templates.CMakeBuild import CMakeBuild
from hpccm.building_blocks.packages import packages

def get_stage(container):
    # generate baseimage
    hpccm.config.set_container_format(container)
    Stage0 = hpccm.Stage()
    Stage0 += baseimage(image='ubuntu:bionic')

    # copy project from outside in the container
    if container == 'singularity':
        Stage0 += copy(src='../hello_world_tool', dest='/opt/')
    else:
        # docker
        Stage0 += copy(src='./hello_world_tool', dest='/opt/hello_world_tool')

    # install compiler tools
    Stage0 += cmake(eula=True)
    Stage0 += packages(ospackages=['g++', 'make'])

    # build and install project
    cmb = CMakeBuild()
    cm = []
    cm.append(cmb.configure_step(build_directory='/opt/build_hello_world_tool',
                                 directory='/opt/hello_world_tool/'))
    cm.append(cmb.build_step(target='install'))
    Stage0 += shell(commands=cm)

    # script that runs when
    # - singularity uses the run parameter or the image runs directly
    # - docker uses the run parameter without arguments
    Stage0 += runscript(commands=['hello_world_tool'])

    return Stage0

def main():

    parser = argparse.ArgumentParser(
        description='Build commands:\n sudo singularity build single-stage.sif singularity.def\n singularity build --fakeroot single-stage.sif singularity.def\n cd .. && docker build -f single-stage/Dockerfile -t single-stage:dev . && cd single-stage\n\nRun commands:\n ./singularity\n docker run single-stage:dev',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.parse_args()

    with open("Dockerfile", 'w') as filehandle:
        filehandle.write(get_stage('docker').__str__())

    with open("singularity.def", 'w') as filehandle:
        filehandle.write(get_stage('singularity').__str__())


if __name__ == '__main__':
    main()
