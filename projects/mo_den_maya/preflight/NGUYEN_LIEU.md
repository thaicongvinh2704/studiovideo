# Maya — kiểm tra nguyên liệu trước khi dựng

**Cập nhật 21/10/2026:** đã nhận lại và nhập đủ 198 PNG của hai bộ vào
`assets/reusable/mo_den/`. Các đường dẫn `C:\Users\ADMIN\Downloads` trong hồ sơ
kiểm kê cũ là lịch sử. Kiểm tra nhập mới ở `../director_v2/import_audit.json`;
project dựng mới và thông tin bàn giao ở `../director_v2/README.md`.

## Kết luận

Đủ để bắt đầu lập phân cảnh và dựng nháp. Chưa đủ gói tư liệu cuối cho cách dựng
kết hợp minh họa và ảnh thật. Không cần yêu cầu người dùng tạo thêm hàng loạt
vật thể hoặc nhân vật lúc này.

## Đã có và đã kiểm tra

| Hạng mục | Kết quả |
|---|---|
| SRT người dùng gửi | 275 cue; kết thúc 00:17:03,726; khoảng 4049 đơn vị tách bằng khoảng trắng. Không thấy timestamp đảo hoặc chồng lấn. Chưa căn với lời đọc mới. |
| Gói Maya ID 151–198 | 48 PNG: 30 bối cảnh (10 nhóm × 3 trạng thái), 18 vật thể có alpha. CRC ZIP không lỗi, giải mã Pillow và Qt đủ 48/48; hash khớp toàn bộ danh mục. |
| Gói tái sử dụng ID 001–150 | Tìm thấy `Mo_Den_150_Anh_Tai_Su_Dung_v1.zip` trong Downloads. Đủ 150 PNG: 136 tách nền, 14 phông. CRC và giải mã Pillow/Qt không lỗi. Chưa nhập vào thư viện dùng chung. |
| Mỏ Đen | 24 ảnh theo manifest hiện có; không thiếu tệp được chỉ mục. |
| Giọng | `Mỏ Đen · giọng Bắc · bản B`; WAV mẫu khớp hash đã chốt. Có model và mã giọng trên máy để tạo lời mới. |

Đã mở ba bảng xem nhanh của toàn bộ 48 ảnh Maya và bảng chọn lọc vật thể/phông
trong bộ 150. Bối cảnh Maya cùng hướng nét/màu và các chuỗi trạng thái có thể
dùng để kể sự thay đổi. Đây không phải phê duyệt phục dựng khảo cổ hay kiểm tra
thẩm mỹ mọi ảnh ở độ phóng lớn.

Phông Maya khoảng 1671–1672 × 941 px; vật thể mới 1254 × 1254 px. Có thể dùng
khung ngang 1080p nhưng tránh phóng cận mạnh. Ảnh là PNG phẳng: chuyển nước,
mũi tên, khói hay vật rơi cần lớp vector/overlay riêng; không coi ba trạng thái
là hoạt hình liên tục hoặc suy ra có thể tách sẵn mọi bộ phận.

## Nguyên liệu còn phải chuẩn bị cho bản cuối

