# Phòng lỗi nội dung ngay từ nền tảng

Phiên bản 2.0 về chính sách — 14/10/2026.

Tài liệu này chuyển 50 rủi ro đã rà soát thành yêu cầu phòng ngừa cho bộ bàn giao. Chính sách mới của người dùng ưu tiên chuẩn bị trước, hạn chế vòng AI tự đánh giá và tạo lại. Vì vậy, những đề xuất trước đây về hai vòng tự sửa, A/B hoặc kiểm tra từng cảnh bằng agent **không còn là mặc định**.

## 1. Chính sách áp dụng

- Phân tích nội dung nằm trong lượt lập kế hoạch cần thiết, không tạo thêm một agent đánh giá riêng.
- Công cụ local kiểm tra schema, references, thời gian, dữ liệu và trạng thái.
- Sau tạo, file decode/kích thước/alpha có thể được kiểm tra local; kiểm tra kỹ thuật không chứng minh hình đúng ý.
- 0 lần tự tạo lại vì chất lượng; không gán điểm “hay” rồi tự sinh lại.
- Lỗi có bằng chứng được ghi theo object/time range. Sửa đúng phần; không làm lại toàn bài.
- Vấn đề ngữ nghĩa chưa chắc được hỏi/đánh dấu tại đúng đoạn; không bắt mọi cảnh qua xác nhận.
- Gu nghệ thuật được lưu theo phạm vi và ví dụ cụ thể, không quy thành công thức cứng cho mọi video.

Mức lỗi: **P0** sai ý/dữ kiện cốt lõi/phiên bản, **P1** khó hiểu/hỏng nhịp/hành động, **P2** chi tiết sở thích. P0 chặn “sẵn sàng đăng”, vẫn cho nháp có trạng thái rõ. Không lấy điểm tổng để che lỗi P0. Hệ thống không tự xuất bản.

## 2. Danh mục và biện pháp

