project(AnalysisTools)
cmake_minimum_required(VERSION 3.0)

set(AnalysisTools_DIR "${PROJECT_SOURCE_DIR}")
include("${AnalysisTools_DIR}/cmake/include/common.cmake")

file(GLOB SRM_TOOLS_LIST "Run/srm_tools/*")
add_library(AnalysisTools OBJECT ${HEADER_LIST} ${SOURCE_LIST} ${EXE_SOURCE_LIST} ${SCRIPT_LIST} ${CONFIG_LIST} ${SRM_TOOLS_LIST})
set_target_properties(AnalysisTools PROPERTIES EXCLUDE_FROM_ALL 1)
