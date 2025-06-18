#include "cli11/CLI.hpp" // <<< FIX THIS LINE (was "lib/cli11/CLI.hpp")
#include "Analysis.h"
#include "Reporter.h"
#include <iostream>
#include <fstream>  // <<< ADD THIS LINE
#include <memory>   // <<< ADD THIS LINE

int main(int argc, char** argv) {
    CLI::App app{"MPI Uniform Participation Analyzer"};

    // --- Define CLI options ---
    std::vector<std::string> input_files;
    std::string output_file;
    bool json_output = false;
    bool csv_output = false;
    bool verbose = false;
    std::string logfile;
    bool strict = false;
    
    app.add_option("-i,--input", input_files, "Input LLVM IR file(s)")->required()->check(CLI::ExistingFile);
    app.add_option("-o,--output", output_file, "Write report to output file");
    app.add_flag("--json", json_output, "Export report in JSON format");
    app.add_flag("--csv", csv_output, "Export report in CSV format");
    app.add_flag("-v,--verbose", verbose, "Enable detailed processing logs");
    app.add_flag("--strict", strict, "Treat warnings (e.g., unmatched calls) as errors");
    app.add_option("--logfile", logfile, "Redirect verbose logs to a file");
    
    // Version flag
    app.add_flag_callback("--version", [](){ 
        std::cout << "mpi-analyser version 2.0" << std::endl; 
        throw CLI::Success{}; 
    }, "Print tool version");

    CLI11_PARSE(app, argc, argv);

    // --- Main Logic ---
    if (verbose) std::cerr << "[VERBOSE] Verbose mode enabled." << std::endl;
    
    MPIAnalysis engine(verbose);
    for (const auto& file : input_files) {
        if (!engine.processFile(file)) {
            std::cerr << "ERROR: Failed to process file: " << file << std::endl;
            return 1;
        }
    }

    engine.runAnalysis();
    const auto& results = engine.getResults();

    // --- Select Reporter ---
    std::unique_ptr<Reporter> reporter;
    if (json_output) {
        reporter = std::make_unique<JsonReporter>();
    } else if (csv_output) {
        reporter = std::make_unique<CsvReporter>();
    } else {
        reporter = std::make_unique<TextReporter>();
    }

    // --- Output Generation ---
    if (!output_file.empty()) {
        std::ofstream outfile(output_file);
        if (!outfile) {
            std::cerr << "ERROR: Could not open output file: " << output_file << std::endl;
            return 1;
        }
        reporter->generateReport(results, outfile);
        std::cout << "Report successfully written to " << output_file << std::endl;
    } else {
        reporter->generateReport(results, std::cout);
    }
    
    // --- Strict Mode ---
    if (strict && (!results.unmatchedSends.empty() || !results.unmatchedReceives.empty())) {
        std::cerr << "STRICT MODE: Unmatched MPI calls detected, exiting with error." << std::endl;
        return 1;
    }

    return 0;
}