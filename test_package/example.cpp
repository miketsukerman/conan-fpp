#include <iostream>

#include "parser/CommandLineParser.h"

using namespace fpp;

int main(int argc, char** argv)
{
    parser::CommandLineParser parser("Franca+ IDL parser");

    try {
        parser.parse(argc, argv);

        parser.addGenerator("test", [](std::string outputFile, const fpp::ast::types::NodePtr& ast ) {
            std::cout << "test" << std::endl;
        });

        parser.process();

    } catch (const CLI::ParseError &e) {
        parser.exit(e);
    }

    return 0;
}
