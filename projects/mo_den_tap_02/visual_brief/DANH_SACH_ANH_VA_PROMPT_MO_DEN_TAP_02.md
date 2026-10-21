# Mỏ Đen — Tập 2: kiểm kê hình ảnh, yêu cầu tư liệu và prompt tạo asset

**Bản đạo diễn hình ảnh · 21/10/2026 · trạng thái: danh sách yêu cầu, chưa có asset mới được tạo hoặc phê duyệt.**

## Kết luận nhanh

Kịch bản có 73 đoạn lời, 460 cue SRT nháp và thời lượng dự kiến 18:22.875; chưa có bản thu âm tập 2 trong gói ZIP. Các mốc thời gian bên dưới chỉ để tìm đúng đoạn, phải căn lại sau khi có voice thật. Tôi đã kiểm tra danh mục và xem contact sheet của toàn bộ 198 PNG: hash đều khớp catalog. Kho có 24 pose Mỏ Đen, 150 đạo cụ/minh họa generic và 48 ảnh nền/vật thể Maya. Không tìm thấy chân dung/tư liệu lịch sử của các nhân vật tập 2 hay ảnh địa danh tập 2 trong các PNG đó.

Danh sách tách ba loại việc: 62 yêu cầu minh họa/pose có prompt tạo cụ thể; 37 yêu cầu tìm/tải tư liệu thật có nguồn (không được thay bằng ảnh AI); 25 đồ họa thời gian/số liệu phải dựng bằng SVG/compositor để giữ số chính xác. Tổng cộng 124 đầu việc hình ảnh, trong đó asset cùng họ được ghép lớp và tái sử dụng có kiểm soát; con số không phải 124 cảnh.

**Ưu tiên:** P1 = cần trước khi dựng rough cut có thể xem; P2 = cần khi tương ứng xuất hiện hoặc có thể giải quyết bằng tư liệu nguồn/đồ họa đã liệt kê. Ảnh tạo mới không bao gồm nhân vật lịch sử giả photorealistic. Nguồn thật phải được tìm từ kho có quyền, ghi registry và credit.

## Chuẩn đạo diễn áp dụng

Đọc [quy định đạo diễn hình ảnh](../../../QUY_DINH_DAO_DIEN_HINH_ANH.md) và [chuẩn nhân vật](../../../AGENTS.md) trước sản xuất. Maya V2 trước đó đã bị người dùng chê lặp nhiều đại cảnh trống; không dùng V2 làm mẫu. Đếm cùng họ bối cảnh, đổi crop hoặc zoom không xóa lượt lặp. Đại cảnh trống chỉ dùng ngắn để định vị; mỗi lần trở lại phải có thông tin hoặc hành động mới.

- Khung hình 16:9, 1920×1080 khi ghép; vật thể PNG tách nền thật và thường dựng ở canvas vuông/khung theo brief. Mỗi layer có tên và tọa độ ổn định.
- Hình minh họa mới theo phong cách ba ảnh `assets/styles/explainer_reference_v1/`; các ảnh này chỉ là tham chiếu nét/màu/bố cục, không dùng nhân vật người bị loại.
- Mỏ Đen phải theo đúng `assets/characters/mo_den/manifest.json`. 24 ảnh hiện có là tĩnh; không nói ảnh tĩnh có body animation hoặc lip-sync. Pose bổ sung phải giữ nguyên model đã duyệt, tạo file riêng và kiểm tra nhận diện.
- Không tạo chữ/số/bản đồ bằng model ảnh. Text, nhãn, ngày, mũi tên, đường thời gian và số liệu dựng bằng SVG/compositor từ thông số trong brief.
- Tư liệu lịch sử không được tạo sinh. Nếu chưa tìm được ảnh dùng hợp pháp, để mục ở trạng thái HOLD; dùng minh họa có nhãn hoặc đồ họa trừu tượng thay vì giả ảnh thật.
- Tránh người lịch sử được tạo thành ảnh chụp giả. Với cảnh người thật, dùng ảnh/tranh/hiện vật có nguồn hoặc không cho thấy mặt người.

## Những gì kho hiện tại đã đáp ứng

| Kho | Nội dung có thể dùng | Giới hạn khi làm tập 2 |
|---|---|---|
| Mỏ Đen · 24 PNG | 24 biểu cảm tĩnh; có tò mò, suy nghĩ, ngạc nhiên, lo lắng, giải thích. | Thiếu góc 3/4 trái/phải, chỉ đúng hướng, giữ thước/thẻ, tương tác tủ, nhìn qua vai/xuống bàn. Dùng pose hiện tại nếu khung không đòi cử chỉ cụ thể. |
| Generic · 001–150 | Đồ đời sống, dụng cụ nghiên cứu, kiến trúc/đá, tiền/vật liệu, địa hình/sinh vật, thời tiết, biểu tượng và một số nền. | Có thể tái dùng thước, lịch, thẻ, bàn, kính, sách dạng biểu tượng; không thay được ảnh/hiện vật lịch sử có catalog. |
| Maya · 151–198 | Bối cảnh/đạo cụ Maya về hồ nước, ruộng, kho, nhà, cung điện, khu cháy, thạch cao/zeolit, ngô và nước. | Không dùng nền đô thị Maya làm Giza, Tenochtitlan, London, Nhật, Oxford hay Mars. 48 ảnh này không phải bộ ảnh lịch sử chung. |
| Tư liệu lịch sử tập 2 | Chưa thấy ảnh chân dung, địa danh hoặc vật chứng gốc tập 2 trong PNG 198 bộ. | Phải tìm nguồn theo 37 mục R01–R37 bên dưới; một số cần quyền/credit trước khi xuất. |

Các contact sheet và danh mục có trong thư mục này. Danh mục kiểm tra theo từng file: [inventory_verified.json](inventory_verified.json).

## Coverage theo kịch bản

| Đoạn | Thời gian SRT nháp | Nội dung cần kể bằng hình | Bộ asset chính |
|---|---:|---|---|
| 01–08 | 00:00–01:57.938 | Mở đầu đồng thời; Quang Trung/Washington; cùng năm 1789; không suy ra từng gặp nhau; “tủ ký ức”. | A01–A09, R01–R03, R36, V01–V03, C01–C04 |
| 09–16 | 01:57.938–04:03.938 | Khufu; khoảng cách 2550 TCN–đầu Công nguyên–2026; không có năm 0; đảo điểm nhìn. | A10–A12, R04–R05, V04–V06, C05–C09 |
| 17–28 | 04:03.938–07:06.938 | Cleopatra/Apollo; phông nền đánh lừa; ma mút còn ở Wrangel; quần thể cuối. | A13–A17, R06–R09, V07–V10, C08–C10 |
| 29–34 | 07:06.938–08:43.688 | Oxford từ năm 1096 và Tenochtitlan từ năm 1325; Aztec từ năm 1428; phân biệt thành phố/đế chế. | A18–A23, R10–R14, V11–V13, C03/C04 |
| 35–40 | 08:43.688–10:14.812 | London Underground năm 1863, tàu hơi nước; samurai, cải cách 1868/1876 và đời sống tiếp tục. | A24–A30, R15–R19, V14, C01–C04 |
| 41–46 | 10:14.812–11:48.750 | Darwin/Lincoln cùng ngày sinh; mốc 1859/1860; tuổi 50/51; thành tựu không xuất hiện sẵn. | A05–A07, A31–A33, R20–R21/R35, V15–V16, C02/C09 |
| 47–57 | 11:48.750–14:36.938 | Wright: 12 giây/37 m; Apollo; đời người giả định; vải/gỗ và nhánh vật liệu khác sang Ingenuity; đổi tốc độ. | A34–A45, R22–R26, V17–V21, C03/C05/C06/C08 |
| 58–64 | 14:36.938–16:15.750 | Chaplin vượt hình tượng phim câm; sống tới thời Apple; phim năm 1940 có thoại; ảnh lớp 1 ví von. | A04/A07/A46–A50, R27–R30, V22–V23, C06/C09 |
| 65–70 | 16:15.750–17:44.062 | Bảo Đại: vai trò vua và đời người khác nhau; Windows 95; không bịa việc sử dụng PC. | A04/A07/A51–A52, R31–R34/R32, V24, C01/C02/C07/C10 |
| 71–73 | 17:44.062–18:22.875 | Hồi nhắc các cặp; câu hỏi về người thật và bức tranh; khép tủ, CTA. | A01/A02/A04/A09, V01/V07/V14/V22/V24/V25, C10 |

Cue và mốc trong `PHU_DE_DU_KIEN.srt`/`DIEN_GIONG_DAY_DU.txt` chưa đồng bộ với voice thật. Không xuất subtitle chính thức từ mốc nháp.

## Prompt khóa chung

Dán phần này trước prompt từng asset nếu công cụ tạo ảnh không giữ được yêu cầu trong brief:

```text
Tuân thủ prompt theo nghĩa đen. Tạo đúng một asset được chỉ định, trên một canvas riêng; không thêm đạo cụ, nhân vật, chữ, sự kiện hoặc phong cảnh không được yêu cầu. Không tự sáng tác dữ kiện lịch sử. Ba ảnh tham chiếu phong cách chỉ định hình nền, nét mực, độ phẳng màu và độ hoàn thiện; không được sao chép người trong ảnh tham chiếu. Dùng nền trắng/ngà, viền mực tối đồng đều hơi hữu cơ, mảng màu phẳng ấm, silhouette rõ và ít texture. PNG phải có alpha thật khi brief yêu cầu, không giả alpha bằng caro. Không sinh văn bản/số/logo/bản đồ. Giữ canvas, trục, góc nhìn, hướng sáng và điểm tiếp xúc đồng nhất giữa các lớp. Nếu không thấy hoặc không có ảnh reference được gọi tên, dừng và hỏi xin reference thay vì đoán.
```

### Khóa riêng cho Mỏ Đen

```text
Dùng chính các file master trong assets/characters/mo_den/library/named_24_v01 và mở manifest.json. Giữ nguyên mèo nhỏ thân tròn kem/nâu nhạt; mặt nạ, tai, bàn chân, đuôi nâu đậm; mắt xanh xám; nét viền đơn giản. Không đổi giống, tỉ lệ đầu/thân, mảng màu hoặc tuổi. Pose là ảnh tĩnh một trạng thái. Không tạo lip-sync, không rig giả. Chân trước vẫn là chân mèo, không có bàn tay/ngón người. Giữ chân/đuôi/toàn silhouette trong canvas. Mọi pose mới là bản nháp cần so cạnh master trước khi dùng.
```

## I. Minh họa và pose Mỏ Đen cần tạo

Mỗi mục dưới đây là một prompt độc lập. Các lượt dùng cùng một họ bối cảnh phải tuân giới hạn lặp; ưu tiên cận hành động, bằng chứng, vật thể có điểm đến và phản ứng của Mỏ Đen, không dựng thêm hàng loạt nền rộng.

### A01 · Tủ ký ức: thân tủ độc lập

**Ưu tiên:** P1 · **Đoạn lời:** 02, 08, 73

**Mục đích hình:** Biến ví von mở và sắp lại ký ức thành hành động có nguyên nhân.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** cabinet_body.png, cabinet_front_occluder.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một tủ hồ sơ gỗ thấp đúng bốn hộc, hai hàng hai cột. Nhìn ba phần tư từ trái, thấy mặt trước và hông phải hẹp; không gian đặt tủ là trường quay tưởng tượng hiện tại, không phải nội thất lịch sử. Thân tủ ở x=0.46–0.88, y=0.18–0.78 trên canvas 3840×2160; mặt đất y=0.80. Mỗi khoang rỗng rõ, không có ngăn kéo gắn sẵn. Chừa vùng x=0.08–0.40 cho Mỏ Đen. Gỗ nâu vừa, bốn ô có cùng kích thước, không hoa văn, không chữ. Mặt trước của thân và gờ che tiền cảnh phải khớp để ngăn kéo A02 có thể trượt ra.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: P02 mở một hộc; P08 các thẻ phân loại sai bị lấy ra; P73 thẻ đúng được xếp lại, đóng hộc. Ba lần rộng tối đa, mỗi lần thông tin khác.
Chi tiết không được xuất hiện: Không biến tủ thành cổng thời gian, không đồng hồ steampunk, không gắn tranh nhân vật hoặc biểu tượng lịch sử sẵn.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** P02 mở một hộc; P08 các thẻ phân loại sai bị lấy ra; P73 thẻ đúng được xếp lại, đóng hộc. Ba lần rộng tối đa, mỗi lần thông tin khác.

**Ranh giới nội dung:** Không biến tủ thành cổng thời gian, không đồng hồ steampunk, không gắn tranh nhân vật hoặc biểu tượng lịch sử sẵn.

**Tham chiếu cần mở trước:** REF_STYLE_01, REF_STYLE_02

### A02 · Ngăn kéo và thẻ rời của tủ

**Ưu tiên:** P1 · **Đoạn lời:** 02, 08, 73

**Mục đích hình:** Có bộ phận thật để thực hiện mở–lấy–xếp, thay vì rung cả ảnh tủ.

**Kho hiện có:** 126 có chồng thẻ liền khối; có thể dùng trang trí nhưng không tách từng thẻ/che khuất đúng hộc được.

**File cần giao:** drawer_body.png, drawer_front.png, blank_card.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dùng A01 đã chốt làm tham chiếu bắt buộc. Một ngăn kéo gỗ rỗng, mặt trước chiếm rộng 0.19 và cao 0.18 canvas 3840×2160, phối cảnh đúng khoang trên trái A01. Một tay nắm đồng đơn giản giữa mặt trước. Xuất riêng thân ngăn và gờ trước để thẻ có thể nằm sau gờ. Thẻ giấy kem thẳng góc, trống hoàn toàn, không in tên hay ảnh; mỗi thẻ là file riêng tái dùng bằng phần mềm. Không tự tạo bốn ngăn khác kiểu.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Ngăn chuyển vị trí theo trục chiều sâu được bố cục cho phép; thẻ đi lên qua mép trước, không xuyên thành gỗ.
Chi tiết không được xuất hiện: Không xuất tủ thứ hai, không chữ giả, không đổ thẻ như máy đánh bạc.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Ngăn chuyển vị trí theo trục chiều sâu được bố cục cho phép; thẻ đi lên qua mép trước, không xuyên thành gỗ.

**Ranh giới nội dung:** Không xuất tủ thứ hai, không chữ giả, không đổ thẻ như máy đánh bạc.

**Tham chiếu cần mở trước:** A01

### A03 · Mặt bàn điều tra nhìn thẳng từ trên

**Ưu tiên:** P2 · **Đoạn lời:** 06, 13, 53, 56

**Mục đích hình:** Đổi ngữ pháp hình sang thao tác cân nhắc bằng chứng và vật liệu.

**Kho hiện có:** 006 là bàn nhìn xiên; không thay được góc top-down để đối chiếu giấy/vật liệu.

**File cần giao:** desk_top_clean.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Góc nhìn thẳng từ trên 90 độ, một vùng mặt bàn gỗ sáng ở trung tâm, bốn mép nằm ngoài khung 3840×2160. Vân gỗ rất nhẹ dưới 10% tương phản. Vùng x=0.10–0.90, y=0.12–0.78 hoàn toàn sạch để ghép ảnh/tài liệu. Ánh sáng tản đều từ trên trái; không đồ vật, không bàn tay, không bóng nhân vật. Đây là mặt bàn người dẫn hiện tại; không gắn với bàn riêng của nhân vật lịch sử.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Giấy/khung nguồn và vật liệu lần lượt được đặt lên, thay đổi quan hệ ở mỗi lần dùng; không coi nền bàn là nội dung chính.
Chi tiết không được xuất hiện: Không thêm kính lúp, bút, cà phê, bản đồ hoặc chữ tự phát.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Giấy/khung nguồn và vật liệu lần lượt được đặt lên, thay đổi quan hệ ở mỗi lần dùng; không coi nền bàn là nội dung chính.

**Ranh giới nội dung:** Không thêm kính lúp, bút, cà phê, bản đồ hoặc chữ tự phát.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A04 · Khung ảnh rỗng có mặt trước và mặt sau

**Ưu tiên:** P1 · **Đoạn lời:** 03, 16, 20, 61, 64, 72

**Mục đích hình:** Tách hình tượng nổi tiếng khỏi toàn bộ cuộc đời.

**Kho hiện có:** 126 là thẻ giấy, chưa có khung rỗng/mặt sau phù hợp.

