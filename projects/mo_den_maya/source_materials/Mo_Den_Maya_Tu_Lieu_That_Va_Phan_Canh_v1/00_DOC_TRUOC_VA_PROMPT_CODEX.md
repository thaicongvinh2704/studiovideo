# Gói hình ảnh và phân cảnh Maya — giao Codex

Gói bổ sung này đi cùng **hai ZIP ảnh cũ**. Không cần mở từng file để gửi: giao nguyên ZIP này cho Codex, giữ hai ZIP cũ trong cùng workspace. Chúng không được chép lại vào gói để tránh tải lại150MB dữ liệu trùng.

## Prompt giao việc — sao chép nguyên đoạn dưới

Hãy tích hợp gói Mo_Den_Maya_Tu_Lieu_That_Va_Phan_Canh_v1 với hai bộ ảnh Mỏ Đen150 và Maya48 đã có trong dự án để dựng video kết hợp hình vẽ và tư liệu thật. Đọc00_DOC_TRUOC,01_KIEM_KE,SHOT_LIST_72_CANH.json,ASSET_REGISTRY.json,GRAPHICS_REGISTRY.json và198_ANH_CU_MANIFEST.json trước khi sửa timeline.

Giữ nguyên công việc giọng đọc đang chạy; không chọn giọng mới, không tạo lại lời đọc và không ghi đè audio/SRT cuối. KICH_BAN_THAM_CHIEU.srt chỉ cung cấp275 cue và mốc cũ. Khi audio cuối sẵn sàng, căn shot bằng source_cue_ids/text_anchor; nếu bản lời đã thay đổi, báo phần không khớp và remap có giải thích, không kéo audio cho vừa mốc cũ.

Tự giải nén, kiểm tra đủ asset, ánh xạ các ID I001–I198 về hai bộ cũ; ID R/E là tư liệu thật/nghiên cứu trong gói; ID G là đồ họa gốc. Giữ một asset registry chung. Không tự thay ảnh nghiên cứu thiếu độ phân giải bằng ảnh AI. Những hình nghiên cứu nhỏ dùng inset và chú giải lớn; không kéo căng hoặc dùng tăng nét AI để bịa chi tiết mẫu.

Dựng theo36 đoạn/72 nhịp hình, có thể chia/ghép hợp lý theo audio. Dùng ảnh thật cho địa điểm/bằng chứng/đời sống; dùng minh họa cho cơ chế và tình huống giả định. Hiện nhãn địa điểm,năm chụp,nguồn khi cần; luôn phân biệt ảnh mẫu thật,sơ đồ giả thuyết và tình huống minh họa. Chuyển động phải giải thích một ý: nước đi vào hồ,mực nước giảm,hàng hóa bị ngắt,nhãn xuất hiện theo lời. Với ảnh tư liệu chỉ pan/zoom/crop nhẹ,không AI làm người/hiện vật hoạt động.

Không vẽ dữ liệu mưa/dân số giả. Không đặt chính xác Witzna khi chưa có tọa độ nguồn. Không dùng bia Tikal thay văn khắc697. Không dùng bản đồ mưa1989–2019 như khí hậu cổ. Giữ bất định929–942±6 và phân biệt692(theo mô hình lõi) với697(văn khắc). Không biến13 năm hạn thành13 năm tuyệt đối không mưa.

Đọc điều kiện CC BY/CC BY-SA; ghi credit và giấy phép đúng từng ảnh, cập nhật mô tả thay đổi thực tế. Chưa dùng những mục trong TU_LIEU_CHUA_DU_QUYEN. Giữ thiết kế mascot đã được duyệt trong dự án; nếu không có rig thì làm bản dựng hình ảnh trước, ghi rõ thiếu asset nhân vật thay vì tự thiết kế lại.

Tạo dựng nháp1920×1080 theo pipeline hiện có, ưu tiên kiểm tra ba đoạn tiêu biểu: Tikal/nước, đồ thị hạn, Witzna/bằng chứng. Sau đó hoàn thiện toàn bộ timeline, kiểm tra phụ đề không che nhãn và nguồn, không kéo giãn ảnh đứng, không giữ một slide dài chỉ vì cue dài. Đầu ra gồm video nháp, timeline/project có thể sửa, asset manifest và credit cuối. Chưa cần thêm nhạc/SFX hoặc xuất bản lên nền tảng.

## Tệp nào dùng làm gì?
|Tệp/thư mục|Vai trò|
|---|---|
|01_Tu_lieu_that|16 file ảnh/hình nghiên cứu đã tải, không chỉ đường link|
|02_Do_hoa_SVG_PNG|8 đồ họa; SVG để sửa/animate, PNG để dùng ngay|
|03_Phan_canh|Cue,shot,text anchor và đường dẫn ảnh cũ|
|04_Nguon_va_quyen|Nguồn,tác giả,giấy phép,credit và mục chưa đủ quyền|
|05_Xem_nhanh|Contact sheet để duyệt nhanh|
|06_Du_lieu_va_ma_nguon|Dữ liệu bản đồ,số liệu và mã dựng để chỉnh tiếp|

Đây là gói tư liệu và kế hoạch dựng, không phải video đã render. Không có audio mới trong gói.
