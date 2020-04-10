cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(EXISTS ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
    conan_define_targets()
else()
    message(WARNING "The file conanbuildinfo.cmake doesn't exist, you have to run conan install first")
endif()

find_package(Threads)

find_package(CLI11 REQUIRED)
find_package(fpg REQUIRED)
find_package(fp REQUIRED)

set(TARGET example)
add_executable(${TARGET} example.cpp)

target_link_libraries(example fp::fp)

configure_file(example.fidl ${CMAKE_BINARY_DIR}/example.fidl)