**File cần giao:** photo_frame_front.png, photo_frame_back.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một khung chữ nhật dọc tỉ lệ 4:5, gỗ nâu mỏng, bốn cạnh vuông, nhìn trực diện không nghiêng. Lỗ ảnh thực sự trong suốt, chiếm 78% rộng và 80% cao khung. Xuất mặt trước và mặt sau rời, cùng canvas 2048×2560, cùng tâm. Mặt sau là tấm bìa nâu không chữ, không móc rườm rà. Viền đủ nhẹ để ảnh chân dung có nguồn vẫn chiếm ưu thế. Mỗi file chỉ một khung, không ghép portrait vào hình sinh.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Khung kéo ra khỏi ảnh, ảnh nhỏ lùi lại để nhường đường đời; không dùng lặp một động tác bật vào ở mọi nhân vật.
Chi tiết không được xuất hiện: Không tạo mặt người, không số năm, không nội dung giả ở mặt sau.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Khung kéo ra khỏi ảnh, ảnh nhỏ lùi lại để nhường đường đời; không dùng lặp một động tác bật vào ở mọi nhân vật.

**Ranh giới nội dung:** Không tạo mặt người, không số năm, không nội dung giả ở mặt sau.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A05 · Hai quyển sách môn học tách riêng

**Ưu tiên:** P1 · **Đoạn lời:** 44, 46

**Mục đích hình:** Gỡ bức tường trí nhớ giữa Darwin và Lincoln.

**Kho hiện có:** Không có sách môn học trong 198 PNG.

**File cần giao:** book_science_closed.png, book_history_closed.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Hai quyển sách đóng bìa cứng đơn giản nhìn xiên 20 độ từ trên, gáy bên trái. Sách thứ nhất xanh rêu nhạt, sách thứ hai nâu gạch; cùng kích thước hình học 3:4 và cùng độ dày. Mỗi sách ở giữa canvas riêng 2048×2048, bìa trống đủ chỗ ghép nhãn bằng chữ vector. Không tranh Darwin/Lincoln in sẵn. Mép giấy màu kem, không trang chữ giả. Bàn là lớp riêng.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Hai sách tách khung trước; vách A06 rút xuống để hai mốc cùng ngày sinh nối ngang.
Chi tiết không được xuất hiện: Không gắn nhãn tiếng Anh, không logo trường học, không biến sách thành lịch sử phát triển tuyến tính.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Hai sách tách khung trước; vách A06 rút xuống để hai mốc cùng ngày sinh nối ngang.

**Ranh giới nội dung:** Không gắn nhãn tiếng Anh, không logo trường học, không biến sách thành lịch sử phát triển tuyến tính.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A06 · Vách phân ngăn ký ức

**Ưu tiên:** P2 · **Đoạn lời:** 08, 44, 64

**Mục đích hình:** Cho thấy sự phân loại do người nhìn tạo ra.

**Kho hiện có:** 036 là tường đá thuộc kiến trúc; không phù hợp ví von sách vở nhẹ nhàng.

**File cần giao:** memory_partition.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một tấm vách mỏng bằng bìa cứng màu xám ấm, dựng thẳng, nhìn trực diện; rộng 12% canvas 3840×2160, cao từ y=0.14 tới 0.78, tâm x=0.50. Có một chân đỡ nhỏ nằm phía sau, không thành tường nhà. Hai mép thẳng, một mặt sạch; xuất độc lập alpha. Đủ rõ là vật trong phép ví von bàn làm việc, không phải hàng rào biên giới hoặc tường lịch sử.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Rút vách xuống đúng câu “sách đã chia môn”; chân dung hai người vẫn đứng yên ở hai phía.
Chi tiết không được xuất hiện: Không vẽ người bị nhốt, không tường Berlin, không tự ghi chữ.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Rút vách xuống đúng câu “sách đã chia môn”; chân dung hai người vẫn đứng yên ở hai phía.

**Ranh giới nội dung:** Không vẽ người bị nhốt, không tường Berlin, không tự ghi chữ.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A07 · Album gia đình mở, ô ảnh trong suốt

**Ưu tiên:** P2 · **Đoạn lời:** 63, 65, 72

**Mục đích hình:** Minh họa hình ảnh đóng băng một thời điểm nhưng con người tiếp tục sống.

**Kho hiện có:** 126 chỉ là thẻ, không có cấu trúc album hai thời điểm.

**File cần giao:** album_pages.png, album_photo_corners.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Album bìa kem mở trên mặt phẳng, nhìn từ trên nghiêng 15 độ. Hai trang nằm x=0.15–0.85, y=0.18–0.73. Mỗi trang chỉ một ô ảnh 4:5, lỗ alpha thật; bốn góc giữ ảnh nhỏ. Không chứa khuôn mặt được sinh. Chừa dải dưới mỗi ảnh cho tuổi/năm do người dựng thêm. Xuất bìa/trang và các góc kẹp tiền cảnh riêng, đúng khớp tọa độ.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Ảnh tuổi nhỏ ở trái, ký hiệu tuổi trưởng thành bên phải; ghi tình huống ví von, không giả thành album gia đình Bảo Đại.
Chi tiết không được xuất hiện: Không giấy khai sinh giả, không ảnh gia đình có thật không rõ nguồn, không lời tự sự mới.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Ảnh tuổi nhỏ ở trái, ký hiệu tuổi trưởng thành bên phải; ghi tình huống ví von, không giả thành album gia đình Bảo Đại.

**Ranh giới nội dung:** Không giấy khai sinh giả, không ảnh gia đình có thật không rõ nguồn, không lời tự sự mới.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A08 · Giá treo áo: nhãn thời đại đánh lừa trí nhớ

**Ưu tiên:** P2 · **Đoạn lời:** 07, 08, 73

**Mục đích hình:** Minh họa việc trang phục chi phối cảm giác về niên đại.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** costume_rack.png, empty_hanger.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một thanh treo ngang thấp trên hai trụ gỗ đơn giản, nhìn trực diện, ở x=0.20–0.80, y=0.22–0.74; hai móc áo trống rời. Không có áo thật mặc định. Áo bào/áo phương Tây chỉ được thêm từ hình tư liệu đã khóa ở khung riêng, không coi chiếc giá là bảo tàng hiện vật. Tách thanh, hai móc để móc có thể được nhấc ra. Thiết kế trường quay tưởng tượng, màu nâu ấm.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Nhãn phân loại rời khỏi móc khi thước thời gian xuất hiện; kết phim nhắc lại bằng cận móc, không phát lại cả mở đầu.
Chi tiết không được xuất hiện: Không sinh long bào triều Nguyễn rồi gán Quang Trung; không để áo tự đổi người.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Nhãn phân loại rời khỏi móc khi thước thời gian xuất hiện; kết phim nhắc lại bằng cận móc, không phát lại cả mở đầu.

**Ranh giới nội dung:** Không sinh long bào triều Nguyễn rồi gán Quang Trung; không để áo tự đổi người.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A09 · Phong bì trống và tờ giấy rời

**Ưu tiên:** P2 · **Đoạn lời:** 06, 70

**Mục đích hình:** Tách sống đồng thời khỏi bằng chứng liên hệ.

**Kho hiện có:** 124/130 có đường liên kết nhưng không có thư chứng cứ; ưu tiên V03 nếu muốn ít đạo cụ.

**File cần giao:** envelope_empty.png, letter_blank.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một phong bì giấy kem trống mở nắp nhìn từ trên, góc giấy thư trắng nhô ra 25%; xuất phong bì và tờ giấy riêng. Canvas 2048×2048, vật chiếm 70%, tâm cố định; không tem, dấu bưu điện, chữ ký, quốc huy hay niên đại. Đây là biểu tượng hiện tại trên bàn Mỏ Đen, không phải thư thực của Quang Trung/Washington.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dừng giấy trước đường nối giữa hai chân dung; nhãn “chưa có bằng chứng liên hệ” do compositor thêm ngay từ đầu.
Chi tiết không được xuất hiện: Không viết thư giả, không gắn chữ ký Washington, không gửi thư thành công rồi mới phủ dấu X.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dừng giấy trước đường nối giữa hai chân dung; nhãn “chưa có bằng chứng liên hệ” do compositor thêm ngay từ đầu.

**Ranh giới nội dung:** Không viết thư giả, không gắn chữ ký Washington, không gửi thư thành công rồi mới phủ dấu X.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A10 · Khối Đại kim tự tháp Khufu, biểu tượng nhận diện

**Ưu tiên:** P1 · **Đoạn lời:** 09, 18, 23, 28

**Mục đích hình:** Cần kim tự tháp Ai Cập đúng hình học để so tuổi.

**Kho hiện có:** 151–153 là đô thị Maya; không được dùng thay Giza.

**File cần giao:** khufu_pyramid_icon.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một khối Đại kim tự tháp Khufu nhìn ba phần tư từ trên nhẹ, góc thấy hai mặt, đá vôi vàng nhạt, chân đế vuông, các mặt dốc liên tục. Đây là biểu tượng kiến trúc sơ lược, không phải phục dựng tiến độ xây dựng hay tình trạng ở một năm cụ thể. Không có đền trên đỉnh, không cầu thang mặt trước kiểu Maya. Tâm x=0.5,y=0.48 trên 2560×2560, vật chiếm 75% rộng; đường chân đế ngang ổn định. Dùng ảnh Giza R04 làm khóa hình, bỏ chi tiết ngoại cảnh.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Xuất hiện nhỏ bên mốc khoảng 2550 TCN; tỷ lệ thời gian được dựng bằng V04/V07, không biến độ lớn kim tự tháp thành thước đo tuổi.
Chi tiết không được xuất hiện: Không kim tự tháp bậc thang Mesoamerica, không tượng Nhân sư đi kèm, không ma mút/Cleopatra/Chúa Giê-su bên chân.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Xuất hiện nhỏ bên mốc khoảng 2550 TCN; tỷ lệ thời gian được dựng bằng V04/V07, không biến độ lớn kim tự tháp thành thước đo tuổi.

**Ranh giới nội dung:** Không kim tự tháp bậc thang Mesoamerica, không tượng Nhân sư đi kèm, không ma mút/Cleopatra/Chúa Giê-su bên chân.

**Tham chiếu cần mở trước:** R04, REF_STYLE_02

### A11 · Cận bề mặt đá và chiều sâu di tích

**Ưu tiên:** P2 · **Đoạn lời:** 10, 13, 15

**Mục đích hình:** Có chi tiết thật sự để cắt cận thay vì zoom toàn cảnh Giza nhiều lần.

**Kho hiện có:** 053 là khối đá chung; dùng được cho ví von vật liệu nhưng không đủ nhận diện bề mặt di tích cụ thể.

**File cần giao:** khufu_stone_close.png, stone_foreground_edge.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Cận 5–7 khối đá vôi xếp hàng ngang, khung 3840×2160, mặt đá hơi thô, cạnh mòn nhẹ, không phù điêu hay chữ. Góc gần trực diện từ bên phải, ánh sáng thấp từ trái tạo bóng ở khe. Tham chiếu ảnh cận đá Khufu R05; chỉ tái hiện phần nhìn thấy, không mô phỏng chính xác bề mặt thế kỷ I TCN. Tách một lớp cạnh đá tiền cảnh ở góc dưới trái, nền đá phía sau và bóng khe nếu cần. Vùng góc phải trên sạch để overlay niên đại.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dẫn mắt từ một khe đá sang vạch đo thời gian; ưu tiên chèn tư liệu R05 khi nói bằng chứng.
Chi tiết không được xuất hiện: Không tự khắc tên Khufu, không giấy nghiệm thu, không nhân chứng giả.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dẫn mắt từ một khe đá sang vạch đo thời gian; ưu tiên chèn tư liệu R05 khi nói bằng chứng.

**Ranh giới nội dung:** Không tự khắc tên Khufu, không giấy nghiệm thu, không nhân chứng giả.

**Tham chiếu cần mở trước:** R05

### A12 · Hai bệ quan sát thời gian

**Ưu tiên:** P2 · **Đoạn lời:** 15, 16

**Mục đích hình:** Đảo vị trí người quan sát mà không bịa Chúa Giê-su đến Giza.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** viewpoint_plinth.png, plinth_front_edge.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Hai bệ gỗ thấp hình chữ nhật cùng kích thước, xuất một master độc lập để nhân đôi, nhìn ngang hơi từ trên. Trên mỗi bệ có khe cắm thẻ trống, không người. Bệ được đặt trong không gian trắng hiện tại, không tại địa điểm khảo cổ. Một cạnh trước rời làm lớp che chân thẻ. Mỏ Đen hiện tại có thể ngồi cạnh bệ; tên “người sống đầu Công nguyên” chỉ là chữ vector, không chân dung tôn giáo.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Camera chuyển từ vị trí “chúng ta” sang vị trí giả định, khoảng đo kéo ngược dài hơn; nhãn “tình huống giả định” xuyên suốt.
Chi tiết không được xuất hiện: Không vẽ Chúa Giê-su đứng trước kim tự tháp, không phục trang nhân vật tôn giáo tự chọn.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Camera chuyển từ vị trí “chúng ta” sang vị trí giả định, khoảng đo kéo ngược dài hơn; nhãn “tình huống giả định” xuyên suốt.

**Ranh giới nội dung:** Không vẽ Chúa Giê-su đứng trước kim tự tháp, không phục trang nhân vật tôn giáo tự chọn.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A13 · Ma mút lông xoăn: toàn thân nghiêng

**Ưu tiên:** P1 · **Đoạn lời:** 22, 23, 25, 26

**Mục đích hình:** Tạo chủ thể sinh vật còn thiếu, đúng loài chứ không thêm lông cho voi hiện đại.

**Kho hiện có:** 104–110 không có ma mút; 106 lạc đà không thể thay.

**File cần giao:** mammoth_profile.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một ma mút lông xoăn trưởng thành, toàn thân hướng sang phải, hông gần ngang. Vai cao, lưng dốc về hông, đầu vòm, tai nhỏ, đuôi ngắn, lông nâu sẫm dài, hai ngà cong xoắn rõ không xuyên vòi. Bốn chân chịu trọng lượng; chân xa nhìn được một phần có lý do che khuất. Vòi thả xuống hơi cong về trước. Canvas 3072×2048 alpha, thân chiếm x=0.12–0.86,y=0.12–0.86. Dựa mô hình/ảnh phục dựng bảo tàng R08, không định lượng kích thước riêng quần thể Wrangel nếu chưa có nguồn.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dùng reveal từ cận lông A14 sang toàn thân; động tác ăn dùng pose A15, không kéo PNG lướt nền và gọi là đi bộ.
Chi tiết không được xuất hiện: Không voi châu Phi tai lớn, không ma mút lùn tự suy đoán, không tuyết phủ toàn thân, không thợ săn, không Giza trong ảnh.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dùng reveal từ cận lông A14 sang toàn thân; động tác ăn dùng pose A15, không kéo PNG lướt nền và gọi là đi bộ.

**Ranh giới nội dung:** Không voi châu Phi tai lớn, không ma mút lùn tự suy đoán, không tuyết phủ toàn thân, không thợ săn, không Giza trong ảnh.

**Tham chiếu cần mở trước:** R08, REF_STYLE_02

### A14 · Ma mút: cận đầu và lông cùng cá thể

**Ưu tiên:** P2 · **Đoạn lời:** 22, 25

**Mục đích hình:** Chuẩn bị tiết lộ chủ thể qua đặc điểm, tránh chỉ chiếu nguyên con suốt đoạn.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** mammoth_head_close.png, mammoth_fur_insert.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa A13 đã khóa, giữ đúng màu lông, ngà, tai và tỷ lệ đầu. Cận ba phần tư đầu từ trái, mắt nhìn sang phải, phần vai vào góc trái dưới, ngà nằm trọn khung không bị cắt. Canvas 2560×2560 alpha, đầu chiếm 65% cao; không thêm nền. Tạo riêng một mảng lông cận để mở ở câu “rất nhiều lông”, sợi stylized thành mảng rõ, không chất liệu ảnh chụp khác phong cách.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Lông → ngà → toàn thân đúng câu gợi ý; không dùng ba hình cùng lúc thành collage.
Chi tiết không được xuất hiện: Không thay cá thể/tuổi, không biểu cảm người, không sừng ở trán.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Lông → ngà → toàn thân đúng câu gợi ý; không dùng ba hình cùng lúc thành collage.

**Ranh giới nội dung:** Không thay cá thể/tuổi, không biểu cảm người, không sừng ở trán.

**Tham chiếu cần mở trước:** A13, R08

### A15 · Ma mút cúi vòi tới cỏ

**Ưu tiên:** P2 · **Đoạn lời:** 23, 26

**Mục đích hình:** Có hành động ăn phù hợp sinh cảnh, không dựa vào rung/zoom.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** mammoth_feeding_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Biến thể từ A13 cùng camera, canvas và dấu chân. Đầu hạ vừa phải, vòi chạm một điểm cỏ dự kiến ở x=0.78,y=0.84; mắt nhìn xuống. Không vẽ cỏ dính vào ảnh cơ thể. Giữ vị trí bốn bàn chân và hình ngà có giải phẫu hợp lý, không co giãn ngà. Cung cấp tư thế chuẩn bị A13 và pose cúi ăn này để chuyển pose có chủ đích; nếu muốn chuyển mượt phải làm in-between có kiểm tra, không giả vờ hai PNG là rig.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Cỏ riêng A17 bị vòi chạm rồi thay trạng thái; một hành động có điểm tiếp xúc.
Chi tiết không được xuất hiện: Không cử động cơ thể bằng mesh làm ngà mềm, không bịa nguyên nhân tuyệt chủng.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Cỏ riêng A17 bị vòi chạm rồi thay trạng thái; một hành động có điểm tiếp xúc.

