# Bảng đối chiếu phát âm (Pronunciation & Context Ledger)
**Dự án:** Mỏ Đen Maya — Hồ sơ Witzna (Bahlam Jol) 697 SCN  
**Quy chuẩn áp dụng:** `VIETNAMESE_NARRATION_STANDARD.md`  
**Giọng đọc:** Mỏ Đen · Giọng Bắc · Hồ sơ Custom H (`projects/mo_den_maya/voice_direction/selected_voice_H.json`)  
**Nguyên tắc:** 
1. Giữ nguyên 100% chính tả gốc trong kịch bản lưu trữ và phụ đề hiển thị (SRT).
2. Phiên âm / chuẩn hóa chỉ áp dụng trong lớp TTS đọc (TTS Reading Layer) để model tổng hợp phát âm tròn vành rõ chữ, không vấp, không nuốt chữ, đúng ngữ điệu tự nhiên.
3. Không tự tiện xóa thanh điệu tiếng Việt hoặc bẻ cao độ.

---

## 1. Bảng đối chiếu chi tiết

| STT | Cụm từ gốc (Kịch bản & Phụ đề) | Cách đọc TTS (Reading Layer) | Loại | Ngữ cảnh / Lý do chuyển đổi |
|---|---|---|---|---|
| 1 | **Witzna** | **Vít-na** | Tên cổ địa danh | Tên phế tích thành phố Maya tại Petén, Guatemala. Phiên âm chuẩn ngữ âm tiếng Việt giúp model VoxCPM2 phát âm dứt khoát, tự nhiên. |
| 2 | **Laguna Ek’Naab** | **La-gu-na Éc Náp** | Tên hồ nước | Hồ nước cạnh Witzna nơi lấy mẫu lõi trầm tích. "Ek'Naab" trong tiếng Maya nghĩa là "Vùng nước đen". Đọc "La-gu-na Éc Náp" giúp khẩu hình tròn, không bị khựng âm dấu nháy. |
| 3 | **Bahlam Jol** | **Ba-lam Hôn** | Tên cổ thành phố | Tên cổ của Witzna tìm thấy trên văn khắc (nghĩa Maya: "Đầu Báo Đốm"). Trong tiếng Maya/Tây Ban Nha, chữ J phát âm như âm H. Đọc "Ba-lam Hôn" chuẩn xác ngữ âm bản địa. |
| 4 | **Naranjo** | **Na-ran-hô** | Tên thành phố Maya | Thành bang đối địch hùng mạnh thời Cổ điển. Tên tiếng Tây Ban Nha chữ 'j' phát âm là /h/ (Na-ran-hô). |
| 5 | **Guatemala** | **Gua-te-ma-la** | Quốc gia | Đất nước ở Trung Mỹ, cái nôi của nền văn minh Maya vùng Petén. |
| 6 | **Năm 2013** | **Năm hai nghìn không trăm mười ba** | Năm dương lịch | Năm đoàn nghiên cứu của David Wahl và Francisco Estrada-Belli lấy mẫu trầm tích. Chuẩn hóa thành chữ tiếng Việt để TTS không đọc số rời rạc kiểu "hai không một ba". |
| 7 | **ngày 21 tháng 5 năm 697** | **ngày hai mươi mốt tháng năm, năm sáu trăm chín mươi bảy** | Mốc lịch sử | Ngày thành phố Bahlam Jol bị Naranjo đốt cháy ghi trên bia đá. Đọc chuẩn xác ngày tháng năm tiếng Việt. |
| 8 | **năm 690 đến 700** | **năm sáu trăm chín mươi đến bảy trăm** | Khoảng niên đại | Khoảng xác định niên đại carbon của lớp than dưới đáy hồ. Đọc chuẩn xác khoảng thời gian. |
| 9 | **năm 697** | **năm sáu trăm chín mươi bảy** | Năm lịch sử | Mốc thời gian cuộc tấn công diễn ra. |
| 10 | **Hơn một nghìn ba trăm năm sau** | *(Giữ nguyên chữ)* | Thời lượng | Đã được viết bằng chữ hoàn chỉnh trong bản gốc. |
| 11 | **cuối thế kỷ thứ bảy** | *(Giữ nguyên chữ)* | Thế kỷ | Đã được viết bằng chữ hoàn chỉnh trong bản gốc. |
| 12 | **một thế kỷ** | *(Giữ nguyên chữ)* | Thế kỷ | Đã được viết bằng chữ hoàn chỉnh trong bản gốc. |
| 13 | **hơn một nghìn năm sau** | *(Giữ nguyên chữ)* | Thời lượng | Đã được viết bằng chữ hoàn chỉnh trong bản gốc. |

---

## 2. Kiểm chứng kỹ thuật và QC phát âm
- Đã kiểm tra phát âm trên bộ tổng hợp giọng VoxCPM2.
- Lớp phát âm tiếng Việt đảm bảo đủ 6 thanh điệu (ngang, huyền, sắc, hỏi, ngã, nặng) chuẩn giọng Bắc.
- File SRT xuất xưởng đối chiếu chính xác: hiển thị từ gốc tiếng Maya / Tây Ban Nha / chữ số nguyên bản cho người xem.
