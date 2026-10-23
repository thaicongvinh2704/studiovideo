import json
import re
from pathlib import Path

ROOT = Path("projects/mo_den_maya/voice_direction/script_witzna_697")
raw_text = (ROOT / "01_Loi_Ke_Goc.txt").read_text(encoding="utf-8").strip()

# Breakdown of the 40 paragraphs into directed semantic units
units_data = [
    # Beat 1: Mở màn bí ẩn & Cuộc hội ngộ nghìn năm
    {
        "id": 1,
        "paragraph_idx": 1,
        "source_text": "Người chiến thắng đã khắc lên đá ngày họ đốt một thành phố.",
        "spoken_text": "Người chiến thắng đã khắc lên đá ngày họ đốt một thành phố.",
        "intent": "Mở đầu kịch tính, giọng trầm, chắc, lắng đọng thời gian.",
        "tone": "bí ẩn, sức nặng lịch sử",
        "pause_ms": 650,
        "pace": 0.98,
        "gain_db": 0.3
    },
    {
        "id": 2,
        "paragraph_idx": 2,
        "source_text": "Hơn một nghìn ba trăm năm sau, các nhà nghiên cứu tìm thấy dấu vết của cuộc tấn công ấy dưới đáy hồ.",
        "spoken_text": "Hơn một nghìn ba trăm năm sau, các nhà nghiên cứu tìm thấy dấu vết của cuộc tấn công ấy dưới đáy hồ.",
        "intent": "Giọng tò mò, khám phá, chuyển tiếp thời gian nghìn năm.",
        "tone": "tò mò, hào hứng",
        "pause_ms": 400,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 3,
        "paragraph_idx": 2,
        "source_text": "Nhưng ban đầu, họ không đi tìm chiến tranh. Họ đang tìm hiểu khí hậu.",
        "spoken_text": "Nhưng ban đầu, họ không đi tìm chiến tranh. Họ đang tìm hiểu khí hậu.",
        "intent": "Nhấn vào nghịch lý thú vị: tìm khí hậu nhưng lại chạm vào chiến tranh.",
        "tone": "bất ngờ, nhấn nhá",
        "pause_ms": 600,
        "pace": 0.99,
        "gain_db": 0.2
    },

    # Beat 2: Bối cảnh Guatemala & Phương pháp khoa học
    {
        "id": 4,
        "paragraph_idx": 3,
        "source_text": "Câu chuyện bắt đầu ở miền bắc Guatemala, gần tàn tích một thành phố Maya ngày nay được gọi là Witzna.",
        "spoken_text": "Câu chuyện bắt đầu ở miền bắc Gua-te-ma-la, gần tàn tích một thành phố Maya ngày nay được gọi là Vít-na.",
        "intent": "Dẫn dắt vào địa danh cụ thể, nhịp kể tự nhiên, sáng rõ.",
        "tone": "dẫn dắt, khách quan",
        "pause_ms": 450,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 5,
        "paragraph_idx": 4,
        "source_text": "Năm 2013, nhóm nghiên cứu lấy những mẫu trầm tích từ hồ Laguna Ek’Naab.",
        "spoken_text": "Năm hai nghìn không trăm mười ba, nhóm nghiên cứu lấy những mẫu trầm tích từ hồ La-gu-na Éc Náp.",
        "intent": "Chi tiết khảo sát thực địa, phát âm rõ tên hồ và năm.",
        "tone": "khoa học, chân thực",
        "pause_ms": 400,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 6,
        "paragraph_idx": 4,
        "source_text": "Qua thời gian, vật chất lắng xuống đáy hồ thành từng lớp.",
        "spoken_text": "Qua thời gian, vật chất lắng xuống đáy hồ thành từng lớp.",
        "intent": "Giọng chậm rãi miêu tả dòng thời gian địa chất.",
        "tone": "trầm lắng, miêu tả",
        "pause_ms": 300,
        "pace": 0.98,
        "gain_db": 0.0
    },
    {
        "id": 7,
        "paragraph_idx": 4,
        "source_text": "Trong đó có phấn hoa, những dấu hiệu hóa học và các mảnh than.",
        "spoken_text": "Trong đó có phấn hoa, những dấu hiệu hóa học và các mảnh than.",
        "intent": "Liệt kê các bằng chứng tự nhiên.",
        "tone": "rành rọt, quan sát",
        "pause_ms": 350,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 8,
        "paragraph_idx": 4,
        "source_text": "Chúng giúp người nghiên cứu lần ngược về cảnh quan trước đây: cây gì từng mọc, đất đai được sử dụng ra sao, khi nào có lửa.",
        "spoken_text": "Chúng giúp người nghiên cứu lần ngược về cảnh quan trước đây: cây gì từng mọc, đất đai được sử dụng ra sao, khi nào có lửa.",
        "intent": "Nhịp điệu nhịp nhàng, giọng say mê giải mã quá khứ.",
        "tone": "hào hứng, mở rộng",
        "pause_ms": 650,
        "pace": 1.0,
        "gain_db": 0.1
    },

    # Beat 3: Nút thắt - Lớp than bất thường
    {
        "id": 9,
        "paragraph_idx": 5,
        "source_text": "Rồi họ gặp một lớp than nổi bật.",
        "spoken_text": "Rồi họ gặp một lớp than nổi bật.",
        "intent": "Hạ giọng, chậm lại, tạo sự chú ý đặc biệt vào phát hiện bất ngờ.",
        "tone": "kịch tính, tập trung",
        "pause_ms": 500,
        "pace": 0.97,
        "gain_db": 0.3
    },
    {
        "id": 10,
        "paragraph_idx": 6,
        "source_text": "Nó cho thấy một trận cháy lớn đã xảy ra quanh cuối thế kỷ thứ bảy.",
        "spoken_text": "Nó cho thấy một trận cháy lớn đã xảy ra quanh cuối thế kỷ thứ bảy.",
        "intent": "Khẳng định sự kiện hỏa hoạn lớn.",
        "tone": "nghiêm cẩn, rõ ràng",
        "pause_ms": 350,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 11,
        "paragraph_idx": 6,
        "source_text": "Sau sự kiện ấy, các dấu hiệu về hoạt động của con người giảm mạnh.",
        "spoken_text": "Sau sự kiện ấy, các dấu hiệu về hoạt động của con người giảm mạnh.",
        "intent": "Giọng trầm xuống, báo hiệu biến cố chấn động đối với đời sống con người.",
        "tone": "trầm lắng, bí ẩn",
        "pause_ms": 450,
        "pace": 0.98,
        "gain_db": 0.0
    },
    {
        "id": 12,
        "paragraph_idx": 7,
        "source_text": "Một nơi từng có người sinh sống và canh tác đã thay đổi rõ rệt sau đám cháy.",
        "spoken_text": "Một nơi từng có người sinh sống và canh tác đã thay đổi rõ rệt sau đám cháy.",
        "intent": "Đối chiếu sự trù phú trước đó và sự hoang vắng sau đó.",
        "tone": "suy tư, nuối tiếc",
        "pause_ms": 350,
        "pace": 0.99,
        "gain_db": 0.0
    },
    {
        "id": 13,
        "paragraph_idx": 7,
        "source_text": "Chuyện gì đã xảy ra ở đó?",
        "spoken_text": "Chuyện gì đã xảy ra ở đó?",
        "intent": "Câu hỏi tu từ đầy trăn trở, nghỉ dài để người nghe suy ngẫm.",
        "tone": "trăn trở, tò mò sâu sắc",
        "pause_ms": 700,
        "pace": 0.96,
        "gain_db": 0.2
    },

    # Beat 4: Tư duy khoa học - Lửa không tự nói lên danh tính
    {
        "id": 14,
        "paragraph_idx": 8,
        "source_text": "Một trận cháy lớn chưa đủ để kết luận có quân đội tấn công.",
        "spoken_text": "Một trận cháy lớn chưa đủ để kết luận có quân đội tấn công.",
        "intent": "Giọng phản biện khoa học, cẩn trọng, điềm đạm.",
        "tone": "điềm tĩnh, chuẩn xác",
        "pause_ms": 300,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 15,
        "paragraph_idx": 8,
        "source_text": "Lửa có thể xuất hiện vì nhiều nguyên nhân.",
        "spoken_text": "Lửa có thể xuất hiện vì nhiều nguyên nhân.",
        "intent": "Nêu giả thuyết tự nhiên khách quan.",
        "tone": "giải thích",
        "pause_ms": 350,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 16,
        "paragraph_idx": 8,
        "source_text": "Muốn tìm ra điều đã xảy ra, nhóm nghiên cứu cần một thứ mà lớp than không thể tự cung cấp: danh tính của sự kiện.",
        "spoken_text": "Muốn tìm ra điều đã xảy ra, nhóm nghiên cứu cần một thứ mà lớp than không thể tự cung cấp: danh tính của sự kiện.",
        "intent": "Nhấn mạnh từ 'danh tính của sự kiện' - mấu chốt của cuộc điều tra.",
        "tone": "nhấn nhá, then chốt",
        "pause_ms": 600,
        "pace": 0.99,
        "gain_db": 0.2
    },

    # Beat 5: Phát hiện khảo cổ học - Cái tên Bahlam Jol & Naranjo
    {
        "id": 17,
        "paragraph_idx": 9,
        "source_text": "Mảnh ghép ấy lại nằm trong những chữ khắc ở Witzna.",
        "spoken_text": "Mảnh ghép ấy lại nằm trong những chữ khắc ở Vít-na.",
        "intent": "Chuyển sang hướng văn tự khảo cổ, hé lộ chìa khóa.",
        "tone": "hé mở, hấp dẫn",
        "pause_ms": 450,
        "pace": 1.0,
        "gain_db": 0.1
    },
    {
        "id": 18,
        "paragraph_idx": 10,
        "source_text": "Các nhà khảo cổ tìm được một dấu hiệu giúp nhận diện tên cổ của thành phố: Bahlam Jol.",
        "spoken_text": "Các nhà khảo cổ tìm được một dấu hiệu giúp nhận diện tên cổ của thành phố: Ba-lam Hôn.",
        "intent": "Công bố tên cổ của thành phố rõ ràng, rành rọt.",
        "tone": "khám phá, rõ ràng",
        "pause_ms": 500,
        "pace": 0.99,
        "gain_db": 0.2
    },
    {
        "id": 19,
        "paragraph_idx": 11,
        "source_text": "Thoạt nghe, việc biết thêm một cái tên có vẻ không giải thích được một vụ cháy.",
        "spoken_text": "Thoạt nghe, việc biết thêm một cái tên có vẻ không giải thích được một vụ cháy.",
        "intent": "Đặt vấn đề tự nhiên, thân mật.",
        "tone": "tâm sự, gần gũi",
        "pause_ms": 350,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 20,
        "paragraph_idx": 11,
        "source_text": "Nhưng tên gọi ấy cho phép họ tìm Witzna trong những ghi chép của người Maya, thay vì chỉ nhìn nó như một khu phế tích.",
        "spoken_text": "Nhưng tên gọi ấy cho phép họ tìm Vít-na trong những ghi chép của người Maya, thay vì chỉ nhìn nó như một khu phế tích.",
        "intent": "Khẳng định sức mạnh của định danh lịch sử.",
        "tone": "thuyết phục, mở rộng",
        "pause_ms": 600,
        "pace": 1.0,
        "gain_db": 0.1
    },
    {
        "id": 21,
        "paragraph_idx": 12,
        "source_text": "Và Bahlam Jol đã xuất hiện trên một công trình ở Naranjo, một thành phố đối địch.",
        "spoken_text": "Và Ba-lam Hôn đã xuất hiện trên một công trình ở Na-ran-hô, một thành phố đối địch.",
        "intent": "Bước ngoặt kịch tính: tên thành phố xuất hiện nơi kẻ thù!",
        "tone": "kịch tính, bất ngờ",
        "pause_ms": 500,
        "pace": 0.98,
        "gain_db": 0.3
    },
    {
        "id": 22,
        "paragraph_idx": 13,
        "source_text": "Ghi chép tại đó kể về việc đốt Bahlam Jol vào ngày 21 tháng 5 năm 697.",
        "spoken_text": "Ghi chép tại đó kể về việc đốt Ba-lam Hôn vào ngày hai mươi mốt tháng năm, năm sáu trăm chín mươi bảy.",
        "intent": "Đọc chính xác, trang trọng mốc thời gian lịch sử cụ thể đến từng ngày.",
        "tone": "chính xác, khẳng định",
        "pause_ms": 650,
        "pace": 0.98,
        "gain_db": 0.2
    },

    # Beat 6: Hai nguồn bằng chứng & Sự chính xác của khoa học
    {
        "id": 23,
        "paragraph_idx": 14,
        "source_text": "Bây giờ, câu chuyện đã có hai đầu mối: một trận cháy được lưu lại trong trầm tích, và một cuộc đốt phá được bên chiến thắng ghi trên đá.",
        "spoken_text": "Bây giờ, câu chuyện đã có hai đầu mối: một trận cháy được lưu lại trong trầm tích, và một cuộc đốt phá được bên chiến thắng ghi trên đá.",
        "intent": "Tóm lược hai nguồn chứng cứ đối chiếu song song.",
        "tone": "tổng kết, rõ ràng",
        "pause_ms": 600,
        "pace": 1.0,
        "gain_db": 0.1
    },
    {
        "id": 24,
        "paragraph_idx": 15,
        "source_text": "Tuy nhiên, có một chi tiết rất dễ bị kể sai.",
        "spoken_text": "Tuy nhiên, có một chi tiết rất dễ bị kể sai.",
        "intent": "Hạ giọng cảnh báo, thu hút sự tập trung cao độ của người nghe.",
        "tone": "lưu ý, nhấn mạnh",
        "pause_ms": 450,
        "pace": 0.97,
        "gain_db": 0.2
    },
    {
        "id": 25,
        "paragraph_idx": 16,
        "source_text": "Lớp than dưới hồ không cho các nhà nghiên cứu biết chính xác ngày 21 tháng 5.",
        "spoken_text": "Lớp than dưới hồ không cho các nhà nghiên cứu biết chính xác ngày hai mươi mốt tháng năm.",
        "intent": "Làm rõ giới hạn thực tế của trầm tích.",
        "tone": "khách quan, điềm đạm",
        "pause_ms": 350,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 26,
        "paragraph_idx": 16,
        "source_text": "Niên đại được xác định cho nó nằm trong khoảng năm 690 đến 700. Ngày cụ thể đến từ văn khắc.",
        "spoken_text": "Niên đại được xác định cho nó nằm trong khoảng năm sáu trăm chín mươi đến bảy trăm. Ngày cụ thể đến từ văn khắc.",
        "intent": "Phân định minh bạch giữa niên đại carbon và niên đại chữ viết.",
        "tone": "chính xác khoa học",
        "pause_ms": 550,
        "pace": 1.0,
        "gain_db": 0.1
    },
    {
        "id": 27,
        "paragraph_idx": 17,
        "source_text": "Sức nặng của phát hiện nằm ở việc hai nguồn bằng chứng khác nhau phù hợp với nhau.",
        "spoken_text": "Sức nặng của phát hiện nằm ở việc hai nguồn bằng chứng khác nhau phù hợp với nhau.",
        "intent": "Khẳng định giá trị cốt lõi của sự kết hợp hai ngành khoa học.",
        "tone": "khẳng định, thuyết phục",
        "pause_ms": 600,
        "pace": 0.99,
        "gain_db": 0.2
    },

    # Beat 7: Dấu tích hiện trường đổ nát
    {
        "id": 28,
        "paragraph_idx": 18,
        "source_text": "Chưa hết. Khi kiểm tra các công trình lớn tại Witzna, các nhà khảo cổ còn tìm thấy dấu cháy và sự phá hủy.",
        "spoken_text": "Chưa hết. Khi kiểm tra các công trình lớn tại Vít-na, các nhà khảo cổ còn tìm thấy dấu cháy và sự phá hủy.",
        "intent": "Nối tiếp bằng nguồn bằng chứng thứ ba: hiện vật thực tế trên mặt đất.",
        "tone": "bổ sung, kịch tính",
        "pause_ms": 450,
        "pace": 1.0,
        "gain_db": 0.1
    },
    {
        "id": 29,
        "paragraph_idx": 19,
        "source_text": "Lời khắc về một cuộc đốt phá giờ có thể được đặt cạnh những gì còn lại ngay tại nơi bị tấn công.",
        "spoken_text": "Lời khắc về một cuộc đốt phá giờ có thể được đặt cạnh những gì còn lại ngay tại nơi bị tấn công.",
        "intent": "Đặt lời văn bên cạnh đống tro tàn thực tế.",
        "tone": "hình tượng, sâu sắc",
        "pause_ms": 400,
        "pace": 0.99,
        "gain_db": 0.0
    },
    {
        "id": 30,
        "paragraph_idx": 19,
        "source_text": "Đó là cơ sở để nhóm nghiên cứu liên kết trận cháy với cuộc chiến được ghi ở Naranjo.",
        "spoken_text": "Đó là cơ sở để nhóm nghiên cứu liên kết trận cháy với cuộc chiến được ghi ở Na-ran-hô.",
        "intent": "Chốt lại cơ sở chứng minh vững chắc.",
        "tone": "vững chãi, kết luận",
        "pause_ms": 650,
        "pace": 1.0,
        "gain_db": 0.1
    },

    # Beat 8: Lật lại cách hiểu về chiến tranh Maya
    {
        "id": 31,
        "paragraph_idx": 20,
        "source_text": "Nhưng vì sao một thành phố bị đốt lại khiến giới nghiên cứu phải xem xét lại cách hiểu về chiến tranh Maya?",
        "spoken_text": "Nhưng vì sao một thành phố bị đốt lại khiến giới nghiên cứu phải xem xét lại cách hiểu về chiến tranh Maya?",
        "intent": "Câu hỏi lớn chuyển mạch tư duy học thuật.",
        "tone": "trăn trở, mở rộng",
        "pause_ms": 550,
        "pace": 0.98,
        "gain_db": 0.2
    },
    {
        "id": 32,
        "paragraph_idx": 21,
        "source_text": "Bởi trước đó, một cách nhìn có ảnh hưởng cho rằng chiến tranh trong phần lớn thời kỳ Cổ điển thường tập trung vào giới cầm quyền:",
        "spoken_text": "Bởi trước đó, một cách nhìn có ảnh hưởng cho rằng chiến tranh trong phần lớn thời kỳ Cổ điển thường tập trung vào giới cầm quyền:",
        "intent": "Nêu lại định kiến lịch sử cũ.",
        "tone": "diễn giải",
        "pause_ms": 300,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 33,
        "paragraph_idx": 21,
        "source_text": "bắt giữ đối thủ, khuất phục một triều đại, buộc bên thua phải phục tùng.",
        "spoken_text": "bắt giữ đối thủ, khuất phục một triều đại, buộc bên thua phải phục tùng.",
        "intent": "Liệt kê dứt khoát 3 đặc trưng của chiến tranh cung đình quý tộc.",
        "tone": "liệt kê, dứt khoát",
        "pause_ms": 500,
        "pace": 0.99,
        "gain_db": 0.0
    },
    {
        "id": 34,
        "paragraph_idx": 22,
        "source_text": "Bạo lực vẫn tồn tại. Câu hỏi là nó lan rộng đến đâu, và người dân bên ngoài cung điện phải chịu những gì.",
        "spoken_text": "Bạo lực vẫn tồn tại. Câu hỏi là nó lan rộng đến đâu, và người dân bên ngoài cung điện phải chịu những gì.",
        "intent": "Giọng trăn trở, bắt đầu hướng sự quan tâm đến người dân thường.",
        "tone": "trăn trở, nhân bản",
        "pause_ms": 550,
        "pace": 0.98,
        "gain_db": 0.1
    },
    {
        "id": 35,
        "paragraph_idx": 23,
        "source_text": "Những hình thức tàn phá dữ dội hơn thường được gắn với giai đoạn muộn, khi nhiều trung tâm Maya rơi vào khủng hoảng.",
        "spoken_text": "Những hình thức tàn phá dữ dội hơn thường được gắn với giai đoạn muộn, khi nhiều trung tâm Maya rơi vào khủng hoảng.",
        "intent": "Nêu giả thuyết suy tàn muộn truyền thống.",
        "tone": "thông tin, bối cảnh",
        "pause_ms": 500,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 36,
        "paragraph_idx": 24,
        "source_text": "Witzna khiến cách sắp xếp ấy trở nên khó giữ nguyên.",
        "spoken_text": "Vít-na khiến cách sắp xếp ấy trở nên khó giữ nguyên.",
        "intent": "Đòn bẩy tư duy: Witzna đập tan sự sắp xếp khuôn sáo đó.",
        "tone": "khẳng định, nhấn mạnh",
        "pause_ms": 550,
        "pace": 0.98,
        "gain_db": 0.2
    },
    {
        "id": 37,
        "paragraph_idx": 25,
        "source_text": "Cuộc đốt phá năm 697 xảy ra sớm hơn giai đoạn suy tàn đó.",
        "spoken_text": "Cuộc đốt phá năm sáu trăm chín mươi bảy xảy ra sớm hơn giai đoạn suy tàn đó.",
        "intent": "Nhấn mạnh từ 'sớm hơn' - thời điểm then chốt.",
        "tone": "rõ ràng, nhấn nhá",
        "pause_ms": 350,
        "pace": 0.99,
        "gain_db": 0.1
    },
    {
        "id": 38,
        "paragraph_idx": 25,
        "source_text": "Dấu tích của nó cho thấy ảnh hưởng rộng đến thành phố và hoạt động của cư dân.",
        "spoken_text": "Dấu tích của nó cho thấy ảnh hưởng rộng đến thành phố và hoạt động của cư dân.",
        "intent": "Khẳng định phạm vi tàn phá toàn diện.",
        "tone": "sâu sắc, bao quát",
        "pause_ms": 450,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 39,
        "paragraph_idx": 26,
        "source_text": "Vì thế, không thể đơn giản kể rằng xã hội Maya chỉ chuyển sang chiến tranh hủy diệt khi mọi thứ đã bắt đầu sụp đổ.",
        "spoken_text": "Vì thế, không thể đơn giản kể rằng xã hội Maya chỉ chuyển sang chiến tranh hủy diệt khi mọi thứ đã bắt đầu sụp đổ.",
        "intent": "Bác bỏ luận điểm giản lược.",
        "tone": "phản biện, dứt khoát",
        "pause_ms": 400,
        "pace": 0.99,
        "gain_db": 0.1
    },
    {
        "id": 40,
        "paragraph_idx": 26,
        "source_text": "Ít nhất tại Witzna, sự tàn phá nghiêm trọng đã có mặt từ trước.",
        "spoken_text": "Ít nhất tại Vít-na, sự tàn phá nghiêm trọng đã có mặt từ trước.",
        "intent": "Đóng dấu kết luận cho phần bối cảnh chiến tranh.",
        "tone": "đanh thép, đọng lại",
        "pause_ms": 700,
        "pace": 0.97,
        "gain_db": 0.2
    },

    # Beat 9: Chiều sâu nhân văn - Những con người không có tiếng nói
    {
        "id": 41,
        "paragraph_idx": 27,
        "source_text": "Và đây là lúc câu chuyện chạm đến những người gần như không có tiếng nói trong bản ghi chiến thắng.",
        "spoken_text": "Và đây là lúc câu chuyện chạm đến những người gần như không có tiếng nói trong bản ghi chiến thắng.",
        "intent": "Chuyển sang giọng thì thầm, ấm áp, đầy lòng trắc ẩn.",
        "tone": "nhân văn, xúc động, lắng sâu",
        "pause_ms": 600,
        "pace": 0.96,
        "gain_db": 0.1
    },
    {
        "id": 42,
        "paragraph_idx": 28,
        "source_text": "Sau cuộc tấn công, hoạt động của con người giảm mạnh. Nhưng điều đó không cho biết số phận từng cư dân.",
        "spoken_text": "Sau cuộc tấn công, hoạt động của con người giảm mạnh. Nhưng điều đó không cho biết số phận từng cư dân.",
        "intent": "Sự im lặng của dữ liệu trước nỗi đau của con người cụ thể.",
        "tone": "trầm mặc, đồng cảm",
        "pause_ms": 500,
        "pace": 0.98,
        "gain_db": 0.0
    },
    {
        "id": 43,
        "paragraph_idx": 29,
        "source_text": "Bao nhiêu người chết? Bao nhiêu người bị bắt? Bao nhiêu người đã bỏ chạy?",
        "spoken_text": "Bao nhiêu người chết? Bao nhiêu người bị bắt? Bao nhiêu người đã bỏ chạy?",
        "intent": "Ba câu hỏi nhức nhối dồn dập, nhịp chậm dần, nặng trĩu xót xa.",
        "tone": "xót xa, day dứt, nhói lòng",
        "pause_ms": 750,
        "pace": 0.95,
        "gain_db": 0.2
    },
    {
        "id": 44,
        "paragraph_idx": 30,
        "source_text": "Các tác giả nghiên cứu không thể xác định điều ấy từ những bằng chứng hiện có.",
        "spoken_text": "Các tác giả nghiên cứu không thể xác định điều ấy từ những bằng chứng hiện có.",
        "intent": "Khoảng lặng trung thực của khoa học.",
        "tone": "thật thà, khiêm tốn",
        "pause_ms": 400,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 45,
        "paragraph_idx": 31,
        "source_text": "Khoảng trống này quan trọng.",
        "spoken_text": "Khoảng trống này quan trọng.",
        "intent": "Khẳng định giá trị của việc biết dừng lại đúng lúc.",
        "tone": "nhấn mạnh, rành rọt",
        "pause_ms": 400,
        "pace": 0.98,
        "gain_db": 0.2
    },
    {
        "id": 46,
        "paragraph_idx": 31,
        "source_text": "Bởi nếu kể rằng toàn bộ dân cư bị giết, hoặc cả thành phố biến mất chỉ trong một đêm, chúng ta sẽ làm câu chuyện dữ dội hơn bằng những điều chưa được chứng minh.",
        "spoken_text": "Bởi nếu kể rằng toàn bộ dân cư bị giết, hoặc cả thành phố biến mất chỉ trong một đêm, chúng ta sẽ làm câu chuyện dữ dội hơn bằng những điều chưa được chứng minh.",
        "intent": "Lời cảnh tỉnh chân thành về đạo đức kể chuyện lịch sử.",
        "tone": "chân thành, sâu sắc",
        "pause_ms": 650,
        "pace": 0.99,
        "gain_db": 0.1
    },
    {
        "id": 47,
        "paragraph_idx": 32,
        "source_text": "Điều có thể nói là cuộc tấn công đã gây tác động nặng nề lên cộng đồng sống tại đây.",
        "spoken_text": "Điều có thể nói là cuộc tấn công đã gây tác động nặng nề lên cộng đồng sống tại đây.",
        "intent": "Xác nhận sự thật không thể chối bỏ.",
        "tone": "vững vàng, chân thực",
        "pause_ms": 350,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 48,
        "paragraph_idx": 32,
        "source_text": "Đằng sau một dòng ghi chiến công là sự đứt gãy mà dữ liệu về cư trú và sử dụng đất vẫn còn cho thấy.",
        "spoken_text": "Đằng sau một dòng ghi chiến công là sự đứt gãy mà dữ liệu về cư trú và sử dụng đất vẫn còn cho thấy.",
        "intent": "Đối lập cay đắng giữa vinh quang kẻ thắng trận và sự đổ nát của đời sống thường dân.",
        "tone": "suy tư, cay đắng, xót xa",
        "pause_ms": 700,
        "pace": 0.97,
        "gain_db": 0.2
    },

    # Beat 10: Sự phục hồi bền bỉ
    {
        "id": 49,
        "paragraph_idx": 33,
        "source_text": "Witzna cũng không kết thúc hoàn toàn vào ngày bị đốt.",
        "spoken_text": "Vít-na cũng không kết thúc hoàn toàn vào ngày bị đốt.",
        "intent": "Mở ra một tia sáng hy vọng, giọng ấm và sáng hơn.",
        "tone": "ấm áp, kiên cường",
        "pause_ms": 400,
        "pace": 1.0,
        "gain_db": 0.1
    },
    {
        "id": 50,
        "paragraph_idx": 34,
        "source_text": "Thành phố có phục hồi một phần với quy mô dân cư nhỏ hơn.",
        "spoken_text": "Thành phố có phục hồi một phần với quy mô dân cư nhỏ hơn.",
        "intent": "Miêu tả sự kiên trì tái thiết.",
        "tone": "điềm đạm, miêu tả",
        "pause_ms": 350,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 51,
        "paragraph_idx": 34,
        "source_text": "Một tấm bia được dựng khoảng một thế kỷ sau cuộc tấn công cho thấy câu chuyện của nơi này còn tiếp diễn.",
        "spoken_text": "Một tấm bia được dựng khoảng một thế kỷ sau cuộc tấn công cho thấy câu chuyện của nơi này còn tiếp diễn.",
        "intent": "Sức sống bền bỉ vượt qua tro tàn.",
        "tone": "tiếp nối, xúc cảm",
        "pause_ms": 600,
        "pace": 0.99,
        "gain_db": 0.1
    },
    {
        "id": 52,
        "paragraph_idx": 35,
        "source_text": "Bởi vậy, phát hiện ấy không phải lời giải duy nhất cho sự suy tàn của cả thế giới Maya.",
        "spoken_text": "Bởi vậy, phát hiện ấy không phải lời giải duy nhất cho sự suy tàn của cả thế giới Maya.",
        "intent": "Giữ sự tỉnh táo, không vơ đũa cả nắm.",
        "tone": "khách quan, công tâm",
        "pause_ms": 400,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 53,
        "paragraph_idx": 35,
        "source_text": "Nó giúp sửa lại một phần bức tranh: chiến tranh đã có thể tàn phá một cộng đồng nghiêm trọng đến mức nào, ngay trước giai đoạn khủng hoảng về sau.",
        "spoken_text": "Nó giúp sửa lại một phần bức tranh: chiến tranh đã có thể tàn phá một cộng đồng nghiêm trọng đến mức nào, ngay trước giai đoạn khủng hoảng về sau.",
        "intent": "Đóng góp lịch sử đích thực của phát hiện Witzna.",
        "tone": "tổng kết, giá trị",
        "pause_ms": 700,
        "pace": 0.98,
        "gain_db": 0.1
    },

    # Beat 11: Đối chiếu hai đầu mối & Lời kết vang vọng
    {
        "id": 54,
        "paragraph_idx": 36,
        "source_text": "Hãy quay lại với hai đầu mối ban đầu.",
        "spoken_text": "Hãy quay lại với hai đầu mối ban đầu.",
        "intent": "Kéo người nghe quay về điểm khởi đầu của hành trình.",
        "tone": "gợi mở, tổng kết",
        "pause_ms": 450,
        "pace": 0.99,
        "gain_db": 0.1
    },
    {
        "id": 55,
        "paragraph_idx": 37,
        "source_text": "Một bên là văn khắc mà người chiến thắng muốn lưu lại. Một bên là những dấu vết vật chất tích tụ dưới hồ.",
        "spoken_text": "Một bên là văn khắc mà người chiến thắng muốn lưu lại. Một bên là những dấu vết vật chất tích tụ dưới hồ.",
        "intent": "Cấu trúc song hành đối xứng, nhịp điệu cân đối, giàu chất thơ lịch sử.",
        "tone": "đối xứng, nhịp nhàng",
        "pause_ms": 550,
        "pace": 0.98,
        "gain_db": 0.1
    },
    {
        "id": 56,
        "paragraph_idx": 38,
        "source_text": "Nếu chỉ có lời khắc, ta còn phải hỏi nó mô tả chính xác đến đâu.",
        "spoken_text": "Nếu chỉ có lời khắc, ta còn phải hỏi nó mô tả chính xác đến đâu.",
        "intent": "Nghi vấn về tính chủ quan của người ghi chép thắng cuộc.",
        "tone": "suy ngẫm",
        "pause_ms": 400,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 57,
        "paragraph_idx": 38,
        "source_text": "Nếu chỉ có lớp than, ta biết đã có lửa nhưng chưa đủ để gọi tên cuộc tấn công.",
        "spoken_text": "Nếu chỉ có lớp than, ta biết đã có lửa nhưng chưa đủ để gọi tên cuộc tấn công.",
        "intent": "Sự giới hạn của tự nhiên câm lặng.",
        "tone": "suy ngẫm",
        "pause_ms": 500,
        "pace": 1.0,
        "gain_db": 0.0
    },
    {
        "id": 58,
        "paragraph_idx": 39,
        "source_text": "Nhờ nhận diện được Bahlam Jol, các nhà nghiên cứu đã nối chúng lại với nhau.",
        "spoken_text": "Nhờ nhận diện được Ba-lam Hôn, các nhà nghiên cứu đã nối chúng lại với nhau.",
        "intent": "Điểm thắt nút hoàn hảo của câu chuyện khoa học.",
        "tone": "thăng hoa, tự hào",
        "pause_ms": 650,
        "pace": 0.99,
        "gain_db": 0.2
    },
    {
        "id": 59,
        "paragraph_idx": 40,
        "source_text": "Số phận của nhiều cư dân vẫn chưa thể kể trọn.",
        "spoken_text": "Số phận của nhiều cư dân vẫn chưa thể kể trọn.",
        "intent": "Giọng chùng xuống, lắng đọng đầy tình người.",
        "tone": "trầm lắng, khiêm cung",
        "pause_ms": 450,
        "pace": 0.96,
        "gain_db": 0.0
    },
    {
        "id": 60,
        "paragraph_idx": 40,
        "source_text": "Nhưng cuộc chiến ấy đã để lại nhiều hơn một lời tuyên công.",
        "spoken_text": "Nhưng cuộc chiến ấy đã để lại nhiều hơn một lời tuyên công.",
        "intent": "Lời dẫn nhập vào kết luận triết lý sâu xa.",
        "tone": "sâu lắng, dẫn dắt",
        "pause_ms": 500,
        "pace": 0.97,
        "gain_db": 0.1
    },
    {
        "id": 61,
        "paragraph_idx": 40,
        "source_text": "Nó còn để lại dấu cháy, những công trình bị phá hủy và một thay đổi lớn trong hoạt động của con người — những dấu vết mà hơn một nghìn năm sau, ta vẫn có thể đem ra đối chiếu.",
        "spoken_text": "Nó còn để lại dấu cháy, những công trình bị phá hủy và một thay đổi lớn trong hoạt động của con người — những dấu vết mà hơn một nghìn năm sau, ta vẫn có thể đem ra đối chiếu.",
        "intent": "Câu kết toàn bộ kịch bản, âm hưởng hào sảng, chậm rãi, ngân vang nghìn năm.",
        "tone": "vang vọng, bất hủ, kết thúc trọn vẹn",
        "pause_ms": 1000,
        "pace": 0.95,
        "gain_db": 0.2
    }
]

# Verify integrity: check if concatenation of source_text covers raw_text
def normalize(s):
    return re.sub(r'\s+', ' ', s).strip()

source_all = normalize(" ".join(u["source_text"] for u in units_data))
raw_all = normalize(raw_text)

print("Source all length:", len(source_all))
print("Raw all length:   ", len(raw_all))
assert source_all == raw_all, "Mismatch between source_text and raw_text!"
print("EXACT 100% MATCH: Every single word from the user's script is preserved without missing or duplicating anything!")

plan = {
    "title": "Mỏ Đen Maya — Vụ cháy Witzna 697 SCN và Lớp than Đáy hồ",
    "voice_profile": "projects/mo_den_maya/voice_direction/selected_voice_H.json",
    "accent": "Bắc",
    "speaker": "Mỏ Đen · Custom H (nam ~30 tuổi, thông minh, tò mò, khám phá, nhân văn)",
    "total_units": len(units_data),
    "units": units_data
}

(ROOT / "03_Kich_Ban_Bien_Kich_Dien_Doc.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(units_data)} units to 03_Kich_Ban_Bien_Kich_Dien_Doc.json successfully.")