**Ranh giới nội dung:** Không cử động cơ thể bằng mesh làm ngà mềm, không bịa nguyên nhân tuyệt chủng.

**Tham chiếu cần mở trước:** A13, A17

### A16 · Wrangel: lát cắt sinh cảnh lãnh nguyên

**Ưu tiên:** P1 · **Đoạn lời:** 23, 24, 26

**Mục đích hình:** Thiết lập đảo xa Giza bằng môi trường phù hợp và vị trí bản đồ riêng.

**Kho hiện có:** 083 là đảo đá nhỏ biểu tượng, 088 là sông băng; không đại diện địa hình Wrangel.

**File cần giao:** wrangel_sky_far.png, wrangel_ground_mid.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Bối cảnh minh họa lãnh nguyên ven biển Bắc Cực, mùa không phủ tuyết kín: nền đất nâu xám thấp, cỏ thấp vàng xám, đồi thấp xa, biển xanh xám mảnh ở chân trời y=0.43. Canvas 3840×2160; vùng y=0.58–0.80 đủ mặt đất để đặt ma mút ở x=0.55; bên trái chừa chỗ Mỏ Đen trong lớp minh họa có nhãn. Không vẽ động vật/người. Tham chiếu ảnh địa hình đảo Wrangel R09, không gọi là tái dựng chính xác môi trường 4000 năm trước.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Một lần định vị ngắn rồi cắt cận ma mút/cỏ hoặc bản đồ, không dùng nền Wrangel liên tục để phủ mọi câu.
Chi tiết không được xuất hiện: Không núi băng khổng lồ, rừng thông, kim tự tháp, lều săn, hạt tuyết bay dày.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Một lần định vị ngắn rồi cắt cận ma mút/cỏ hoặc bản đồ, không dùng nền Wrangel liên tục để phủ mọi câu.

**Ranh giới nội dung:** Không núi băng khổng lồ, rừng thông, kim tự tháp, lều săn, hạt tuyết bay dày.

**Tham chiếu cần mở trước:** R09

### A17 · Cỏ lãnh nguyên: nguyên vẹn và sau gặm

**Ưu tiên:** P2 · **Đoạn lời:** 23, 26

**Mục đích hình:** Chi tiết hành động để có diễn biến mà không bịa biến cố.

**Kho hiện có:** 101 có cỏ xanh chung, không cùng sinh cảnh/màu với Wrangel; có thể dùng ở ví von không định danh.

**File cần giao:** tundra_grass_before.png, tundra_grass_after.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Hai trạng thái của cùng cụm cỏ thấp khô vàng xám, gốc ở x=0.5,y=0.78 trên canvas 2048×1024 alpha. Bản nguyên vẹn có 7–9 lá cong đơn giản; bản sau gặm thấp hơn khoảng một phần ba, cùng gốc/rễ và màu. Không thêm hoa, không cây nhiệt đới. Dùng cùng hướng sáng A16. Cụm cỏ tách khỏi ma mút để điều khiển điểm chạm.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Đổi trạng thái đúng lúc vòi chạm, giữ vài nhịp rồi cắt; không lặp ăn suốt phần tuyệt chủng.
Chi tiết không được xuất hiện: Không thể hiện một ngọn cỏ là chứng cứ thức ăn cuối cùng, không cỏ mọc phép thuật.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Đổi trạng thái đúng lúc vòi chạm, giữ vài nhịp rồi cắt; không lặp ăn suốt phần tuyệt chủng.

**Ranh giới nội dung:** Không thể hiện một ngọn cỏ là chứng cứ thức ăn cuối cùng, không cỏ mọc phép thuật.

**Tham chiếu cần mở trước:** A16

### A18 · Bục đọc và bản thảo học tập trung đại

**Ưu tiên:** P1 · **Đoạn lời:** 29, 33

**Mục đích hình:** Cho thấy hoạt động học, tránh lấy kiến trúc Oxford đời sau làm hình năm 1096.

**Kho hiện có:** 006 bàn chung dùng được nhưng chưa có bục/sách phù hợp.

**File cần giao:** medieval_lectern.png, manuscript_open_blank.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một bục đọc gỗ mộc thấp nhìn ba phần tư, trên bục đặt quyển bản thảo mở, giấy kem không chữ. Không logo Oxford, không huy hiệu đại học, không mũ tốt nghiệp, không nội thất nhà thờ xác định. Canvas 2560×2560 alpha; bục chiếm 65% cao, sách tách lớp và được căn đúng mặt nghiêng. Đây là minh họa hoạt động học trung đại, không phục dựng phòng dạy Oxford 1096.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Mở trang sách và đưa mốc “có bằng chứng giảng dạy” vào cạnh sách; ảnh Oxford hiện nay R10 có nhãn thời điểm riêng.
Chi tiết không được xuất hiện: Không in 1096 như ngày thành lập, không sách in hiện đại, không Radcliffe Camera năm 1096.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Mở trang sách và đưa mốc “có bằng chứng giảng dạy” vào cạnh sách; ảnh Oxford hiện nay R10 có nhãn thời điểm riêng.

**Ranh giới nội dung:** Không in 1096 như ngày thành lập, không sách in hiện đại, không Radcliffe Camera năm 1096.

**Tham chiếu cần mở trước:** S_OXFORD, REF_STYLE_01

### A19 · Cận góc trang bản thảo và dấu tiếp nối

**Ưu tiên:** P2 · **Đoạn lời:** 29, 33

**Mục đích hình:** Gợi nhiều thế hệ học tập bằng hành động trao/chuyển trang không cần tạo đám đông.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** manuscript_page.png, page_turn_corner.png, quill_plain.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Góc nhìn top-down, một trang bản thảo kem nằm x=0.18–0.80,y=0.12–0.78. Mép trang hơi không đều, không giả cổ quá mức. Một góc phải dưới được lật lên thành lớp riêng, phần sau vẫn trắng. Không chữ Latin tự bịa. Bút lông rời đặt ngoài vùng trang, chỉ là đạo cụ tổng quát. Không tay người và không khẳng định vật này từng thuộc một học giả cụ thể.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Trang hiện tại chuyển đi, trang mới cùng chỗ xuất hiện để diễn tả tiếp nối; mốc năm không chạy như lịch lật máy.
Chi tiết không được xuất hiện: Không tài liệu 1096 giả, không chữ ký, không văn bản trông như nguồn gốc.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Trang hiện tại chuyển đi, trang mới cùng chỗ xuất hiện để diễn tả tiếp nối; mốc năm không chạy như lịch lật máy.

**Ranh giới nội dung:** Không tài liệu 1096 giả, không chữ ký, không văn bản trông như nguồn gốc.

**Tham chiếu cần mở trước:** A18

### A20 · Ghế dài học tập, thay thế đồ vật qua thế hệ

**Ưu tiên:** P2 · **Đoạn lời:** 33, 34

**Mục đích hình:** Tạo cảnh vừa có chủ thể và sự tiếp nối, tránh thêm đại cảnh trường trống.

**Kho hiện có:** Ảnh 005/006 có thể tái dùng nếu góc phù hợp; cần góc ngang để ghép người dẫn đúng mặt bàn.

**File cần giao:** study_bench.png, study_table_front.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một ghế dài gỗ đơn giản và mặt bàn tương ứng, nhìn ngang hơi từ trên, không kiến trúc hậu cảnh. Canvas 3840×2160 alpha; ghế từ x=0.15 đến 0.85, mặt bàn y=0.50. Chừa các vùng đặt sách riêng; không khắc tên đại học. Tách mép bàn tiền cảnh để có thể đặt Mỏ Đen ngồi sau với chân không xuyên gỗ. Không dùng làm bằng chứng nội thất Oxford năm 1096.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Sách bản thảo nhường cho sách thời sau, người dẫn nêu tiếp nối; không biến đổi vật thành lịch sử nội thất đã xác minh.
Chi tiết không được xuất hiện: Không laptop trong hình 1096, không sinh viên mặc lễ phục hiện đại.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Sách bản thảo nhường cho sách thời sau, người dẫn nêu tiếp nối; không biến đổi vật thành lịch sử nội thất đã xác minh.

**Ranh giới nội dung:** Không laptop trong hình 1096, không sinh viên mặc lễ phục hiện đại.

**Tham chiếu cần mở trước:** A18

### A21 · Tenochtitlan: mô hình giải thích đô thị trên hồ

**Ưu tiên:** P1 · **Đoạn lời:** 30, 31, 32

**Mục đích hình:** Thay toàn bộ nền Maya bằng hình đúng khu vực và loại đô thị.

**Kho hiện có:** 151–180 là các họ nền Maya và bị loại khỏi vai trò Aztec.

**File cần giao:** tenochtitlan_lake_base.png, tenochtitlan_city_mass.png, tenochtitlan_causeways.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Góc nhìn trên cao xiên 35 độ của đô thị giữa hồ: đảo trung tâm, đường đắp nối bờ, kênh nước và khối nhà thấp; khu nghi lễ theo mô hình bảo tàng R12 đã chọn. Chỉ dựng sau khi xác định giai đoạn của ảnh mô hình/sơ đồ. Nếu tham chiếu là đầu thế kỷ XVI, ghi giai đoạn đó; không gọi ảnh là Tenochtitlan năm 1325 hoặc đế chế Aztec năm 1428. Canvas 3840×2160; đảo ở vùng giữa, hồ làm khoảng phân cách. Tách hồ/đất, khối đô thị và đường đắp.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Một lần định vị; lớp nhãn phân biệt “thành phố” và “liên minh đế chế”; không dùng lớn ở mọi câu Aztec.
Chi tiết không được xuất hiện: Không Tikal/Chichen Itza, không rừng Maya, không rồng châu Á, không phục dựng chính xác từ trí tưởng tượng.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Một lần định vị; lớp nhãn phân biệt “thành phố” và “liên minh đế chế”; không dùng lớn ở mọi câu Aztec.

**Ranh giới nội dung:** Không Tikal/Chichen Itza, không rừng Maya, không rồng châu Á, không phục dựng chính xác từ trí tưởng tượng.

**Tham chiếu cần mở trước:** R12, R13

### A22 · Tenochtitlan: cận kênh và mép nhà

**Ưu tiên:** P2 · **Đoạn lời:** 31, 32

**Mục đích hình:** Cho thấy vùng đất có đời sống/đô thị, không dùng một sân trống làm đại diện cả châu lục.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** tenochtitlan_canal_back.png, canal_foreground_bank.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa đúng mô hình R12 đã chọn và A21; góc thấp gần mặt nước vào một đoạn kênh nhỏ, hai mép kiến trúc đá/vữa thấp, đường nhìn chếch sang phải. Chỉ vẽ thuyền không người nếu mẫu tham chiếu xác nhận hình dáng. Canvas 3840×2160; tách mép kênh tiền cảnh, nước và nhà phía sau. Không tự thêm đền lớn. Đây là minh họa cùng giai đoạn với nguồn mô hình, không phải ảnh chứng minh Mexico trước năm 1428.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dẫn mắt qua quan hệ nước–đô thị rồi sang bản đồ và mốc; không cho thuyền đi vòng vô nghĩa.
Chi tiết không được xuất hiện: Không mái Maya/tàu buồm châu Âu/ngựa/xe bánh sắt.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dẫn mắt qua quan hệ nước–đô thị rồi sang bản đồ và mốc; không cho thuyền đi vòng vô nghĩa.

**Ranh giới nội dung:** Không mái Maya/tàu buồm châu Âu/ngựa/xe bánh sắt.

**Tham chiếu cần mở trước:** A21, R12

### A23 · Lớp dấu vết cư trú trước mốc đế chế

**Ưu tiên:** P2 · **Đoạn lời:** 31

**Mục đích hình:** Hình cần chứng minh “trước năm 1428 không phải vùng đất trống”.

**Kho hiện có:** 022 hộp mẫu có sẵn có thể dùng nếu không cần ba ảnh lớn; giữ A23 như tùy chọn bố cục.

**File cần giao:** evidence_tray.png, evidence_tray_front.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một khay trưng bày đương đại màu kem, nhìn từ trên, có ba hốc rỗng. Ghép vào mỗi hốc ảnh hiện vật/di tích R14 có niên đại trước 1428; không sinh gốm hoặc hoa văn giả. Bố cục lệch nhịp: một hốc lớn bên trái, hai hốc nhỏ bên phải. Xuất khay và mép tiền cảnh riêng; nhãn nguồn dựng ngoài hốc.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Hiện lần lượt niên đại của các bằng chứng đã chọn; giữ địa điểm khác nhau rõ ràng.
Chi tiết không được xuất hiện: Không gán tất cả hiện vật cho người Aztec, không dùng gốm Maya như đại diện mọi Mexico.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Hiện lần lượt niên đại của các bằng chứng đã chọn; giữ địa điểm khác nhau rõ ràng.

**Ranh giới nội dung:** Không gán tất cả hiện vật cho người Aztec, không dùng gốm Maya như đại diện mọi Mexico.

**Tham chiếu cần mở trước:** R14

### A24 · Ga Metropolitan Railway giai đoạn mở tuyến

**Ưu tiên:** P1 · **Đoạn lời:** 35, 36, 37

**Mục đích hình:** Cần ga đúng thời đầu máy hơi nước, không metro ngày nay.

**Kho hiện có:** 148 hành lang đá không phải ga; 138 đường làng không phải London.

**File cần giao:** metropolitan_station_back.png, platform_front_mask.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Bám tranh hoặc ảnh ga trong hồ sơ R15 đã xác định niên đại. Góc ngang tầm sân ga, nhìn dọc đường ray vào điểm tụ x=.72,y=.42; mép sân ga ở một phần ba dưới. Vòm, gạch và khoảng thông thoáng theo nguồn. Chỉ vẽ kiến trúc nền, không tàu, người hoặc biển chữ. Canvas 3840×2160; tách nền sau và gờ sân ga tiền cảnh để tàu A25 chạy phía sau. Tên ga do compositor nhập. Ghi rõ nếu nguồn là minh họa đời sau.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Tàu vào ga có đích dừng; cắt chi tiết bánh/hơi trước khi quay rộng lần2.
Chi tiết không được xuất hiện: Không đèn LED, cửa chắn sân ga, thẻ Oyster, vòng tròn Underground hiện đại, ray điện thứ ba nếu chưa kiểm chứng.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Tàu vào ga có đích dừng; cắt chi tiết bánh/hơi trước khi quay rộng lần2.

**Ranh giới nội dung:** Không đèn LED, cửa chắn sân ga, thẻ Oyster, vòng tròn Underground hiện đại, ray điện thứ ba nếu chưa kiểm chứng.

**Tham chiếu cần mở trước:** R15, R16

### A25 · Đầu máy và toa đúng giai đoạn 1863

**Ưu tiên:** P1 · **Đoạn lời:** 35, 36, 37

**Mục đích hình:** Khóa công nghệ được nói đến; ngăn nhầm tàu điện.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** steam_locomotive_body.png, steam_locomotive_wheels.png, early_passenger_carriage.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Vẽ đầu máy hơi nước nghiêng ngang sang phải theo hình R16 đã ghi loại và năm. Không tự chọn đầu máy Metropolitan A Class đời 1864 rồi ghi là máy ngày mở tuyến năm 1863. Nếu chưa xác định máy ngày khai trương, gọi là “đầu máy hơi nước minh họa thời kỳ đầu” và bỏ số hiệu. Canvas 3840×2160 alpha; trục ray y=.76, đầu máy rộng 60%. Toa hành khách xuất riêng, cùng tỷ lệ và góc. Thân không có khói gắn liền; bánh tách rời, có mốc tâm.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Thân tiến tới vị trí dừng, bánh quay đúng tốc độ tương đối, hơi thoát lên; không giật tàu qua khung lặp.
Chi tiết không được xuất hiện: Không đầu máy Mỹ viễn Tây, tàu điện, ống khói quá cao so với đường hầm; không số hiệu tự bịa.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Thân tiến tới vị trí dừng, bánh quay đúng tốc độ tương đối, hơi thoát lên; không giật tàu qua khung lặp.

**Ranh giới nội dung:** Không đầu máy Mỹ viễn Tây, tàu điện, ống khói quá cao so với đường hầm; không số hiệu tự bịa.

**Tham chiếu cần mở trước:** R16

### A26 · Cận cơ cấu bánh đầu máy

**Ưu tiên:** P2 · **Đoạn lời:** 36, 37

