# Minimum CMake version required
cmake_minimum_required(VERSION 3.20)

# Define the project
project(MPIPolishedTool VERSION 2.0 LANGUAGES CXX)

# Set the C++ standard to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- CRITICAL FIX 1: Force the build type to Release ---
# This ensures our code is built without debug symbols, matching LLVM.
set(CMAKE_BUILD_TYPE Release)
message(STATUS "Build type set to: ${CMAKE_BUILD_TYPE}")

# --- CRITICAL FIX 2: Match the C Runtime Library with LLVM's ---
# The pre-built LLVM libs use the static CRT (/MT). We must match it.
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded")
message(STATUS "MSVC Runtime Library set to: ${CMAKE_MSVC_RUNTIME_LIBRARY}")

# --- Use llvm-config precisely ---
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

# --- Configure the Project ---
add_executable(mpi-analyser
    src/main.cpp
    src/Analysis.cpp
    src/Reporter.cpp
)

# --- Apply the flags and paths correctly ---
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