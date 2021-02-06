cmake_minimum_required(VERSION 3.13)
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
project(@{PACKAGE_NAME})

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  # include
  # OTHER_LOCATIONS_TO_INCLUDE ...
)

# Declare a C++ executable
add_executable(${PROJECT_NAME}
  src/@{PACKAGE_NAME}_main.c
  # OTHER_SOURCE_FILES_TO_COMPILE ...
)
# Specify libraries to link a library or executable target against
target_link_libraries(${PROJECT_NAME}
  pico_stdlib
  # OTHER_LIBRARIES_TO_LINK ...
)

# create map/bin/hex/uf2 file in addition to ELF.
pico_add_extra_outputs(${PROJECT_NAME})
