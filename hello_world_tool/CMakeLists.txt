# version 3.12 is not necessary
# it's just for testing the container
cmake_minimum_required(VERSION 3.12)

project(hello_world_tool)

include_directories(include/)

# if the RPATH is not set, set it to a default path
if("${CMAKE_INSTALL_RPATH}" STREQUAL "")
  set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
  set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
endif()

add_library(hello SHARED lib/hello.cpp)
add_executable(hello_world_tool main.cpp)
target_link_libraries(hello_world_tool PUBLIC hello)

install(TARGETS hello_world_tool hello
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin)

install(FILES include/hello.h DESTINATION include)
