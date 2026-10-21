# Mỏ Đen — bộ ảnh đặt tên cho AI / studio

24 PNG riêng, nền trong suốt, 2048 × 2048 px. Hình ảnh giữ nguyên từng byte từ bộ đã giao; chỉ đổi tên và bổ sung mô tả.

## Quy tắc tên

`mo_den_[số]_[biểu_cảm_tiếng_Anh]_[tư_thế_tiếng_Anh].png`

Tên file dùng chữ thường ASCII và dấu gạch dưới để dễ đọc bằng script. `manifest.json` chứa đường dẫn tương đối, nhãn tiếng Việt, biểu cảm, tư thế, mô tả và tình huống sử dụng.

## Câu lệnh đưa cho AI dựng video

> Đọc manifest.json. Với từng cảnh, chọn đúng ảnh Mỏ Đen dựa trên emotion, pose và use_cases_en. Dùng chính xác đường dẫn trong trường file. Không đoán tên file. Giữ cùng vị trí và tỷ lệ toàn khung PNG khi đổi ảnh.

## Danh sách

| Mã | Biểu cảm | File |
|---|---|---|
| mo_den_01 | Bình thường | PNG/mo_den_01_neutral_seated_paws_resting.png |
| mo_den_02 | Vui vẻ | PNG/mo_den_02_happy_seated_greeting.png |
| mo_den_03 | Cười lớn | PNG/mo_den_03_laughing_seated_paw_on_belly.png |
| mo_den_04 | Buồn | PNG/mo_den_04_sad_seated_head_lowered.png |
| mo_den_05 | Tức giận | PNG/mo_den_05_angry_seated_paws_clenched.png |
| mo_den_06 | Sửng sốt | PNG/mo_den_06_shocked_seated_paws_raised.png |
| mo_den_07 | Lo lắng | PNG/mo_den_07_worried_seated_paws_clasped.png |
| mo_den_08 | Láu cá | PNG/mo_den_08_smug_seated_one_paw_shrug.png |
| mo_den_09 | Bối rối | PNG/mo_den_09_confused_seated_scratching_head.png |
| mo_den_10 | Chán ghét | PNG/mo_den_10_disgusted_seated_paw_held_out.png |
| mo_den_11 | Quyết tâm | PNG/mo_den_11_determined_seated_paws_on_hips.png |
| mo_den_12 | Ngại ngùng | PNG/mo_den_12_embarrassed_seated_paws_together.png |
| mo_den_13 | Tò mò | PNG/mo_den_13_curious_seated_paw_near_chin.png |
| mo_den_14 | Hoài nghi | PNG/mo_den_14_skeptical_seated_arms_crossed.png |
| mo_den_15 | Suy nghĩ | PNG/mo_den_15_thinking_seated_chin_rest.png |
| mo_den_16 | Nhận ra | PNG/mo_den_16_realization_seated_paw_raised.png |
| mo_den_17 | Nhẹ nhõm | PNG/mo_den_17_relieved_seated_paw_on_chest.png |
| mo_den_18 | Cười gượng | PNG/mo_den_18_awkward_smile_seated_paw_behind_neck.png |
| mo_den_19 | Sợ hãi | PNG/mo_den_19_scared_seated_paws_near_cheeks.png |
| mo_den_20 | Thất vọng | PNG/mo_den_20_disappointed_seated_paws_lowered.png |
| mo_den_21 | Bất lực | PNG/mo_den_21_helpless_seated_both_paws_shrug.png |
| mo_den_22 | Buồn ngủ | PNG/mo_den_22_sleepy_seated_yawning.png |
| mo_den_23 | Tự hào | PNG/mo_den_23_proud_seated_paws_on_hips.png |
| mo_den_24 | Giải thích | PNG/mo_den_24_explaining_seated_open_paw_gesture.png |

## Lưu ý

Ảnh là tư thế tĩnh, chưa tách lớp hoặc gắn chuyển động. File JSON giúp AI tra cứu; studio chỉ tự động sử dụng nếu có chức năng đọc manifest hoặc bước chọn tài nguyên tương ứng.

Bản giao 2048 px được chuẩn hóa từ ảnh sinh gốc 1254 px. Không thay đổi chất lượng hoặc màu sắc so với bộ ZIP trước.
