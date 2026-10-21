# Chuẩn hình ảnh đề xuất theo nhân vật người dùng

Trạng thái: bản định hướng và khung hình đối chiếu. Ảnh chuẩn đã lưu; chưa có bộ nhân vật chuyển động mới được người dùng duyệt. Không coi việc lưu ảnh hoặc giữ checksum là đã sửa xong hình thể và diễn hoạt.

## Hướng vẽ chung

Minh họa 2D nét mực mềm, màu phẳng, nền sáng thoáng. Nhân vật người dùng là chuẩn để thiết kế cảnh. Không trộn nhân vật viền đen ít chi tiết với nền sơn nhiều lớp, ánh sáng điện ảnh, phối cảnh hiện thực hoặc chi tiết dày.

| Thành phần | Chuẩn chung |
|---|---|
| Nét | Viền đen hơi tự nhiên, đầu nét tròn; nhất quán về trọng lượng khi đặt trong cùng cảnh |
| Màu | Màu phẳng: than đen, da kem, xanh quần; màu cảnh bổ trợ bằng xanh lá dịu, cát, nâu đất |
| Khối | Đường cong mềm, cách điệu có chủ ý; nhà và vật dụng vẫn có cấu trúc dễ hiểu |
| Chi tiết | Vài nét diễn tả mái/cột/lá; không phủ texture, không đổ bóng nhiều tầng |
| Không gian | Cảnh liên tục có gần/xa và điểm tiếp đất; nền trắng hoặc sáng thoáng |
| Người phụ | Cùng cấu trúc đầu, mắt, bàn tay, bàn chân và độ đơn giản; tuổi, tóc, trang phục có biến thể rõ |

## Những gì phải giữ ở người dẫn

`art/presenter_master.png` là bản sao nguyên tệp người dùng gửi: tóc đen vuốt lệch, mặt góc 3/4, đầu lớn, nét mắt/mũi/miệng riêng, áo đen có dấu cộng trắng, quần xanh, giày trắng. Không thay bằng kiểu mặt tròn khác trong quá trình dựng cảnh.

Khung đối chiếu hiện dùng nguyên ảnh này trong một lớp hình Studio, chỉ thay đổi vị trí và phóng thu đồng đều. Không dùng model tạo ảnh để vẽ lại người dẫn. Việc dùng ảnh gốc giữ đúng tạo hình trong **tư thế chỉ tay có sẵn**; nó không tự tạo ra một rig chuyển động đúng cho tư thế mới.

## Quy trình cho bản chuyển động tiếp theo

1. Dựng một bộ nguồn sạch theo ảnh, dùng một hệ tọa độ gốc. Lập bảng mẫu đứng, góc 3/4, nghiêng, biểu cảm; các góc chưa biết phải được thiết kế và xem lại, không suy ra là đã đúng từ một ảnh.
2. Chốt tỷ lệ đầu/thân/chi, đường viền, màu và vị trí dấu cộng. So sánh hình chồng với ảnh chuẩn ở tư thế chỉ tay.
3. Tách các phần trong cùng hệ tọa độ, có phần hình nằm chồng dưới khớp. Không co từng phần theo khung `fit=contain` riêng rồi nối bằng tọa độ ước lượng.
4. Cố định điểm vai/khuỷu/cổ tay/hông/gối/cổ chân và hướng bàn tay. Quần phải có phần hông liền khối để không tạo khoảng hở dưới áo. Tư thế ngồi và góc tay đặc biệt có hình thay thế được vẽ riêng.
5. Lưu rig và thư viện tư thế thành một phiên bản dùng lại giữa các cảnh. Nền tạo riêng, không tự tạo lại người dẫn theo từng prompt.
6. Kiểm tra từng khung khi đổi pose: không hở khớp, xoay ngón tay sai, xuyên thân, đổi chiều dài hoặc trượt chân. Xem một đoạn 5–8 giây ở kích thước xuất thật trước khi áp dụng toàn phim.
7. Chốt một khung gồm người dẫn + người phụ + nhà + cây + đạo cụ rồi giữ chung quy chuẩn cho toàn bộ tài nguyên mới. Bản phối hợp chưa được coi là duyệt chỉ vì video xuất thành công.

## Tệp đối chiếu

- `reference_manifest.json`: checksum và phạm vi cố định thực tế của ảnh gốc.
- `imagegen_prompt.json`: prompt tạo nền theo ảnh, bằng imagegen tích hợp.
- `style_comparison.png`: ảnh chuẩn và cảnh phối hợp để so sánh.
- `scene_preview.png`: bố cục thử trong Studio; ảnh người dẫn vẫn dùng tệp gốc.
- `preview_project.json` + `assets/`: dự án tĩnh mở được trong Studio, không phải một video diễn hoạt hoàn chỉnh.

Ảnh AI trong bản định hướng chỉ dùng đánh giá ngôn ngữ hình ảnh. Người phụ và chi tiết sinh hoạt trong đó là minh họa, không phải bản phục dựng khảo cổ được chứng nhận.

## Nguồn về quy trình

- [Toon Boom: Character Model Sheets](https://learn.toonboom.com/modules/character-design/topic/character-model-sheets): bảng thiết kế nhân vật làm chuẩn dùng chung.
- [Toon Boom: How to Rig a Cut-out Character](https://docs.toonboom.com/help/harmony-24/essentials/getting-started/character-building.html): tách phần chuyển động theo lớp và quan hệ cha/con dựa trên mẫu nhân vật.
- [Toon Boom: Pre-production](https://learn.toonboom.com/modules/animation-workflow/topic/pre-production): giải quyết thiết kế chung trước nền, hoạt hình và tô màu.
