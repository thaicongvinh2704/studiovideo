from pathlib import Path
import importlib.util, json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = HERE.parent / 'source_materials'
spec = importlib.util.spec_from_file_location('tap2_assets', HERE / 'build_brief.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)
ART = catalog.ITEMS[:52]

# Editorial cleanup of several source strings that had lost word boundaries.
# Keep the production fields here readable in both the Markdown brief and JSON.
ART_COPY = {
    'A27': ('Ba hình hơi nước nối tiếp của cùng một luồng, xám trắng với viền nâu xám nhẹ và alpha mềm. Xuất riêng trên canvas 2048×2048, điểm phát x=.50,y=.85; lần lượt nhỏ, nở rồi tan. Không chứa đầu máy hoặc chữ.', 'Khói rời ống rồi bay lên và tan. Không lặp suốt phim, không che đầu máy hoặc đẩy khói vào mặt người dẫn.', 'Không khói nổ, lửa, hiệu ứng chiến tranh hoặc âm thanh sai ngữ cảnh.'),
    'A28': ('Khung cửa toa gỗ và một phần ghế theo R16, nhìn từ trong ra ngoài ngang tầm mắt. Cửa sổ trong suốt ở x=.30–.82,y=.16–.68; chỉ giữ nội thất mép trái và dưới. Không người. Tách gờ cửa tiền cảnh.', 'Cảnh ngoài chuyển ngang rồi dừng cùng tàu. Người dẫn nhìn theo hướng tàu chạy.', 'Không cửa tự động, kính panorama hoặc màn hình quảng cáo.'),
    'A29': ('Cặp kiếm dài và ngắn trong vỏ, tham chiếu bộ daisho thời Edo ở R17. Nhìn ngang hơi từ trên, chuôi bên trái, vỏ kéo sang phải; hai kiếm là hai file riêng, canvas 2560×1440 alpha. Chỉ dùng hoa văn thấy trong hiện vật.', 'Khi lời kể chuyển sang thay đổi pháp lý, thay hình tượng đặc quyền bằng nhãn mốc. Người trong R18 vẫn còn; con người không biến mất cùng thanh kiếm.', 'Không kiếm fantasy, họa tiết tự bịa, lưỡi sáng laser hoặc cảnh rút kiếm tấn công.'),
    'A30': ('Theo ảnh kiến trúc dân dụng Edo R19: một đoạn hiên, cột gỗ và cửa trượt đóng; góc ngang, không phải toàn phố. Canvas 3840×2160; cột ở x=.16, ngưỡng y=.77, vùng x=.30–.65 để ghép Mỏ Đen. Tách cột trước và nền hiên.', 'Mỏ Đen nhìn mốc 1868→1876 rồi cắt sang ảnh người thuộc giai đoạn chuyển tiếp. Ngôi nhà không biến thành Tokyo.', 'Không hoa anh đào hoặc cổng torii trang trí; không khẳng định đây là nhà của một samurai cụ thể.'),
    'A31': ('Khay gỗ ba ô chứa mẫu tự nhiên tổng quát: vỏ sò, lá khô và một bọ nhỏ. Tách khay và từng mẫu thành lớp riêng. Góc nhìn từ trên; canvas 2560×1440, không chữ hoặc mã hồ sơ. Đây không phải bộ mẫu của Darwin. Nếu cần bằng chứng, dùng ảnh R20 đã xác minh. Màu olive và nâu kem, theo nét bộ 198 ảnh.', 'Đưa mẫu vào theo nhịp lời kể về học tập và công việc. Không gắn kính hiển vi hiện đại với Darwin.', 'Không tự vẽ sổ tay Darwin; không dùng con bọ làm bằng chứng cho một phát hiện cụ thể.'),
    'A32': ('Dựa vào bản đầu On the Origin of Species năm 1859 trong R21. Tạo khối sách minh họa đúng màu và tỷ lệ bìa, góc ba phần tư nhẹ, gáy bên trái. Canvas 2560×2560 alpha. Xuất bìa trống và khối ruột riêng để compositor ghép ảnh bìa/trang tên thật. Không sinh chữ.', 'Mốc 1859 xuất hiện khi sách vào hình; sau đó chuyển sang sự kiện năm 1860.', 'Không gọi bản tái bản là bản đầu; không đặt DNA xoắn kép lên bìa năm 1859.'),
    'A33': ('Hộp gỗ đơn giản có khe trên, góc ba phần tư; một phiếu giấy trống đặt phía trên. Canvas 2048×2048 alpha, hộp chiếm 65%. Đây là ký hiệu biên tập, không phục dựng thùng phiếu hoặc lá phiếu năm 1860. Không cờ, con dấu hay tên ứng viên; compositor thêm nhãn.', 'Phiếu đi vào khe đúng ở từ “đắc cử”; tuổi 51 theo V16 xuất hiện bên dưới.', 'Không dựng lễ tuyên thệ ở mốc 1860; không máy bỏ phiếu điện tử.'),
    'A34': ('Dựa ảnh chuyến bay ngày 17/12/1903 và sơ đồ bảo tàng R22. Vẽ Wright Flyer hai tầng cánh bọc vải, khung gỗ, cánh lái nâng phía trước, bánh lái phía sau và hai cánh quạt đẩy đúng bố trí. Không bánh đáp hiện đại. Góc ba phần tư ngang theo nguồn, mũi sang phải; canvas 3840×2160 alpha. Tách thân/cánh cố định và cặp cánh quạt.', 'Bay ngang thấp trên bãi. Gắn số liệu 12 giây/37 mét với V17; nếu rút ngắn nhịp phim, ghi là minh họa.', 'Không máy bay Thế chiến I, động cơ phản lực, bánh xe tự thêm hoặc cabin kín.'),
    'A35': ('Cận một phần cánh khớp A34/R22: dải vải kem căng trên thanh gỗ mảnh, nhìn xiên từ trên để đọc kết cấu. Canvas 2560×1440; tách vải và thanh gỗ. Không đặt toàn máy bay cùng file. Đây là minh họa cấu tạo, không xác định vị trí cắt hiện vật nếu nguồn không ghi.', 'Tô sáng vật liệu rồi chuyển sang ảnh hiện vật R24. Không mô phỏng phá hủy máy bay lịch sử.', 'Không gán vị trí chính xác cho mảnh hiện vật nếu chưa xác minh; không dùng vải nylon hiện đại.'),
    'A36': ('Dựa R22: bãi cát phẳng và đường ray phóng thấp, không sân bay. Canvas 3840×2160; chân trời y=.40; ray từ x=.12,y=.77 đến x=.75,y=.65, phối cảnh khớp A34. Xuất bãi và ray riêng, không người hoặc công trình. Khóa phối cảnh trước khi tạo.', 'Máy bay rời điểm xuất phát, bóng tách khỏi đất. Chuyển sang tư liệu thật trước khi khẳng định thời lượng 12 giây.', 'Không đường băng nhựa, tháp điều khiển hoặc xe tải hiện đại.'),
    'A37': ('Theo ảnh Eagle trong R23, vẽ module Mặt Trăng trên chân đáp: tầng dưới cách nhiệt vàng, tầng trên xám, thang ở đúng mặt nhìn theo nguồn. Canvas 2560×2560 alpha, đủ chân đáp, góc ba phần tư. Không cờ hoặc phi hành gia sinh. Không thêm chữ NASA bằng AI; nhận diện phải theo ảnh nguồn.', 'Đặt trên A38 để neo năm 1969; chuyển sang R24 và sơ đồ nhánh vật liệu khi nhắc mảnh vải.', 'Không tàu con thoi, Artemis hoặc tên lửa Saturn V trên Mặt Trăng; không gắn vải bên ngoài module.'),
    'A38': ('Mặt đất xám có bụi mịn và đá nhỏ theo ảnh Apollo 11 trong R23; địa hình tương đối bằng, trời đen. Canvas 3840×2160; chân trời y=.38; vùng đặt module x=.40–.80,y=.60–.82. Tách nền xa và đất gần. Ghi “minh họa” ngoài hình.', 'Chỉ dùng làm cảnh thiết lập ngắn, sau đó cắt sang chân đổ bộ, ảnh thật hoặc niên biểu. Không dùng nền cho mọi câu về khoảng cách.', 'Không phóng đại Trái Đất; không mây, kim tự tháp hoặc dấu chân trước khi có người đổ bộ.'),
    'A39': ('Chỉ dựng sau khi lấy được ảnh hiện vật R24. Giữ đường viền và tỷ lệ theo catalog; một mảnh vải riêng trên nền alpha, nhìn trực diện. Không ép thành hình chữ nhật nếu nguồn khác dạng. Canvas 2048×2048; vật chiếm khoảng 60%. Ghi “minh họa theo hiện vật”; ảnh thật phải xuất hiện trước. Nếu thiếu nguồn, dùng ký hiệu trung tính V19.', 'Từ ảnh nguồn R24 chuyển sang bản minh họa có viền khớp. Apollo là nhánh riêng đi và về.', 'Không dùng cuộn vải 064, không bịa số niêm phong, không gọi hình sinh là ảnh hiện vật thật.'),
    'A40': ('Dựa hồ sơ R24 nhưng vẽ riêng mảnh gỗ. Giữ đường viền, hướng thớ và tỷ lệ dài/rộng theo nguồn; không tự suy kích thước. Canvas 2048×2048 alpha, vật chiếm khoảng 60%. Vân gỗ nhẹ, không giống khúc củi lớn. Compositor thêm tên và kích thước nếu catalog có.', 'Hai vật cùng nhánh Apollo; chỉ gắn gỗ với hành trình năm 1969, không đưa sang Ingenuity.', 'Không dùng gỗ 055 làm vật chứng; không tưởng tượng vết cháy hoặc lỗ đinh.'),
    'A41': ('Dùng ảnh hoặc sơ đồ vị trí mảnh vải trên Ingenuity từ R25. Vẽ riêng theo mảnh này; không nhân đôi A39 rồi đổi màu. Nếu nguồn thiếu ảnh chi tiết đáng tin, dùng ký hiệu vải trung tính V19 ghi “mảnh khác”. Canvas 2048×2048 alpha; không tự thêm logo, vít hoặc tem.', 'Nhánh Ingenuity xuất phát riêng từ Flyer, không nối từ Mặt Trăng. Hiện chữ “mảnh khác” cùng lúc.', 'Không kể một mảnh đi cả hai chuyến; không đặt mảnh gỗ trên Ingenuity nếu chưa có nguồn.'),
    'A42': ('Dựa ảnh NASA/JPL R26: thân Ingenuity hình hộp nhỏ bọc cách nhiệt, bốn chân thanh mảnh, hai tầng rotor đồng trục và tấm pin trên cùng theo nguồn. Canvas 2560×2560 alpha, toàn thân từ y=.10 đến .88. Tách thân/chân và tấm pin; rotor ở A43. Không biến thành drone bốn cánh.', 'Rotor quay; thân nâng lên, treo ổn định rồi hạ. Nếu dùng video thật dài 39,1 giây, giữ đúng tốc độ phát.', 'Không drone bốn cánh, cánh quạt máy bay hoặc con người trên Sao Hỏa.'),
    'A43': ('Bám A42 và tỷ lệ rotor trong R26. Xuất riêng từng tầng trên canvas 2560×2560 alpha, cùng pivot x=.50 và cùng trục đã khóa. Tạo bóng ellipse mềm thành lớp riêng. Nếu góc nhìn làm xoay 2D sai, dùng vòng quay mờ có ellipse đúng. Không thêm khói.', 'Hai rotor quay ngược chiều theo thiết kế. Khi thân nâng, bóng nhạt và tách xa vừa phải; kiểm tra độ cao so với mặt đất.', 'Không để cánh xuyên tấm pin; không dán bóng vào PNG; không jitter giả bay.'),
    'A44': ('Theo cảnh Mastcam-Z trong R26: đất nâu đỏ nhạt, đá nhỏ thưa, nền xa theo bố cục nguồn. Giữ bầu trời ngoài khung nếu ảnh gốc không có. Canvas 3840×2160; vùng hạ cánh x=.50,y=.76. Tách đất gần và nền xa, không gắn sẵn Ingenuity; khớp hướng sáng với A43.', 'Bay lên, treo rồi hạ trong cảnh ngắn. Ưu tiên video R26 nếu cần chuyển động thật.', 'Không tự thêm cỏ, nước, lửa, đô thị Sao Hỏa hoặc miệng núi lửa.'),
    'A45': ('Một đôi giày trẻ em trung tính và một cặp kính đọc tròn; mỗi vật một file trên canvas 2048×2048 alpha, góc ba phần tư từ trên, tông nâu kem. Không nhãn hiệu hoặc ảnh gia đình. Đây là ký hiệu trong trường quay hiện tại, không phải đồ vật của nhân chứng sinh năm 1900.', 'Tuổi 3 và 69 được nhập bằng vector; nối hai vật với mốc 1903 và 1969, ghi “người giả định sinh năm 1900”.', 'Không gợi rằng mọi người 69 tuổi đều cần gậy; không gán đồ vật cho Wright.'),
    'A46': ('Dải phim 35 mm cách điệu màu đen xám; một khung giữa rỗng, trong suốt thật, lỗ răng cưa vuông đều hai bên. Canvas 3840×2160 alpha; khung ở x=.25–.75,y=.15–.75. Không sinh ảnh Chaplin. Xuất dải trước và đoạn cuộn cong góc dưới phải riêng. Không logo hoặc tiêu đề.', 'Đặt ảnh phim có nguồn trong khung. Khung trượt khỏi hình khi ảnh Chaplin lớn tuổi xuất hiện cạnh niên biểu.', 'Không tô màu ảnh phim rồi gọi là ảnh thật; không đồng nhất The Tramp với trang phục Chaplin suốt đời.'),
    'A47': ('Một mũ quả dưa đen và một gậy cong mảnh, nhìn ba phần tư; mỗi vật riêng trên canvas 2048×2048 alpha, không nhân vật. Bám hình dáng phim R27; mũ không thành mũ cao bồi, gậy không thành gậy y tế. Nét mực và bóng phẳng theo bộ minh họa.', 'Đặt mũ và gậy xuống để câu chuyện về con người lớn tuổi tiếp tục. Không cho Mỏ Đen đóng giả Chaplin.', 'Không gắn ria mép rời lên mèo, đồng phục quân sự hoặc quảng cáo Apple.'),
    'A48': ('Micro phòng thu đầu thế kỷ XX có giá đỡ, dựa ảnh R29 nếu dùng đúng cảnh phim năm 1940. Canvas 2048×2048 alpha, nghiêng nhẹ sang phải; không logo hoặc chữ diễn văn. Nếu nguồn không cho thấy micro, dùng biểu tượng âm thanh vector V22 thay vì gán mẫu chính xác.', 'Dùng cùng ảnh phim năm 1940 và biểu tượng âm thanh; không ghép giọng giả đọc diễn văn.', 'Không micro podcast hiện đại; không trích lời phim ngoài kịch bản.'),
    'A49': ('Dựa ảnh Apple I trong catalog R30. Bo mạch nằm ngang, nhìn ba phần tư từ trên; giữ đúng nhóm và khối linh kiện, không biến thành bo mạch PC năm 1995. Canvas 2560×2048 alpha; chiếm 75% chiều rộng. Không màn hình, bàn phím hoặc vỏ tích hợp. Không sinh chữ/logo; compositor thêm tên Apple I nếu cần.', 'Ảnh hiện vật R30 xuất hiện trước; sau đó sơ đồ đi cạnh mốc năm 1976. Không đặt bo mạch trong tay Chaplin.', 'Không Macintosh 1984, Apple II 1977, iPhone hoặc logo phát sáng trên laptop.'),
    'A50': ('Theo ảnh hệ Apple I trong R30, vẽ màn hình CRT và bàn phím rời. Không khẳng định đây là bộ phụ kiện bán kèm tiêu chuẩn nếu catalog không nói. Màn hình trống trong suốt, ở x=.23–.77,y=.18–.62 trên canvas 2048×2048; góc ba phần tư nhẹ. Tách vỏ và lớp che. Thêm ánh xanh phosphor ở hậu kỳ; không sinh chữ.', 'Chuyển từ bo mạch sang thiết bị rời; ghi “cấu hình minh họa”. Nếu thiếu nguồn, chỉ dùng bo mạch A49.', 'Không bắt buộc có chuột; không nút Start, giao diện hiện đại hoặc logo Apple mới trên máy cũ.'),
    'A51': ('Máy PC để bàn màu be, màn hình CRT tỷ lệ 4:3, thùng máy hộp, bàn phím và chuột có dây; tách từng bộ phận theo thiết bị R33. Góc ba phần tư nhẹ từ trái, canvas 3840×2160 alpha. Màn hình ở x=.48–.77,y=.18–.62, chừa lỗ trong suốt để ghép giao diện Windows 95 thật từ R32. Không người hoặc nội thất cung đình. Đây là máy tính giả định của khán giả hiện nay, không phải đồ của Bảo Đại.', 'Con trỏ đi vào nút Start trên ảnh giao diện thật; cắt sang chân dung Bảo Đại bằng khung tách rõ.', 'Không màn hình phẳng, laptop, RGB, Windows XP/11, iPhone hoặc Bảo Đại dùng chuột.'),
    'A52': ('Một ghế làm việc xám đơn giản, không nhãn, nhìn từ sau ba phần tư; canvas 2048×2048 alpha. Khớp góc bàn A51, ghế bên trái PC. Không người, áo bào, gậy hoặc vương miện. Mặt ghế và lưng đọc rõ, không chiếm màn hình. Đây là đạo cụ ví von hiện tại cho đoạn 70.', 'Dừng máy quay trên ghế trống đúng câu “không có bằng chứng”, rồi trở về niên biểu. Không lấp ghế bằng nhân vật lịch sử.', 'Không chân dung Bảo Đại trên lưng ghế; không ám chỉ ông vừa rời ghế.'),
}
for item in ART:
    if item['id'] in ART_COPY:
        item['spec'], item['motion'], item['forbid'] = ART_COPY[item['id']]
ART_NAMES = {
    'A25':'Đầu máy và toa đúng giai đoạn 1863',
    'A27':'Hơi nước tách lớp',
    'A29':'Cặp kiếm đeo samurai: đạo cụ nhận diện',
    'A30':'Khung cửa nhà Edo dùng cho người dẫn',
    'A32':'Sách xuất bản năm 1859: bìa nền có khóa nguồn',
    'A34':'Wright Flyer năm 1903: toàn bộ máy bay',
    'A37':'Module Mặt Trăng Apollo 11',
    'A38':'Mặt đất Mặt Trăng: vùng đặt module',
    'A41':'Mảnh vải khác đi Ingenuity',
    'A42':'Ingenuity: thân và càng đáp',
    'A43':'Ingenuity: rotor và bóng độc lập',
    'A44':'Bãi bay Sao Hỏa, góc theo chuyến đầu',
    'A45':'Hai đồ vật gợi tuổi 3 và 69',
    'A46':'Dải phim với một khung ảnh mở',
    'A47':'Mũ quả dưa và gậy của hình tượng màn ảnh',
    'A48':'Micro thời phim có tiếng',
    'A49':'Apple I: bo mạch năm 1976',
    'A50':'Màn hình CRT và bàn phím rời thời máy tính sớm',
    'A51':'Máy PC giữa thập niên 1990',
    'A52':'Ghế trống trong cảnh máy tính ví von',
}
ART_PURPOSES = {
    'A32':'Có chủ thể xuất bản rõ; chữ bìa chỉ lấy từ ảnh nguồn hoặc typesetting chính xác.',
    'A33':'Phân biệt đắc cử năm 1860 với nhậm chức năm 1861.',
    'A34':'Khóa cấu trúc và hướng bay của phương tiện; tách đủ lớp cho đoạn bay ngắn.',
    'A36':'Cho chuyến bay điểm bắt đầu và kết thúc có quan hệ rõ với mặt đất.',
    'A37':'Phân biệt tàu đổ bộ với tên lửa phóng; dùng ngắn và đúng.',
    'A38':'Tạo lớp không gian riêng; không ghép Cleopatra và phi hành gia vào một cảnh.',
    'A39':'Phân biệt hiện vật cụ thể với cuộn vải minh họa chung.',
    'A40':'Lời đọc nêu cả vải và gỗ; thể hiện đủ hai vật chứng.',
    'A41':'Phân biệt hai mảnh, tránh kể thành hành trình từ Mặt Trăng đến Sao Hỏa.',
    'A42':'Đúng phương tiện bay trên Sao Hỏa, đủ lớp cho cảnh cất và hạ.',
    'A43':'Tạo chuyển động bay có cấu trúc thay vì rung cả hình.',
    'A44':'Phân biệt địa hình Sao Hỏa với Mặt Trăng.',
    'A45':'Đo tiến bộ bằng một đời người giả định mà không bịa nhân chứng.',
    'A46':'Cho hình tượng Chaplin bước ra khỏi khung một thời kỳ.',
    'A47':'Nhận diện The Tramp bằng đạo cụ thay vì lặp chân dung.',
    'A48':'Nhấn rằng Chaplin không chỉ gắn với phim câm.',
    'A49':'Thay điện thoại bằng công nghệ đúng thời kỳ.',
    'A50':'Cho thấy cấu hình máy tính đời đầu, không để khán giả tự hình dung iPhone năm 1976.',
    'A51':'Đặt Windows 95 trên máy đúng thời, không gán thao tác cho Bảo Đại.',
    'A52':'Thể hiện câu từ chối suy diễn bằng chỗ ngồi trống có chủ đích.',
}
for item in ART:
    item['name'] = ART_NAMES.get(item['id'], item['name'])
    item['purpose'] = ART_PURPOSES.get(item['id'], item['purpose'])
ART_EXISTING = {
    'A20':'Ảnh 005/006 có thể tái dùng nếu góc phù hợp; cần góc ngang để ghép người dẫn đúng mặt bàn.',
    'A31':'Ảnh 022 (hộp mẫu) và 110 (bọ) có thể tái sử dụng. Chỉ tạo khay mới nếu cần góc nhìn từ trên.',
    'A35':'Ảnh 064 (cuộn vải) và 055 (gỗ) là đạo cụ chung, không đại diện hiện vật Flyer.',
    'A52':'Ghế 005 có thể tái dùng nếu góc phù hợp với bố cục PC đã khóa.',
}
for item in ART:
    item['existing'] = ART_EXISTING.get(item['id'], item['existing'])

CAT = [
('C01','Mỏ Đen ngồi 3/4 nhìn phải',[2,9,24,29,35],'Ngồi đúng nhận diện trong manifest mo_den_01; xoay toàn thân vừa phải sang phải khoảng 25–30°, đầu nhìn thêm 10° về phải, mắt vào mục tiêu ngoài khung. Hai chân trước nghỉ trước bụng; miệng khép, tò mò. Giữ nguyên tai, mặt nạ nâu, mắt xanh xám, bụng kem, chân và đuôi.','Dùng khi Mỏ Đen dẫn mắt vào vật chứng bên phải. Đây là ảnh pose mới cần kiểm tra nhận diện; không lật gương file hiện có.'),
('C02','Mỏ Đen ngồi 3/4 nhìn trái',[3,17,42,66],'Dùng cùng model sheet đã duyệt: thân xoay khoảng 25° sang trái, đầu và mắt nhìn trái, hai chân trước nghỉ, miệng khép, một bên mày hơi nâng. Không phản chiếu ngang PNG cũ; phải vẽ lại các mảng mặt và đuôi nhất quán.','Đối góc với C01 ở bố cục chân dung đôi hoặc cảnh PC.'),
('C03','Mỏ Đen chỉ sang phải',[4,12,18,48],'Mèo ngồi theo đúng model sheet, góc 3/4 sang phải. Một chân trước mở và vươn chéo tới điểm ngoài thân ở phía trên phải; bàn chân vẫn là bàn chân mèo cách điệu, không ngón tay người. Chân còn lại tựa trước bụng. Mắt nhìn đúng đầu ngón/chân đang chỉ. Toàn thân, tai, đuôi nằm trọn canvas alpha.','Dùng với đường thời gian, mốc Apollo hoặc điểm cần chú ý; vẽ mũi tên riêng.'),
('C04','Mỏ Đen chỉ sang trái',[3,30,43,67],'Cùng quy tắc nhận diện như C03 nhưng thân xoay trái và chân trước chỉ về phía trái. Vẽ lại đúng giải phẫu cách điệu từ reference; không mirror để tạo bên trái. Giữ cổ tay/bàn chân rõ, chân còn lại tựa thân, mắt nhìn mục tiêu.','Dùng đối góc theo bố cục và hướng nhìn; không lặp ở mọi đoạn.'),
('C05','Mỏ Đen giữ thước đo',[12,14,18,73],'Mỏ Đen ngồi chính diện 3/4. Hai chân trước đỡ một cây thước gỗ thẳng nằm ngang trước bụng; các đầu bàn chân ôm mép thước có tiếp xúc rõ. Xuất một bản thân không đạo cụ và một lớp chân trước riêng để compositor đặt thước thật đúng phối cảnh. Giữ thước rời; không in vạch/số bằng AI.','Cử chỉ nâng thước hoặc đặt thước xuống phải căn câu đọc; không làm thước cong.'),
('C06','Mỏ Đen cầm thẻ tư liệu trống',[6,29,52,56],'Mỏ Đen nhìn khán giả, hai chân trước đỡ mép dưới một thẻ trống ngang trước ngực. Thẻ là hình chữ nhật kem riêng, không chữ/ảnh giả. Hai chân trước phải phủ lên mép thẻ đúng lớp; mặt mèo và mắt không bị che. Tạo một file nhân vật không thẻ và một file hai chân trước cho compositing.','Chỉ dùng khi người dẫn đưa tài liệu ra; ảnh/tư liệu thật ghép sau, có nguồn.'),
('C07','Mỏ Đen mở ngăn kéo',[2,8,73],'Theo đúng pose master, ngồi cạnh tủ A01. Thân nghiêng nhẹ về phía tủ, mắt nhìn tay nắm; một chân trước vươn ngắn tới tay nắm, có điểm tiếp xúc tự nhiên, không kéo dài như cánh tay người. Chân sau giữ trên mặt đất. Xuất thân và chân trước che tay nắm thành hai file cùng canvas. Không vẽ tủ vào ảnh mèo.','Tạo thêm pose buông tay nếu cần; chuyển động chính do ngăn kéo A02 trượt ra.'),
('C08','Mỏ Đen nhìn qua vai vào bằng chứng',[15,26,52,55],'Góc nhìn sau vai nhưng vẫn thấy một phần má và mặt nạ bên phải; dùng chính silhouette, tai, đuôi và màu lông trong model sheet. Thân ngồi hướng vào vùng chứng cứ bên phải, không tự thiết kế lưng mới. Toàn thân nằm gọn trong canvas, không crop để giấu cấu trúc.','Đặt nhân vật nhỏ vừa phải để dẫn mắt tới vật chứng; không che chủ thể.'),
('C09','Mỏ Đen nhìn xuống mặt bàn',[13,45,53,63],'Mèo ngồi 3/4, đầu cúi vừa khoảng 12–15°, mắt nhìn điểm thấp bên phải như đang cân nhắc hiện vật. Hai chân trước gần bụng, không chạm vật nếu chưa có lớp bàn tay tương ứng. Miệng khép, suy nghĩ tập trung; giữ đặc điểm gương mặt đúng master.','Dùng một nhịp phản ứng rồi cắt sang chi tiết vật chứng.'),
('C10','Mỏ Đen mời khán giả nhìn lại',[16,28,40,57,72],'Ngồi thẳng đối diện khán giả, giữ tỉ lệ master. Một chân trước mở nhẹ sang bên như lời mời quan sát, thấp ngang ngực; chân kia tựa bụng. Biểu cảm bình tĩnh, ấm, miệng nhỏ; không cười rộng. Canvas vuông RGBA, toàn thân, chân và đuôi không bị cắt.','Dùng cho câu hỏi/kết luận. Đây là pose tĩnh, không tạo môi nói hay rig giả.'),
]

# Real historical evidence is acquired from catalogued collections; never generated.
SOURCES = [
('R01','Quang Trung / Nguyễn Huệ: hình đại diện có nguồn','01,03–07,71','Tìm tranh hoặc tượng do bảo tàng/cơ quan di sản định danh; lưu toàn ảnh, crop mặt riêng và caption. Ghi tác giả, thời điểm tác phẩm, nơi lưu giữ. Gắn nhãn “tranh/tượng minh họa đời sau” nếu không phải ảnh đương thời. Không dùng diễn viên phim làm ảnh thật.','Không gọi chân dung minh họa là ảnh chụp người thật.'),
('R02','George Washington: chân dung Lansdowne','01,03–07,71','Lấy toàn bộ Lansdowne Portrait của Gilbert Stuart, 1796, từ Smithsonian National Portrait Gallery (NPG.2001.13) hoặc nguồn có quyền tương đương; giữ file gốc và credit. Tạo crop mặt từ chính ảnh đó. Đây là chân dung năm 1796, không phải hình lễ nhậm chức năm 1789.','Không tái tạo lại chân dung bằng AI; không ghi ảnh này là tại lễ nhậm chức.'),
('R03','Lễ tuyên thệ Washington tại New York, 30/4/1789','05','Tìm tranh/khắc/tư liệu sự kiện có tác giả và niên đại tác phẩm; caption phải phân biệt tranh hồi cố với tư liệu đương thời. Ưu tiên khung có Washington và bối cảnh nghi lễ, không cần đám đông trang trí. Dùng ảnh Federal Hall hiện nay chỉ khi ghi là địa điểm hiện nay.','Không đổi New York thành Washington DC; không gọi tranh đời sau là ảnh chụp 1789.'),
('R04','Đại kim tự tháp Khufu ở Giza: ảnh toàn thể','09,17–24,28','Chọn ảnh hiện nay có caption xác định Pyramid of Khufu, góc nhận ra đúng kim tự tháp giữa quần thể Giza, độ phân giải đủ crop. Lưu cảnh gốc và crop. Đây là ảnh di tích hiện nay, chỉ làm khóa hình kiến trúc; không đại diện công trường cổ.','Không lấy kim tự tháp Maya hoặc kim tự tháp Khafre rồi đổi nhãn.'),
('R05','Hiện vật vữa thuộc Đại kim tự tháp','09–15','Tải hồ sơ The Met object 17.6.143: Specimen of Mortar from the Great Pyramid, ca. 2550 BCE, reign of Khufu. Giữ tên hiện vật/caption đúng. Lời giải thích tư liệu trong ZIP đã gọi sai nó là phù điêu trận chiến; cần sửa chú thích nguồn trước dựng. Bổ sung một ảnh cận đá Giza có caption riêng nếu cần texture.','Không phóng mẫu vữa thành ảnh tường đá; không gọi là phù điêu.'),
('R06','Cleopatra VII: đồng xu hoặc hiện vật được catalog','17–21','Chọn hiện vật có hồ sơ bảo tàng ghi rõ Cleopatra VII, số catalog, niên đại và nơi lưu giữ; ảnh đủ lớn để đọc chân dung nghiêng/biểu tượng. Lấy mặt trước/sau nếu có và giữ caption. Nếu dùng tác phẩm đời sau phải ghi rõ đó là hình dung hậu thế.','Không dùng Nefertiti, nữ hoàng phim, hay ảnh AI gắn thành Cleopatra.'),
('R07','Apollo 11: ảnh thật trên bề mặt Mặt Trăng','18–19,49,52–53','Chọn ảnh NASA Apollo 11 có mã frame/caption xác định module, phi hành gia hoặc cảnh bề mặt. Lưu ảnh gốc, caption, credit và danh tính người trong ảnh khi biết. Một crop phải truy ngược về ảnh gốc.','Không trộn Apollo khác, không ghép Cleopatra vào cùng cảnh lịch sử.'),
('R08','Ma mút lông xoăn: mô hình hoặc bộ xương khoa học','22–26','Chọn ảnh bảo tàng ghi rõ woolly mammoth, ưu tiên ảnh toàn thân nghiêng và cận đầu/ngà để khóa A13–A15. Ghi đó là mô hình phục dựng hay bộ xương. Kiểm tra quyền ảnh riêng.','Không yêu cầu ảnh chụp ma mút sống; không gọi mô hình là sinh vật thật.'),
('R09','Đảo Wrangel: ảnh hiện nay có định danh','23–26','Tìm ảnh lãnh nguyên/bờ biển do đơn vị nghiên cứu hoặc bảo tồn ghi địa danh Wrangel, kèm credit. Dùng để khóa địa hình tổng quát hiện nay; ảnh hiện đại không chứng minh mùa hoặc cảnh năm 2000 TCN.','Không thay bằng ảnh bất kỳ ở Greenland/Svalbard; không tuyết dày mặc định.'),
('R10','Oxford hiện nay: sinh hoạt hoặc không gian học','29,33–34','Chọn ảnh Oxford hiện nay có địa điểm/tác giả rõ, có người đi lại hoặc hoạt động học thay vì chỉ mặt tiền trống. Lưu caption và quyền. Nếu dùng Radcliffe Camera, ghi kiến trúc hiện nay, không gắn với năm 1096.','Không dùng công trình đời sau làm hình Oxford năm 1096.'),
('R11','Nguồn chính thức cho mốc giảng dạy Oxford 1096','29–34','Lưu trang lịch sử University of Oxford và đoạn nói có bằng chứng dạy học từ 1096, không có ngày thành lập rõ. Ghi URL, ngày truy cập và trích ý ngắn trong hồ sơ dựng. Nếu đưa screenshot lên hình, giữ nguồn/tiêu đề đủ đọc; đây là trang hiện đại, không phải văn kiện 1096.','Không thiết kế thiệp khai trương đại học năm 1096.'),
('R12','Mô hình/sơ đồ Tenochtitlan có niên đại tái hiện','30–32','Tìm ảnh mô hình hoặc sơ đồ từ INAH/Museo del Templo Mayor hay học thuật có trách nhiệm; lưu tên người làm, giai đoạn được mô tả và quyền ảnh. Cần một góc toàn đô thị giữa hồ và một góc gần kênh/đường đắp. Nếu mô hình biểu diễn đầu thế kỷ XVI, nhãn phải nói đúng giai đoạn đó.','Không lấy thành phố Maya làm Aztec; không gọi mô hình 1519 là hình năm 1325/1428.'),
('R13','Di tích Templo Mayor / Tenochtitlan hiện nay','30–34','Chọn ảnh khảo cổ tại địa điểm được định danh, có caption cơ quan quản lý/nhà nghiên cứu và credit. Dùng như dấu tích hiện nay, không phải nguyên trạng thành phố cổ. Cắt sang góc cận có chủ thể, tránh lặp đại cảnh mô hình R12.','Không nhập mọi kim tự tháp Mesoamerica thành một nền văn hóa.'),
('R14','Hiện vật/văn hóa ở Mexico có trước 1428','31','Chọn ít nhất một hiện vật hoặc di tích có hồ sơ xác định cộng đồng, địa điểm và niên đại trước 1428. Lưu caption đầy đủ và quyền. Chỉ khẳng định đúng phạm vi bằng chứng; không dùng một hiện vật đơn lẻ đại diện mọi châu Mỹ.','Không gán mọi cư dân/vật phẩm Mexico trước 1428 là Aztec.'),
('R15','London Metropolitan Railway: ga thời kỳ mở tuyến','35–37','Tìm tranh/ảnh ga giai đoạn 1863 từ London Transport Museum hoặc kho tư liệu có catalog; ghi ga, ngày ảnh/tranh và medium. Nếu là tranh hồi cố, ghi “minh họa”. Cần thấy đường ray, mép sân ga và kết cấu mái đủ để khớp A24.','Không dùng ga Tube hiện nay rồi bỏ nhãn thời gian.'),
('R16','Đầu máy hơi nước/toa mở tuyến năm 1863','35–37','Tìm catalog museum về đầu máy/toa thực sự phục vụ khai trương Metropolitan Railway ngày 10/1/1863; ghi loại máy, năm chế tạo và ảnh. Cần góc ngang toàn máy, bánh và cửa toa nếu có. Nếu tư liệu chỉ khóa được đầu máy thời kỳ đầu nhưng không phải máy khai trương, chú thích “minh họa thời kỳ đầu” và không đặt số hiệu giả.','Không dùng A Class đặt hàng năm 1864 rồi nói là máy khai trương 1863.'),
('R17','Kiếm/giáp samurai cuối Edo có hồ sơ','34–40','Chọn kiếm có catalog V&A hoặc bảo tàng tương đương, niên đại/giai đoạn rõ; ảnh thấy chuôi và vỏ, thêm cận hiện vật nếu dùng. Giáp phải có nhãn thời kỳ/chức năng, không mặc định ai cũng mặc giáp khi đi lại. Giữ số catalog và quyền ảnh.','Không dùng cosplay, katana fantasy hoặc giáp Trung Hoa.'),
('R18','Ảnh samurai thế kỷ XIX có định danh','35,38–40','Tìm ảnh lưu trữ có caption “samurai”, tên người nếu xác định, nhiếp ảnh gia và niên đại ước tính. Nếu là ảnh studio dàn dựng, ghi rõ. Dùng để cho thấy con người tiếp tục tồn tại qua chuyển đổi địa vị; không vẽ họ biến mất năm 1876.','Không gán người mặc kimono bất kỳ thành samurai năm 1863.'),
('R19','Nhà/cửa thời Edo: ảnh hoặc phục dựng có nhãn','38–40','Chọn tư liệu kiến trúc dân dụng cuối Edo có cơ quan lưu giữ/định danh; ảnh phục dựng hiện nay phải ghi rõ. Chỉ cần hiên, cột, cửa trượt làm khóa góc A30; không cần ảnh toàn phố.','Không gắn nhà phim trường thành ảnh chụp phố Nhật năm 1863.'),
('R20','Darwin khoảng năm 1859: chân dung/tài liệu','42–46','Ưu tiên chân dung có ngày chụp khoảng 1859 hoặc gần tuổi 50, ghi người chụp và nguồn. Ảnh Darwin già hơn vẫn dùng được nếu ngày ảnh hiện rõ và không gắn nhãn tuổi 50. Sổ/mẫu chỉ dùng khi catalog liên hệ trực tiếp với Darwin.','Không dùng ảnh già rồi chú thích “Darwin 50 tuổi”; không gán mẫu tự nhiên chung cho ông.'),
('R21','Bản in đầu On the Origin of Species, 1859','43,45','Tìm bìa/trang tên scan từ thư viện khoa học hoặc archive, ghi edition, nhà xuất bản, năm, mã bản. Giữ bản scan gốc; dựng một mặt phẳng phối cảnh từ scan nếu cần.','Không in bìa DNA hiện đại hoặc chữ AI; không trộn ấn bản tái bản với bản đầu.'),
('R22','Chuyến bay Wright ngày 17/12/1903','47–48,51–52','Lấy ảnh chuyến bay đầu Wright Flyer có caption xác định ngày, Orville điều khiển và Wilbur tại mặt đất; lưu toàn khung. Bổ sung ảnh/sơ đồ cấu trúc chiếc Flyer 1903 cho A34. Không dùng ảnh chuyến bay khác làm chuyến đầu 12 giây.','Không gán nhầm phi công hoặc dùng máy bay đời sau.'),
('R23','Apollo 11 Eagle và vật chứng chuyến đi','49,52–53','Lấy ảnh Eagle/module trên Mặt Trăng có frame ID, tên nhiệm vụ và credit NASA; nếu dùng ảnh hiện vật vật liệu đi theo, giữ đúng provenance. Không xóa/vẽ thêm chi tiết lên ảnh nguồn rồi trình bày như bản gốc.','Không gắn mảnh vải lên ngoài module nếu nguồn không chứng minh vị trí.'),
('R24','Mảnh vải và gỗ từ Wright Flyer mang trên Apollo 11','52–53,56','Tải hồ sơ hiện vật Smithsonian NASM A19721288000. Cần ảnh cận của cả vải và gỗ, tên catalog, mô tả kích thước/provenance, điều kiện sử dụng. Trang hiện có thể chặn tải; nếu không lấy được, tìm NASA/Smithsonian khác có hồ sơ tương đương. Chưa có file ảnh xác minh thì không sinh hình giả hiện vật.','Không thay bằng cuộn vải/gỗ generic; không bỏ mất một trong hai mảnh.'),
('R25','Mảnh vải khác trên Ingenuity','54,56','Lấy NASA/JPL PIA24438 “Pride of the West and Mars”; giữ caption nói mảnh muslin 1,3 × 1,3 cm được bọc bảo vệ và gắn dưới tấm pin. Mở ảnh gốc, kiểm vị trí hiển thị và credit trước khi tạo A41. Đây là mảnh khác với vải/gỗ Apollo.','Không sao chép mảnh Apollo và gọi là vật đã chuyển sang Sao Hỏa.'),
('R26','Video/ảnh chuyến bay đầu Ingenuity ngày 19/4/2021','54–55','Lấy video NASA/JPL PIA24521/Mastcam-Z gồm cất cánh, treo, hạ; giữ credit và tốc độ phát. Tổng chuyến bay 39,1 giây. Ưu tiên dùng video thật cho chuyển động.','Không gọi render 3D là video thật; nêu đúng “chuyến bay có động cơ, điều khiển đầu tiên trên hành tinh khác”.'),
('R27','Chaplin trong vai The Tramp','58–61','Chọn still có tên phim/năm và nguồn quyền rõ; một ảnh toàn thân để thấy mũ, gậy, dáng và một crop mặt từ cùng ảnh. Ảnh di sản Chaplin không mặc định tự do thương mại; lưu credit/điều kiện.','Không dùng cosplay hoặc gọi trang phục vai diễn là đồ cả đời Chaplin.'),
('R28','Chaplin ngoài hình tượng Tramp ở tuổi trưởng thành/già','59,61,64','Chọn chân dung đời thực có người chụp, năm hoặc khoảng năm, nguồn lưu trữ. Không phục hồi mặt bằng AI. Đặt cạnh R27 với ngày ảnh để cho thấy đời ông tiếp tục, không tạo cảm giác ông xuất hiện tại Apple.','Không ghép ria mép/áo The Tramp vào ảnh đời thật.'),
('R29','The Great Dictator (1940): xác nhận phim có lời thoại','62','Tìm still/trailer chính thức có credit và tên phim/năm; chỉ cần một hình xác thực, không cần trích diễn văn. Kiểm tra quyền clip/hình riêng. Có thể thay bằng bìa poster lưu trữ nếu quyền rõ.','Không dùng ảnh Hitler thật; không tạo/nhái lời diễn văn hoặc âm thanh Chaplin.'),
('R30','Apple I: bo mạch máy tính năm 1976','59–60','Chọn ảnh hiện vật Apple I của Computer History Museum hoặc catalog đáng tin; lưu tên model, năm và credit. Lấy một ảnh toàn bo mạch và một cận có thể crop. Mọi thiết bị CRT/bàn phím đi kèm phải có nguồn riêng; không mặc định là bộ bán kèm năm 1976.','Không dùng Apple II/Macintosh/iPhone làm Apple I.'),
('R31','Bảo Đại thời trị vì: chân dung có nguồn','65–69,71','Chọn chân dung do Bảo tàng Lịch sử Quốc gia hoặc archive định danh; lưu caption, ngày/ước lượng, credit và quyền. Lấy toàn khung và crop mặt từ cùng file. Ảnh áo bào không tự động là lúc lên ngôi năm 1926.','Không nhầm Khải Định; không vẽ áo bào giả bằng AI.'),
('R32','Windows 95: ảnh chụp giao diện thật','66,70','Lấy screenshot đúng Windows 95 có taskbar và Start menu. Dùng desktop và menu mở thành hai trạng thái từ cùng hệ điều hành. Lưu phiên bản/nguồn; không để AI viết chữ trong giao diện.','Không dùng Windows 98/XP/11 hoặc mockup chữ sai.'),
('R33','PC CRT giữa thập niên 1990','66,70','Tìm ảnh catalog máy tính để bàn beige với CRT 4:3, thùng máy, bàn phím và chuột có dây; ghi mẫu/năm nếu có. Chỉ làm đạo cụ bối cảnh cho ví von của người kể, không gán là máy của Bảo Đại.','Không laptop, màn hình phẳng hoặc RGB hiện đại.'),
('R34','Bảo Đại sau thoái vị: ảnh có ngày/địa điểm','67–69','Tìm ảnh archive sau 1945 có caption, địa điểm, người chụp và năm; nếu chỉ có ảnh một giai đoạn trước, không chú thích Paris 1997. Dùng ảnh thật có quyền; nếu không có ảnh phù hợp, kể phần sau bằng trục đời người, không sinh mặt già giả.','Không suy ảnh Paris 1997 từ ảnh không ngày; không mô tả ông còn làm vua.'),
('R35','Lincoln giai đoạn 1859–1860','42–46','Chọn ảnh có catalog LOC và ngày chụp giai đoạn 1859–1860; giữ đúng trạng thái râu trong ảnh. Nếu dùng ảnh giai đoạn bầu cử, caption phải nêu rõ phạm vi. Cần chân dung rõ để đặt tuổi 51 bên dưới.','Không dùng ảnh năm 1864 rồi gọi là Lincoln ở tuổi 51.'),
('R36','Nguồn Washington: ngày tháng, lễ nhậm chức','03–05','Lưu Mount Vernon/National Archives hoặc nguồn lịch sử uy tín cho sinh 1732, mất 1799 và nhậm chức tại New York ngày 30/4/1789. Nối URL với từng mệnh đề trong registry; không tạo ảnh giấy chứng nhận.','Không lấy sống đồng thời làm bằng chứng hai người từng biết nhau.'),
('R37','Hồ Gươm: chỉ dùng làm ví von địa điểm','20','Nếu dùng câu ví von, chọn một ảnh Hồ Gươm hiện nay có địa điểm và quyền ảnh rõ; hoặc bỏ ảnh thật và dùng sơ đồ hai khung chung một địa điểm. Không lấy ảnh người quen hay ghép chân dung lịch sử vào ảnh thật.','Không để “cùng nơi” bị hiểu là “cùng thời”.'),
]

GRAPHICS = [
('V01','Hai đường đời Nguyễn Huệ và Washington',[1,3,4,71],'Hai hàng tách biệt trên cùng trục năm 1732–1800; Washington 1732–1799, Nguyễn Huệ 1753–1792 (năm sinh Nguyễn Huệ ghi “thường được ghi nhận”). Dùng cùng scale năm, tô rõ toàn bộ đời Nguyễn Huệ nằm trong đời Washington. Gắn ngoặc “21 tuổi tính theo năm sinh” và “sống thêm 7 năm theo hiệu năm”. Không làm hai chân dung gặp nhau.'),
('V02','Hai sự kiện riêng cùng năm 1789',[1,5],'Một mốc năm lớn ở giữa; trái: Tết Kỷ Dậu, Quang Trung đánh bại quân Thanh; phải: 30/4/1789, Washington nhậm chức tại New York. Mỗi sự kiện nằm trong khung/địa điểm riêng. Không đường nối quan hệ hay cảnh gặp mặt.'),
('V03','Cùng thời không có nghĩa là liên hệ',[6,24,60,70],'Hai hồ sơ đặt xa nhau, nhãn “cùng thời” ở trên và vùng trống ghi “chưa có bằng chứng gặp, thư từ hoặc biết nhau”. Chữ được dàn bằng SVG/compositor. Không tạo thư giả, đường ảnh hưởng hay dấu X sau khi đã gây hiểu nhầm.'),
('V04','Độ tuổi của kim tự tháp và khoảng tới năm 2026',[9,10,12,13],'Một trục đúng tỷ lệ thứ tự cho khoảng 2550 TCN, 7–4 TCN, 2026 SCN. Tính khoảng theo các mốc chọn: 2543–2546 năm và 2029–2032 năm; đoạn trước Chúa Giê-su dài hơn khoảng 511–517 năm. Ghi rõ mọi năm xây là xấp xỉ. Không đặt năm 0.'),
('V05','Lịch TCN/SCN không có năm 0',[11,14],'Bốn nhãn 2 TCN, 1 TCN, 1 SCN, 2 SCN với khoảng cách mỗi năm bằng nhau; không có ô số 0. Ví dụ phép tính 7 + 2026 − 1 = 2032. Không tạo lịch lật trang khiến một khoảng năm biến thành hai.'),
('V06','Đổi điểm nhìn trong phép so kim tự tháp',[15,16],'Hai điểm nhìn giả định trên cùng thước: người ở đầu Công nguyên nhìn về công trình khoảng 2000 tuổi; người hiện nay nhìn về di tích khoảng 2000 tuổi. Ghi nhãn đây là tình huống để đo khoảng cách, không phải nói Chúa Giê-su đã tới Giza. Không vẽ Chúa Giê-su.'),
('V07','Cleopatra: 2520 năm về kim tự tháp, 1998 năm tới Apollo','17–19,21,71','Dùng mốc Cleopatra mất năm 30 TCN. Hai đoạn cùng tỷ lệ: 2550→30 TCN khoảng 2520 năm; 30 TCN→1969 khoảng 1998 năm. Chênh khoảng 522 năm, tương ứng gần với mốc Khufu. Không đổi điểm neo sang năm sinh Cleopatra giữa phép tính.'),
('V08','Cùng địa điểm không chứng minh cùng thời',[20,21],'Hai khung ảnh cùng địa điểm nhưng khác nhãn thời gian, sau đó tách ra trên trục; nếu dùng Hồ Gươm thì ghi là ví von. Không tạo cảnh Cleopatra thăm kim tự tháp đang xây.'),
('V09','Bản đồ Giza và đảo Wrangel','23–26','Bản đồ có nguồn và bờ biển thật, Giza ở Ai Cập và Wrangel ở Bắc Băng Dương. Dùng inset vùng cực nếu cần; ghi vị trí định vị hiện nay. Không vẽ tuyến di cư giữa chúng hoặc để đảo nằm sai phía đường đổi ngày.'),
('V10','Nhiều vùng đã mất ma mút, Wrangel còn quần thể cuối','23–27','Sơ đồ khái niệm hai hàng: phần lớn vùng phân bố biến mất trước, quần thể Wrangel tiếp tục tới khoảng 4000 BP (xấp xỉ 2000 TCN). Ghi “khoảng”, không biểu thị số lượng cá thể hay nguyên nhân tuyệt chủng chưa được chứng minh. Không vẽ con ma mút cuối cùng chết.'),
('V11','Oxford và hai mốc Mexico là ba loại sự kiện','29–32','Trục 1000–1500: 1096 là bằng chứng giảng dạy Oxford; 1325 là mốc truyền thống của thành phố Tenochtitlan; 1428 là liên minh thường dùng làm mốc đế chế Aztec. Tính chênh 229 và 332 năm theo đúng cặp; nhãn tên loại mốc luôn hiện. Không gọi 1096 là lễ thành lập chính thức.'),
('V12','Mexico trước 1428 không trống',[31],'Bản đồ có nguồn và một/tối thiểu một hiện vật R14 có địa điểm, văn hóa, niên đại được ghi rõ; sau đó thêm nhãn liên minh 1428. Không fade-in người từ hư không và không gọi toàn cư dân vùng Mexico là Aztec.'),
('V13','Thành phố sống và di tích','33–34','Đặt ảnh Oxford hiện nay bên một di tích Mexico có caption; thay đổi nhãn thời gian để chỉ ra cảm giác “còn sáng đèn = mới” đánh lừa trí nhớ. Không xếp hạng văn minh hoặc dùng ảnh không cùng phạm vi.'),
('V14','1863, 1868, 1876: thay đổi kéo dài','35,38–40,71','Trục 1860–1880 với hai hàng: tuyến đường sắt London mở 1863; Minh Trị 1868; các thay đổi địa vị samurai culminate 1876. Đường đời người tiếp tục sau mốc luật. Không làm mọi samurai biến mất trong một ngày.'),
('V15','Darwin và Lincoln sinh cùng ngày','41–42,44','Một trang lịch duy nhất ghi 12/2/1809; hai nhánh tới hồ sơ Darwin ở Anh và Lincoln ở Mỹ, tách địa lý và lĩnh vực. Ghi đây là trùng hợp, không hàm ý cùng bệnh viện, quen biết hoặc điềm báo.'),
('V16','Tuổi của Darwin và Lincoln khi đạt mốc nổi tiếng','43,45–46','Darwin sinh năm 1809, Origin xuất bản năm 1859, khoảng 50 tuổi; Lincoln sinh năm 1809, đắc cử năm 1860, khoảng 51 tuổi. Chỉ dùng ảnh đúng năm hoặc ghi rõ ngày ảnh khác. Không biến đổi chân dung.'),
('V17','Chuyến bay Wright: 12 giây, khoảng 37 mét',[48],'Vẽ thước 37 m (120 ft = 36,576 m, làm tròn) từ vị trí rời ray tới điểm hạ; đồng hồ 12 giây chỉ chạy đúng khi thời lượng video tương ứng. Nếu dựng rút gọn phải ghi minh họa rút gọn. Không suy tốc độ đồng đều.'),
('V18','Một đời giả định sinh năm 1900','49–50','Trục thời gian nối 1903 và 1969. Người giả định sinh năm 1900 khoảng 3 tuổi khi Flyer bay và khoảng 69 tuổi khi Apollo 11 hạ cánh; ghi “người giả định”. Từ 17/12/1903 đến 20/7/1969 chưa đủ 66 năm, nên chỉ nêu hiệu số năm là 66, không nói tròn 66 năm.'),
('V19','Hai nhánh vật liệu từ Flyer','52–56','Nhánh A: mảnh vải và gỗ Flyer → Apollo 11 → trở về Trái Đất. Nhánh B: mảnh vải khác → Ingenuity → Sao Hỏa. Gắn nhãn “mảnh khác” ngay trên nhánh B. Không vẽ mũi tên từ Mặt Trăng sang Sao Hỏa.'),
('V20','Chuyến bay Ingenuity 39,1 giây','54–55','Ba trạng thái cùng camera: cất cánh, treo, hạ; tổng 39,1 giây theo JPL, lời đọc làm tròn 39 giây. Nếu dùng clip thật, ghi tốc độ phát. Nêu đầy đủ phạm vi “chuyến bay có động cơ, được điều khiển đầu tiên trên một hành tinh khác”.'),
('V21','Lịch sử đổi tốc độ khác nhau','51,56–57','So sánh đúng hai ví dụ đã nêu: hàng thiên niên kỷ quanh Kim tự tháp và vài thập niên hàng không/vũ trụ. Nếu đổi thang đồ họa phải ghi thang; không tạo đồ thị tăng trưởng công nghệ giả định.'),
('V22','Chaplin: khung vai diễn và đường đời','58–64,71','Đường đời 1889–1977 tách khỏi khung vai The Tramp. Gắn The Great Dictator 1940 có lời thoại; Apple Computer Company founded as partnership 1/4/1976. Phân biệt mốc partnership với incorporation 1977. Không ngụ ý Chaplin dùng Apple.'),
('V23','Apple năm 1976 là máy tính, không phải iPhone','59–60','Đưa ảnh Apple I/bo mạch có nguồn và mốc năm 1976; đặt điện thoại hiện đại ở ô “liên tưởng hôm nay”, tách bạch để sửa cú nhầm. Không đặt điện thoại vào tay Chaplin.'),
('V24','Bảo Đại: vai trò vua kết thúc năm 1945, đời tới năm 1997','65–70,71','Hai thanh song song: đời người 1913–1997; thời kỳ lên ngôi 1926–thoái vị 1945. Đặt Windows 95 ra mắt ngày 24/8/1995 và ngày mất 31/7/1997. 1945→1997 chênh 52 năm theo hiệu năm; không kéo áo bào đến 1997 và không nói ông dùng máy tính.'),
('V25','Kết: đặt các phép so về đúng ngăn','71–73','Chỉ hồi nhắc 5 cặp: Quang Trung/Washington; Cleopatra/Giza/Apollo; samurai/London; Chaplin/Apple; Bảo Đại/Windows 95. Mỗi cặp dùng một biểu tượng và một kết luận đúng; chuyển 2–3 nhịp, không làm lưới 20 ô nhỏ. Kết lại tủ A01 với Mỏ Đen và lời kêu gọi ngắn.'),
]

SOURCE_LINKS = {
'R01':'https://baotanglichsuquocgia.vn/vi/Articles/3097/15721/ky-niem-225-nam-1789-2014-hoang-dje-quang-trung-nguyen-hue-djai-pha-quan-xam-luoc-man-thanh.html',
'R02':'https://npg.si.edu/object/npg_NPG.2001.13',
'R03':'https://www.mountvernon.org/george-washington/the-first-president/inauguration/timeline',
'R05':'https://www.metmuseum.org/art/collection/search/558193',
'R06':'https://www.britishmuseum.org/collection/term/BIOG57627',
'R07':'https://www.nasa.gov/missions/apollo/apollo-11/apollo-11-mission-overview/',
'R08':'https://www.nhm.ac.uk/discover/were-all-mammoths-woolly.html',
'R09':'https://pmc.ncbi.nlm.nih.gov/articles/PMC6121868/',
'R10':'https://www.ox.ac.uk/about/the-university/history',
'R11':'https://www.ox.ac.uk/about/the-university/history',
'R12':'https://www.inah.gob.mx/images/boletines/2025/213/Boletin%20213.pdf',
'R13':'https://www.inah.gob.mx/',
'R14':'https://deas.inah.gob.mx/pdf/publicaciones/publicaciones/publicacion%2839963%29-3447.pdf',
'R15':'https://library.ltmuseum.co.uk/Portal/Default/en-GB/RecordView/Index/108',
'R16':'https://library.ltmuseum.co.uk/Portal/Default/en-GB/RecordView/Index/97',
'R17':'https://www.vam.ac.uk/articles/samurai-japanese-arms-armour',
'R18':'https://www.vam.ac.uk/articles/samurai-japanese-arms-armour',
'R19':'https://www.vam.ac.uk/articles/samurai-japanese-arms-armour',
'R20':'https://darwinproject.ac.uk/people/about-darwin',
'R21':'https://darwinproject.ac.uk/people/about-darwin',
'R22':'https://science.nasa.gov/photojournal/the-wright-brothers/',
'R23':'https://www.nasa.gov/missions/apollo/apollo-11/apollo-11-mission-overview/',
'R24':'https://airandspace.si.edu/collection-objects/wood-and-fabric-1903-wright-flyer-apollo11/nasm_A19721288000',
'R25':'https://www.jpl.nasa.gov/images/pia24438-pride-of-the-west-mdash-and-mars/',
'R26':'https://www.jpl.nasa.gov/images/pia24521-perseverances-mastcam-z-video-of-ingenuitys-first-full-flight/',
'R27':'https://www.charliechaplin.com/en/articles/21-Overview-of-His-Life',
'R28':'https://www.charliechaplin.com/en/articles/21-Overview-of-His-Life',
'R29':'https://www.charliechaplin.com/en/films/5-The-Great-Dictator',
'R30':'https://computerhistory.org/apple-timeline/',
'R31':'https://baotanglichsu.vn/VI/Articles/3098/19511/bao-djai-vi-hoang-dje-cuoi-cung-trong-lich-su-phong-kien-viet-nam.html',
'R32':'https://blogs.windows.com/windows-insider/2020/08/24/looking-back-the-25th-anniversary-of-windows-95/',
'R33':'https://computerhistory.org/',
'R34':'https://baotanglichsu.vn/VI/Articles/3098/19511/bao-djai-vi-hoang-dje-cuoi-cung-trong-lich-su-phong-kien-viet-nam.html',
'R35':'https://www.loc.gov/exhibits/lincoln/candidate-lincoln.html',
'R36':'https://www.mountvernon.org/george-washington/the-first-president/inauguration/timeline',
'R37':'',
}

def paras_text(p):
    return ', '.join(f'{x:02d}' for x in p) if isinstance(p, list) else str(p)

def md_escape(s):
    return str(s).replace('|','\\|')

def emit_item(item, cat=False):
    lines=[f"### {item['id']} · {item['name']}", '',
           f"**Ưu tiên:** {item['priority']} · **Đoạn lời:** {paras_text(item['paragraphs'])}", '',
           f"**Mục đích hình:** {item['purpose']}", '',
           f"**Kho hiện có:** {item['existing']}", '',
           f"**File cần giao:** {', '.join(item['outputs'])}", '',
           '**PROMPT — sao chép nguyên khối:**', '', '```text',
           'Tạo đúng các file riêng được liệt kê, không ghép nhiều asset thành contact sheet/collage. Tham chiếu phong cách là 3 ảnh explainer_reference_v1 trong thư mục dự án: nền trắng/ngà, nét mực tối hơi hữu cơ, khối màu phẳng ấm, chi tiết gọn, hình đọc rõ ở khung 1920×1080. Các ảnh đó chỉ tham chiếu ngôn ngữ minh họa; không sao chép nhân vật người trong ảnh. Với Mỏ Đen, bắt buộc dùng ảnh reference và manifest riêng của nhân vật.',
           item['spec'],
           'Bố cục và góc máy phải theo đúng chỉ dẫn vừa nêu. Xuất asset PNG RGBA nền trong suốt thật, không vẽ ô caro; giữ khoảng an toàn quanh silhouette; không chữ, số, logo, watermark, viền giao diện hay chú thích. Mỗi lớp phải khớp canvas/kích thước/tọa độ của lớp liên quan đã khóa. Nếu không thể xác minh một chi tiết lịch sử từ reference được cung cấp, để trống hoặc báo thiếu reference; không tự bổ sung.',
           'CẤM: tự sáng tác chủ thể/sự kiện/hiện vật/chi tiết kiến trúc ngoài mô tả; thêm người lịch sử, đạo cụ hoặc biểu tượng không được yêu cầu; đổi góc, màu, niên đại; ghép chữ giả; thay đổi thiết kế Mỏ Đen. Không diễn giải prompt theo hướng “sáng tạo tự do”.',
           'Lớp chuyển động cần phục vụ hành động sau: '+item['motion'],
           'Chi tiết không được xuất hiện: '+item['forbid'],
           'Trước khi giao, kèm file gốc, kích thước, alpha, mã kiểm tra SHA-256 và tên reference đã dùng. Không báo “đúng lịch sử” nếu chỉ tạo theo mô tả mà chưa có nguồn đối chiếu.',
           '```','',f"**Thiết kế chuyển động/diễn tiến:** {item['motion']}",'',
           f"**Ranh giới nội dung:** {item['forbid']}",'']
    if item.get('refs'):
        lines += [f"**Tham chiếu cần mở trước:** {item['refs']}",'']
    return '\n'.join(lines)

def create():
    (HERE/'asset_requests.json').write_text(json.dumps({'project':'Mỏ Đen tập 2','artwork_prompts':ART+[dict(id=i,name=n,paragraphs=p,family='MO_DEN',purpose='Pose tĩnh để đặt Mỏ Đen vào không gian kể chuyện, giữ nhận diện đã có.',spec=s,motion=m,forbid='Không đổi model/nhận diện; không thêm ngón tay người/áo quần; không giả lip-sync hoặc rig; giữ RGBA nền trong.',refs='assets/characters/mo_den/manifest.json và các file PNG được dẫn trong brief.',priority='P1' if i in ['C01','C02','C03','C04','C05','C07','C08'] else 'P2',outputs=[i.lower()+'_pose.png'],existing='Bộ 24 pose hiện có là ảnh mèo tĩnh, chủ yếu ngồi; chưa có góc xoay và tương tác đạo cụ này.') for i,n,p,s,m in CAT]},ensure_ascii=False,indent=2),encoding='utf-8')
    out=[]
    out += ['# Mỏ Đen — Tập 2: kiểm kê hình ảnh, yêu cầu tư liệu và prompt tạo asset','',
    '**Bản đạo diễn hình ảnh · 21/10/2026 · trạng thái: danh sách yêu cầu, chưa có asset mới được tạo hoặc phê duyệt.**','',
    '## Kết luận nhanh','',
    'Kịch bản có 73 đoạn lời, 460 cue SRT nháp và thời lượng dự kiến 18:22.875; chưa có bản thu âm tập 2 trong gói ZIP. Các mốc thời gian bên dưới chỉ để tìm đúng đoạn, phải căn lại sau khi có voice thật. Tôi đã kiểm tra danh mục và xem contact sheet của toàn bộ 198 PNG: hash đều khớp catalog. Kho có 24 pose Mỏ Đen, 150 đạo cụ/minh họa generic và 48 ảnh nền/vật thể Maya. Không tìm thấy chân dung/tư liệu lịch sử của các nhân vật tập 2 hay ảnh địa danh tập 2 trong các PNG đó.','',
    'Danh sách tách ba loại việc: 62 yêu cầu minh họa/pose có prompt tạo cụ thể; 37 yêu cầu tìm/tải tư liệu thật có nguồn (không được thay bằng ảnh AI); 25 đồ họa thời gian/số liệu phải dựng bằng SVG/compositor để giữ số chính xác. Tổng cộng 124 đầu việc hình ảnh, trong đó asset cùng họ được ghép lớp và tái sử dụng có kiểm soát; con số không phải 124 cảnh.','',
    '**Ưu tiên:** P1 = cần trước khi dựng rough cut có thể xem; P2 = cần khi tương ứng xuất hiện hoặc có thể giải quyết bằng tư liệu nguồn/đồ họa đã liệt kê. Ảnh tạo mới không bao gồm nhân vật lịch sử giả photorealistic. Nguồn thật phải được tìm từ kho có quyền, ghi registry và credit.','',
    '## Chuẩn đạo diễn áp dụng','',
    'Đọc [quy định đạo diễn hình ảnh](../../../QUY_DINH_DAO_DIEN_HINH_ANH.md) và [chuẩn nhân vật](../../../AGENTS.md) trước sản xuất. Maya V2 trước đó đã bị người dùng chê lặp nhiều đại cảnh trống; không dùng V2 làm mẫu. Đếm cùng họ bối cảnh, đổi crop hoặc zoom không xóa lượt lặp. Đại cảnh trống chỉ dùng ngắn để định vị; mỗi lần trở lại phải có thông tin hoặc hành động mới.','',
    '- Khung hình 16:9, 1920×1080 khi ghép; vật thể PNG tách nền thật và thường dựng ở canvas vuông/khung theo brief. Mỗi layer có tên và tọa độ ổn định.','- Hình minh họa mới theo phong cách ba ảnh `assets/styles/explainer_reference_v1/`; các ảnh này chỉ là tham chiếu nét/màu/bố cục, không dùng nhân vật người bị loại.','- Mỏ Đen phải theo đúng `assets/characters/mo_den/manifest.json`. 24 ảnh hiện có là tĩnh; không nói ảnh tĩnh có body animation hoặc lip-sync. Pose bổ sung phải giữ nguyên model đã duyệt, tạo file riêng và kiểm tra nhận diện.','- Không tạo chữ/số/bản đồ bằng model ảnh. Text, nhãn, ngày, mũi tên, đường thời gian và số liệu dựng bằng SVG/compositor từ thông số trong brief.','- Tư liệu lịch sử không được tạo sinh. Nếu chưa tìm được ảnh dùng hợp pháp, để mục ở trạng thái HOLD; dùng minh họa có nhãn hoặc đồ họa trừu tượng thay vì giả ảnh thật.','- Tránh người lịch sử được tạo thành ảnh chụp giả. Với cảnh người thật, dùng ảnh/tranh/hiện vật có nguồn hoặc không cho thấy mặt người.','',
    '## Những gì kho hiện tại đã đáp ứng','',
    '| Kho | Nội dung có thể dùng | Giới hạn khi làm tập 2 |','|---|---|---|',
    '| Mỏ Đen · 24 PNG | 24 biểu cảm tĩnh; có tò mò, suy nghĩ, ngạc nhiên, lo lắng, giải thích. | Thiếu góc 3/4 trái/phải, chỉ đúng hướng, giữ thước/thẻ, tương tác tủ, nhìn qua vai/xuống bàn. Dùng pose hiện tại nếu khung không đòi cử chỉ cụ thể. |',
    '| Generic · 001–150 | Đồ đời sống, dụng cụ nghiên cứu, kiến trúc/đá, tiền/vật liệu, địa hình/sinh vật, thời tiết, biểu tượng và một số nền. | Có thể tái dùng thước, lịch, thẻ, bàn, kính, sách dạng biểu tượng; không thay được ảnh/hiện vật lịch sử có catalog. |',
    '| Maya · 151–198 | Bối cảnh/đạo cụ Maya về hồ nước, ruộng, kho, nhà, cung điện, khu cháy, thạch cao/zeolit, ngô và nước. | Không dùng nền đô thị Maya làm Giza, Tenochtitlan, London, Nhật, Oxford hay Mars. 48 ảnh này không phải bộ ảnh lịch sử chung. |',
    '| Tư liệu lịch sử tập 2 | Chưa thấy ảnh chân dung, địa danh hoặc vật chứng gốc tập 2 trong PNG 198 bộ. | Phải tìm nguồn theo 37 mục R01–R37 bên dưới; một số cần quyền/credit trước khi xuất. |','',
    'Các contact sheet và danh mục có trong thư mục này. Danh mục kiểm tra theo từng file: [inventory_verified.json](inventory_verified.json).','',
    '## Coverage theo kịch bản','',
    '| Đoạn | Thời gian SRT nháp | Nội dung cần kể bằng hình | Bộ asset chính |','|---|---:|---|---|',
    '| 01–08 | 00:00–01:57.938 | Mở đầu đồng thời; Quang Trung/Washington; cùng năm 1789; không suy ra từng gặp nhau; “tủ ký ức”. | A01–A09, R01–R03, R36, V01–V03, C01–C04 |',
    '| 09–16 | 01:57.938–04:03.938 | Khufu; khoảng cách 2550 TCN–đầu Công nguyên–2026; không có năm 0; đảo điểm nhìn. | A10–A12, R04–R05, V04–V06, C05–C09 |',
    '| 17–28 | 04:03.938–07:06.938 | Cleopatra/Apollo; phông nền đánh lừa; ma mút còn ở Wrangel; quần thể cuối. | A13–A17, R06–R09, V07–V10, C08–C10 |',
    '| 29–34 | 07:06.938–08:43.688 | Oxford từ năm 1096 và Tenochtitlan từ năm 1325; Aztec từ năm 1428; phân biệt thành phố/đế chế. | A18–A23, R10–R14, V11–V13, C03/C04 |',
    '| 35–40 | 08:43.688–10:14.812 | London Underground năm 1863, tàu hơi nước; samurai, cải cách 1868/1876 và đời sống tiếp tục. | A24–A30, R15–R19, V14, C01–C04 |',
    '| 41–46 | 10:14.812–11:48.750 | Darwin/Lincoln cùng ngày sinh; mốc 1859/1860; tuổi 50/51; thành tựu không xuất hiện sẵn. | A05–A07, A31–A33, R20–R21/R35, V15–V16, C02/C09 |',
    '| 47–57 | 11:48.750–14:36.938 | Wright: 12 giây/37 m; Apollo; đời người giả định; vải/gỗ và nhánh vật liệu khác sang Ingenuity; đổi tốc độ. | A34–A45, R22–R26, V17–V21, C03/C05/C06/C08 |',
    '| 58–64 | 14:36.938–16:15.750 | Chaplin vượt hình tượng phim câm; sống tới thời Apple; phim năm 1940 có thoại; ảnh lớp 1 ví von. | A04/A07/A46–A50, R27–R30, V22–V23, C06/C09 |',
    '| 65–70 | 16:15.750–17:44.062 | Bảo Đại: vai trò vua và đời người khác nhau; Windows 95; không bịa việc sử dụng PC. | A04/A07/A51–A52, R31–R34/R32, V24, C01/C02/C07/C10 |',
    '| 71–73 | 17:44.062–18:22.875 | Hồi nhắc các cặp; câu hỏi về người thật và bức tranh; khép tủ, CTA. | A01/A02/A04/A09, V01/V07/V14/V22/V24/V25, C10 |','',
    'Cue và mốc trong `PHU_DE_DU_KIEN.srt`/`DIEN_GIONG_DAY_DU.txt` chưa đồng bộ với voice thật. Không xuất subtitle chính thức từ mốc nháp.','',
    '## Prompt khóa chung','',
    'Dán phần này trước prompt từng asset nếu công cụ tạo ảnh không giữ được yêu cầu trong brief:','',
    '```text','Tuân thủ prompt theo nghĩa đen. Tạo đúng một asset được chỉ định, trên một canvas riêng; không thêm đạo cụ, nhân vật, chữ, sự kiện hoặc phong cảnh không được yêu cầu. Không tự sáng tác dữ kiện lịch sử. Ba ảnh tham chiếu phong cách chỉ định hình nền, nét mực, độ phẳng màu và độ hoàn thiện; không được sao chép người trong ảnh tham chiếu. Dùng nền trắng/ngà, viền mực tối đồng đều hơi hữu cơ, mảng màu phẳng ấm, silhouette rõ và ít texture. PNG phải có alpha thật khi brief yêu cầu, không giả alpha bằng caro. Không sinh văn bản/số/logo/bản đồ. Giữ canvas, trục, góc nhìn, hướng sáng và điểm tiếp xúc đồng nhất giữa các lớp. Nếu không thấy hoặc không có ảnh reference được gọi tên, dừng và hỏi xin reference thay vì đoán.','```','',
    '### Khóa riêng cho Mỏ Đen','',
    '```text','Dùng chính các file master trong assets/characters/mo_den/library/named_24_v01 và mở manifest.json. Giữ nguyên mèo nhỏ thân tròn kem/nâu nhạt; mặt nạ, tai, bàn chân, đuôi nâu đậm; mắt xanh xám; nét viền đơn giản. Không đổi giống, tỉ lệ đầu/thân, mảng màu hoặc tuổi. Pose là ảnh tĩnh một trạng thái. Không tạo lip-sync, không rig giả. Chân trước vẫn là chân mèo, không có bàn tay/ngón người. Giữ chân/đuôi/toàn silhouette trong canvas. Mọi pose mới là bản nháp cần so cạnh master trước khi dùng.','```','']
    out += ['## I. Minh họa và pose Mỏ Đen cần tạo','',
    'Mỗi mục dưới đây là một prompt độc lập. Các lượt dùng cùng một họ bối cảnh phải tuân giới hạn lặp; ưu tiên cận hành động, bằng chứng, vật thể có điểm đến và phản ứng của Mỏ Đen, không dựng thêm hàng loạt nền rộng.','']
    out += [emit_item(i) for i in ART]
    cat_items=[]
    for id,name,ps,s,m in CAT:
        cat_items.append(dict(id=id,name='Mỏ Đen — '+name,paragraphs=ps,family='MO_DEN',purpose='Tạo pose tĩnh để Mỏ Đen tham gia cảnh khi góc nhìn/cử chỉ đang thiếu.',spec=s,motion=m,forbid='Không thiết kế mèo mới; không đổi model, mặt nạ, màu, tuổi, tỉ lệ; không có ngón tay người; không gắn sẵn đạo cụ/nền; không giả lip-sync/rig.',refs='assets/characters/mo_den/manifest.json; mở PNG master được nêu trong brief trước khi vẽ.',priority='P1' if id in ['C01','C02','C03','C04','C05','C07','C08'] else 'P2',outputs=[id.lower()+'_pose.png'],existing='24 pose hiện tại đều là PNG tĩnh, phần lớn ngồi và thiếu hướng/cử chỉ này.'))
    out += [emit_item(i,True) for i in cat_items]
    out += ['## II. Tư liệu thật cần tìm/tải, không dùng ảnh tạo sinh','',
    'Các mục R là công việc nghiên cứu, xin quyền/tải và ghi credit. “Chưa có trong kho” không đồng nghĩa “chưa tồn tại trên Internet”. Mở nguồn gốc, kiểm tra quyền của chính file được chọn và ghi vào registry; link cơ quan bên dưới là đầu mối, không phải phê duyệt sử dụng.','',
    '| ID | Đoạn lời | Tư liệu cần lấy và điều kiện | Không chấp nhận |','|---|---|---|---|']
    for id,name,ps,specification,ban in SOURCES:
        link=SOURCE_LINKS.get(id,'')
        title=f'[{name}]({link})' if link else name
        out += [f'| **{id} · {md_escape(title)}** | {ps} | {md_escape(specification)} | {md_escape(ban)} |']
    out += ['', '### Điều kiện duyệt tư liệu thật','',
    '- Lưu file gốc, URL cụ thể, tên tác giả/cơ quan, caption, số hiện vật/frame, ngày truy cập, quyền/giấy phép và credit cần hiện. Tư liệu web có thể thay đổi hoặc chặn; kiểm tra file thật trước khi dựng.','- Ghi nhãn ảnh hiện nay, tranh hồi cố, mô hình phục dựng, screenshot giao diện và ảnh hiện vật đúng loại của nó. Không gọi tất cả là ảnh lịch sử đương thời.','- Nếu một link là trang tổng quan, tìm tới đúng record ảnh/object; không crop ảnh từ trang tìm kiếm hoặc từ video không rõ nguồn.','- Yêu cầu trích đoạn nhỏ cần thiết trong phim, không sao chép toàn trang/bài nghiên cứu vào video.','- R05: tên catalog trong hồ sơ đầu vào cần đính chính. The Met ghi đây là mẫu vữa từ Đại kim tự tháp, ca.2550 BCE, không phải “phù điêu trận chiến”.','- R24/R25: phân biệt vật liệu Flyer mang trên Apollo với mảnh muslin khác trên Ingenuity. Mọi đồ họa tuyến hành trình phải là hai nhánh riêng.','',
    '## III. Đồ họa chính xác phải dựng bằng SVG/compositor','',
    'Đây là bản vẽ vector/đồ họa, không nên prompt model ảnh sinh số liệu. Mỗi mục phải lấy số từ kịch bản/hồ sơ nguồn và có thể soát lại độc lập.','',
    '| ID | Đoạn | Bố cục và dữ kiện khóa |','|---|---|---|']
    for id,name,ps,specification in GRAPHICS:
        out += [f'| **{id} · {name}** | {ps} | {md_escape(specification)} |']
    out += ['', '## Quy tắc không lặp hình và không tạo cảnh sai','',
    '- Không đặt ma mút ở Giza. Chỉ đặt phép so thời gian hoặc hai hình riêng có nhãn; Wrangel là địa điểm của quần thể cuối.','- Không dùng nền Maya 151–180 làm Aztec/Tenochtitlan hoặc Ai Cập. Cần R12/R13 và đồ họa bản đồ riêng.','- Không dùng tàu điện Tube hiện đại cho năm 1863. Dùng đầu máy hơi nước thời kỳ mở tuyến, khóa theo catalog; nếu không tìm được máy khai trương cụ thể, ghi là minh họa thời kỳ đầu.','- Không vẽ samurai biến mất năm 1876; vẽ mốc thay đổi địa vị/đặc quyền và để đường đời người tiếp tục.','- Không khẳng định người cùng thời từng gặp, trao thư hoặc biết công việc nhau nếu kịch bản không có bằng chứng. Không thêm thư giữa Quang Trung và Washington.','- Không cho Chaplin dùng Apple, không đặt iPhone vào năm 1976, không cho Bảo Đại sử dụng Windows 95. Các mốc đồng thời là phép so trên trục, không phải tương tác.','- Không ghép hai mảnh vật liệu Flyer thành một vật di chuyển từ Mặt Trăng tới Sao Hỏa.','- Họ nền rộng/trung bình dùng tối đa 3 lượt trong phim; cùng bố cục rộng trống tối đa 1 lần. Mỗi lần trở lại phải có thông tin mới. Đổi crop, tiêu đề hoặc zoom không tính là hình mới.','- Ảnh tư liệu thật mặc định tối đa 2 lần; khi quay lại phải cho xem chi tiết khác có ích và giữ nguồn.','- Mỗi cảnh cần thời điểm theo voice thật, chủ thể, hành động, thông tin mới và lý do cắt. Chuyển động cần điểm đến hoặc hệ quả; pan/zoom tự nó không tạo nội dung.','- Kiểm tra từng đoạn 60–90 giây với voice sau khi dựng. Contact sheet và số shot không thay việc kiểm tra xem hình có kể đúng không.','',
    '## Checklist nhận asset','',
    '- Tên file đúng ID, một asset/file, canvas đúng, alpha thật với asset cần tách nền.','- So sánh với ảnh reference đã ghi, đọc hình ở cỡ thực sẽ xuất lên 1080p và crop cận; kiểm tra mép, tỷ lệ, hướng sáng, điểm chạm và lớp che.','- Đối với Mỏ Đen: so nhận diện cạnh master; pose mới không được tự động coi là đã duyệt.','- Với số liệu/bản đồ: so từng nhãn, dấu âm/dương, đơn vị, tỷ lệ, địa điểm và ngày với nguồn; chữ do compositor vẽ.','- Với ảnh thật: xác nhận nguồn, đúng vật/nhân vật, quyền và credit. Nếu chưa chắc, không đưa vào timeline.','- Dùng xong hãy ghi asset ID và shot ID vào registry. Không phát lại cùng nền để lấp voice dài.','',
    '## Tình trạng thời lượng','',
    'Gói hiện có `LOI_DOC.txt`, `DIEN_GIONG_DAY_DU.txt`, `PHU_DE_DU_KIEN.srt` và `NGUON_VA_KIEM_CHUNG.md`; chưa có WAV voice cuối tập 2. Mốc 18:22.875 là cuối SRT dự kiến, cue chia theo tốc độ giả định chứ chưa căn âm. Tài liệu nối theo đoạn kịch bản, không giả vờ có timecode hình chính xác đến frame. Khi voice được duyệt, thay cột đoạn bằng timecode đọc thật.','',
    '## Nguồn và file trong dự án','',
    '- Kịch bản đầu vào đã lưu tại `projects/mo_den_tap_02/source_materials/`.','- Catalog 150 ảnh: `projects/mo_den_maya/preflight/generic_150_catalog.json`; PNG nằm tại `assets/reusable/mo_den/generic_150/`.','- Catalog 48 ảnh Maya: `projects/mo_den_maya/preflight/maya_48_catalog.json`; PNG nằm tại `assets/reusable/mo_den/maya_48/`.','- Catalog mèo: `assets/characters/mo_den/manifest.json`; ảnh gốc trong `assets/characters/mo_den/library/named_24_v01/`.','- Phong cách minh họa: `assets/styles/explainer_reference_v1/manifest.json` và ba PNG cùng thư mục.','- Quy tắc không lặp: `QUY_DINH_DAO_DIEN_HINH_ANH.md`.','- Sơ đồ kiểm kê toàn bộ ảnh 198 mục: `inventory_verified.json`, `inventory_001_030.jpg` đến `inventory_181_198.jpg`.','- Cơ quan nguồn gốc đầu mối: '+', '.join(f'[{k}]({v})' for k,v in list(SOURCE_LINKS.items())[:15] if v)+'.','']
    md=HERE/'DANH_SACH_ANH_VA_PROMPT_MO_DEN_TAP_02.md'
    md.write_text('\n'.join(out),encoding='utf-8')
    index={'project':'Mỏ Đen — tập 2','created':'2026-10-21','status':'brief only; no assets generated/approved',
           'artwork_prompts':ART+[dict(id=i,name='Mỏ Đen — '+n,paragraphs=p,purpose='Pose tĩnh đặt nhân vật đúng góc/cử chỉ cần thiết.',spec=s,motion=m,forbid='Không đổi nhận diện; ảnh tĩnh; không tay người/lip-sync.',refs='assets/characters/mo_den/manifest.json',priority='P1',outputs=[i.lower()+'_pose.png']) for i,n,p,s,m in CAT],
           'real_asset_requests':[{'id':i,'name':n,'paragraphs':p,'requirements':s,'reject':b,'source_url':SOURCE_LINKS.get(i,'')} for i,n,p,s,b in SOURCES],
           'vector_graphics':[{'id':i,'name':n,'paragraphs':p,'spec':s} for i,n,p,s in GRAPHICS]}
    (HERE/'asset_requests.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
    print(md)
    print('art prompts',len(ART)+len(CAT),'real-image acquisition requests',len(SOURCES),'vector specs',len(GRAPHICS),'total',len(ART)+len(CAT)+len(SOURCES)+len(GRAPHICS))

if __name__=='__main__': create()
