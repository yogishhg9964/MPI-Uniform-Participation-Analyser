# MPI Uniform Participation Analyzer

![Language](https://img.shields.io/badge/Language-C%2B%2B17-blue.svg)
![Build](https://img.shields.io/badge/Build-CMake-orange.svg)
![Framework](https://img.shields.io/badge/Framework-LLVM-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

A **professional, standalone command-line tool** for performing static analysis on MPI-based C/C++ programs.  
It parses LLVM Intermediate Representation (IR) to detect communication patterns, identify matching `MPI_Send`/`MPI_Recv` pairs, and report on **uniform participation** across MPI processes.

---

## ✨ Features

- **Professional CLI**: Rich command-line options for input, output, verbosity, and format, powered by [CLI11](https://github.com/CLIUtils/CLI11).
- **Multiple Output Formats**: Human-readable (plain text) and machine-readable formats like JSON or CSV.
- **Robust Analysis**: Groups and matches MPI calls by communicator and tag. Detects complete pairs and unmatched sends/receives.
- **Flexible Input**: Accepts one or more LLVM IR files in a single run.
- **Extensible Architecture**: Clean separation between CLI parsing, analysis, and reporting logic.
- **Modern Build System**: Cross-platform build powered by CMake and Ninja.

---

## 📁 Project Structure

```
MPI-polished-tool/
│
├— build/                # CMake build output (not in repo)
├— external/             # External dependencies (not in repo)
│   ├— LLVM/             # LLVM + Clang toolchain
│   └— MPI/              # Microsoft MPI headers and libs
│
├— lib/
│   └— cli11/            # CLI11 single-header library
│       └— CLI.hpp
│
├— src/
│   ├— main.cpp          # CLI parsing + main logic
│   ├— Analysis.h/.cpp   # Core analysis engine
│   ├— Reporter.h/.cpp   # Report formatting + output
│   └— Data.h            # Common data structures
│
├— tests/
│   ├— uniform_comm.c    # Uniform MPI communication test
│   └— mismatched_tag.c  # Mismatched tag test
│
├— CMakeLists.txt        # Modern, LLVM-integrated CMake build
└— README.md             # You're reading it!
```

---

## ⚙️ Prerequisites

Make sure the following are installed (on **Windows**):

- **Microsoft Build Tools** (MSVC)  
  Install via *Build Tools for Visual Studio* → "Desktop development with C++" workload  
- **CMake** (>= v3.15)  
  Install: `winget install -e --id Kitware.CMake`
- **Ninja**  
  Install: `winget install -e --id Ninja-build.Ninja`
- **Git**  
  Install from [https://git-scm.com](https://git-scm.com)

---

## 🧰 Setup and Build Instructions

### 1. Clone the Repository

```powershell
git clone https://github.com/yogishhg9964/MPI-Uniform-Participation-Analyser MPI-polished-tool
cd MPI-polished-tool
```

---

### 2. Download and Place Dependencies

#### Create the external directory:

```powershell
mkdir external
```

#### LLVM + Clang:

- Download the `.tar.xz` archive from [LLVM Releases](https://github.com/llvm/llvm-project/releases)
- Extract using 7-Zip, **rename** folder to `LLVM`
- Place it under: `./external/LLVM/`

#### Microsoft MPI:

- Copy from `C:\Program Files\Microsoft MPI\` to `./external/`
- Rename folder to `MPI`

Final Paths:
```
./external/LLVM/bin/
./external/MPI/Include/
```

---

### 3. Generate Test LLVM IR Files

```powershell
mkdir tests/build

# Compile to IR
./external/LLVM/bin/clang -S -emit-llvm tests/uniform_comm.c -o tests/build/uniform_comm.ll -I"./external/MPI/Include"
```

---

### 4. Configure and Build

#### Configure:

```powershell
cmake -G "Ninja" `
  -DCMAKE_C_COMPILER="./external/LLVM/bin/clang.exe" `
  -DCMAKE_CXX_COMPILER="./external/LLVM/bin/clang++.exe" `
  -B build
```

#### Build:

```powershell
cmake --build build
```

✅ If successful, the `mpi-analyser.exe` will be created in `./build/`.

---

## 🚀 Usage

### Help Menu

```powershell
./build/mpi-analyser.exe --help
```

### Basic Run

```powershell
./build/mpi-analyser.exe --input tests/build/uniform_comm.ll
```

### Verbose + JSON Output

```powershell
./build/mpi-analyser.exe `
  --input tests/build/uniform_comm.ll `
  --verbose `
  --json `
  --output report.json
```

---

## ✅ Final `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.15)
project(MPIPolishedTool VERSION 2.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(LLVM_CONFIG_EXECUTABLE "${CMAKE_CURRENT_SOURCE_DIR}/external/LLVM/bin/llvm-config.exe")

execute_process(COMMAND ${LLVM_CONFIG_EXECUTABLE} --ldflags OUTPUT_VARIABLE LLVM_LDFLAGS_STR OUTPUT_STRIP_TRAILING_WHITESPACE)
execute_process(COMMAND ${LLVM_CONFIG_EXECUTABLE} --libs core irreader support asmparser bitreader bitstreamreader remarks binaryformat targetparser demangle --system-libs OUTPUT_VARIABLE LLVM_LIBS_STR OUTPUT_STRIP_TRAILING_WHITESPACE)

separate_arguments(LLVM_LDFLAGS_LIST NATIVE_COMMAND "${LLVM_LDFLAGS_STR}")
separate_arguments(LLVM_LIBS_LIST NATIVE_COMMAND "${LLVM_LIBS_STR}")

add_executable(mpi-analyser
    src/main.cpp
    src/Analysis.cpp
    src/Reporter.cpp
)

target_include_directories(mpi-analyser PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/lib"
    "${CMAKE_CURRENT_SOURCE_DIR}/external/LLVM/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/external/MPI/Include"
)

target_link_options(mpi-analyser PRIVATE ${LLVM_LDFLAGS_LIST})
target_link_libraries(mpi-analyser PRIVATE ${LLVM_LIBS_LIST})

message(STATUS "Successfully configured MPI Polished Tool using llvm-config")
```


## 🙏 Acknowledgments

- [LLVM Project](https://llvm.org) – for their powerful compiler infrastructure.
- [CLI11](https://github.com/CLIUtils/CLI11) – for simplifying modern C++ CLI development.

---

💡 *Build once. Analyze everywhere.*