**Mục đích hình:** Cho thấy động lực hơi nước bằng một cận cảnh có thông tin.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** wheel_detail_back.png, wheel_detail_rotor.png, wheel_detail_rod.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa A25 đã khóa, cắt góc ngang gần một cụm bánh chủ động và thanh truyền, không đổi thiết kế. Canvas 2560×1440 alpha; bánh và tay quay là layer riêng, tọa độ pivot ghi bằng pixel trong sidecar. Thân máy phía sau là lớp riêng. Nếu tư liệu không đủ về thanh truyền, chỉ vẽ bánh và dùng hơi A27 làm tín hiệu; không bịa cơ khí.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Một vòng chuyển động cơ khí hợp lý hoặc chỉ lướt cận bánh với khói; mô tả minh họa, không mô phỏng kỹ thuật.
Chi tiết không được xuất hiện: Không bánh xoay mà thanh truyền đứng xuyên trục, không bánh răng steampunk.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Một vòng chuyển động cơ khí hợp lý hoặc chỉ lướt cận bánh với khói; mô tả minh họa, không mô phỏng kỹ thuật.

**Ranh giới nội dung:** Không bánh xoay mà thanh truyền đứng xuyên trục, không bánh răng steampunk.

**Tham chiếu cần mở trước:** A25, R16

### A27 · Hơi nước tách lớp

**Ưu tiên:** P2 · **Đoạn lời:** 36, 37

**Mục đích hình:** Có phần chuyển động riêng cho tàu mà không phủ cả cảnh bằng hiệu ứng.

**Kho hiện có:** 111/121 là gió/mây thời tiết; không dùng thay hơi đầu máy.

**File cần giao:** steam_01.png, steam_02.png, steam_03.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Ba hình hơi nước nối tiếp của cùng một luồng, xám trắng với viền nâu xám nhẹ và alpha mềm. Xuất riêng trên canvas 2048×2048, điểm phát x=.50,y=.85; lần lượt nhỏ, nở rồi tan. Không chứa đầu máy hoặc chữ.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Khói rời ống rồi bay lên và tan. Không lặp suốt phim, không che đầu máy hoặc đẩy khói vào mặt người dẫn.
Chi tiết không được xuất hiện: Không khói nổ, lửa, hiệu ứng chiến tranh hoặc âm thanh sai ngữ cảnh.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Khói rời ống rồi bay lên và tan. Không lặp suốt phim, không che đầu máy hoặc đẩy khói vào mặt người dẫn.

**Ranh giới nội dung:** Không khói nổ, lửa, hiệu ứng chiến tranh hoặc âm thanh sai ngữ cảnh.

**Tham chiếu cần mở trước:** A25

### A28 · Cận cửa toa thời đầu đường sắt ngầm

**Ưu tiên:** P2 · **Đoạn lời:** 35, 37

**Mục đích hình:** Thay góc máy sang vị trí hành khách, tránh chỉ có đại cảnh ga.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** carriage_window_frame.png, carriage_window_front.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Khung cửa toa gỗ và một phần ghế theo R16, nhìn từ trong ra ngoài ngang tầm mắt. Cửa sổ trong suốt ở x=.30–.82,y=.16–.68; chỉ giữ nội thất mép trái và dưới. Không người. Tách gờ cửa tiền cảnh.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Cảnh ngoài chuyển ngang rồi dừng cùng tàu. Người dẫn nhìn theo hướng tàu chạy.
Chi tiết không được xuất hiện: Không cửa tự động, kính panorama hoặc màn hình quảng cáo.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Cảnh ngoài chuyển ngang rồi dừng cùng tàu. Người dẫn nhìn theo hướng tàu chạy.

**Ranh giới nội dung:** Không cửa tự động, kính panorama hoặc màn hình quảng cáo.

**Tham chiếu cần mở trước:** R16, A25

### A29 · Cặp kiếm đeo samurai: đạo cụ nhận diện

**Ưu tiên:** P1 · **Đoạn lời:** 34, 35, 38, 40

**Mục đích hình:** Nhấn biểu tượng địa vị có nguồn thay vì võ sĩ fantasy.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** samurai_long_sheathed.png, samurai_short_sheathed.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Cặp kiếm dài và ngắn trong vỏ, tham chiếu bộ daisho thời Edo ở R17. Nhìn ngang hơi từ trên, chuôi bên trái, vỏ kéo sang phải; hai kiếm là hai file riêng, canvas 2560×1440 alpha. Chỉ dùng hoa văn thấy trong hiện vật.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Khi lời kể chuyển sang thay đổi pháp lý, thay hình tượng đặc quyền bằng nhãn mốc. Người trong R18 vẫn còn; con người không biến mất cùng thanh kiếm.
Chi tiết không được xuất hiện: Không kiếm fantasy, họa tiết tự bịa, lưỡi sáng laser hoặc cảnh rút kiếm tấn công.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Khi lời kể chuyển sang thay đổi pháp lý, thay hình tượng đặc quyền bằng nhãn mốc. Người trong R18 vẫn còn; con người không biến mất cùng thanh kiếm.

**Ranh giới nội dung:** Không kiếm fantasy, họa tiết tự bịa, lưỡi sáng laser hoặc cảnh rút kiếm tấn công.

**Tham chiếu cần mở trước:** R17, R18

### A30 · Khung cửa nhà Edo dùng cho người dẫn

**Ưu tiên:** P2 · **Đoạn lời:** 38, 39

**Mục đích hình:** Một góc vừa để kể đời người đi qua thay đổi chế độ.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** edo_doorway_back.png, edo_post_foreground.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Theo ảnh kiến trúc dân dụng Edo R19: một đoạn hiên, cột gỗ và cửa trượt đóng; góc ngang, không phải toàn phố. Canvas 3840×2160; cột ở x=.16, ngưỡng y=.77, vùng x=.30–.65 để ghép Mỏ Đen. Tách cột trước và nền hiên.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Mỏ Đen nhìn mốc 1868→1876 rồi cắt sang ảnh người thuộc giai đoạn chuyển tiếp. Ngôi nhà không biến thành Tokyo.
Chi tiết không được xuất hiện: Không hoa anh đào hoặc cổng torii trang trí; không khẳng định đây là nhà của một samurai cụ thể.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Mỏ Đen nhìn mốc 1868→1876 rồi cắt sang ảnh người thuộc giai đoạn chuyển tiếp. Ngôi nhà không biến thành Tokyo.

**Ranh giới nội dung:** Không hoa anh đào hoặc cổng torii trang trí; không khẳng định đây là nhà của một samurai cụ thể.

**Tham chiếu cần mở trước:** R19

### A31 · Khay mẫu tự nhiên và góc làm việc khoa học

**Ưu tiên:** P2 · **Đoạn lời:** 43, 45, 46

**Mục đích hình:** Gợi quá trình tích lũy trước thành tựu thay vì chỉ giữ một chân dung.

**Kho hiện có:** Ảnh 022 (hộp mẫu) và 110 (bọ) có thể tái sử dụng. Chỉ tạo khay mới nếu cần góc nhìn từ trên.

**File cần giao:** specimen_tray_blank.png, shell_generic.png, leaf_dry_generic.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Khay gỗ ba ô chứa mẫu tự nhiên tổng quát: vỏ sò, lá khô và một bọ nhỏ. Tách khay và từng mẫu thành lớp riêng. Góc nhìn từ trên; canvas 2560×1440, không chữ hoặc mã hồ sơ. Đây không phải bộ mẫu của Darwin. Nếu cần bằng chứng, dùng ảnh R20 đã xác minh. Màu olive và nâu kem, theo nét bộ 198 ảnh.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Đưa mẫu vào theo nhịp lời kể về học tập và công việc. Không gắn kính hiển vi hiện đại với Darwin.
Chi tiết không được xuất hiện: Không tự vẽ sổ tay Darwin; không dùng con bọ làm bằng chứng cho một phát hiện cụ thể.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Đưa mẫu vào theo nhịp lời kể về học tập và công việc. Không gắn kính hiển vi hiện đại với Darwin.

**Ranh giới nội dung:** Không tự vẽ sổ tay Darwin; không dùng con bọ làm bằng chứng cho một phát hiện cụ thể.

**Tham chiếu cần mở trước:** R20

### A32 · Sách xuất bản năm 1859: bìa nền có khóa nguồn

**Ưu tiên:** P1 · **Đoạn lời:** 43, 45

**Mục đích hình:** Có chủ thể xuất bản rõ; chữ bìa chỉ lấy từ ảnh nguồn hoặc typesetting chính xác.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** origin_book_blank_cover.png, origin_book_pageblock.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa vào bản đầu On the Origin of Species năm 1859 trong R21. Tạo khối sách minh họa đúng màu và tỷ lệ bìa, góc ba phần tư nhẹ, gáy bên trái. Canvas 2560×2560 alpha. Xuất bìa trống và khối ruột riêng để compositor ghép ảnh bìa/trang tên thật. Không sinh chữ.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Mốc 1859 xuất hiện khi sách vào hình; sau đó chuyển sang sự kiện năm 1860.
Chi tiết không được xuất hiện: Không gọi bản tái bản là bản đầu; không đặt DNA xoắn kép lên bìa năm 1859.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Mốc 1859 xuất hiện khi sách vào hình; sau đó chuyển sang sự kiện năm 1860.

**Ranh giới nội dung:** Không gọi bản tái bản là bản đầu; không đặt DNA xoắn kép lên bìa năm 1859.

**Tham chiếu cần mở trước:** R21

### A33 · Hộp phiếu biểu tượng cho bầu cử

**Ưu tiên:** P2 · **Đoạn lời:** 43, 45

**Mục đích hình:** Phân biệt đắc cử năm 1860 với nhậm chức năm 1861.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** ballot_box_symbol.png, ballot_blank.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Hộp gỗ đơn giản có khe trên, góc ba phần tư; một phiếu giấy trống đặt phía trên. Canvas 2048×2048 alpha, hộp chiếm 65%. Đây là ký hiệu biên tập, không phục dựng thùng phiếu hoặc lá phiếu năm 1860. Không cờ, con dấu hay tên ứng viên; compositor thêm nhãn.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Phiếu đi vào khe đúng ở từ “đắc cử”; tuổi 51 theo V16 xuất hiện bên dưới.
Chi tiết không được xuất hiện: Không dựng lễ tuyên thệ ở mốc 1860; không máy bỏ phiếu điện tử.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Phiếu đi vào khe đúng ở từ “đắc cử”; tuổi 51 theo V16 xuất hiện bên dưới.

**Ranh giới nội dung:** Không dựng lễ tuyên thệ ở mốc 1860; không máy bỏ phiếu điện tử.

**Tham chiếu cần mở trước:** S_LINCOLN

### A34 · Wright Flyer năm 1903: toàn bộ máy bay

**Ưu tiên:** P1 · **Đoạn lời:** 47, 48, 51

**Mục đích hình:** Khóa cấu trúc và hướng bay của phương tiện; tách đủ lớp cho đoạn bay ngắn.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** flyer_structure.png, flyer_propellers.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa ảnh chuyến bay ngày 17/12/1903 và sơ đồ bảo tàng R22. Vẽ Wright Flyer hai tầng cánh bọc vải, khung gỗ, cánh lái nâng phía trước, bánh lái phía sau và hai cánh quạt đẩy đúng bố trí. Không bánh đáp hiện đại. Góc ba phần tư ngang theo nguồn, mũi sang phải; canvas 3840×2160 alpha. Tách thân/cánh cố định và cặp cánh quạt.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Bay ngang thấp trên bãi. Gắn số liệu 12 giây/37 mét với V17; nếu rút ngắn nhịp phim, ghi là minh họa.
Chi tiết không được xuất hiện: Không máy bay Thế chiến I, động cơ phản lực, bánh xe tự thêm hoặc cabin kín.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Bay ngang thấp trên bãi. Gắn số liệu 12 giây/37 mét với V17; nếu rút ngắn nhịp phim, ghi là minh họa.

**Ranh giới nội dung:** Không máy bay Thế chiến I, động cơ phản lực, bánh xe tự thêm hoặc cabin kín.

**Tham chiếu cần mở trước:** R22

### A35 · Cận vải bọc cánh và khung gỗ Flyer

**Ưu tiên:** P1 · **Đoạn lời:** 48, 52, 56

**Mục đích hình:** Nối hình máy bay với vật liệu thật được mang theo.

**Kho hiện có:** Ảnh 064 (cuộn vải) và 055 (gỗ) là đạo cụ chung, không đại diện hiện vật Flyer.

**File cần giao:** flyer_wing_fabric.png, flyer_wing_frame.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Cận một phần cánh khớp A34/R22: dải vải kem căng trên thanh gỗ mảnh, nhìn xiên từ trên để đọc kết cấu. Canvas 2560×1440; tách vải và thanh gỗ. Không đặt toàn máy bay cùng file. Đây là minh họa cấu tạo, không xác định vị trí cắt hiện vật nếu nguồn không ghi.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Tô sáng vật liệu rồi chuyển sang ảnh hiện vật R24. Không mô phỏng phá hủy máy bay lịch sử.
Chi tiết không được xuất hiện: Không gán vị trí chính xác cho mảnh hiện vật nếu chưa xác minh; không dùng vải nylon hiện đại.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Tô sáng vật liệu rồi chuyển sang ảnh hiện vật R24. Không mô phỏng phá hủy máy bay lịch sử.

**Ranh giới nội dung:** Không gán vị trí chính xác cho mảnh hiện vật nếu chưa xác minh; không dùng vải nylon hiện đại.

**Tham chiếu cần mở trước:** A34, R22, R24

### A36 · Bãi cát và đường phóng Flyer

**Ưu tiên:** P2 · **Đoạn lời:** 48

**Mục đích hình:** Cho chuyến bay điểm bắt đầu và kết thúc có quan hệ rõ với mặt đất.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** kitty_hawk_ground.png, flyer_launch_rail.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa R22: bãi cát phẳng và đường ray phóng thấp, không sân bay. Canvas 3840×2160; chân trời y=.40; ray từ x=.12,y=.77 đến x=.75,y=.65, phối cảnh khớp A34. Xuất bãi và ray riêng, không người hoặc công trình. Khóa phối cảnh trước khi tạo.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Máy bay rời điểm xuất phát, bóng tách khỏi đất. Chuyển sang tư liệu thật trước khi khẳng định thời lượng 12 giây.
Chi tiết không được xuất hiện: Không đường băng nhựa, tháp điều khiển hoặc xe tải hiện đại.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Máy bay rời điểm xuất phát, bóng tách khỏi đất. Chuyển sang tư liệu thật trước khi khẳng định thời lượng 12 giây.

**Ranh giới nội dung:** Không đường băng nhựa, tháp điều khiển hoặc xe tải hiện đại.

**Tham chiếu cần mở trước:** R22, A34

### A37 · Module Mặt Trăng Apollo 11

**Ưu tiên:** P1 · **Đoạn lời:** 18, 49, 52

**Mục đích hình:** Phân biệt tàu đổ bộ với tên lửa phóng; dùng ngắn và đúng.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** apollo11_lm.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Theo ảnh Eagle trong R23, vẽ module Mặt Trăng trên chân đáp: tầng dưới cách nhiệt vàng, tầng trên xám, thang ở đúng mặt nhìn theo nguồn. Canvas 2560×2560 alpha, đủ chân đáp, góc ba phần tư. Không cờ hoặc phi hành gia sinh. Không thêm chữ NASA bằng AI; nhận diện phải theo ảnh nguồn.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Đặt trên A38 để neo năm 1969; chuyển sang R24 và sơ đồ nhánh vật liệu khi nhắc mảnh vải.
Chi tiết không được xuất hiện: Không tàu con thoi, Artemis hoặc tên lửa Saturn V trên Mặt Trăng; không gắn vải bên ngoài module.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Đặt trên A38 để neo năm 1969; chuyển sang R24 và sơ đồ nhánh vật liệu khi nhắc mảnh vải.

**Ranh giới nội dung:** Không tàu con thoi, Artemis hoặc tên lửa Saturn V trên Mặt Trăng; không gắn vải bên ngoài module.

**Tham chiếu cần mở trước:** R23

### A38 · Mặt đất Mặt Trăng: vùng đặt module

**Ưu tiên:** P2 · **Đoạn lời:** 18, 49

**Mục đích hình:** Tạo lớp không gian riêng; không ghép Cleopatra và phi hành gia vào một cảnh.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** moon_backdrop.png, moon_ground_foreground.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Mặt đất xám có bụi mịn và đá nhỏ theo ảnh Apollo 11 trong R23; địa hình tương đối bằng, trời đen. Canvas 3840×2160; chân trời y=.38; vùng đặt module x=.40–.80,y=.60–.82. Tách nền xa và đất gần. Ghi “minh họa” ngoài hình.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Chỉ dùng làm cảnh thiết lập ngắn, sau đó cắt sang chân đổ bộ, ảnh thật hoặc niên biểu. Không dùng nền cho mọi câu về khoảng cách.
Chi tiết không được xuất hiện: Không phóng đại Trái Đất; không mây, kim tự tháp hoặc dấu chân trước khi có người đổ bộ.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Chỉ dùng làm cảnh thiết lập ngắn, sau đó cắt sang chân đổ bộ, ảnh thật hoặc niên biểu. Không dùng nền cho mọi câu về khoảng cách.

