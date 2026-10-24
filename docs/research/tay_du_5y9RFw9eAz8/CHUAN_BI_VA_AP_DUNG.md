# Chuẩn bị để dựng theo ngôn ngữ hình ảnh của video mẫu

Đề xuất cho Studio, 24/10/2026. Các số lượng và thời gian gợi ý dưới đây là định mức khởi đầu để lập kế hoạch, không phải số tài sản hoặc thời lượng đã đo của tác giả.

## 1. Chốt một câu hỏi rồi thiết kế cách trả lời bằng hình

Với mỗi đoạn, điền bốn ý trước khi xin thêm ảnh:

1. Khán giả đang thắc mắc điều gì?
2. Cần nhìn thấy hành động, quan hệ, đối chiếu hay chứng cứ nào để hiểu?
3. Hình sẽ đổi trạng thái ở đâu, và sau đó khác trước thế nào?
4. Nếu bỏ cảnh, khán giả mất thông tin/cảm xúc cụ thể nào?

Ví dụ “A có quyền ra lệnh, B vẫn không chịu phục” có thể tổ chức thành: hai người trong cùng không gian → đạo cụ/động tác ra lệnh → phản ứng của B → Mỏ Đen nhận xét ngắn → trích đoạn hoặc sơ đồ giải thích vì sao. Cảnh này cần tài sản phục vụ quan hệ quyền lực, không tự động cần thêm ba phông cung điện.

## 2. Bộ tư liệu cần chuẩn bị

| Nhóm | Chuẩn bị cụ thể | Tái sử dụng ra sao | Cách làm trong Studio |
|---|---|---|---|
| Mỏ Đen | Dùng 24 PNG trong manifest. Chọn 01 bình thường, 13 tò mò, 14 hoài nghi, 15 suy nghĩ, 16 nhận ra, 21 bất lực, 24 giải thích khi hợp ý; 03 cười chỉ dùng đúng nhịp. | Thay vai kể/phản ứng; giữ nhận diện và chân chuẩn, kiểm tra ảnh 03 lệch trái. | Dùng exact path trong `assets/characters/mo_den/manifest.json`; giữ ảnh gốc. Không cần xin lại bộ biểu cảm. |
| Người/vai truyện | Danh sách theo kịch bản; mỗi người có hình nhận diện và đúng pose mà cảnh cần: nhìn trái/phải, ra lệnh, nhận vật, phản đối, nằm/quỳ nếu thực sự có trong nội dung. | Giữ cùng trang phục và tỷ lệ qua các cảnh; dùng lại hình khi vai và góc phù hợp. | Trước hết kiểm kê bộ Phong Thần hiện có; người vẽ vector phải qua chuẩn/QC nhân vật hiện hành. Không tự sinh người thay thế hoặc vặn PNG thành pose mới. |
| Bộ tương tác | Với mỗi động từ: pose trước + vật rời + vị trí tiếp xúc + trạng thái sau. Ví dụ “trao sắc”: người trao, người nhận, sắc, tay/điểm giữ, sắc ở tay ai sau đó. | Một bộ có thể đóng nhiều tình huống nhưng phải đổi mục đích/diễn biến thực. | Có thể dựng người tĩnh bằng cut và thay pose đã chuẩn bị; chuyển động người mới cần đúng phạm vi được người dùng cho phép. |
| Đạo cụ | Sách, cuộn sắc, bàn, ghế, vũ khí, bình, hộp, thẻ chức vị; trạng thái mở/đóng/nguyên/vỡ khi cảnh cần. | Dùng lại đồ rời, không gắn chữ hoặc tay vào bản duy nhất. | Đồ đơn giản, mũi tên, đường, khung và dấu chỉ bằng vector. Đồ đặc thù cần bản đủ nhận diện. |
| Bối cảnh có chỗ diễn | Cửa vào, mặt sàn/mặt bàn, chỗ đứng/ngồi, vùng trống đối thoại và các vật cản phía trước. | Cảnh rộng để định vị; chi tiết hoặc sơ đồ cho phần phân tích. Ghi họ bối cảnh và mục đích quay lại. | Tách vật che trước, nền xa và sàn nếu tương tác đòi hỏi; không bắt buộc tách mọi nền thành hàng chục lớp. |
| Biểu tượng giải thích | Bong bóng thoại/nghĩ, dấu hỏi, tim, giọt mồ hôi, gạch chéo, đường nối, nhãn tên, khung so sánh. | Dùng theo chức năng; thay hình nằm trong bong bóng. | Text và vector sửa được; không đóng cứng số/chữ tiếng Việt vào PNG. |
| Tư liệu đối chiếu | Trang sách/tranh/ảnh chụp/bản đồ/đoạn phim phù hợp luận điểm; lưu nguồn và phần cần chỉ. | Trở lại khi phân tích một chi tiết mới, có crop/đánh dấu rõ. | Ghi vai `evidence`, `illustration`, `adaptation` hoặc `humor` trong sổ tư liệu; đây là phân loại biên tập, không thay cổng QC `role=character`. |
| Chữ và số | Tiêu đề ngắn; nhãn người/vật; mốc thời gian; lời thoại ngắn; dòng xuất xứ; SRT lời kể riêng. | Tạo thành mẫu chữ thống nhất nhưng không đổ toàn bộ lời đọc lên hình. | Chọn font có đủ dấu tiếng Việt; thử ở cỡ xem điện thoại. |
| Tiếng nói và nhịp | Dùng audio đã chốt; đánh mốc câu và từ kích hoạt hành động/tiết lộ, có khoảng giữ cho người đọc. | Giữ speaker và vùng giọng; Maya dùng H/Bắc/1,25× một lần theo chuẩn hiện hành. | SFX/nhạc chỉ lập cue cần thiết; chưa phân tích nghe SFX của mẫu nên không khẳng định họ dùng gì. |

