cmake_minimum_required(VERSION 3.5)
project(linux)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
        line.cpp
        )

include_directories(
        /usr/local/Cellar/gsl/2.2.1/include
)
link_libraries(
        /usr/local/Cellar/gsl/2.2.1/lib/libgsl.a
)


add_executable(line ${SOURCE_FILES})