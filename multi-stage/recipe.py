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
    cm.append('./config --prefix=/opt/openssl_install -Wl,-rpath=/usr/local/lib')
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
    # the stages need "names" so that they can reference each other
    Stage0 += baseimage(image='ubuntu:bionic', _as='Stage0')

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
    cmb = CMakeBuild(prefix="/opt/hello_install/")
    cm = []
    cm.append(cmb.configure_step(build_directory='/opt/build_hello_world_tool',
                                 directory='/opt/hello_world_tool/',
                                 opts=['-DCMAKE_INSTALL_RPATH=/usr/local/lib/']))
    cm.append(cmb.build_step(target='install'))
    Stage0 += shell(commands=cm)

    Stage0 += shell(commands=build_openssl(name='openssl-1.1.1c',
                                            build_dir='/opt/openssl_build'))

    # add release stage
    Stage1 = hpccm.Stage()
    Stage1 += baseimage(image='ubuntu:bionic', _as='Stage1')
    Stage1 += copy(_from='Stage0',
                   src='/opt/hello_install/',
                   dest='/usr/local/')

    Stage1 += copy(_from='Stage0',
                   src='/opt/openssl_install/',
                   dest='/usr/local/')

    # the commands merge the bin, lib ect. folders of hello_install and openssl_install
    # in the /usr/local folder
    if container == "singularity":
        Stage1 += shell(commands=['cp -rl /usr/local/hello_install/* /usr/local/',
                                  'cp -rl /usr/local/openssl_install/* /usr/local/',
                                  'rm -r /usr/local/hello_install/',
                                  'rm -r /usr/local/openssl_install/'])



    # script that runs when
    # - singularity uses the run parameter or the image runs directly
    # - docker uses the run parameter without arguments
    Stage1 += runscript(commands=['hello_world_tool'])

    return [Stage0, Stage1]

def main():
    parser = argparse.ArgumentParser(
        description='Build commands:\n sudo singularity build multi-stage.sif singularity.def\n singularity build --fakeroot multi-stage.sif singularity.def\n cd .. && docker build -f multi-stage/Dockerfile -t multi-stage:dev . && cd multi-stage\n\nRun commands:\n ./singularity\n docker run multi-stage:dev',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.parse_args()

    with open("Dockerfile", 'w') as filehandle:
        recipe = []
        for stage in get_stage('docker'):
            recipe.append('')
            recipe.append(stage.__str__())
        filehandle.write('\n'.join(recipe))

    with open("singularity.def", 'w') as filehandle:
        recipe = []
        for stage in get_stage('singularity'):
            recipe.append('')
            recipe.append(stage.__str__())
        filehandle.write('\n'.join(recipe))

if __name__ == '__main__':
    main()