### Định dạng nên nhận

- Nhân vật/đạo cụ: PNG alpha thật hoặc SVG; mỗi pose/vật một file; không nền giả trong suốt, không chữ dính vào người, không cắt tai/chân/vũ khí ngoài ý muốn.
- Với tư thế giao tiếp: ghi rõ hướng nhìn, hướng vật nhận/trao, toàn thân/bán thân, điểm đặt chân và điểm tay/vật gặp nhau. Chừa khoảng quanh vũ khí và tóc.
- Nền: đủ chi tiết ở vùng diễn, chừa chỗ cho người. Đạo cụ cần thay trạng thái để rời; một nền đẹp nhưng bàn và ghế che hết nhân vật vẫn không dùng được cho cảnh trao vật.
- Tư liệu thật: bản gốc, đường dẫn nguồn, trang hoặc timecode, ghi chú vai trò. Hình gây cười không được dùng làm bằng chứng về nhân vật/sự kiện.
- Tên gợi ý: `person_id_pose_view_emotion_v01.png`, `prop_id_state_v01.svg`, `bg_family_view_v01.png`. Đường dẫn và ID thật phải lấy từ catalog, không tự đoán file.

## 3. Chuẩn bị theo thứ tự để tránh tạo một kho lớn mà vẫn thiếu cảnh

**Bước A — chia lời kể thành đơn vị ý nghĩa.** Dùng nội dung đã chốt và audio thực tế. Xác định chỗ kể sự kiện, chỗ giải thích, chỗ đối chiếu, chỗ bình luận. Không coi mỗi dấu phẩy là một cảnh.

**Bước B — lập bảng đạo diễn trước bảng yêu cầu ảnh.** Mỗi đơn vị chọn một việc hình ảnh phải làm. Có thể giữ bố cục qua nhiều đơn vị nếu quan hệ/hành động vẫn tiến triển.

**Bước C — kiểm kê theo từng cảnh.** Đánh `đã có đúng`, `có nhưng cần kiểm tra`, `thiếu`. Tên file không chứng minh pose dùng được. Với Mỏ Đen mở ảnh thực tế; với người thực hiện QC theo quy định. Chỉ gửi yêu cầu phần thiếu gắn với shot cụ thể.

**Bước D — ưu tiên một đoạn đại diện 30–45 giây.** Chọn đoạn có ít nhất một quan hệ, một hành động/hệ quả và một nhịp giải thích. Lập bảng ảnh cho cả đoạn; nếu cần kiểm tra chuyển động thì chọn 5–15 giây trong đoạn đó. Đây là đề xuất bước tiếp theo, chưa tự sửa hoặc render phim.

**Bước E — duyệt hình và nhịp.** Xem ở cỡ nhỏ, tua qua các thay đổi và xem cùng audio. Sửa khi người xem không rõ ai làm gì hoặc không đọc kịp. Một contact sheet chỉ giúp duyệt bố cục; không chứng nhận chuyển động mượt hay căn lời đúng.

**Bước F — triển khai các đoạn còn lại.** Dùng cách tổ chức đã được chứng minh ở đoạn đại diện, đồng thời thay đổi cách kể theo nội dung. Giữ quy định về lặp họ bối cảnh và cấu trúc bố cục; đừng lặp cùng một màn vào–đứng–ra với mọi câu.

**Bước G — người dùng duyệt bản edit toàn phim, rồi mới render final.** Giữ nguyên điều kiện duyệt trước render đã chốt ngày 24/10/2026.