| ID | Rủi ro | Phòng ngừa trước thực hiện | Khi có bằng chứng lỗi |
|---|---|---|---|
| R01 | SRT/audio mâu thuẫn | Audio revision + transcript diff gắn thời gian | Xác định đúng đoạn; không tin ASR hơn bản gốc mặc định |
| R02 | Mất phủ định/điều kiện | Giữ raw text, đánh dấu từ đổi nghĩa trong brief | Patch chữ/hình liên quan; không tự viết lại lời |
| R03 | Nhầm chủ thể/đại từ | Entity IDs và quan hệ người nói–đối tượng | Đổi đúng entity/asset trong scene |
| R04 | Hiểu ẩn dụ theo nghĩa đen | Ghi intended meaning trong brief | Sửa chiến lược minh họa trước sinh thêm ảnh |
| R05 | Sai số, đơn vị, thời kỳ | Dữ liệu số chuẩn hóa, chữ dựng thật | Sửa cùng nguồn dữ liệu và dependencies |
| R06 | ASR sai tên riêng | Từ điển tên/biến thể; lưu lời gốc | Chỉ yêu cầu xác nhận vị trí mơ hồ |
| R07 | Tự thêm dữ kiện | Quyền sửa narration rõ; claim registry | Tách đề xuất sửa nghĩa khỏi sửa trình bày |
| R08 | Kịch bản/giọng gốc yếu | Nhận xét ngay trong bước kế hoạch | Nêu giới hạn hoặc đề xuất đoạn cụ thể, không che bằng hiệu ứng |
| R09 | Nguồn không hỗ trợ claim | Lưu nguồn và phạm vi phát biểu được hỗ trợ | Đánh dấu chưa xác minh, không tạo nguồn giả |
| R10 | Giả thuyết thành sự thật | certainty_type trong claim và brief | Sửa biểu đạt ở hình/chữ/nhạc liên quan |
| R11 | Hình bịa thêm chi tiết | exact_details/forbidden_details + loại minh họa | Thay chi tiết sai; nhãn tái dựng không hợp thức hóa sai lệch |
| R12 | Sai người/nơi/thời kỳ | Provenance và subject/period metadata | Thay đúng asset, giữ motion nếu còn phù hợp |
| R13 | Bản đồ/biểu đồ sai | Dựng từ dữ liệu; không diffusion chữ/số | Sửa nguồn dữ liệu, tái render span liên quan |
| R14 | Hình nối ngụ ý nhân quả sai | Ghi quan hệ thời gian/nhân quả trong outline | Sửa thứ tự hoặc thêm ngữ cảnh có căn cứ |
| R15 | Crop hoặc biểu tượng mất ngữ cảnh | Giữ bản đầy đủ, crop metadata và tone notes | Mở crop/thay minh họa cụ thể |
| R16 | Mở đầu hứa mà không trả lời | opening_promise gắn payoff | Sửa outline trước tạo; sửa lời chỉ theo quyền |
| R17 | Tiết lộ sớm | reveal_rules gắn anchor, kể cả text/SFX | Dời đúng event; không cần đổi asset nếu vẫn dùng được |
| R18 | Cảnh rời rạc | Outline toàn bài và mục đích đoạn nối | Sửa scene brief/transition liên quan |
| R19 | Thời gian/hồi tưởng rối | Timeline sự kiện riêng với timeline kể | Thêm mốc có căn cứ, sửa thứ tự trình bày |
| R20 | Ý phụ lấn trọng tâm | Phân cấp main/support/example | Điều chỉnh thời lượng/độ nhấn trong plan |
| R21 | Nhịp cắt máy móc | Chia theo ý và hành động, không theo cue cố định | Dữ liệu lặp chỉ là gợi ý; không tự phá nhịp có chủ ý |
| R22 | Cảm xúc cao liên tục | Emotional intent và khoảng nghỉ theo đoạn | Giảm nhấn tại đoạn cụ thể |
| R23 | Hài/nhạc/biểu cảm sai tông | tone_limits theo nội dung | Thay đúng phản ứng/âm thanh |
| R24 | Kết thúc hụt hoặc quá lời | Danh sách câu hỏi đang mở và bằng chứng kết luận | Để rõ điều chưa biết, không tự bịa câu trả lời |
| R25 | Hình chỉ khớp từ khóa | Vai trò hình và điều người xem cần hiểu | Thay ý tưởng trước khi gọi model |
| R26 | Chỉ zoom ảnh thay hành động | action contract và capability check | Bổ sung đúng rig/pose hoặc đổi cách giải thích minh bạch |
| R27 | Nhân vật lệch nhận diện | Character kit/style revision và references | Thay part/pose lệch, không sinh lại nhân vật mọi scene |
| R28 | Phong cách trộn vô cớ | Style profile, quy tắc khung tư liệu | Điều chỉnh asset/bố cục, giữ khác biệt có chủ đích |
| R29 | Tay rời đạo cụ/xuyên hình | Attachments/pivots/z-order/prerequisites | Sửa rig hoặc keyframe cụ thể |
| R30 | Chỉ/nhìn/phản ứng sai | Target IDs và event triggers | Sửa target/anchor/pose |
| R31 | Trạng thái vật thể không liên tục | State vào/ra cảnh, lịch sử entity | Sửa đoạn nối hoặc giải thích bước nhảy có chủ ý |
| R32 | Chuyển động che điểm chính | Focal target và vùng giữ rõ | Giảm action phụ hoặc đổi z-order |
| R33 | Lặp preset/sao chép mẫu | Episode history và capability mở rộng | Tạo recipe/asset có mục đích, không random để khác |
| R34 | Quá nhiều thuật ngữ/thực thể | Audience assumption, thứ tự giải thích | Chia ý/nhãn rõ; sửa lời chỉ khi được phép |
| R35 | Quá tải nghe–đọc–nhìn | Một điểm nhìn chính, text role rõ | Giảm chữ trang trí; không tự bỏ phụ đề truy cập |
| R36 | Chữ nhỏ/lỗi dấu/che hình | Font local, safe zones, text metrics | Sửa layout/chữ, không sinh lại ảnh |
| R37 | Lời–hình lệch | Audio master + anchors + quantization | Sửa event/time map, không đoán lại bằng prompt |
| R38 | Cắt nghỉ/TTS lộ nối | Preserve mặc định; edit policy và voice profile | Hoàn tác đoạn hoặc xin chỉ dẫn riêng |
| R39 | Nhạc lấn lời/SFX sai | Audio plan, gain/fades và reveal anchors | Remix audio, không render hình nếu hình không đổi |
| R40 | Hiệu ứng quá dày/khó tiếp cận | Motion purpose, contrast/text, tùy chọn giảm motion | Điều chỉnh action liên quan, không chứng nhận tự động tính tiếp cận |
| R41 | Agent tự chấm thiên lệch | Không dùng điểm tự chấm làm điều kiện hoàn thành | Cần bằng chứng/mẫu/nhận xét cụ thể nếu có yêu cầu xem lại |
| R42 | Ảnh tĩnh bỏ sót chuyển động/audio | Ghi media capability và phạm vi quan sát | Chỉ mở đúng clip cần xem khi có vấn đề, không giả đã xem/nghe |
| R43 | Điểm tổng che lỗi lớn | P0 tách khỏi thẩm mỹ, không KPI số hiệu ứng | Giữ issue mở cho đến khi xử lý thực |
| R44 | Sửa dây chuyền/vô hạn | Patch scope, revision, 0 quality retries tự động | Undo hoặc xin quyết định có phạm vi, không reset project |
| R45 | Dùng cache/bản duyệt cũ | Dependency hashes và snapshot export | Invalidate đúng phạm vi rồi tạo output mới |
| R46 | Resume mất/lặp cảnh/placeholder | Job checkpoints, coverage và artifact validation | Tiếp tục job đúng phần; nháp không gắn final-ready |
| R47 | Thiếu tài nguyên làm giảm chất lượng ngầm | Resource profile, queue, explicit fallback policy | Giữ task blocked; không tự cloud/hạ resolution |
| R48 | Điều kiện tài nguyên không rõ | Source/license registry trước sử dụng | Thay asset hoặc giữ trạng thái chưa xác minh quyền |
| R49 | Học quá mức một góp ý | Preference scope và ví dụ/lý do | Sửa đúng scope; không đổi mọi dự án |
| R50 | Đoạn ngắn đẹp nhưng dài/chủ đề khác kém | Plan toàn bài và episode metadata | Ghi giới hạn bằng chứng; không thêm nhiều benchmark ngoài mục tiêu |