**Ranh giới nội dung:** Không phóng đại Trái Đất; không mây, kim tự tháp hoặc dấu chân trước khi có người đổ bộ.

**Tham chiếu cần mở trước:** R23

### A39 · Mảnh vải đi Apollo: bản vẽ hiện vật có đối chiếu

**Ưu tiên:** P1 · **Đoạn lời:** 52, 53, 56

**Mục đích hình:** Phân biệt hiện vật cụ thể với cuộn vải minh họa chung.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** apollo_flyer_fabric.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Chỉ dựng sau khi lấy được ảnh hiện vật R24. Giữ đường viền và tỷ lệ theo catalog; một mảnh vải riêng trên nền alpha, nhìn trực diện. Không ép thành hình chữ nhật nếu nguồn khác dạng. Canvas 2048×2048; vật chiếm khoảng 60%. Ghi “minh họa theo hiện vật”; ảnh thật phải xuất hiện trước. Nếu thiếu nguồn, dùng ký hiệu trung tính V19.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Từ ảnh nguồn R24 chuyển sang bản minh họa có viền khớp. Apollo là nhánh riêng đi và về.
Chi tiết không được xuất hiện: Không dùng cuộn vải 064, không bịa số niêm phong, không gọi hình sinh là ảnh hiện vật thật.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Từ ảnh nguồn R24 chuyển sang bản minh họa có viền khớp. Apollo là nhánh riêng đi và về.

**Ranh giới nội dung:** Không dùng cuộn vải 064, không bịa số niêm phong, không gọi hình sinh là ảnh hiện vật thật.

**Tham chiếu cần mở trước:** R24

### A40 · Mảnh gỗ đi Apollo: bản vẽ hiện vật có đối chiếu

**Ưu tiên:** P1 · **Đoạn lời:** 52, 53

**Mục đích hình:** Lời đọc nêu cả vải và gỗ; thể hiện đủ hai vật chứng.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** apollo_flyer_wood.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa hồ sơ R24 nhưng vẽ riêng mảnh gỗ. Giữ đường viền, hướng thớ và tỷ lệ dài/rộng theo nguồn; không tự suy kích thước. Canvas 2048×2048 alpha, vật chiếm khoảng 60%. Vân gỗ nhẹ, không giống khúc củi lớn. Compositor thêm tên và kích thước nếu catalog có.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Hai vật cùng nhánh Apollo; chỉ gắn gỗ với hành trình năm 1969, không đưa sang Ingenuity.
Chi tiết không được xuất hiện: Không dùng gỗ 055 làm vật chứng; không tưởng tượng vết cháy hoặc lỗ đinh.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Hai vật cùng nhánh Apollo; chỉ gắn gỗ với hành trình năm 1969, không đưa sang Ingenuity.

**Ranh giới nội dung:** Không dùng gỗ 055 làm vật chứng; không tưởng tượng vết cháy hoặc lỗ đinh.

**Tham chiếu cần mở trước:** R24

### A41 · Mảnh vải khác đi Ingenuity

**Ưu tiên:** P1 · **Đoạn lời:** 54, 56

**Mục đích hình:** Phân biệt hai mảnh, tránh kể thành hành trình từ Mặt Trăng đến Sao Hỏa.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** ingenuity_flyer_fabric.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dùng ảnh hoặc sơ đồ vị trí mảnh vải trên Ingenuity từ R25. Vẽ riêng theo mảnh này; không nhân đôi A39 rồi đổi màu. Nếu nguồn thiếu ảnh chi tiết đáng tin, dùng ký hiệu vải trung tính V19 ghi “mảnh khác”. Canvas 2048×2048 alpha; không tự thêm logo, vít hoặc tem.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Nhánh Ingenuity xuất phát riêng từ Flyer, không nối từ Mặt Trăng. Hiện chữ “mảnh khác” cùng lúc.
Chi tiết không được xuất hiện: Không kể một mảnh đi cả hai chuyến; không đặt mảnh gỗ trên Ingenuity nếu chưa có nguồn.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Nhánh Ingenuity xuất phát riêng từ Flyer, không nối từ Mặt Trăng. Hiện chữ “mảnh khác” cùng lúc.

**Ranh giới nội dung:** Không kể một mảnh đi cả hai chuyến; không đặt mảnh gỗ trên Ingenuity nếu chưa có nguồn.

**Tham chiếu cần mở trước:** R25

### A42 · Ingenuity: thân và càng đáp

**Ưu tiên:** P1 · **Đoạn lời:** 54, 55

**Mục đích hình:** Đúng phương tiện bay trên Sao Hỏa, đủ lớp cho cảnh cất và hạ.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** ingenuity_body_legs.png, ingenuity_solar_panel.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa ảnh NASA/JPL R26: thân Ingenuity hình hộp nhỏ bọc cách nhiệt, bốn chân thanh mảnh, hai tầng rotor đồng trục và tấm pin trên cùng theo nguồn. Canvas 2560×2560 alpha, toàn thân từ y=.10 đến .88. Tách thân/chân và tấm pin; rotor ở A43. Không biến thành drone bốn cánh.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Rotor quay; thân nâng lên, treo ổn định rồi hạ. Nếu dùng video thật dài 39,1 giây, giữ đúng tốc độ phát.
Chi tiết không được xuất hiện: Không drone bốn cánh, cánh quạt máy bay hoặc con người trên Sao Hỏa.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Rotor quay; thân nâng lên, treo ổn định rồi hạ. Nếu dùng video thật dài 39,1 giây, giữ đúng tốc độ phát.

**Ranh giới nội dung:** Không drone bốn cánh, cánh quạt máy bay hoặc con người trên Sao Hỏa.

**Tham chiếu cần mở trước:** R26

### A43 · Ingenuity: rotor và bóng độc lập

**Ưu tiên:** P1 · **Đoạn lời:** 55

**Mục đích hình:** Tạo chuyển động bay có cấu trúc thay vì rung cả hình.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** ingenuity_rotor_upper.png, ingenuity_rotor_lower.png, ingenuity_ground_shadow.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Bám A42 và tỷ lệ rotor trong R26. Xuất riêng từng tầng trên canvas 2560×2560 alpha, cùng pivot x=.50 và cùng trục đã khóa. Tạo bóng ellipse mềm thành lớp riêng. Nếu góc nhìn làm xoay 2D sai, dùng vòng quay mờ có ellipse đúng. Không thêm khói.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Hai rotor quay ngược chiều theo thiết kế. Khi thân nâng, bóng nhạt và tách xa vừa phải; kiểm tra độ cao so với mặt đất.
Chi tiết không được xuất hiện: Không để cánh xuyên tấm pin; không dán bóng vào PNG; không jitter giả bay.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Hai rotor quay ngược chiều theo thiết kế. Khi thân nâng, bóng nhạt và tách xa vừa phải; kiểm tra độ cao so với mặt đất.

**Ranh giới nội dung:** Không để cánh xuyên tấm pin; không dán bóng vào PNG; không jitter giả bay.

**Tham chiếu cần mở trước:** A42, R26

### A44 · Bãi bay Sao Hỏa, góc theo chuyến đầu

**Ưu tiên:** P2 · **Đoạn lời:** 54, 55

**Mục đích hình:** Phân biệt địa hình Sao Hỏa với Mặt Trăng.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** mars_firstflight_back.png, mars_ground_near.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Theo cảnh Mastcam-Z trong R26: đất nâu đỏ nhạt, đá nhỏ thưa, nền xa theo bố cục nguồn. Giữ bầu trời ngoài khung nếu ảnh gốc không có. Canvas 3840×2160; vùng hạ cánh x=.50,y=.76. Tách đất gần và nền xa, không gắn sẵn Ingenuity; khớp hướng sáng với A43.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Bay lên, treo rồi hạ trong cảnh ngắn. Ưu tiên video R26 nếu cần chuyển động thật.
Chi tiết không được xuất hiện: Không tự thêm cỏ, nước, lửa, đô thị Sao Hỏa hoặc miệng núi lửa.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Bay lên, treo rồi hạ trong cảnh ngắn. Ưu tiên video R26 nếu cần chuyển động thật.

**Ranh giới nội dung:** Không tự thêm cỏ, nước, lửa, đô thị Sao Hỏa hoặc miệng núi lửa.

**Tham chiếu cần mở trước:** R26

### A45 · Hai đồ vật gợi tuổi 3 và 69

**Ưu tiên:** P2 · **Đoạn lời:** 47, 50

**Mục đích hình:** Đo tiến bộ bằng một đời người giả định mà không bịa nhân chứng.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** child_shoes_symbol.png, reading_glasses_symbol.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một đôi giày trẻ em trung tính và một cặp kính đọc tròn; mỗi vật một file trên canvas 2048×2048 alpha, góc ba phần tư từ trên, tông nâu kem. Không nhãn hiệu hoặc ảnh gia đình. Đây là ký hiệu trong trường quay hiện tại, không phải đồ vật của nhân chứng sinh năm 1900.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Tuổi 3 và 69 được nhập bằng vector; nối hai vật với mốc 1903 và 1969, ghi “người giả định sinh năm 1900”.
Chi tiết không được xuất hiện: Không gợi rằng mọi người 69 tuổi đều cần gậy; không gán đồ vật cho Wright.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Tuổi 3 và 69 được nhập bằng vector; nối hai vật với mốc 1903 và 1969, ghi “người giả định sinh năm 1900”.

**Ranh giới nội dung:** Không gợi rằng mọi người 69 tuổi đều cần gậy; không gán đồ vật cho Wright.

**Tham chiếu cần mở trước:** REF_STYLE_01

### A46 · Dải phim với một khung ảnh mở

**Ưu tiên:** P1 · **Đoạn lời:** 58, 61, 62, 64

**Mục đích hình:** Cho hình tượng Chaplin bước ra khỏi khung một thời kỳ.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** film_frame_open.png, film_tail_curl.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dải phim 35 mm cách điệu màu đen xám; một khung giữa rỗng, trong suốt thật, lỗ răng cưa vuông đều hai bên. Canvas 3840×2160 alpha; khung ở x=.25–.75,y=.15–.75. Không sinh ảnh Chaplin. Xuất dải trước và đoạn cuộn cong góc dưới phải riêng. Không logo hoặc tiêu đề.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Đặt ảnh phim có nguồn trong khung. Khung trượt khỏi hình khi ảnh Chaplin lớn tuổi xuất hiện cạnh niên biểu.
Chi tiết không được xuất hiện: Không tô màu ảnh phim rồi gọi là ảnh thật; không đồng nhất The Tramp với trang phục Chaplin suốt đời.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Đặt ảnh phim có nguồn trong khung. Khung trượt khỏi hình khi ảnh Chaplin lớn tuổi xuất hiện cạnh niên biểu.

**Ranh giới nội dung:** Không tô màu ảnh phim rồi gọi là ảnh thật; không đồng nhất The Tramp với trang phục Chaplin suốt đời.

**Tham chiếu cần mở trước:** R27, R28

### A47 · Mũ quả dưa và gậy của hình tượng màn ảnh

**Ưu tiên:** P2 · **Đoạn lời:** 58, 61

**Mục đích hình:** Nhận diện The Tramp bằng đạo cụ thay vì lặp chân dung.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** tramp_bowler.png, tramp_cane.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một mũ quả dưa đen và một gậy cong mảnh, nhìn ba phần tư; mỗi vật riêng trên canvas 2048×2048 alpha, không nhân vật. Bám hình dáng phim R27; mũ không thành mũ cao bồi, gậy không thành gậy y tế. Nét mực và bóng phẳng theo bộ minh họa.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Đặt mũ và gậy xuống để câu chuyện về con người lớn tuổi tiếp tục. Không cho Mỏ Đen đóng giả Chaplin.
Chi tiết không được xuất hiện: Không gắn ria mép rời lên mèo, đồng phục quân sự hoặc quảng cáo Apple.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Đặt mũ và gậy xuống để câu chuyện về con người lớn tuổi tiếp tục. Không cho Mỏ Đen đóng giả Chaplin.

**Ranh giới nội dung:** Không gắn ria mép rời lên mèo, đồng phục quân sự hoặc quảng cáo Apple.

**Tham chiếu cần mở trước:** R27

### A48 · Micro thời phim có tiếng

**Ưu tiên:** P2 · **Đoạn lời:** 62

**Mục đích hình:** Nhấn rằng Chaplin không chỉ gắn với phim câm.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** period_microphone.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Micro phòng thu đầu thế kỷ XX có giá đỡ, dựa ảnh R29 nếu dùng đúng cảnh phim năm 1940. Canvas 2048×2048 alpha, nghiêng nhẹ sang phải; không logo hoặc chữ diễn văn. Nếu nguồn không cho thấy micro, dùng biểu tượng âm thanh vector V22 thay vì gán mẫu chính xác.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dùng cùng ảnh phim năm 1940 và biểu tượng âm thanh; không ghép giọng giả đọc diễn văn.
Chi tiết không được xuất hiện: Không micro podcast hiện đại; không trích lời phim ngoài kịch bản.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dùng cùng ảnh phim năm 1940 và biểu tượng âm thanh; không ghép giọng giả đọc diễn văn.

**Ranh giới nội dung:** Không micro podcast hiện đại; không trích lời phim ngoài kịch bản.

**Tham chiếu cần mở trước:** R29

### A49 · Apple I: bo mạch năm 1976

**Ưu tiên:** P1 · **Đoạn lời:** 59, 60

**Mục đích hình:** Thay điện thoại bằng công nghệ đúng thời kỳ.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** apple1_board.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dựa ảnh Apple I trong catalog R30. Bo mạch nằm ngang, nhìn ba phần tư từ trên; giữ đúng nhóm và khối linh kiện, không biến thành bo mạch PC năm 1995. Canvas 2560×2048 alpha; chiếm 75% chiều rộng. Không màn hình, bàn phím hoặc vỏ tích hợp. Không sinh chữ/logo; compositor thêm tên Apple I nếu cần.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Ảnh hiện vật R30 xuất hiện trước; sau đó sơ đồ đi cạnh mốc năm 1976. Không đặt bo mạch trong tay Chaplin.
Chi tiết không được xuất hiện: Không Macintosh 1984, Apple II 1977, iPhone hoặc logo phát sáng trên laptop.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Ảnh hiện vật R30 xuất hiện trước; sau đó sơ đồ đi cạnh mốc năm 1976. Không đặt bo mạch trong tay Chaplin.

**Ranh giới nội dung:** Không Macintosh 1984, Apple II 1977, iPhone hoặc logo phát sáng trên laptop.

**Tham chiếu cần mở trước:** R30, S_APPLE

### A50 · Màn hình CRT và bàn phím rời thời máy tính sớm

**Ưu tiên:** P2 · **Đoạn lời:** 60

**Mục đích hình:** Cho thấy cấu hình máy tính đời đầu, không để khán giả tự hình dung iPhone năm 1976.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** early_crt_frame.png, early_keyboard.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Theo ảnh hệ Apple I trong R30, vẽ màn hình CRT và bàn phím rời. Không khẳng định đây là bộ phụ kiện bán kèm tiêu chuẩn nếu catalog không nói. Màn hình trống trong suốt, ở x=.23–.77,y=.18–.62 trên canvas 2048×2048; góc ba phần tư nhẹ. Tách vỏ và lớp che. Thêm ánh xanh phosphor ở hậu kỳ; không sinh chữ.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Chuyển từ bo mạch sang thiết bị rời; ghi “cấu hình minh họa”. Nếu thiếu nguồn, chỉ dùng bo mạch A49.
Chi tiết không được xuất hiện: Không bắt buộc có chuột; không nút Start, giao diện hiện đại hoặc logo Apple mới trên máy cũ.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Chuyển từ bo mạch sang thiết bị rời; ghi “cấu hình minh họa”. Nếu thiếu nguồn, chỉ dùng bo mạch A49.

**Ranh giới nội dung:** Không bắt buộc có chuột; không nút Start, giao diện hiện đại hoặc logo Apple mới trên máy cũ.

**Tham chiếu cần mở trước:** R30

### A51 · Máy PC giữa thập niên 1990

**Ưu tiên:** P1 · **Đoạn lời:** 66, 70

**Mục đích hình:** Đặt Windows 95 trên máy đúng thời, không gán thao tác cho Bảo Đại.

**Kho hiện có:** Kho 198 PNG không có chủ thể đặc thù này.

