# version 3.12 is not necessary
# it's just for testing the container
cmake_minimum_required(VERSION 3.12)

project(hello_world_tool)

# enable rpath linkage
# the rpath is necessary, that the hello_world_tool executable can find the libhello.so
# without rpath, the libhello.so have to be in the LD_LIBRARY_PATH
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

include_directories(include/)

add_library(hello SHARED lib/hello.cpp)
add_executable(hello_world_tool main.cpp)
target_link_libraries(hello_world_tool PUBLIC hello)

install(TARGETS hello_world_tool hello
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin)

install(FILES include/hello.h DESTINATION include)
