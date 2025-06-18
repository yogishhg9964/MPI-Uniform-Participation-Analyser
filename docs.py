from fpdf import FPDF

# ----------------- PDF Class Setup with Advanced Formatting -----------------
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'MPI Analyser: User & Development Guide', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, label, 0, 1, 'L', 1)
        self.ln(4)
        
    def sub_chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 7, label, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, text_content):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, text_content)
        self.ln()

    def code_block(self, code_content, lang=''):
        if lang:
            self.set_font('Courier', 'I', 9)
            self.cell(0, 5, f"({lang})", 0, 1, 'L')
        
        self.set_font('Courier', '', 9)
        self.set_fill_color(230, 230, 230)
        self.multi_cell(0, 4.5, code_content.strip(), border=1, fill=1)
        self.ln()

# ----------------- ALL CONTENT DEFINITIONS (DEFINED FIRST) -----------------

introduction = """
Welcome to the MPI Analyser, a standalone command-line tool designed to perform static analysis on MPI-based C/C++ programs. By parsing LLVM Intermediate Representation (IR), this tool detects MPI communication patterns, identifies matching Send/Recv pairs, and warns about potential deadlocks caused by unmatched calls.

This guide provides instructions for both end-users who want to run the tool and developers who want to build it from source.
"""

features = """
- Rich Command-Line Interface: Professional CLI options for specifying inputs, outputs, formats, and behavior.
- Multiple Output Formats: Generate human-readable text reports for the terminal, or machine-readable JSON and CSV formats for integration with other tools.
- Efficient Analysis Engine: Uses modern C++ and hash maps to efficiently group and match MPI operations by communicator and tag.
- Robust Error Handling: Provides clear warnings for unmatched calls and supports a `--strict` mode to treat these warnings as fatal errors.
- Verbose Logging: A `--verbose` mode provides detailed insight into the tool's parsing and analysis steps.
- Cross-Platform Build System: Uses CMake and Ninja to enable building the tool on Windows, Linux, and macOS.
"""

how_to_use = """
The tool is designed to be run from the command line. The primary input is one or more LLVM IR files (`.ll`).

**Command Syntax:**
`mpi-analyser.exe [OPTIONS] --input <file1.ll> [<file2.ll> ...]`

**Command-Line Options:**
  `-i, --input <file>`: (Required) One or more input LLVM IR files.
  `-o, --output <file>`: Write the report to a specified output file instead of the console.
  `--json`: Format the report as JSON.
  `--csv`: Format the report as CSV.
  `-v, --verbose`: Enable detailed processing and debugging logs.
  `--strict`: Treat any unmatched MPI calls as a fatal error and exit with an error code.
  `--version`: Print the tool's version information and exit.
  `--help`: Display the full list of commands and options.

**Example Usage:**

1. Basic analysis of a single file, printing to the console:
"""
example1 = "D:\\...\\build> ./Debug/mpi-analyser.exe --input ../test-build/uniform_comm.ll"
example2_text = "\n2. Analyzing multiple files and saving the report as a JSON file:"
example2 = "D:\\...\\build> ./Debug/mpi-analyser.exe --input ../test-build/uniform.ll ../test-build/mismatched.ll --json -o report.json"
example3_text = "\n3. Running in verbose and strict mode:"
example3 = "D:\\...\\build> ./Debug/mpi-analyser.exe --input ../test-build/mismatched_tag.ll --verbose --strict"

how_to_build_intro = """
To compile the MPI Analyser from source, you need a specific set of tools and a correctly structured project directory. This guide assumes the project is located at `D:\\MPI-polished-tool` and its dependencies are at `D:\\CompilerDesign-MPI-Analysis`."""

build_prerequisites = """
- **LLVM + Clang Development Kit:** The `.tar.xz` archive, not the `.exe` installer.
- **Microsoft C++ (MSVC) Build Tools:** With the "Desktop development with C++" workload installed.
- **Microsoft MPI SDK:** The `.msi` file, which contains the required `mpi.h`.
- **CMake (Version 3.20+):** The official version from kitware.com.
- **Ninja Build System:** A fast, modern build tool.
"""

build_steps = """
All commands should be run from a PowerShell terminal.

**1. Generate Test IR Files (One-Time Setup):**
   First, compile the C test files into the LLVM IR that the tool analyzes.
"""
build_command1 = """# Run from the project root (e.g., D:\\MPI-polished-tool)
mkdir test-build
D:/CompilerDesign-MPI-Analysis/LLVM/bin/clang -S -emit-llvm tests/uniform_comm.c -o test-build/uniform_comm.ll -I"D:/CompilerDesign-MPI-Analysis/MPI/Include"
"""
build_command2_text = """
**2. Configure and Build the Tool:**
   This two-step process uses CMake to prepare the build files and Ninja to compile the code.
"""
build_command2 = """# Run from the project root
mkdir build
cd build
cmake -G "Ninja" -DCMAKE_C_COMPILER="D:/CompilerDesign-MPI-Analysis/LLVM/bin/clang.exe" -DCMAKE_CXX_COMPILER="D:/CompilerDesign-MPI-Analysis/LLVM/bin/clang++.exe" ..
ninja
"""

development_journey = """... (Content from previous versions) ...""" # Placeholder for brevity

architecture = """... (Content from previous versions) ...""" # Placeholder for brevity

