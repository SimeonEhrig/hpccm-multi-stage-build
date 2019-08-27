import argparse
import hpccm

from hpccm.primitives import baseimage, copy, shell, runscript
from hpccm.building_blocks.cmake import cmake
from hpccm.templates.CMakeBuild import CMakeBuild
from hpccm.templates.wget import wget
from hpccm.templates.tar import tar
from hpccm.building_blocks.packages import packages

def build_openssl(name: str, build_dir: str) -> [str]:
    """install openssl
    :param name: name of the version (e.g. openssl-1.1.1c)
                 should be sliced from the official URL
    :type name: str
    :param build_dir: path where source code is stored and built
    :type build_dir: str
    :returns: list of bash commands
    :rtype: [str]
    """
    cm=[]
    wget_ssl = wget()
    tar_ssl = tar()
    cm.append(wget_ssl.download_step(url='https://www.openssl.org/source/'+name+'.tar.gz',
                                     directory=build_dir))
    cm.append(tar_ssl.untar_step(tarball=build_dir+'/'+name+'.tar.gz', directory=build_dir))
    cm.append('cd '+build_dir+'/'+name)
    cm.append('./config -Wl,-rpath=/usr/local/lib')
    cm.append('make -j')
    cm.append('make install -j')
    cm.append('cd -')
    return cm

def get_stage(container):
    # generate baseimage
    hpccm.config.set_container_format(container)
    # version >3.2 is necessary for multi-stage build
    if container == 'singularity':
        hpccm.config.set_singularity_version('3.3')
    Stage0 = hpccm.Stage()
    Stage0 += baseimage(image='ubuntu:bionic')

    # copy project from outside in the container
    if container == 'singularity':
        Stage0 += copy(src='../hello_world_tool', dest='/opt/')
    else:
        # docker: cannot copy files from outsite the build context
        # so, we need to move the build context one level up
        Stage0 += copy(src='./hello_world_tool', dest='/opt/hello_world_tool')

    # install compiler tools
    Stage0 += cmake(eula=True, version='3.14.5')
    Stage0 += packages(ospackages=['g++', 'make', 'wget', 'build-essential'])

    # build and install project
    cmb = CMakeBuild()
    cm = []
    cm.append(cmb.configure_step(build_directory='/opt/build_hello_world_tool',
                                 directory='/opt/hello_world_tool/'))
    cm.append(cmb.build_step(target='install'))
    Stage0 += shell(commands=cm)

    Stage0 += shell(commands=build_openssl(name='openssl-1.1.1c',
                                            build_dir='/opt/openssl_build'))

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
