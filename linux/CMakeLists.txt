cmake_minimum_required(VERSION 3.5)
project(linux)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    concatenate.cpp
    line.cpp
    normalize.cpp
    reconstruct.cpp
    train_youtube.sh)

add_executable(linux ${SOURCE_FILES})