final_cmake_code = """
# Minimum CMake version required
cmake_minimum_required(VERSION 3.20)

# Define the project
project(MPIPolishedTool VERSION 2.0 LANGUAGES CXX)

# Set the C++ standard to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# CRITICAL FIX 1: Force the build type to Release
set(CMAKE_BUILD_TYPE Release)
message(STATUS "Build type set to: ${CMAKE_BUILD_TYPE}")

# CRITICAL FIX 2: Match the C Runtime Library with LLVM's
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded")
message(STATUS "MSVC Runtime Library set to: ${CMAKE_MSVC_RUNTIME_LIBRARY}")

# Use llvm-config precisely
set(LLVM_CONFIG_EXECUTABLE "D:/CompilerDesign-MPI-Analysis/LLVM/bin/llvm-config.exe")

# Get ONLY the library names (as a string)
execute_process(
    COMMAND ${LLVM_CONFIG_EXECUTABLE} --libs core irreader support asmparser bitreader bitstreamreader remarks binaryformat targetparser demangle --system-libs
    OUTPUT_VARIABLE LLVM_LIBS_STR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Remove the problematic libxml2s.lib
string(REPLACE "libxml2s.lib" "" LLVM_LIBS_STR_CLEAN "${LLVM_LIBS_STR}")
separate_arguments(LLVM_LIBS_LIST NATIVE_COMMAND "${LLVM_LIBS_STR_CLEAN}")

# Configure the Project
add_executable(mpi-analyser
    src/main.cpp
    src/Analysis.cpp
    src/Reporter.cpp
)

# Apply the flags and paths correctly
execute_process(COMMAND ${LLVM_CONFIG_EXECUTABLE} --includedir OUTPUT_VARIABLE LLVM_INCLUDE_DIR OUTPUT_STRIP_TRAILING_WHITESPACE)
target_include_directories(mpi-analyser PRIVATE 
    "${CMAKE_CURRENT_SOURCE_DIR}/lib"
    "${LLVM_INCLUDE_DIR}"
    "D:/CompilerDesign-MPI-Analysis/MPI/Include"
)

execute_process(COMMAND ${LLVM_CONFIG_EXECUTABLE} --libdir OUTPUT_VARIABLE LLVM_LIB_DIR OUTPUT_STRIP_TRAILING_WHITESPACE)
target_link_directories(mpi-analyser PRIVATE 
    "${LLVM_LIB_DIR}"
)

target_link_libraries(mpi-analyser PRIVATE 
    ${LLVM_LIBS_LIST}
)

message(STATUS "Successfully configured MPI Polished Tool")
"""

# ----------------- PDF GENERATION LOGIC -----------------
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# --- Section 1: Introduction ---
pdf.chapter_title('1. Introduction')
pdf.chapter_body(introduction)
pdf.sub_chapter_title('Key Features')
pdf.chapter_body(features)

# --- Section 2: User Guide ---
pdf.add_page()
pdf.chapter_title('2. How to Use the Tool (User Guide)')
pdf.chapter_body(how_to_use)
pdf.code_block(example1, lang='PowerShell')
pdf.chapter_body(example2_text)
pdf.code_block(example2, lang='PowerShell')
pdf.chapter_body(example3_text)
pdf.code_block(example3, lang='PowerShell')

# --- Section 3: Developer Guide ---
pdf.add_page()
pdf.chapter_title('3. How to Build From Source (Developer Guide)')
pdf.chapter_body(how_to_build_intro)
pdf.sub_chapter_title('Prerequisites')
pdf.chapter_body(build_prerequisites)
pdf.sub_chapter_title('Build Steps')
pdf.chapter_body(build_steps)
pdf.code_block(build_command1, lang='PowerShell')
pdf.chapter_body(build_command2_text)
pdf.code_block(build_command2, lang='PowerShell')

# --- Section 4: Project History (Challenges) ---
# Note: Re-using the full text from the previous version for this script to be self-contained
challenges_and_solutions = """
We faced a series of classic and complex setup issues. Here is a summary of each problem and its solution.

- Challenge 1: `command not found` for compilers.
  - Solution: Manually add the path to LLVM's `bin` directory to the system PATH.

- Challenge 2: Hardcoded Paths in `llvm-config`.
  - Solution: Extract the LLVM archive directly to its final destination instead of moving it after extraction.

- Challenge 3: `'mpi.h' file not found`.
  - Solution: Install the MS-MPI SDK and use the `-I` flag to provide the include path to the compiler.

- Challenge 4: Compiler Errors related to C++17 features.
  - Solution: Add the `-std=c++17` flag to the compiler command.

- Challenge 5: Linker Errors (`unresolved external symbol`).
  - Solution: A "dependency chase." We had to add linker flags (`-l...`) for every missing LLVM and system library.

- Challenge 6: CMake using MSVC instead of Clang on Windows.
  - Solution: Use the `-G "Ninja"` generator flag and explicitly set `CMAKE_CXX_COMPILER` to force CMake to use Clang.

- Challenge 7: Linker errors due to C Runtime Mismatches (`_ITERATOR_DEBUG_LEVEL`, `RuntimeLibrary`).
  - Solution: Explicitly set `CMAKE_BUILD_TYPE` to `Release` and `CMAKE_MSVC_RUNTIME_LIBRARY` to `MultiThreaded` to match the pre-built LLVM libraries.
"""
pdf.add_page()
pdf.chapter_title('4. The Development Journey (Project History)')
pdf.chapter_body(challenges_and_solutions)

# --- Appendix: Source Code ---
pdf.add_page()
pdf.chapter_title('Appendix A: Final CMakeLists.txt')
pdf.code_block(final_cmake_code, lang='CMake')

# --- Save PDF ---
pdf_file_path = "MPI_Analyser_Guide.pdf"
pdf.output(pdf_file_path)

print(f"Success! The guide has been created: {pdf_file_path}")