### Quy mô gợi ý cho đoạn đại diện, không phải bộ bắt buộc cho mọi video

Với một đoạn 30–45 giây có hai vai truyện: chọn khoảng 2–4 pose thực sự cần cho mỗi vai; 3–6 đạo cụ/trạng thái; 1–2 không gian có chỗ diễn; một sơ đồ hoặc tư liệu nếu luận điểm cần; 2–3 biểu cảm Mỏ Đen đã có. Số này có thể nhỏ hơn nhiều nếu chỉ giải thích một quan hệ. Chỉ chốt số ảnh sau khi có bảng đạo diễn.

## 4. Sáu kiểu dàn dựng có thể sử dụng

Các kiểu dưới đây là cách lựa chọn, không phải chu kỳ sáu cảnh lặp suốt phim. Giới hạn lặp bố cục của Studio vẫn áp dụng.

### A. Đặt vấn đề → cho thấy điều cần chú ý

Mỏ Đen hoài nghi nhìn về vật → mở khung chi tiết vật → nhãn ngắn chỉ đúng phần quan trọng. Khi vào hình chi tiết, giảm hoặc bỏ Mỏ Đen để tránh tranh sự chú ý.

### B. Hành động → tiếp xúc → hệ quả

Đặt hai đối tượng đủ gần để hiểu quan hệ → thực hiện/thay pose tại điểm tiếp xúc → giữ kết quả một nhịp → phản ứng. Với người tĩnh, có thể dùng ba pose và cut rõ; không mặc định cần rig toàn thân. Nếu dùng chuyển động, điểm tiếp xúc và vật cầm phải theo đúng người giữ.

### C. Nêu tưởng tượng → thay hình để phản biện

Nhân vật nghĩ về một vật/phiên bản → nội dung trong bong bóng thay sang hình đối chiếu → phản ứng. Dùng nhãn để phân biệt nguyên tác, chuyển thể và suy diễn hài. Đây là bài học từ 03:18–03:23, không phải lời mời lấy chính hình meme của mẫu.

### D. Hai mốc → đường nối → con số → kết luận

Hiện hai mốc, rồi mới đường nối, rồi mới thời gian/khoảng cách. Khi đổi phép so sánh, đổi đúng đầu/cuối và nhãn. Một khung nhìn cho một quan hệ đang được giải thích; đừng phóng toàn bộ sơ đồ liên tục.

### E. Diễn lại → bằng chứng → trở lại câu hỏi

Cảnh truyện làm người xem hiểu vấn đề → đưa trang/ảnh đủ lớn, chỉ đúng chi tiết → trở lại Mỏ Đen với câu hỏi/kết luận. Chỉ thêm bảng nguồn khi có nguồn thật; không dựng nhãn chương/trang giả.

### F. Bàn trống → có vật → nhãn giải mã

Chuẩn bị chỗ đặt → hiện vật theo ý kể → nhãn ngắn giúp nhận diện → một hình hệ quả hoặc phản ứng. Đây là trình tự ở đoạn 11:04–11:11; dùng tốt cho bảo vật, vật liệu, đồ cống nạp, chức vị hoặc thành phần hệ thống.

## 5. Một shot brief cần chứa những gì

| Trường | Nội dung phải có |
|---|---|
| Mốc | Audio file/cue, in/out thực tế; đánh dấu `chưa căn` nếu mới lập ý. |
| Câu kể | Bản gốc và cụm đang cần minh họa; không tự thêm lời thoại làm đổi kịch bản. |
| Mục tiêu | Sau nhịp này khán giả hiểu điều gì mới? |
| Điểm nhìn | Chủ thể đầu tiên và thứ tự mắt chuyển sang các phần sau. |
| Dàn cảnh | Ai ở đâu, nhìn ai, vùng trống cho vật/chữ, lớp trước/sau. |
| Trạng thái | Trước → hành động/tiết lộ → sau; có thể là pose tĩnh, đồ rời hoặc sơ đồ. |
| Tài sản | Exact path, pose, hướng, trạng thái vật; ghi rõ thiếu gì. |
| Chuyển động | Di chuyển/đổi pose/xoay/hiện dần/vẽ nét; điểm đầu/cuối và lý do. `Không` cũng là lựa chọn hợp lệ. |
| Chữ/nguồn | Text ngắn, vị trí, khi hiện/tắt; nguồn thật hoặc nhãn minh họa. |
| Tái sử dụng | Họ bối cảnh/bố cục, lần dùng, thông tin mới; ngoại lệ có bằng chứng. |
| Duyệt | Ảnh/chuỗi hiện tại, lỗi cần sửa, trạng thái người dùng. Không tự đánh đạt thẩm mỹ bằng số liệu. |

