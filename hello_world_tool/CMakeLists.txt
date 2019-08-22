cmake_minimum_required(VERSION 3.4.3)

project(hello_world_tool)

include_directories(include/)

add_library(hello SHARED lib/hello.cpp)
add_executable(hello_world_tool main.cpp)
target_link_libraries(hello_world_tool hello)

install(TARGETS hello_world_tool RUNTIME DESTINATION bin)
install(TARGETS hello DESTINATION lib)
install(FILES include/hello.h DESTINATION include)
