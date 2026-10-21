// Local persistent batch wrapper; synthesis uses the upstream public clone API.
#define main upstream_cli_main
#include "voxcpm2_cli.cpp"
#undef main
#include "nlohmann/json.hpp"
#include <filesystem>
#include <iostream>

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("Expected one JSON job path");
        std::ifstream input(argv[1]);
        nlohmann::json job; input >> job;
        VoxCPM2Runtime runtime;
        if (!runtime.init(job.at("base_lm"), job.at("acoustic"),
                          job.value("gpu_layers", -1), job.value("gpu", false)))
            throw std::runtime_error(runtime.last_error());
        runtime.set_n_threads(job.value("threads", 6));
        int ref_rate = 0;
        auto ref = load_wav_mono(job.at("reference"), ref_rate);
        if (ref.empty()) throw std::runtime_error("Empty reference");
        for (const auto& unit : job.at("units")) {
            std::string output = unit.at("output");
            if (std::filesystem::exists(output)) {
                std::cout << "CACHED " << unit.at("id") << std::endl;
                continue;
            }
            VoxCPM2GenerateParams params;
            params.max_steps = job.value("max_steps", 350);
            params.inference_timesteps = 10;
            params.cfg_value = 2.0f;
            params.temperature = 1.0f;
            params.seed = unit.value("seed", 284617);
            params.reference_sample_rate = ref_rate;
            auto begin = std::chrono::steady_clock::now();
            std::cout << "START " << unit.at("id") << std::endl;
            auto pcm = runtime.generate_with_clone(unit.at("text"), ref, params);
            if (pcm.empty() || !runtime.last_error().empty()) throw std::runtime_error(runtime.last_error());
            float peak = 0;
            for (float value : pcm) {
                if (!std::isfinite(value)) throw std::runtime_error("Nonfinite PCM");
                peak = std::max(peak, std::abs(value));
            }
            if (peak >= 1.0f) throw std::runtime_error("Raw PCM would clip");
            auto temporary = output + ".partial.wav";
            write_wav(temporary, pcm, params.target_sr);
            if (!std::filesystem::exists(temporary)) throw std::runtime_error("WAV write failed");
            std::filesystem::rename(temporary, output);
            double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
            nlohmann::json result = {{"id",unit.at("id")},{"seconds",double(pcm.size())/params.target_sr},
                                     {"elapsed_seconds",elapsed},{"peak",peak},{"seed",params.seed},
                                     {"text",unit.at("text")},{"complete",true}};
            {
                std::ofstream receipt(output+".partial.json");
                receipt << result.dump(2);
                receipt.flush();
                if (!receipt) throw std::runtime_error("Receipt write failed");
            }
            std::filesystem::rename(output+".partial.json",output+".json");
            std::cout << "DONE " << result.dump() << std::endl;
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "BATCH_ERROR " << error.what() << std::endl;
        return 1;
    }
}
