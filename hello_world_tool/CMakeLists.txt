# version 3.12 is not necessary
# it's just for testing the container
cmake_minimum_required(VERSION 3.12)

project(hello_world_tool)

include_directories(include/)

add_library(hello SHARED lib/hello.cpp)
add_executable(hello_world_tool main.cpp)
target_link_libraries(hello_world_tool PUBLIC hello)

install(TARGETS hello_world_tool hello
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin)

install(FILES include/hello.h DESTINATION include)