**File cần giao:** pc1995_monitor_frame.png, pc1995_tower.png, pc1995_keyboard_mouse.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Máy PC để bàn màu be, màn hình CRT tỷ lệ 4:3, thùng máy hộp, bàn phím và chuột có dây; tách từng bộ phận theo thiết bị R33. Góc ba phần tư nhẹ từ trái, canvas 3840×2160 alpha. Màn hình ở x=.48–.77,y=.18–.62, chừa lỗ trong suốt để ghép giao diện Windows 95 thật từ R32. Không người hoặc nội thất cung đình. Đây là máy tính giả định của khán giả hiện nay, không phải đồ của Bảo Đại.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Con trỏ đi vào nút Start trên ảnh giao diện thật; cắt sang chân dung Bảo Đại bằng khung tách rõ.
Chi tiết không được xuất hiện: Không màn hình phẳng, laptop, RGB, Windows XP/11, iPhone hoặc Bảo Đại dùng chuột.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Con trỏ đi vào nút Start trên ảnh giao diện thật; cắt sang chân dung Bảo Đại bằng khung tách rõ.

**Ranh giới nội dung:** Không màn hình phẳng, laptop, RGB, Windows XP/11, iPhone hoặc Bảo Đại dùng chuột.

**Tham chiếu cần mở trước:** R32, R33

### A52 · Ghế trống trong cảnh máy tính ví von

**Ưu tiên:** P2 · **Đoạn lời:** 70

**Mục đích hình:** Thể hiện câu từ chối suy diễn bằng chỗ ngồi trống có chủ đích.

**Kho hiện có:** Ghế 005 có thể tái dùng nếu góc phù hợp với bố cục PC đã khóa.

**File cần giao:** empty_computer_chair.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Một ghế làm việc xám đơn giản, không nhãn, nhìn từ sau ba phần tư; canvas 2048×2048 alpha. Khớp góc bàn A51, ghế bên trái PC. Không người, áo bào, gậy hoặc vương miện. Mặt ghế và lưng đọc rõ, không chiếm màn hình. Đây là đạo cụ ví von hiện tại cho đoạn 70.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dừng máy quay trên ghế trống đúng câu “không có bằng chứng”, rồi trở về niên biểu. Không lấp ghế bằng nhân vật lịch sử.
Chi tiết không được xuất hiện: Không chân dung Bảo Đại trên lưng ghế; không ám chỉ ông vừa rời ghế.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dừng máy quay trên ghế trống đúng câu “không có bằng chứng”, rồi trở về niên biểu. Không lấp ghế bằng nhân vật lịch sử.

**Ranh giới nội dung:** Không chân dung Bảo Đại trên lưng ghế; không ám chỉ ông vừa rời ghế.

**Tham chiếu cần mở trước:** A51

### C01 · Mỏ Đen — Mỏ Đen ngồi 3/4 nhìn phải

**Ưu tiên:** P1 · **Đoạn lời:** 02, 09, 24, 29, 35

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c01_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Ngồi đúng nhận diện trong manifest mo_den_01; xoay toàn thân vừa phải sang phải khoảng 25–30°, đầu nhìn thêm 10° về phải, mắt vào mục tiêu ngoài khung. Hai chân trước nghỉ trước bụng; miệng khép, tò mò. Giữ nguyên tai, mặt nạ nâu, mắt xanh xám, bụng kem, chân và đuôi.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dùng khi Mỏ Đen dẫn mắt vào vật chứng bên phải. Đây là ảnh pose mới cần kiểm tra nhận diện; không lật gương file hiện có.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dùng khi Mỏ Đen dẫn mắt vào vật chứng bên phải. Đây là ảnh pose mới cần kiểm tra nhận diện; không lật gương file hiện có.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C02 · Mỏ Đen — Mỏ Đen ngồi 3/4 nhìn trái

**Ưu tiên:** P1 · **Đoạn lời:** 03, 17, 42, 66

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c02_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Dùng cùng model sheet đã duyệt: thân xoay khoảng 25° sang trái, đầu và mắt nhìn trái, hai chân trước nghỉ, miệng khép, một bên mày hơi nâng. Không phản chiếu ngang PNG cũ; phải vẽ lại các mảng mặt và đuôi nhất quán.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Đối góc với C01 ở bố cục chân dung đôi hoặc cảnh PC.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Đối góc với C01 ở bố cục chân dung đôi hoặc cảnh PC.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C03 · Mỏ Đen — Mỏ Đen chỉ sang phải

**Ưu tiên:** P1 · **Đoạn lời:** 04, 12, 18, 48

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c03_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Mèo ngồi theo đúng model sheet, góc 3/4 sang phải. Một chân trước mở và vươn chéo tới điểm ngoài thân ở phía trên phải; bàn chân vẫn là bàn chân mèo cách điệu, không ngón tay người. Chân còn lại tựa trước bụng. Mắt nhìn đúng đầu ngón/chân đang chỉ. Toàn thân, tai, đuôi nằm trọn canvas alpha.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dùng với đường thời gian, mốc Apollo hoặc điểm cần chú ý; vẽ mũi tên riêng.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dùng với đường thời gian, mốc Apollo hoặc điểm cần chú ý; vẽ mũi tên riêng.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C04 · Mỏ Đen — Mỏ Đen chỉ sang trái

**Ưu tiên:** P1 · **Đoạn lời:** 03, 30, 43, 67

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c04_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Cùng quy tắc nhận diện như C03 nhưng thân xoay trái và chân trước chỉ về phía trái. Vẽ lại đúng giải phẫu cách điệu từ reference; không mirror để tạo bên trái. Giữ cổ tay/bàn chân rõ, chân còn lại tựa thân, mắt nhìn mục tiêu.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dùng đối góc theo bố cục và hướng nhìn; không lặp ở mọi đoạn.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dùng đối góc theo bố cục và hướng nhìn; không lặp ở mọi đoạn.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C05 · Mỏ Đen — Mỏ Đen giữ thước đo

**Ưu tiên:** P1 · **Đoạn lời:** 12, 14, 18, 73

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c05_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Mỏ Đen ngồi chính diện 3/4. Hai chân trước đỡ một cây thước gỗ thẳng nằm ngang trước bụng; các đầu bàn chân ôm mép thước có tiếp xúc rõ. Xuất một bản thân không đạo cụ và một lớp chân trước riêng để compositor đặt thước thật đúng phối cảnh. Giữ thước rời; không in vạch/số bằng AI.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Cử chỉ nâng thước hoặc đặt thước xuống phải căn câu đọc; không làm thước cong.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Cử chỉ nâng thước hoặc đặt thước xuống phải căn câu đọc; không làm thước cong.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C06 · Mỏ Đen — Mỏ Đen cầm thẻ tư liệu trống

**Ưu tiên:** P2 · **Đoạn lời:** 06, 29, 52, 56

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c06_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Mỏ Đen nhìn khán giả, hai chân trước đỡ mép dưới một thẻ trống ngang trước ngực. Thẻ là hình chữ nhật kem riêng, không chữ/ảnh giả. Hai chân trước phải phủ lên mép thẻ đúng lớp; mặt mèo và mắt không bị che. Tạo một file nhân vật không thẻ và một file hai chân trước cho compositing.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Chỉ dùng khi người dẫn đưa tài liệu ra; ảnh/tư liệu thật ghép sau, có nguồn.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Chỉ dùng khi người dẫn đưa tài liệu ra; ảnh/tư liệu thật ghép sau, có nguồn.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C07 · Mỏ Đen — Mỏ Đen mở ngăn kéo

**Ưu tiên:** P1 · **Đoạn lời:** 02, 08, 73

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c07_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Theo đúng pose master, ngồi cạnh tủ A01. Thân nghiêng nhẹ về phía tủ, mắt nhìn tay nắm; một chân trước vươn ngắn tới tay nắm, có điểm tiếp xúc tự nhiên, không kéo dài như cánh tay người. Chân sau giữ trên mặt đất. Xuất thân và chân trước che tay nắm thành hai file cùng canvas. Không vẽ tủ vào ảnh mèo.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Tạo thêm pose buông tay nếu cần; chuyển động chính do ngăn kéo A02 trượt ra.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Tạo thêm pose buông tay nếu cần; chuyển động chính do ngăn kéo A02 trượt ra.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C08 · Mỏ Đen — Mỏ Đen nhìn qua vai vào bằng chứng

**Ưu tiên:** P1 · **Đoạn lời:** 15, 26, 52, 55

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c08_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Góc nhìn sau vai nhưng vẫn thấy một phần má và mặt nạ bên phải; dùng chính silhouette, tai, đuôi và màu lông trong model sheet. Thân ngồi hướng vào vùng chứng cứ bên phải, không tự thiết kế lưng mới. Toàn thân nằm gọn trong canvas, không crop để giấu cấu trúc.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Đặt nhân vật nhỏ vừa phải để dẫn mắt tới vật chứng; không che chủ thể.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Đặt nhân vật nhỏ vừa phải để dẫn mắt tới vật chứng; không che chủ thể.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C09 · Mỏ Đen — Mỏ Đen nhìn xuống mặt bàn

**Ưu tiên:** P2 · **Đoạn lời:** 13, 45, 53, 63

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c09_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Mèo ngồi 3/4, đầu cúi vừa khoảng 12–15°, mắt nhìn điểm thấp bên phải như đang cân nhắc hiện vật. Hai chân trước gần bụng, không chạm vật nếu chưa có lớp bàn tay tương ứng. Miệng khép, suy nghĩ tập trung; giữ đặc điểm gương mặt đúng master.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dùng một nhịp phản ứng rồi cắt sang chi tiết vật chứng.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dùng một nhịp phản ứng rồi cắt sang chi tiết vật chứng.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

### C10 · Mỏ Đen — Mỏ Đen mời khán giả nhìn lại

**Ưu tiên:** P2 · **Đoạn lời:** 16, 28, 40, 57, 72

**Mục đích hình:** Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.

**Kho hiện có:** 24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.

**File cần giao:** c10_pose.png

**PROMPT — sao chép nguyên khối:**

```text
Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.
Ngồi thẳng đối diện khán giả, giữ tỉ lệ master. Một chân trước mở nhẹ sang bên như lời mời quan sát, thấp ngang ngực; chân kia tựa bụng. Biểu cảm bình tĩnh, ấm, miệng nhỏ; không cười rộng. Canvas vuông RGBA, toàn thân, chân và đuôi không bị cắt.
Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.
CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.
Lớp chuyển động cần phục vụ hành động sau: Dùng cho câu hỏi/kết luận. Đây là pose tĩnh, không tạo môi nói hay rig giả.
Chi tiết không được xuất hiện: Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.
Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.
```

**Thiết kế chuyển động/diễn tiến:** Dùng cho câu hỏi/kết luận. Đây là pose tĩnh, không tạo môi nói hay rig giả.

**Ranh giới nội dung:** Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.

**Tham chiếu cần mở trước:** assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.

## II. Tư liệu thật cần tìm/tải, không dùng ảnh tạo sinh

Các mục R là công việc nghiên cứu, xin quyền/tải và ghi credit. “Chưa có trong kho” không đồng nghĩa “chưa tồn tại trên Internet”. Mở nguồn gốc, kiểm tra quyền của chính file được chọn và ghi vào registry; link cơ quan bên dưới là đầu mối, không phải phê duyệt sử dụng.

