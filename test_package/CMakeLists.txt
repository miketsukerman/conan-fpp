cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
conan_define_targets()

include(CTest)
include(Catch)

find_package(
  Boost REQUIRED
  COMPONENTS program_options filesystem system log log_setup
  REQUIRED)
find_package(Threads)

find_package(fpg REQUIRED)
find_package(fp REQUIRED)

set(TARGET example)
add_executable(${TARGET} example.cpp)

set(deps
    fp::fp
    fpg::fpg
    CONAN_PKG::catch2
    Boost::program_options
    Boost::filesystem
    Boost::system
    Boost::log
    Boost::log_setup)

target_link_libraries(example ${deps})

catch_discover_tests(${TARGET})