## 3. Mẫu scene brief dùng để phòng lỗi

Ví dụ giả định, không lấy dữ kiện lịch sử thật:

| Trường | Nội dung minh họa |
|---|---|
| Mục đích | Cho thấy lực kéo và hệ quả khi dây đứt |
| Lời gốc | “Họ kéo khối đá lên dốc, nhưng sợi dây bất ngờ đứt.” |
| Điều đã biết | Có người, dây, đá và dốc; chưa biết dây sẽ đứt |
| Điều cần hiểu thêm | Dây nối lực kéo; khi dây đứt, trạng thái chuyển động thay đổi |
| Hình cần có | Nhân vật từ kit, đá, dốc, dây nguyên và dây đứt |
| Không tự thêm | Không thêm niên đại, địa danh hoặc đồ vật lịch sử chưa được cung cấp |
| Diễn xuất | Chuẩn bị kéo → kéo → phản ứng sau sự kiện |
| Anchor | “kéo”, “lên dốc”, “nhưng”, “đứt” theo word IDs đã căn |
| Ràng buộc | Tay gắn đầu dây; dây gắn đá; hướng kéo nhất quán; trạng thái đứt không xuất hiện trước reveal |
| Âm thanh | Hiệu ứng đứt tùy chọn đúng anchor; lời vẫn nghe rõ |
| Tài nguyên | Tái sử dụng kit/đạo cụ; không cần gọi diffusion nếu đủ |
| Điều kiện chạy | Rig hỗ trợ action; anchors resolved; asset đủ; timeline không conflict |

Nếu chưa có recipe kéo, agent không được gọi action không tồn tại. Có thể bổ sung recipe bằng công cụ/triển khai trong phạm vi dự án, hoặc chọn cách minh họa khác đã được chỉ rõ; không âm thầm thay bằng zoom toàn ảnh.

## 4. Sáu nhóm chức năng thay cho 50 module riêng

1. Hồ sơ nội dung và quyền sửa lời.
2. Sổ dữ kiện, nguồn và tài nguyên.
3. Biên tập toàn bài, scene brief và episode history.
4. Nhân vật, action capabilities và trạng thái liên tục.
5. Preflight/issue evidence không dùng AI chấm lặp.
6. Revision, dependency, queue và phục hồi.

Những nhóm này phải nằm trong dữ liệu/công cụ thật, không chỉ là một prompt dài dặn agent “hãy làm chính xác”. Các kiểm chứng nền tảng dùng `04`; không chạy 50 vòng kiểm thử AI tương ứng 50 rủi ro.

## 5. Cơ sở và giới hạn

Danh mục là phân tích thiết kế cho yêu cầu người dùng, không phải tỷ lệ lỗi đo được hay bảo đảm tất cả model đều mắc. Prompt chặt, nguồn và dữ liệu có cấu trúc giúp giảm sai lệch nhưng không chứng minh ý tưởng hay hoặc hình đúng tuyệt đối.

Tài liệu tham khảo về giảm quá tải lời–hình và giới hạn tự sửa suy luận:

- Fiorella & Mayer, phần tóm tắt chương Principles for Reducing Extraneous Processing in Multimedia Learning: https://doi.org/10.1017/9781108894333.019 . Áp dụng như định hướng bố cục/thông tin, không phải công thức retention YouTube.
- Huang và cộng sự, Large Language Models Cannot Self-Correct Reasoning Yet: https://arxiv.org/abs/2310.01798 . Kết quả trong model/bài thử của nghiên cứu không được ngoại suy thành xếp hạng model hiện tại; lý do thực tiễn ở đây là không coi tự chấm như bằng chứng độc lập.

Không cần thêm một AI trả phí để phòng các lỗi này. Người dùng vẫn có thể xem thành phẩm và góp ý; studio không ép phát sinh vòng sản xuất mới chỉ vì người dùng mở preview.
