#define CATCH_CONFIG_MAIN // This tells Catch to provide a main() - only do this in one cpp file
#include <iostream>

#include <catch2/catch.hpp>

#include <parser/SourceFileManager.h>
#include <parser/ASTConstructor.h>

using namespace fpp::parser;

TEST_CASE("Example test for conan package", "")
{
    constexpr auto inputFileName = "example.fidl";

    auto sourceFilesManager = std::make_shared<SourceFileManager>();
    sourceFilesManager->addInputFile(inputFileName);
    ASTConstructor abstractSyntaxTree(sourceFilesManager);

    abstractSyntaxTree.build();
    auto parseErrors = abstractSyntaxTree.errors();

    REQUIRE(parseErrors.size() == 0);
}
