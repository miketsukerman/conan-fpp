import os

from conans import ConanFile, CMake, RunEnvironment, tools


class FppTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "virtualrunenv"
    requires = "fpp/1.0.0"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            inputFile="{}/example.fidl".format(os.getcwd())
            os.chdir("bin")
            self.run(".{}example -i {} -g test -o test".format(os.sep,inputFile), run_environment=True)
