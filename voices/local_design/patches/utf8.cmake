# Preserve Vietnamese text passed via Windows command-line arguments.
# Keep this local build overlay separate from the upstream runtime source.
get_property(_studio_voice_utf8 GLOBAL PROPERTY STUDIO_VOICE_UTF8)
if(WIN32 AND NOT _studio_voice_utf8)
  set_property(GLOBAL PROPERTY STUDIO_VOICE_UTF8 TRUE)
  enable_language(RC)
  cmake_language(DEFER CALL include
    "D:/stickman-animation-studio/stickman-animation-studio/voices/local_design/driver/CMakeLists.txt")
  cmake_language(DEFER CALL target_sources voxcpm2-cli PRIVATE
    "D:/stickman-animation-studio/stickman-animation-studio/voices/local_design/patches/utf8.rc")
  cmake_language(DEFER CALL set_property SOURCE
    "${CMAKE_SOURCE_DIR}/src/llama-moe-slot.cpp" DIRECTORY "${CMAKE_SOURCE_DIR}/src"
    APPEND PROPERTY COMPILE_OPTIONS "-include"
    "D:/stickman-animation-studio/stickman-animation-studio/voices/local_design/patches/windows_iovec.h")
endif()
