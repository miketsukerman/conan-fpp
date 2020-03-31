from conans import ConanFile, CMake, tools
import sys, os

class FppConan(ConanFile):
    name = "fpp"
    version = "1.0.0"
    license = "Apache2"
    author = "Michael Tsukerman <miketsukerman@gmail.com>"
    url = "https://github.com/miketsukerman/fpp"
    description = "Franca plus parser"
    topics = ("franca", "parser", "genivi")
    settings = "os", "compiler", "build_type", "arch"
    requires = "bison/3.3.2@bincrafters/stable", "flex/2.6.4@bincrafters/stable","CLI11/1.8.0@cliutils/stable"
    generators = "cmake"
    options = {
        "enable_testsuite": [True, False],
        "enable_docs": [True, False],
        "enable_python": [True, False],
        "enable_java": [True, False],
        "code_coverage": [True, False],
        "python_version": ["3.5", "3.6", "3.7", "3.8", "auto"]
    }
    default_options = {
        "enable_testsuite": True,
        "enable_docs": False,
        "enable_python": False,
        "enable_java": False,
        "code_coverage": False,
        "python_version": "auto",
        "fmt:header_only" : True,
        "spdlog:header_only" : True
    }
    scm = {
         "type": "git",
         "subfolder": "fpp",
         "url": "https://github.com/miketsukerman/fpp.git",
         "revision": "master"
    }
  
    def config_options(self):
        if self.options.python_version == None or self.options.python_version == "auto":
            self.options.python_version = self.get_current_python_version()

    def requirements(self):
        self.requires("spdlog/[>=1.4.1]",private=True)

        if self.options.enable_java:
            self.requires("jni.hpp/4.0.1")
            self.requires("java_installer/9.0.0@bincrafters/stable")
        if self.options.enable_testsuite:
            self.requires("catch2/2.11.1")
        if self.options.enable_python:
            self.requires("pybind11/2.3.0@conan/stable")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_DOCS"] = self.options.enable_docs
        cmake.definitions["ENABLE_PYTHON_SUPPORT"] = self.options.enable_python
        cmake.definitions["ENABLE_TESTSUITE"] = self.options.enable_testsuite
        cmake.definitions["ENABLE_JAVA_SUPPORT"] = self.options.enable_java
        cmake.definitions["CODE_COVERAGE"] = self.options.code_coverage
        cmake.definitions["ENABLE_TESTSUITE"] = self.options.enable_testsuite

        if self.options.enable_python:
            cmake.definitions["PYTHON_SITE_PACKAGES_DIRECTORY"] = os.path.join(self.package_folder, "lib")
            cmake.definitions["PYBIND11_PYTHON_VERSION"] = self.options.python_version

        cmake.configure(source_folder=self.scm["subfolder"])
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.test()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.name = self.name
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib"))
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)

    def get_current_python_version(self):
        return "{}.{}".format(sys.version_info.major, sys.version_info.minor)