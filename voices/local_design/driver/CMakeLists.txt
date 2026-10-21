find_package(Threads REQUIRED)
# Upstream reserves 32768 tokens for every short TTS request. Each Maya request
# has < 350 output patches + reference/text, so 2048 keeps headroom without a
# multi-gigabyte unused KV cache. Preserve upstream source; compile an overlay.
file(READ "${CMAKE_SOURCE_DIR}/tools/omni/voxcpm2/voxcpm2_llm.cpp" _studio_llm)
string(REPLACE "cparams_local.n_ctx       = 32768;" "cparams_local.n_ctx       = 2048;" _studio_llm "${_studio_llm}")
file(WRITE "${CMAKE_BINARY_DIR}/studio_voxcpm2_llm.cpp" "${_studio_llm}")
set_property(TARGET voxcpm2_llm PROPERTY SOURCES
  "${CMAKE_BINARY_DIR}/studio_voxcpm2_llm.cpp")
file(READ "${CMAKE_SOURCE_DIR}/tools/omni/voxcpm2/voxcpm2_runtime.cpp" _studio_runtime)
string(REPLACE "config.max_length     = 32768;" "config.max_length     = 2048;" _studio_runtime "${_studio_runtime}")
file(READ "${CMAKE_CURRENT_LIST_DIR}/../patches/reference_prefill_cached.cpp.txt" _studio_cached_prefill)
set(_studio_original_prefill "    if (has_feat) {\n        std::vector<float> loc_hidden = run_locenc_sequence(inputs.audio_feat, seq_len);\n        if (loc_hidden.empty()) {\n            return fail(\"LocEnc sequence forward failed\");\n        }\n        feat_embed = run_enc_to_lm(loc_hidden, seq_len);\n        if (feat_embed.empty()) {\n            return fail(\"enc_to_lm projection failed\");\n        }\n\n        for (int i = 0; i < seq_len; ++i) {\n")
string(FIND "${_studio_runtime}" "${_studio_original_prefill}" _studio_match)
if(_studio_match EQUAL -1)
  message(FATAL_ERROR "Upstream reference prefill changed; inspect before applying overlay")
endif()
string(REPLACE "${_studio_original_prefill}" "${_studio_cached_prefill}" _studio_runtime "${_studio_runtime}")
# The same PCM reference is encoded for every sentence by the clone API.
# Reuse the exact returned feature vector for this single-model batch only.
string(REPLACE
  "    const int          actual_sample_rate = sample_rate > 0 ? sample_rate : audio_vae.config.sample_rate;"
  "    static thread_local const VoxCPM2Runtime* studio_encoder_owner = nullptr;\n    static thread_local int studio_encoder_rate = 0;\n    static thread_local std::vector<float> studio_encoder_pcm, studio_encoder_features;\n    const bool studio_encoder_cache = std::getenv(\"STUDIO_SINGLE_REFERENCE_CACHE\") != nullptr;\n    if (studio_encoder_cache && studio_encoder_owner == this && studio_encoder_rate == sample_rate && studio_encoder_pcm == reference_wav) return studio_encoder_features;\n    const int          actual_sample_rate = sample_rate > 0 ? sample_rate : audio_vae.config.sample_rate;"
  _studio_runtime "${_studio_runtime}")
string(REPLACE
  "    auto result = tensor_to_vector(patch_major);\n    ggml_gallocr_free(galloc);\n    return result;"
  "    auto result = tensor_to_vector(patch_major);\n    ggml_gallocr_free(galloc);\n    if (studio_encoder_cache) { studio_encoder_owner = this; studio_encoder_rate = sample_rate; studio_encoder_pcm = reference_wav; studio_encoder_features = result; }\n    return result;"
  _studio_runtime "${_studio_runtime}")
file(WRITE "${CMAKE_BINARY_DIR}/studio_voxcpm2_runtime.cpp" "${_studio_runtime}")
set_property(TARGET voxcpm2_runtime PROPERTY SOURCES
  "${CMAKE_BINARY_DIR}/studio_voxcpm2_runtime.cpp")
if(TARGET ggml-vulkan)
  target_include_directories(ggml-vulkan PRIVATE
    "${CMAKE_CURRENT_LIST_DIR}/../vendor/vulkan/SPIRV-Headers/include")
endif()
add_executable(studio-voice-batch "${CMAKE_CURRENT_LIST_DIR}/batch.cpp" "${CMAKE_CURRENT_LIST_DIR}/../patches/utf8.rc")
target_include_directories(studio-voice-batch PRIVATE
  "${CMAKE_SOURCE_DIR}/tools/omni/voxcpm2" "${CMAKE_SOURCE_DIR}/vendor")
target_link_libraries(studio-voice-batch PRIVATE voxcpm2_runtime llama-common ggml Threads::Threads)
target_compile_features(studio-voice-batch PRIVATE cxx_std_17)