| Đoạn SRT | Còn thiếu trong hai gói ảnh | Cách bổ sung |
|---|---|---|
| 01:20–02:47; các lần chuyển địa điểm | Bản đồ địa lý thật của vùng Maya, vị trí Tikal, Itzan, Witzna, Yucatán và các địa điểm liên quan | Dùng dữ liệu địa lý có nguồn, vẽ lớp nhãn/mốc/tuyến bằng vector; không yêu cầu ảnh sinh mới. |
| 02:47–05:54 | Ảnh thật Tikal/hồ chứa và hình bằng chứng của nghiên cứu lọc nước/ô nhiễm | Tìm nguồn thực địa/nghiên cứu và ghi nguồn. Dùng 181–195 để giải thích khái niệm, không nhận là thiết kế khảo cổ chính xác. |
| 05:54–09:24 | Minh họa dữ liệu lượng mưa, thời đoạn hạn; vị trí/hồ sơ Itzan | Lập đồ thị và timeline vector theo nguồn gốc, phân biệt số liệu đo/tái dựng với sơ đồ minh họa. |
| 09:24–10:51 | Tư liệu riêng Witzna, dấu cháy/chữ khắc liên quan | Tìm hình nghiên cứu hoặc ảnh thực địa có nguồn. 175–177 chỉ minh họa khái quát, không phải phục dựng cuộc tấn công. |
| 12:28–14:38 | Ảnh thật Chichén Itzá, Mayapán và người Maya ngày nay | Thu thập tư liệu có thông tin nguồn/cách sử dụng; không dùng ảnh nhân vật cổ đại để đại diện cộng đồng hiện nay. |
| 14:38–15:06 | Hình giải thích chu kỳ lịch và nguồn bác bỏ lời đồn 2012 | Dựng sơ đồ đơn giản theo nguồn, dùng lịch bàn 198 cho ví von hiện đại; không bịa chữ khắc. |
| Toàn tập | WAV lời đọc thực tế, nhạc/SFX được chọn | Tạo lời tiếng Việt bằng bản B; nghe kiểm tra tên riêng, ghép theo ý nghĩa rồi căn lại SRT. Nhạc/SFX nhẹ có thể chọn sau, không cản dựng nháp. |

Các nguồn được ghi kèm gói Maya đã hữu ích, nhưng chưa đối chiếu hết từng
khẳng định trong 275 cue. Cần bảng nguồn theo cảnh trước khi khóa nội dung.
Những giấy tờ nghiên cứu cụ thể không đòi hỏi người dùng tự tạo thêm tranh.

## Công việc dựng còn lại, không phải yêu cầu người dùng gửi thêm ảnh

- Chia kịch bản thành cảnh/nhịp kể, mỗi hình có mục đích giải thích; không bắt
  buộc một cue phụ đề là một cảnh hay một lần tạo giọng riêng.
- Chuẩn hóa và lưu cách đọc Maya, Tikal, Corriental, Guatemala, zeolit,
  Chichancanab, Yucatán, Itzan, Witzna, Naranjo, Chichén Itzá, Mayapán,
  Smithsonian. Không đổi tên gốc trên phụ đề để ép TTS phát âm.
- Chốt đoạn dùng ảnh thật, đoạn minh họa và chuyển động của mũi tên/nước/nhãn.
- Kiểm tra lại luồng ghép và xuất PNG Mỏ Đen; tài liệu hiện tại vẫn ghi bộ chọn
  mèo và QC xuất riêng chưa hoàn thiện. Không gắn mèo thành vật thể để né QC.
- Nghe QC lời đọc, kiểm tra nguồn, bố cục, phụ đề và render thử trước khi xuất dài.

## Nguồn mới đã tìm được để tiếp tục đối chiếu

Ngoài tám đường dẫn trong `HUONG_DAN.md` của gói Maya, đã tìm được các đầu mối:

- Lượng mưa Chichancanab: https://www.cam.ac.uk/research/news/scientists-measure-severity-of-drought-during-the-maya-collapse
- Nghiên cứu hạn nhiều năm ở tây bắc Yucatán: DOI 10.1126/sciadv.adw7661
  (trang Science trả 403 trong lần kiểm tra này; chưa đọc toàn văn).
- Phân biệt suy sụp chính trị và đô thị, liên quan đoạn 11:19:
  https://www.cambridge.org/core/journals/latin-american-antiquity/article/abs/maya-urban-activities-during-the-terminal-classic-collapse-ad-7601000/77B933B77CCC6B53FEA4851607BC6B0A
- Itzan: https://bg.copernicus.org/articles/22/7079/2025/

Đây là danh sách đầu mối, không phải ghi nhận toàn bộ kịch bản đã qua fact-check.
Chi tiết máy kiểm tra ở `inventory_audit.json`; dữ liệu danh mục và bảng ảnh
trong cùng thư mục. Các file gốc trong Downloads không bị chỉnh sửa.
