# hpccm-multi-stage-build
This is an example to test the multi-level build feature of [hpccm](https://github.com/NVIDIA/hpc-container-maker) with self-compiled projects. The targets are Docker and Singularity.

# Differences between single- and multi-stage build
## memory saving
 * singularity: 175MB vs. 32MB
 * docker:      514MB vs. 86MB
## differences in the build receipt
 * set install prefix to different locations
  * the default path (`/usr/local/`) is not suitable because the folder contains build and release applications
 * set rpath, if runtime application use shared libraries
  * the rpath is set in the executable and allows linking without `LD_LIBRARY_PATH`
  * must be set to the second stage installation path (usually `/usr/local/lib`)
 * add "names" to the stages for references (parameter `_as`)
 * add a second stage
  * copy files from the first in the second stage
  * use `__str__()` function on both stages