Mẫu CSV rỗng: [MAU_SHOT_BRIEF.csv](MAU_SHOT_BRIEF.csv). Chưa điền timecode giả cho phim Phong Thần.

## 6. Công cụ hiện có và phần cần chuẩn bị thêm

Đã đọc mã `studio/renderer.py` và `studio/animation.py`: có thứ tự lớp, biến đổi vị trí/kích thước/xoay/opacity, pivot/attachment trong các luồng tương ứng và camera có keyframe. Những thành phần này là nền để dàn cảnh bằng ảnh rời. Đây là quan sát mã, chưa phải xác nhận mọi kỹ thuật bên dưới đã hoạt động trong giao diện hay đã được kiểm tra cho PNG Mỏ Đen.

| Việc | Hướng áp dụng | Tình trạng trong nghiên cứu này |
|---|---|---|
| Đưa ảnh/đồ rời lên lớp và đặt mốc | Dùng hệ object/key hiện có; ghép theo hành động. | Có cấu trúc trong mã; chưa tạo cảnh mới. |
| Mũi tên theo đường cong và hiện dần | Tạo vector/đường có đầu-cuối, giữ đầu mũi tên đúng mốc. | Cần xác minh khả năng vẽ nét theo thời gian trước khi hứa dùng ngay. |
| Bong bóng đổi nội dung | Tách vỏ, hình bên trong và đuôi; kiểm tra crop/che hình. | Cần dựng và kiểm tra một mẫu thực tế. |
| Người nhận/trao vật | Asset có pose phù hợp; điểm nắm, trục xoay vật và lớp tay đúng. | Chưa xác nhận tài sản/attachment tương ứng đã đủ. |
| Đổi pose không nhảy tỷ lệ | Dùng chuẩn chân/đầu và bounding box, xem ảnh trước và sau. | Bộ mèo đã có căn chuẩn; ảnh 03 cần kiểm tra lệch. |
| Tiền cảnh lớn mờ/hậu cảnh rõ | Chuẩn bị lớp mờ riêng hoặc xác minh hiệu ứng blur. | Không coi là đã có blur động chỉ từ hỗ trợ scale/opacity. |
| Lưu bài học cho agent khác | Đọc báo cáo nghiên cứu và dẫn chứng trước khi lập shot. | Bộ tài liệu này đã lưu; chưa sửa quy định gốc hay áp vào phim. |

Không cần đổi engine dựng chỉ để bắt chước diện mạo. Việc đầu tiên là có shot brief và bộ đồ diễn đủ; chỉ bổ sung công cụ ở chỗ một cảnh đại diện chứng minh đang thiếu.

## 7. QC tập trung vào câu chuyện trong hình

1. Xem ba trạng thái trước/giữa/sau: ai làm gì với ai/vật gì có rõ không? Nếu chỉ đổi nền, phải viết lại mục tiêu cảnh.
2. Xem ở cỡ điện thoại: đọc được mặt, đạo cụ, đường nối, nhãn và điểm nhìn chính không?
3. Xem điểm nắm/tiếp xúc: vật có rời tay, xuyên người, sai lớp hoặc đổi kích thước khi thay pose không?
4. Kiểm tra tư thế có tài sản thật: không biến pose ngồi thành đứng/quỳ bằng kéo ảnh; không thêm miệng/tay làm mất nhận diện.
5. Xem chuyển động ở tốc độ thật với audio: người đọc có kịp hiểu trước khi hình tắt không, từ nhấn có đúng lúc xảy ra sự kiện không?
6. Xem đoạn 60–90 giây: có trùng họ nền, cỡ cảnh, bố cục, gag và tiết mục xuất hiện không? Ghi ngoại lệ có hình thật theo quy định.
7. Kiểm tra chứng cứ: trang/ảnh có đúng nguồn và ngữ cảnh không; diễn lại và lời đùa có bị hiểu thành chứng cứ không?
8. Ghi lỗi còn lại bằng hình hiện tại và sửa trước khi trình duyệt. Một phiếu QC hoặc bộ mã chạy được không thay thế đánh giá thẩm mỹ.

## 8. Đề nghị cho bước tiếp theo

Chọn một đoạn trong Phong Thần để làm bảng “lời kể → hành động nhìn thấy → bộ ảnh/vật rời cần có → thứ tự xuất hiện”. Kiểm kê bộ ảnh V2 và bản edit hiện tại theo bảng đó, rồi trình bảng ảnh/preview ngắn cho người dùng duyệt. Chưa kết luận bản edit 102 cảnh hiện tại đáp ứng hay không: lượt này phân tích video tham chiếu, chưa audit từng cảnh Phong Thần.
