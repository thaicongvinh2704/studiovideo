# Dự án Giọng đọc Diễn cảm: Bí ẩn Vụ Cháy Witzna (Bahlam Jol) 697 SCN

## 1. Tổng quan dự án
- **Nhân vật người kể**: Mỏ Đen (giọng Bắc, Custom H, nam ~30 tuổi, thông minh, tò mò, khám phá, giọng ấm áp và giàu lòng trắc ẩn).
- **Hồ sơ giọng chuẩn**: `projects/mo_den_maya/voice_direction/selected_voice_H.json`
- **Engine tổng hợp**: `VoxCPM2 GGUF local` tăng tốc phần cứng GPU qua Vulkan (`build-vulkan/bin/studio-voice-batch.exe`).
- **Tốc độ đọc**: Tăng tốc 1.25x một lần duy nhất theo chuẩn giọng Mỏ Đen đã duyệt ngày 21/10/2026.
- **Tiêu chuẩn chất lượng**: Tuân thủ nghiêm ngặt `VIETNAMESE_NARRATION_STANDARD.md`.

---

## 2. Ý đồ biên kịch & Diễn đạt cảm xúc ("Có hồn nhấn nhá như con người")

Một kịch bản tài liệu khảo cổ học sâu sắc không thể được đọc bằng giọng đều đều vô cảm như máy đọc sách. Người kể chuyện (Mỏ Đen) phải thực sự **hiểu nội dung câu chuyện**, dẫn dắt người nghe qua từng cung bậc:

1. **Mở đầu trầm lắng, bí ẩn (Beat 1 - Cues 1-3)**:
   - *"Người chiến thắng đã khắc lên đá ngày họ đốt một thành phố."*
   - Nhịp chậm (tempo 0.98), giọng chắc và lắng đọng thời gian. Khoảng nghỉ 650ms để dư âm lịch sử thẩm thấu.
2. **Khám phá khoa học thực địa (Beat 2 - Cues 4-8)**:
   - Vùng Petén ở Guatemala, hồ Laguna Ek'Naab và các mẫu trầm tích.
   - Nhịp kể tự nhiên, hào hứng, mở rộng tầm nhìn về phương pháp giải mã quá khứ bằng phấn hoa, hóa chất và than bùn.
3. **Nút thắt kịch tính & Câu hỏi trăn trở (Beat 3 - Cues 9-13)**:
   - Lớp than nổi bật cuối thế kỷ VII và sự đứt gãy hoạt động của con người.
   - Hạ giọng, dồn sự chú ý vào câu hỏi tu từ: *"Chuyện gì đã xảy ra ở đó?"* (khoảng nghỉ dài 700ms).
4. **Tư duy khoa học sắc bén (Beat 4 - Cues 14-16)**:
   - Điềm tĩnh, chặt chẽ: *"Một trận cháy lớn chưa đủ để kết luận có quân đội tấn công... nhóm nghiên cứu cần danh tính của sự kiện."*
5. **Khảo cổ văn tự & Nút thắt then chốt (Beat 5 - Cues 17-22)**:
   - Tên cổ *Bahlam Jol* ("Đầu Báo Đốm") xuất hiện trên bia đá của kẻ thù Naranjo.
   - Ngày định mệnh: *21 tháng 5 năm 697*. Nhịp đọc dứt khoát, khẳng định.
6. **Sự thật khoa học & Chi tiết dễ kể sai (Beat 6 - Cues 23-27)**:
   - Giọng cảnh báo nhẹ, phân định rành rọt giữa niên đại carbon tự nhiên (690-700) và ngày tháng cụ thể từ văn bia.
7. **Lật lại định kiến về chiến tranh Maya (Beat 7-8 - Cues 28-40)**:
   - Đập tan quan niệm cũ rằng chiến tranh Maya thời Cổ điển chỉ giới hạn ở quý tộc cung đình.
   - Witzna chứng minh chiến tranh hủy diệt toàn diện đã xuất hiện từ rất sớm!
8. **Chiều sâu nhân văn & Tiếng nói của thường dân (Beat 9 - Cues 41-48)**:
   - Giọng thì thầm xúc động, trắc ẩn: *"Bao nhiêu người chết? Bao nhiêu người bị bắt? Bao nhiêu người đã bỏ chạy?"*
   - Sự khiêm nhường của khoa học và cái giá đau thương đằng sau một dòng chiến công.
9. **Sự hồi sinh kiên cường (Beat 10 - Cues 49-53)**:
   - Giọng ấm và sáng hơn khi thành phố tái thiết và câu chuyện còn tiếp diễn.
10. **Đúc kết nghìn năm (Beat 11 - Cues 54-61)**:
    - Đối xứng giữa bia đá và lớp than đáy hồ. Câu kết vang vọng, chậm rãi, để lại dư ba sâu lắng.

---

## 3. Cấu trúc thư mục thành phẩm

- `01_Loi_Ke_Goc.txt`: Toàn bộ văn bản gốc của người dùng được bảo toàn 100% từng chữ.
- `02_Bang_Doi_Chieu_Phat_Am.md`: Bảng đối chiếu phát âm tên riêng (Witzna -> Vít-na, Laguna Ek'Naab -> La-gu-na Éc Náp, Bahlam Jol -> Ba-lam Hôn, Naranjo -> Na-ran-hô) và ngày tháng số học.
- `03_Kich_Ban_Bien_Kich_Dien_Doc.json`: Bản thiết kế chi tiết 61 Semantic Units gồm tone, intent, pace, gain và pause_ms.
- `render_witzna_narration.py`: Mã nguồn pipeline tự động hóa chuẩn phòng thu.
- `Mo_Den_Witzna_697_Custom_H_1_25x.wav`: File âm thanh master WAV 48kHz chuẩn phát thanh.
- `Mo_Den_Witzna_697_Custom_H_1_25x.mp3`: File MP3 192kbps tiện nghe thử và chia sẻ.
- `Mo_Den_Witzna_697.srt`: Phụ đề đồng bộ hiển thị văn bản gốc khớp từng mili-giây.
- `report_witzna.json`: Báo cáo kỹ thuật chi tiết (Loudness LUFS, True Peak, duration, hash SHA256).