| ID | Đoạn lời | Tư liệu cần lấy và điều kiện | Không chấp nhận |
|---|---|---|---|
| **R01 · [Quang Trung / Nguyễn Huệ: hình đại diện có nguồn](https://baotanglichsuquocgia.vn/vi/Articles/3097/15721/ky-niem-225-nam-1789-2014-hoang-dje-quang-trung-nguyen-hue-djai-pha-quan-xam-luoc-man-thanh.html)** | 01,03–07,71 | Tìm tranh hoặc tượng do bảo tàng/cơ quan di sản định danh; lưu toàn ảnh, crop mặt riêng và caption. Ghi tác giả, thời điểm tác phẩm, nơi lưu giữ. Gắn nhãn “tranh/tượng minh họa đời sau” nếu không phải ảnh đương thời. Không dùng diễn viên phim làm ảnh thật. | Không gọi chân dung minh họa là ảnh chụp người thật. |
| **R02 · [George Washington: chân dung Lansdowne](https://npg.si.edu/object/npg_NPG.2001.13)** | 01,03–07,71 | Lấy toàn bộ Lansdowne Portrait của Gilbert Stuart, 1796, từ Smithsonian National Portrait Gallery (NPG.2001.13) hoặc nguồn có quyền tương đương; giữ file gốc và credit. Tạo crop mặt từ chính ảnh đó. Đây là chân dung năm 1796, không phải hình lễ nhậm chức năm 1789. | Không tái tạo lại chân dung bằng AI; không ghi ảnh này là tại lễ nhậm chức. |
| **R03 · [Lễ tuyên thệ Washington tại New York, 30/4/1789](https://www.mountvernon.org/george-washington/the-first-president/inauguration/timeline)** | 05 | Tìm tranh/khắc/tư liệu sự kiện có tác giả và niên đại tác phẩm; caption phải phân biệt tranh hồi cố với tư liệu đương thời. Ưu tiên khung có Washington và bối cảnh nghi lễ, không cần đám đông trang trí. Dùng ảnh Federal Hall hiện nay chỉ khi ghi là địa điểm hiện nay. | Không đổi New York thành Washington DC; không gọi tranh đời sau là ảnh chụp 1789. |
| **R04 · Đại kim tự tháp Khufu ở Giza: ảnh toàn thể** | 09,17–24,28 | Chọn ảnh hiện nay có caption xác định Pyramid of Khufu, góc nhận ra đúng kim tự tháp giữa quần thể Giza, độ phân giải đủ crop. Lưu cảnh gốc và crop. Đây là ảnh di tích hiện nay, chỉ làm khóa hình kiến trúc; không đại diện công trường cổ. | Không lấy kim tự tháp Maya hoặc kim tự tháp Khafre rồi đổi nhãn. |
| **R05 · [Hiện vật vữa thuộc Đại kim tự tháp](https://www.metmuseum.org/art/collection/search/558193)** | 09–15 | Tải hồ sơ The Met object 17.6.143: Specimen of Mortar from the Great Pyramid, ca. 2550 BCE, reign of Khufu. Giữ tên hiện vật/caption đúng. Lời giải thích tư liệu trong ZIP đã gọi sai nó là phù điêu trận chiến; cần sửa chú thích nguồn trước dựng. Bổ sung một ảnh cận đá Giza có caption riêng nếu cần texture. | Không phóng mẫu vữa thành ảnh tường đá; không gọi là phù điêu. |
| **R06 · [Cleopatra VII: đồng xu hoặc hiện vật được catalog](https://www.britishmuseum.org/collection/term/BIOG57627)** | 17–21 | Chọn hiện vật có hồ sơ bảo tàng ghi rõ Cleopatra VII, số catalog, niên đại và nơi lưu giữ; ảnh đủ lớn để đọc chân dung nghiêng/biểu tượng. Lấy mặt trước/sau nếu có và giữ caption. Nếu dùng tác phẩm đời sau phải ghi rõ đó là hình dung hậu thế. | Không dùng Nefertiti, nữ hoàng phim, hay ảnh AI gắn thành Cleopatra. |
| **R07 · [Apollo 11: ảnh thật trên bề mặt Mặt Trăng](https://www.nasa.gov/missions/apollo/apollo-11/apollo-11-mission-overview/)** | 18–19,49,52–53 | Chọn ảnh NASA Apollo 11 có mã frame/caption xác định module, phi hành gia hoặc cảnh bề mặt. Lưu ảnh gốc, caption, credit và danh tính người trong ảnh khi biết. Một crop phải truy ngược về ảnh gốc. | Không trộn Apollo khác, không ghép Cleopatra vào cùng cảnh lịch sử. |
| **R08 · [Ma mút lông xoăn: mô hình hoặc bộ xương khoa học](https://www.nhm.ac.uk/discover/were-all-mammoths-woolly.html)** | 22–26 | Chọn ảnh bảo tàng ghi rõ woolly mammoth, ưu tiên ảnh toàn thân nghiêng và cận đầu/ngà để khóa A13–A15. Ghi đó là mô hình phục dựng hay bộ xương. Kiểm tra quyền ảnh riêng. | Không yêu cầu ảnh chụp ma mút sống; không gọi mô hình là sinh vật thật. |
| **R09 · [Đảo Wrangel: ảnh hiện nay có định danh](https://pmc.ncbi.nlm.nih.gov/articles/PMC6121868/)** | 23–26 | Tìm ảnh lãnh nguyên/bờ biển do đơn vị nghiên cứu hoặc bảo tồn ghi địa danh Wrangel, kèm credit. Dùng để khóa địa hình tổng quát hiện nay; ảnh hiện đại không chứng minh mùa hoặc cảnh năm 2000 TCN. | Không thay bằng ảnh bất kỳ ở Greenland/Svalbard; không tuyết dày mặc định. |
| **R10 · [Oxford hiện nay: sinh hoạt hoặc không gian học](https://www.ox.ac.uk/about/the-university/history)** | 29,33–34 | Chọn ảnh Oxford hiện nay có địa điểm/tác giả rõ, có người đi lại hoặc hoạt động học thay vì chỉ mặt tiền trống. Lưu caption và quyền. Nếu dùng Radcliffe Camera, ghi kiến trúc hiện nay, không gắn với năm 1096. | Không dùng công trình đời sau làm hình Oxford năm 1096. |
| **R11 · [Nguồn chính thức cho mốc giảng dạy Oxford 1096](https://www.ox.ac.uk/about/the-university/history)** | 29–34 | Lưu trang lịch sử University of Oxford và đoạn nói có bằng chứng dạy học từ 1096, không có ngày thành lập rõ. Ghi URL, ngày truy cập và trích ý ngắn trong hồ sơ dựng. Nếu đưa screenshot lên hình, giữ nguồn/tiêu đề đủ đọc; đây là trang hiện đại, không phải văn kiện 1096. | Không thiết kế thiệp khai trương đại học năm 1096. |
| **R12 · [Mô hình/sơ đồ Tenochtitlan có niên đại tái hiện](https://www.inah.gob.mx/images/boletines/2025/213/Boletin%20213.pdf)** | 30–32 | Tìm ảnh mô hình hoặc sơ đồ từ INAH/Museo del Templo Mayor hay học thuật có trách nhiệm; lưu tên người làm, giai đoạn được mô tả và quyền ảnh. Cần một góc toàn đô thị giữa hồ và một góc gần kênh/đường đắp. Nếu mô hình biểu diễn đầu thế kỷ XVI, nhãn phải nói đúng giai đoạn đó. | Không lấy thành phố Maya làm Aztec; không gọi mô hình 1519 là hình năm 1325/1428. |
| **R13 · [Di tích Templo Mayor / Tenochtitlan hiện nay](https://www.inah.gob.mx/)** | 30–34 | Chọn ảnh khảo cổ tại địa điểm được định danh, có caption cơ quan quản lý/nhà nghiên cứu và credit. Dùng như dấu tích hiện nay, không phải nguyên trạng thành phố cổ. Cắt sang góc cận có chủ thể, tránh lặp đại cảnh mô hình R12. | Không nhập mọi kim tự tháp Mesoamerica thành một nền văn hóa. |
| **R14 · [Hiện vật/văn hóa ở Mexico có trước 1428](https://deas.inah.gob.mx/pdf/publicaciones/publicaciones/publicacion%2839963%29-3447.pdf)** | 31 | Chọn ít nhất một hiện vật hoặc di tích có hồ sơ xác định cộng đồng, địa điểm và niên đại trước 1428. Lưu caption đầy đủ và quyền. Chỉ khẳng định đúng phạm vi bằng chứng; không dùng một hiện vật đơn lẻ đại diện mọi châu Mỹ. | Không gán mọi cư dân/vật phẩm Mexico trước 1428 là Aztec. |
| **R15 · [London Metropolitan Railway: ga thời kỳ mở tuyến](https://library.ltmuseum.co.uk/Portal/Default/en-GB/RecordView/Index/108)** | 35–37 | Tìm tranh/ảnh ga giai đoạn 1863 từ London Transport Museum hoặc kho tư liệu có catalog; ghi ga, ngày ảnh/tranh và medium. Nếu là tranh hồi cố, ghi “minh họa”. Cần thấy đường ray, mép sân ga và kết cấu mái đủ để khớp A24. | Không dùng ga Tube hiện nay rồi bỏ nhãn thời gian. |
| **R16 · [Đầu máy hơi nước/toa mở tuyến năm 1863](https://library.ltmuseum.co.uk/Portal/Default/en-GB/RecordView/Index/97)** | 35–37 | Tìm catalog museum về đầu máy/toa thực sự phục vụ khai trương Metropolitan Railway ngày 10/1/1863; ghi loại máy, năm chế tạo và ảnh. Cần góc ngang toàn máy, bánh và cửa toa nếu có. Nếu tư liệu chỉ khóa được đầu máy thời kỳ đầu nhưng không phải máy khai trương, chú thích “minh họa thời kỳ đầu” và không đặt số hiệu giả. | Không dùng A Class đặt hàng năm 1864 rồi nói là máy khai trương 1863. |
| **R17 · [Kiếm/giáp samurai cuối Edo có hồ sơ](https://www.vam.ac.uk/articles/samurai-japanese-arms-armour)** | 34–40 | Chọn kiếm có catalog V&A hoặc bảo tàng tương đương, niên đại/giai đoạn rõ; ảnh thấy chuôi và vỏ, thêm cận hiện vật nếu dùng. Giáp phải có nhãn thời kỳ/chức năng, không mặc định ai cũng mặc giáp khi đi lại. Giữ số catalog và quyền ảnh. | Không dùng cosplay, katana fantasy hoặc giáp Trung Hoa. |
| **R18 · [Ảnh samurai thế kỷ XIX có định danh](https://www.vam.ac.uk/articles/samurai-japanese-arms-armour)** | 35,38–40 | Tìm ảnh lưu trữ có caption “samurai”, tên người nếu xác định, nhiếp ảnh gia và niên đại ước tính. Nếu là ảnh studio dàn dựng, ghi rõ. Dùng để cho thấy con người tiếp tục tồn tại qua chuyển đổi địa vị; không vẽ họ biến mất năm 1876. | Không gán người mặc kimono bất kỳ thành samurai năm 1863. |
| **R19 · [Nhà/cửa thời Edo: ảnh hoặc phục dựng có nhãn](https://www.vam.ac.uk/articles/samurai-japanese-arms-armour)** | 38–40 | Chọn tư liệu kiến trúc dân dụng cuối Edo có cơ quan lưu giữ/định danh; ảnh phục dựng hiện nay phải ghi rõ. Chỉ cần hiên, cột, cửa trượt làm khóa góc A30; không cần ảnh toàn phố. | Không gắn nhà phim trường thành ảnh chụp phố Nhật năm 1863. |
| **R20 · [Darwin khoảng năm 1859: chân dung/tài liệu](https://darwinproject.ac.uk/people/about-darwin)** | 42–46 | Ưu tiên chân dung có ngày chụp khoảng 1859 hoặc gần tuổi 50, ghi người chụp và nguồn. Ảnh Darwin già hơn vẫn dùng được nếu ngày ảnh hiện rõ và không gắn nhãn tuổi 50. Sổ/mẫu chỉ dùng khi catalog liên hệ trực tiếp với Darwin. | Không dùng ảnh già rồi chú thích “Darwin 50 tuổi”; không gán mẫu tự nhiên chung cho ông. |
| **R21 · [Bản in đầu On the Origin of Species, 1859](https://darwinproject.ac.uk/people/about-darwin)** | 43,45 | Tìm bìa/trang tên scan từ thư viện khoa học hoặc archive, ghi edition, nhà xuất bản, năm, mã bản. Giữ bản scan gốc; dựng một mặt phẳng phối cảnh từ scan nếu cần. | Không in bìa DNA hiện đại hoặc chữ AI; không trộn ấn bản tái bản với bản đầu. |
| **R22 · [Chuyến bay Wright ngày 17/12/1903](https://science.nasa.gov/photojournal/the-wright-brothers/)** | 47–48,51–52 | Lấy ảnh chuyến bay đầu Wright Flyer có caption xác định ngày, Orville điều khiển và Wilbur tại mặt đất; lưu toàn khung. Bổ sung ảnh/sơ đồ cấu trúc chiếc Flyer 1903 cho A34. Không dùng ảnh chuyến bay khác làm chuyến đầu 12 giây. | Không gán nhầm phi công hoặc dùng máy bay đời sau. |
| **R23 · [Apollo 11 Eagle và vật chứng chuyến đi](https://www.nasa.gov/missions/apollo/apollo-11/apollo-11-mission-overview/)** | 49,52–53 | Lấy ảnh Eagle/module trên Mặt Trăng có frame ID, tên nhiệm vụ và credit NASA; nếu dùng ảnh hiện vật vật liệu đi theo, giữ đúng provenance. Không xóa/vẽ thêm chi tiết lên ảnh nguồn rồi trình bày như bản gốc. | Không gắn mảnh vải lên ngoài module nếu nguồn không chứng minh vị trí. |
| **R24 · [Mảnh vải và gỗ từ Wright Flyer mang trên Apollo 11](https://airandspace.si.edu/collection-objects/wood-and-fabric-1903-wright-flyer-apollo11/nasm_A19721288000)** | 52–53,56 | Tải hồ sơ hiện vật Smithsonian NASM A19721288000. Cần ảnh cận của cả vải và gỗ, tên catalog, mô tả kích thước/provenance, điều kiện sử dụng. Trang hiện có thể chặn tải; nếu không lấy được, tìm NASA/Smithsonian khác có hồ sơ tương đương. Chưa có file ảnh xác minh thì không sinh hình giả hiện vật. | Không thay bằng cuộn vải/gỗ generic; không bỏ mất một trong hai mảnh. |
| **R25 · [Mảnh vải khác trên Ingenuity](https://www.jpl.nasa.gov/images/pia24438-pride-of-the-west-mdash-and-mars/)** | 54,56 | Lấy NASA/JPL PIA24438 “Pride of the West and Mars”; giữ caption nói mảnh muslin 1,3 × 1,3 cm được bọc bảo vệ và gắn dưới tấm pin. Mở ảnh gốc, kiểm vị trí hiển thị và credit trước khi tạo A41. Đây là mảnh khác với vải/gỗ Apollo. | Không sao chép mảnh Apollo và gọi là vật đã chuyển sang Sao Hỏa. |
| **R26 · [Video/ảnh chuyến bay đầu Ingenuity ngày 19/4/2021](https://www.jpl.nasa.gov/images/pia24521-perseverances-mastcam-z-video-of-ingenuitys-first-full-flight/)** | 54–55 | Lấy video NASA/JPL PIA24521/Mastcam-Z gồm cất cánh, treo, hạ; giữ credit và tốc độ phát. Tổng chuyến bay 39,1 giây. Ưu tiên dùng video thật cho chuyển động. | Không gọi render 3D là video thật; nêu đúng “chuyến bay có động cơ, điều khiển đầu tiên trên hành tinh khác”. |
| **R27 · [Chaplin trong vai The Tramp](https://www.charliechaplin.com/en/articles/21-Overview-of-His-Life)** | 58–61 | Chọn still có tên phim/năm và nguồn quyền rõ; một ảnh toàn thân để thấy mũ, gậy, dáng và một crop mặt từ cùng ảnh. Ảnh di sản Chaplin không mặc định tự do thương mại; lưu credit/điều kiện. | Không dùng cosplay hoặc gọi trang phục vai diễn là đồ cả đời Chaplin. |
| **R28 · [Chaplin ngoài hình tượng Tramp ở tuổi trưởng thành/già](https://www.charliechaplin.com/en/articles/21-Overview-of-His-Life)** | 59,61,64 | Chọn chân dung đời thực có người chụp, năm hoặc khoảng năm, nguồn lưu trữ. Không phục hồi mặt bằng AI. Đặt cạnh R27 với ngày ảnh để cho thấy đời ông tiếp tục, không tạo cảm giác ông xuất hiện tại Apple. | Không ghép ria mép/áo The Tramp vào ảnh đời thật. |
| **R29 · [The Great Dictator (1940): xác nhận phim có lời thoại](https://www.charliechaplin.com/en/films/5-The-Great-Dictator)** | 62 | Tìm still/trailer chính thức có credit và tên phim/năm; chỉ cần một hình xác thực, không cần trích diễn văn. Kiểm tra quyền clip/hình riêng. Có thể thay bằng bìa poster lưu trữ nếu quyền rõ. | Không dùng ảnh Hitler thật; không tạo/nhái lời diễn văn hoặc âm thanh Chaplin. |
| **R30 · [Apple I: bo mạch máy tính năm 1976](https://computerhistory.org/apple-timeline/)** | 59–60 | Chọn ảnh hiện vật Apple I của Computer History Museum hoặc catalog đáng tin; lưu tên model, năm và credit. Lấy một ảnh toàn bo mạch và một cận có thể crop. Mọi thiết bị CRT/bàn phím đi kèm phải có nguồn riêng; không mặc định là bộ bán kèm năm 1976. | Không dùng Apple II/Macintosh/iPhone làm Apple I. |
| **R31 · [Bảo Đại thời trị vì: chân dung có nguồn](https://baotanglichsu.vn/VI/Articles/3098/19511/bao-djai-vi-hoang-dje-cuoi-cung-trong-lich-su-phong-kien-viet-nam.html)** | 65–69,71 | Chọn chân dung do Bảo tàng Lịch sử Quốc gia hoặc archive định danh; lưu caption, ngày/ước lượng, credit và quyền. Lấy toàn khung và crop mặt từ cùng file. Ảnh áo bào không tự động là lúc lên ngôi năm 1926. | Không nhầm Khải Định; không vẽ áo bào giả bằng AI. |
| **R32 · [Windows 95: ảnh chụp giao diện thật](https://blogs.windows.com/windows-insider/2020/08/24/looking-back-the-25th-anniversary-of-windows-95/)** | 66,70 | Lấy screenshot đúng Windows 95 có taskbar và Start menu. Dùng desktop và menu mở thành hai trạng thái từ cùng hệ điều hành. Lưu phiên bản/nguồn; không để AI viết chữ trong giao diện. | Không dùng Windows 98/XP/11 hoặc mockup chữ sai. |
| **R33 · [PC CRT giữa thập niên 1990](https://computerhistory.org/)** | 66,70 | Tìm ảnh catalog máy tính để bàn beige với CRT 4:3, thùng máy, bàn phím và chuột có dây; ghi mẫu/năm nếu có. Chỉ làm đạo cụ bối cảnh cho ví von của người kể, không gán là máy của Bảo Đại. | Không laptop, màn hình phẳng hoặc RGB hiện đại. |
| **R34 · [Bảo Đại sau thoái vị: ảnh có ngày/địa điểm](https://baotanglichsu.vn/VI/Articles/3098/19511/bao-djai-vi-hoang-dje-cuoi-cung-trong-lich-su-phong-kien-viet-nam.html)** | 67–69 | Tìm ảnh archive sau 1945 có caption, địa điểm, người chụp và năm; nếu chỉ có ảnh một giai đoạn trước, không chú thích Paris 1997. Dùng ảnh thật có quyền; nếu không có ảnh phù hợp, kể phần sau bằng trục đời người, không sinh mặt già giả. | Không suy ảnh Paris 1997 từ ảnh không ngày; không mô tả ông còn làm vua. |
| **R35 · [Lincoln giai đoạn 1859–1860](https://www.loc.gov/exhibits/lincoln/candidate-lincoln.html)** | 42–46 | Chọn ảnh có catalog LOC và ngày chụp giai đoạn 1859–1860; giữ đúng trạng thái râu trong ảnh. Nếu dùng ảnh giai đoạn bầu cử, caption phải nêu rõ phạm vi. Cần chân dung rõ để đặt tuổi 51 bên dưới. | Không dùng ảnh năm 1864 rồi gọi là Lincoln ở tuổi 51. |
| **R36 · [Nguồn Washington: ngày tháng, lễ nhậm chức](https://www.mountvernon.org/george-washington/the-first-president/inauguration/timeline)** | 03–05 | Lưu Mount Vernon/National Archives hoặc nguồn lịch sử uy tín cho sinh 1732, mất 1799 và nhậm chức tại New York ngày 30/4/1789. Nối URL với từng mệnh đề trong registry; không tạo ảnh giấy chứng nhận. | Không lấy sống đồng thời làm bằng chứng hai người từng biết nhau. |
| **R37 · Hồ Gươm: chỉ dùng làm ví von địa điểm** | 20 | Nếu dùng câu ví von, chọn một ảnh Hồ Gươm hiện nay có địa điểm và quyền ảnh rõ; hoặc bỏ ảnh thật và dùng sơ đồ hai khung chung một địa điểm. Không lấy ảnh người quen hay ghép chân dung lịch sử vào ảnh thật. | Không để “cùng nơi” bị hiểu là “cùng thời”. |

### Điều kiện duyệt tư liệu thật

- Lưu file gốc, URL cụ thể, tên tác giả/cơ quan, caption, số hiện vật/frame, ngày truy cập, quyền/giấy phép và credit cần hiện. Tư liệu web có thể thay đổi hoặc chặn; kiểm tra file thật trước khi dựng.
- Ghi nhãn ảnh hiện nay, tranh hồi cố, mô hình phục dựng, screenshot giao diện và ảnh hiện vật đúng loại của nó. Không gọi tất cả là ảnh lịch sử đương thời.
- Nếu một link là trang tổng quan, tìm tới đúng record ảnh/object; không crop ảnh từ trang tìm kiếm hoặc từ video không rõ nguồn.
- Yêu cầu trích đoạn nhỏ cần thiết trong phim, không sao chép toàn trang/bài nghiên cứu vào video.
- R05: tên catalog trong hồ sơ đầu vào cần đính chính. The Met ghi đây là mẫu vữa từ Đại kim tự tháp, ca.2550 BCE, không phải “phù điêu trận chiến”.
- R24/R25: phân biệt vật liệu Flyer mang trên Apollo với mảnh muslin khác trên Ingenuity. Mọi đồ họa tuyến hành trình phải là hai nhánh riêng.

## III. Đồ họa chính xác phải dựng bằng SVG/compositor

Đây là bản vẽ vector/đồ họa, không nên prompt model ảnh sinh số liệu. Mỗi mục phải lấy số từ kịch bản/hồ sơ nguồn và có thể soát lại độc lập.

| ID | Đoạn | Bố cục và dữ kiện khóa |
|---|---|---|
| **V01 · Hai đường đời Nguyễn Huệ và Washington** | [1, 3, 4, 71] | Hai hàng tách biệt trên cùng trục năm 1732–1800; Washington 1732–1799, Nguyễn Huệ 1753–1792 (năm sinh Nguyễn Huệ ghi “thường được ghi nhận”). Dùng cùng scale năm, tô rõ toàn bộ đời Nguyễn Huệ nằm trong đời Washington. Gắn ngoặc “21 tuổi tính theo năm sinh” và “sống thêm 7 năm theo hiệu năm”. Không làm hai chân dung gặp nhau. |
| **V02 · Hai sự kiện riêng cùng năm 1789** | [1, 5] | Một mốc năm lớn ở giữa; trái: Tết Kỷ Dậu, Quang Trung đánh bại quân Thanh; phải: 30/4/1789, Washington nhậm chức tại New York. Mỗi sự kiện nằm trong khung/địa điểm riêng. Không đường nối quan hệ hay cảnh gặp mặt. |
| **V03 · Cùng thời không có nghĩa là liên hệ** | [6, 24, 60, 70] | Hai hồ sơ đặt xa nhau, nhãn “cùng thời” ở trên và vùng trống ghi “chưa có bằng chứng gặp, thư từ hoặc biết nhau”. Chữ được dàn bằng SVG/compositor. Không tạo thư giả, đường ảnh hưởng hay dấu X sau khi đã gây hiểu nhầm. |
| **V04 · Độ tuổi của kim tự tháp và khoảng tới năm 2026** | [9, 10, 12, 13] | Một trục đúng tỷ lệ thứ tự cho khoảng 2550 TCN, 7–4 TCN, 2026 SCN. Tính khoảng theo các mốc chọn: 2543–2546 năm và 2029–2032 năm; đoạn trước Chúa Giê-su dài hơn khoảng 511–517 năm. Ghi rõ mọi năm xây là xấp xỉ. Không đặt năm 0. |
| **V05 · Lịch TCN/SCN không có năm 0** | [11, 14] | Bốn nhãn 2 TCN, 1 TCN, 1 SCN, 2 SCN với khoảng cách mỗi năm bằng nhau; không có ô số 0. Ví dụ phép tính 7 + 2026 − 1 = 2032. Không tạo lịch lật trang khiến một khoảng năm biến thành hai. |
| **V06 · Đổi điểm nhìn trong phép so kim tự tháp** | [15, 16] | Hai điểm nhìn giả định trên cùng thước: người ở đầu Công nguyên nhìn về công trình khoảng 2000 tuổi; người hiện nay nhìn về di tích khoảng 2000 tuổi. Ghi nhãn đây là tình huống để đo khoảng cách, không phải nói Chúa Giê-su đã tới Giza. Không vẽ Chúa Giê-su. |
| **V07 · Cleopatra: 2520 năm về kim tự tháp, 1998 năm tới Apollo** | 17–19,21,71 | Dùng mốc Cleopatra mất năm 30 TCN. Hai đoạn cùng tỷ lệ: 2550→30 TCN khoảng 2520 năm; 30 TCN→1969 khoảng 1998 năm. Chênh khoảng 522 năm, tương ứng gần với mốc Khufu. Không đổi điểm neo sang năm sinh Cleopatra giữa phép tính. |
| **V08 · Cùng địa điểm không chứng minh cùng thời** | [20, 21] | Hai khung ảnh cùng địa điểm nhưng khác nhãn thời gian, sau đó tách ra trên trục; nếu dùng Hồ Gươm thì ghi là ví von. Không tạo cảnh Cleopatra thăm kim tự tháp đang xây. |
| **V09 · Bản đồ Giza và đảo Wrangel** | 23–26 | Bản đồ có nguồn và bờ biển thật, Giza ở Ai Cập và Wrangel ở Bắc Băng Dương. Dùng inset vùng cực nếu cần; ghi vị trí định vị hiện nay. Không vẽ tuyến di cư giữa chúng hoặc để đảo nằm sai phía đường đổi ngày. |
| **V10 · Nhiều vùng đã mất ma mút, Wrangel còn quần thể cuối** | 23–27 | Sơ đồ khái niệm hai hàng: phần lớn vùng phân bố biến mất trước, quần thể Wrangel tiếp tục tới khoảng 4000 BP (xấp xỉ 2000 TCN). Ghi “khoảng”, không biểu thị số lượng cá thể hay nguyên nhân tuyệt chủng chưa được chứng minh. Không vẽ con ma mút cuối cùng chết. |
| **V11 · Oxford và hai mốc Mexico là ba loại sự kiện** | 29–32 | Trục 1000–1500: 1096 là bằng chứng giảng dạy Oxford; 1325 là mốc truyền thống của thành phố Tenochtitlan; 1428 là liên minh thường dùng làm mốc đế chế Aztec. Tính chênh 229 và 332 năm theo đúng cặp; nhãn tên loại mốc luôn hiện. Không gọi 1096 là lễ thành lập chính thức. |
| **V12 · Mexico trước 1428 không trống** | [31] | Bản đồ có nguồn và một/tối thiểu một hiện vật R14 có địa điểm, văn hóa, niên đại được ghi rõ; sau đó thêm nhãn liên minh 1428. Không fade-in người từ hư không và không gọi toàn cư dân vùng Mexico là Aztec. |
| **V13 · Thành phố sống và di tích** | 33–34 | Đặt ảnh Oxford hiện nay bên một di tích Mexico có caption; thay đổi nhãn thời gian để chỉ ra cảm giác “còn sáng đèn = mới” đánh lừa trí nhớ. Không xếp hạng văn minh hoặc dùng ảnh không cùng phạm vi. |
| **V14 · 1863, 1868, 1876: thay đổi kéo dài** | 35,38–40,71 | Trục 1860–1880 với hai hàng: tuyến đường sắt London mở 1863; Minh Trị 1868; các thay đổi địa vị samurai culminate 1876. Đường đời người tiếp tục sau mốc luật. Không làm mọi samurai biến mất trong một ngày. |
| **V15 · Darwin và Lincoln sinh cùng ngày** | 41–42,44 | Một trang lịch duy nhất ghi 12/2/1809; hai nhánh tới hồ sơ Darwin ở Anh và Lincoln ở Mỹ, tách địa lý và lĩnh vực. Ghi đây là trùng hợp, không hàm ý cùng bệnh viện, quen biết hoặc điềm báo. |
| **V16 · Tuổi của Darwin và Lincoln khi đạt mốc nổi tiếng** | 43,45–46 | Darwin sinh năm 1809, Origin xuất bản năm 1859, khoảng 50 tuổi; Lincoln sinh năm 1809, đắc cử năm 1860, khoảng 51 tuổi. Chỉ dùng ảnh đúng năm hoặc ghi rõ ngày ảnh khác. Không biến đổi chân dung. |
| **V17 · Chuyến bay Wright: 12 giây, khoảng 37 mét** | [48] | Vẽ thước 37 m (120 ft = 36,576 m, làm tròn) từ vị trí rời ray tới điểm hạ; đồng hồ 12 giây chỉ chạy đúng khi thời lượng video tương ứng. Nếu dựng rút gọn phải ghi minh họa rút gọn. Không suy tốc độ đồng đều. |
| **V18 · Một đời giả định sinh năm 1900** | 49–50 | Trục thời gian nối 1903 và 1969. Người giả định sinh năm 1900 khoảng 3 tuổi khi Flyer bay và khoảng 69 tuổi khi Apollo 11 hạ cánh; ghi “người giả định”. Từ 17/12/1903 đến 20/7/1969 chưa đủ 66 năm, nên chỉ nêu hiệu số năm là 66, không nói tròn 66 năm. |
| **V19 · Hai nhánh vật liệu từ Flyer** | 52–56 | Nhánh A: mảnh vải và gỗ Flyer → Apollo 11 → trở về Trái Đất. Nhánh B: mảnh vải khác → Ingenuity → Sao Hỏa. Gắn nhãn “mảnh khác” ngay trên nhánh B. Không vẽ mũi tên từ Mặt Trăng sang Sao Hỏa. |
| **V20 · Chuyến bay Ingenuity 39,1 giây** | 54–55 | Ba trạng thái cùng camera: cất cánh, treo, hạ; tổng 39,1 giây theo JPL, lời đọc làm tròn 39 giây. Nếu dùng clip thật, ghi tốc độ phát. Nêu đầy đủ phạm vi “chuyến bay có động cơ, được điều khiển đầu tiên trên một hành tinh khác”. |
| **V21 · Lịch sử đổi tốc độ khác nhau** | 51,56–57 | So sánh đúng hai ví dụ đã nêu: hàng thiên niên kỷ quanh Kim tự tháp và vài thập niên hàng không/vũ trụ. Nếu đổi thang đồ họa phải ghi thang; không tạo đồ thị tăng trưởng công nghệ giả định. |
| **V22 · Chaplin: khung vai diễn và đường đời** | 58–64,71 | Đường đời 1889–1977 tách khỏi khung vai The Tramp. Gắn The Great Dictator 1940 có lời thoại; Apple Computer Company founded as partnership 1/4/1976. Phân biệt mốc partnership với incorporation 1977. Không ngụ ý Chaplin dùng Apple. |
| **V23 · Apple năm 1976 là máy tính, không phải iPhone** | 59–60 | Đưa ảnh Apple I/bo mạch có nguồn và mốc năm 1976; đặt điện thoại hiện đại ở ô “liên tưởng hôm nay”, tách bạch để sửa cú nhầm. Không đặt điện thoại vào tay Chaplin. |
| **V24 · Bảo Đại: vai trò vua kết thúc năm 1945, đời tới năm 1997** | 65–70,71 | Hai thanh song song: đời người 1913–1997; thời kỳ lên ngôi 1926–thoái vị 1945. Đặt Windows 95 ra mắt ngày 24/8/1995 và ngày mất 31/7/1997. 1945→1997 chênh 52 năm theo hiệu năm; không kéo áo bào đến 1997 và không nói ông dùng máy tính. |
| **V25 · Kết: đặt các phép so về đúng ngăn** | 71–73 | Chỉ hồi nhắc 5 cặp: Quang Trung/Washington; Cleopatra/Giza/Apollo; samurai/London; Chaplin/Apple; Bảo Đại/Windows 95. Mỗi cặp dùng một biểu tượng và một kết luận đúng; chuyển 2–3 nhịp, không làm lưới 20 ô nhỏ. Kết lại tủ A01 với Mỏ Đen và lời kêu gọi ngắn. |

## Quy tắc không lặp hình và không tạo cảnh sai

- Không đặt ma mút ở Giza. Chỉ đặt phép so thời gian hoặc hai hình riêng có nhãn; Wrangel là địa điểm của quần thể cuối.
- Không dùng nền Maya 151–180 làm Aztec/Tenochtitlan hoặc Ai Cập. Cần R12/R13 và đồ họa bản đồ riêng.
- Không dùng tàu điện Tube hiện đại cho năm 1863. Dùng đầu máy hơi nước thời kỳ mở tuyến, khóa theo catalog; nếu không tìm được máy khai trương cụ thể, ghi là minh họa thời kỳ đầu.
- Không vẽ samurai biến mất năm 1876; vẽ mốc thay đổi địa vị/đặc quyền và để đường đời người tiếp tục.
- Không khẳng định người cùng thời từng gặp, trao thư hoặc biết công việc nhau nếu kịch bản không có bằng chứng. Không thêm thư giữa Quang Trung và Washington.
- Không cho Chaplin dùng Apple, không đặt iPhone vào năm 1976, không cho Bảo Đại sử dụng Windows 95. Các mốc đồng thời là phép so trên trục, không phải tương tác.
- Không ghép hai mảnh vật liệu Flyer thành một vật di chuyển từ Mặt Trăng tới Sao Hỏa.
- Họ nền rộng/trung bình dùng tối đa 3 lượt trong phim; cùng bố cục rộng trống tối đa 1 lần. Mỗi lần trở lại phải có thông tin mới. Đổi crop, tiêu đề hoặc zoom không tính là hình mới.
- Ảnh tư liệu thật mặc định tối đa 2 lần; khi quay lại phải cho xem chi tiết khác có ích và giữ nguồn.
- Mỗi cảnh cần thời điểm theo voice thật, chủ thể, hành động, thông tin mới và lý do cắt. Chuyển động cần điểm đến hoặc hệ quả; pan/zoom tự nó không tạo nội dung.
- Kiểm tra từng đoạn 60–90 giây với voice sau khi dựng. Contact sheet và số shot không thay việc kiểm tra xem hình có kể đúng không.

## Checklist nhận asset

- Tên file đúng ID, một asset/file, canvas đúng, alpha thật với asset cần tách nền.
- So sánh với ảnh reference đã ghi, đọc hình ở cỡ thực sẽ xuất lên 1080p và crop cận; kiểm tra mép, tỷ lệ, hướng sáng, điểm chạm và lớp che.
- Đối với Mỏ Đen: so nhận diện cạnh master; pose mới không được tự động coi là đã duyệt.
- Với số liệu/bản đồ: so từng nhãn, dấu âm/dương, đơn vị, tỷ lệ, địa điểm và ngày với nguồn; chữ do compositor vẽ.
- Với ảnh thật: xác nhận nguồn, đúng vật/nhân vật, quyền và credit. Nếu chưa chắc, không đưa vào timeline.
- Dùng xong hãy ghi asset ID và shot ID vào registry. Không phát lại cùng nền để lấp voice dài.

## Tình trạng thời lượng

Gói hiện có `LOI_DOC.txt`, `DIEN_GIONG_DAY_DU.txt`, `PHU_DE_DU_KIEN.srt` và `NGUON_VA_KIEM_CHUNG.md`; chưa có WAV voice cuối tập 2. Mốc 18:22.875 là cuối SRT dự kiến, cue chia theo tốc độ giả định chứ chưa căn âm. Tài liệu nối theo đoạn kịch bản, không giả vờ có timecode hình chính xác đến frame. Khi voice được duyệt, thay cột đoạn bằng timecode đọc thật.

## Nguồn và file trong dự án

- Kịch bản đầu vào đã lưu tại `projects/mo_den_tap_02/source_materials/`.
- Catalog 150 ảnh: `projects/mo_den_maya/preflight/generic_150_catalog.json`; PNG nằm tại `assets/reusable/mo_den/generic_150/`.
- Catalog 48 ảnh Maya: `projects/mo_den_maya/preflight/maya_48_catalog.json`; PNG nằm tại `assets/reusable/mo_den/maya_48/`.
- Catalog mèo: `assets/characters/mo_den/manifest.json`; ảnh gốc trong `assets/characters/mo_den/library/named_24_v01/`.
- Phong cách minh họa: `assets/styles/explainer_reference_v1/manifest.json` và ba PNG cùng thư mục.
- Quy tắc không lặp: `QUY_DINH_DAO_DIEN_HINH_ANH.md`.
- Sơ đồ kiểm kê toàn bộ ảnh 198 mục: `inventory_verified.json`, `inventory_001_030.jpg` đến `inventory_181_198.jpg`.
- Cơ quan nguồn gốc đầu mối: [R01](https://baotanglichsuquocgia.vn/vi/Articles/3097/15721/ky-niem-225-nam-1789-2014-hoang-dje-quang-trung-nguyen-hue-djai-pha-quan-xam-luoc-man-thanh.html), [R02](https://npg.si.edu/object/npg_NPG.2001.13), [R03](https://www.mountvernon.org/george-washington/the-first-president/inauguration/timeline), [R05](https://www.metmuseum.org/art/collection/search/558193), [R06](https://www.britishmuseum.org/collection/term/BIOG57627), [R07](https://www.nasa.gov/missions/apollo/apollo-11/apollo-11-mission-overview/), [R08](https://www.nhm.ac.uk/discover/were-all-mammoths-woolly.html), [R09](https://pmc.ncbi.nlm.nih.gov/articles/PMC6121868/), [R10](https://www.ox.ac.uk/about/the-university/history), [R11](https://www.ox.ac.uk/about/the-university/history), [R12](https://www.inah.gob.mx/images/boletines/2025/213/Boletin%20213.pdf), [R13](https://www.inah.gob.mx/), [R14](https://deas.inah.gob.mx/pdf/publicaciones/publicaciones/publicacion%2839963%29-3447.pdf), [R15](https://library.ltmuseum.co.uk/Portal/Default/en-GB/RecordView/Index/108), [R16](https://library.ltmuseum.co.uk/Portal/Default/en-GB/RecordView/Index/97).
