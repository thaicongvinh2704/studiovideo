"""Authored visual beats V3: Director-grade cinematic plan strictly respecting repetition limits.

Every background family is capped at <= 3 appearances with >= 60s gaps.
Replaced repetitive empty wide shots with:
- Dedicated host reactions / questions (Mỏ Đen inside scene / close-up)
- Meaningful close-up props and evidence
- New high-impact diagrams (G09 Spanish conquest, G10 Astronomy, G11 Calendar, G12 Pollution)
- Clear cause-and-effect animated mechanisms
"""

PLAN_V3 = r'''
1|photo|R01||0|Giữa rừng nhiệt đới
1|world|151|181,195|0|Biết trữ nước. Biết lọc nước.
2|question||195|13|Vì sao phải rời đi?
3|photo|R06||0|Người Maya vẫn sống đến hôm nay
4|host||187,195,053|14|Thành phố đổi khác
4|host||187,195,053|2|Mở lại hồ sơ Maya
5|world|176||6|Một thành phố từng cháy
5|objects||193,195,125|14|Những dấu vết chưa khớp
6|world|172|001|13|Nếu đó là khu bạn sống?
6|objects||001,195|7|Nước bắt đầu thiếu
6|objects||072,103|15|Thực phẩm khó kiếm hơn
7|choice||004,001|15|Khi nào bạn sẽ dọn đi?
8|objects||004,128|14|Nhìn từ phía người phải sống ở đó
8|host||126|8|Không có ngày «chính thức thành di tích»
9|choice||004,001|15|Mỗi gia đình, một lựa chọn
10|world|153||15|Thành phố vắng dần
11|photo|R02||0|Đền đài ở lại rất lâu
12-13|map|G01||0|Nhiều trung tâm, không một thủ đô
14|network||151,178,172|24|Nhiều thành bang cùng tồn tại
14|network||151,178,172|24|Không cùng sụp đổ trong một ngày
15|timeline|classic||0|Khoảng 250–900 sau Công nguyên
15|timeline|classic||0|Những nhịp suy giảm khác nhau
16|objects||151,152,153|14|Mỗi nơi một diễn biến
17|graphics|G10||24|Chữ viết, toán học và thiên văn Maya
17|objects||126,198,053|24|Thành tựu không xóa mọi giới hạn
18|question|||14|Ta có kỳ vọng quá nhiều?
19|compare||121,197|0|Biết mùa mưa ≠ luôn đủ nước
20|objects||183,195|24|Ứng phó cũng có giới hạn
21|network||178,075,127|0|Liên minh · cạnh tranh · giao chiến
21|world|178||24|Kỹ thuật và quyền lực
22|photo|R02||0|Rời những đỉnh đền…
22|world|157|001|13|…xuống nơi lấy nước
23|objects||001,195|0|Nước uống không thể chờ
24|map|G01||0|Tikal · Guatemala
25|world|158|001|15|Giữ nước qua mùa khô
26|photo|R01||0|Rừng vẫn xanh
27|question||094,195|13|Nhiều cây, sao vẫn thiếu nước?
28|compare||094,001|24|Rừng xanh và nước uống
29|water|limestone||0|Nước thấm qua nền đá vôi
30|water|collection||0|Thu nước khi mưa đến
30|water|collection||0|Thu · giữ · điều tiết
30|objects||181,182,183|24|Kênh · hồ · đập
31|host||053|24|Tính toán và tổ chức
32|proof|E03_zeolite_fig3||0|Bằng chứng vật liệu ở Corriental
32|objects||184,185|16|Thạch anh và zeolit
33-35|distance||184,185|15|Gần 30 km
36|proof|E03_zeolite_fig4||0|Một cấu tạo được đề xuất
37|objects||184,185,182|24|Kiến thức và công sức
38|tank||197|0|Ví dụ hiện đại: bồn nước
38|tank||197|0|Năm sau vẫn thiếu mưa
39|tank||197|0|Bồn tốt cũng không tự đầy
40|objects||181,183|14|Hồ vẫn còn đó
40|objects||181,183|0|Kênh có thể vẫn làm việc
41|world|159|001|7|Nhưng nước không còn đủ
42|objects||195,193|14|Còn một câu hỏi khác
43|question||195|13|Nước ấy có uống được không?
44|objects||195,193|7|Hồ chưa cạn, chưa chắc đã yên tâm
45|objects||193,195|7|Có nước ≠ nước an toàn
46|world|161|187|0|Dấu vết dưới đáy hồ
47|proof|E06_pollution_fig4||0|Phân tích trầm tích · 2020
48|proof|E06_pollution_fig4||0|Temple và Palace
49|objects||186|0|Chu sa · sắc tố màu đỏ
50|graphics|G12||0|Sơ đồ cắt lớp ô nhiễm hồ Tikal
51|pollution||186,194,195|14|Từ công trình xuống nguồn nước
52-53|host||195,193|14|Không suy rộng cho mọi hồ
54|question|||7|Chưa thể kết luận nguyên nhân tử vong
55|host||193,195|7|Một số nguồn nước bị đe dọa
56|host||001,195|7|Nước ít hơn, xoay xở khó hơn
57|compare||195,193|0|Lượng nước và chất lượng nước
58|route||001,128|0|Chỗ gần không ổn. Chỗ khác lại xa.
58|objects||001,138|14|Cùng chờ một nguồn nước
59|question||001|13|Ai lấy trước? Ai phải đi xa?
60|network||001,172,172|24|Khi đủ dùng
61|objects||001,195|7|Khi nguồn nước ít lại
62|network||001,172,172|24|Nước và quan hệ cộng đồng
63|question||121,114|13|Hạn hán nghiêm trọng đến đâu?
64|world|162||0|Đọc dấu vết trong trầm tích
64|objects||187,188,189|24|Bùn hồ · măng đá · khoáng vật
65|objects||189,188,031|0|Dấu vết điều kiện nước
66|proof|E07_drought2025_fig2||0|Từ mẫu tới ước tính khí hậu
67|objects||189,195|24|Chichancanab · nghiên cứu 2018
68|rainchart|||0|Lượng mưa giảm khoảng 41–54%
69|host||023|14|Trong khu vực được nghiên cứu
70|world|163|190|0|Ruộng ngô thời tiết thuận lợi
71|proof|E07_drought2025_fig2||0|Tây bắc Yucatán · nghiên cứu 2025
72-73|years|||0|13 năm
74|host||121|14|Không có nghĩa là không mưa giọt nào
75|world|164|191|7|Qua hết mùa vụ này…
75|world|165|191|21|…đến mùa vụ khác
76|years|||0|Một phần tuổi thơ trôi qua
77|objects||190,192|15|Mỗi năm phải tính lại
78|world|166|192|0|Kho lương đầy dự trữ
79|objects||191,195|7|Chu kỳ quen thuộc, thời tiết đổi khác
79|objects||192,195|0|Đợi đất đủ nước
80|host|||7|Chờ đợi cũng có cái giá
81|world|167||7|Sức ép lên từng gia đình
82|map|G01||0|Đi tìm một trường hợp khác
82|world|160||0|Itzan · một câu hỏi chưa khớp
82|compare||195,174|13|Dân số giảm. Hạn tại chỗ?
83|proof|E08_Itzan_fig3||0|Hồ sơ Itzan · Guatemala
84|question||195,125|13|Nếu chỉ nhìn lượng mưa?
85|proof|E08_Itzan_fig3||0|Nghiên cứu Itzan · 2025
85|objects||187,100,031|24|Dấu vết hóa học trong trầm tích
86|host||023|14|Hồ sơ ấy cũng có giới hạn
87|compare||195,174|0|Chưa giải thích tốt bằng hạn tại chỗ
88|network||172,075,178|24|Nhìn thêm quan hệ giữa các vùng
89|world|169||0|Nhìn ra ngoài thành phố
90|trade||172,075,172|0|Hai nơi thường trao đổi hàng hóa
91|world|170|075|0|Đường bất ổn, hàng đến ít dần
92|trade||157,075,171|0|Có nước vẫn cần nơi khác
93|world|155||7|Nước còn, cuộc sống khó hơn
94|choice||004,173|15|Rời đi trước khi hồ cuối cùng cạn
94|host||125|15|Ở đâu? Lúc nào? Phụ thuộc vào đâu?
95|proof|E02_Witzna_cores||0|Một dấu vết rất khác
96|proof|E02_Witzna_cores||0|Witzna · nghiên cứu 2019
96|proof|E01_Witzna_charcoal||0|Dấu vết dưới đất gặp chữ khắc
97|objects||060,187|0|Dấu cháy cuối thế kỷ VII
98|timeline|war||0|697 sau Công nguyên
99|world|176||6|Naranjo · Witzna
99|world|177||7|Đời sống thay đổi sau sự kiện
99|proof|E01_Witzna_charcoal||0|Dấu cháy là một phần bằng chứng
100-101|timeline|war||0|Hãy chú ý đến thời điểm
102|compare||060,114|14|Không gộp mọi chiến tranh vào sau đại hạn
103|host||023|14|Witzna là một trường hợp
104|objects||036,130|0|Công trình còn dùng tốt…
104|host||060|6|…vẫn có thể bị phá hủy
105|proof|E01_Witzna_charcoal||0|Tác động còn kéo dài
106|world|171||7|Đường đi nguy hiểm
106|trade||127,075,155|0|Những mối trao đổi bị gián đoạn
107|network||195,075,172|24|Các sức ép gặp nhau
107|world|154|182|24|Thành phố cần người duy trì
107|objects||154,103|24|Công việc cần sự phối hợp
108|objects||036,130|0|Công trình còn. Liên hệ đứt đoạn.
108|objects||053,130|15|Những thương lượng khó nhìn thấy
109|objects||053,130|15|Vật liệu còn, đồng thuận thì sao?
110|photo|R07||0|Bia Tikal · một loại dấu vết
111|world|179||14|Cung điện im tiếng…
112|compare||178,172|24|Quyền lực và đời sống đô thị
113|host|||14|Có thể không cùng một lúc
114|host||179|14|Trật tự cũ suy yếu
114|host||172|17|Cuộc sống có thể tiếp tục
115|photo|R07||0|Ai có nhiều cơ hội để lại tiếng nói?
116|objects||178,172|24|Từ phía cung điện…
116|objects||154,103|0|…đến người làm ruộng, đổi hàng
117|world|180||15|Im tiếng không có nghĩa mọi thứ ngừng lại
118|objects||172,001|14|Tìm dấu vết bên ngoài cung điện
119|world|173|004|15|Một gia đình rời đi
120|choice||004,172|15|Một cách bảo vệ người thân
121|world|174||20|Một cuộc ra đi, hai phía nhìn
121|route||004,128|0|Đi tiếp cũng có hiểm nguy
122|host||125|14|Chưa biết hết số phận của họ
123|map|G01||0|Nhìn sang những khu vực khác
124|timeline|continuity||0|Đời sống vẫn tiếp diễn
125|timeline|continuity||0|900 chưa phải dấu chấm hết
126|photo|R05||0|Chichén Itzá
126|timeline|continuity||0|Một phần lịch sử dài phía sau
127|photo|R04||0|Mayapán
127|photo|R04||0|Cộng đồng và những quan hệ mới
128|photo|R04||0|Mayapán · khoảng thế kỷ XIII–XV
129|timeline|mayapan||0|Nhiều thế kỷ sau
130|network||178,114,130|0|Sức ép môi trường
130|network||178,114,130|0|Và cách xã hội ứng phó
130|timeline|mayapan||0|Một bối cảnh khủng hoảng riêng
131|compare||R01,R04|14|Tikal và Mayapán: hai câu chuyện riêng
132|timeline|mayapan||0|Giữ rõ khoảng cách thời gian
133|graphics|G09||0|Một chương lịch sử khác: người Tây Ban Nha đến
133|objects||126,130|0|Chiến tranh · dịch bệnh · áp bức
134|timeline|colonial||0|Muộn hơn nhiều thế kỷ
135|timeline|colonial||0|1697
136|timeline|continuity||0|Không gom vào một lần sụp đổ
137-138|photo|R06||0|Những cộng đồng đang sống
139|photo|R03||0|Ngôn ngữ · văn hóa · cuộc sống
140|photo|R02||0|Ngôi đền chỉ kể một phần
141|photo|R02||0|Người đâu hết rồi?
141|question|||13|Thử đổi câu hỏi
142|route||004,128|0|Họ đã thay đổi cuộc sống thế nào?
143|route||004,128|0|Đi theo con người
144|host||125|15|Còn nhiều điều chưa biết
145|host||198|14|Lời đồn năm 2012
145|host||198|8|Kết thúc một chu kỳ lịch
146|graphics|G11||0|So sánh lịch bàn và chu kỳ lịch Maya
147|graphics|G11||8|Hết tháng 12, sang năm mới
148|objects||021|8|Không cần tháo hành tinh
149|question||125|14|Điều chưa hiểu và chuyện bí ẩn
150|summary||182,060,195|24|Tikal · Witzna · Itzan
150|network||195,103,075|0|Một lời giải khó chứa hết
151|objects||125,132|16|Mỗi nơi thêm một mảnh ghép
152|network||195,103,075,127,130|24|Nhiều thứ phải cùng hoạt động
152|world|156||15|Một thành phố tiếp tục sống
153|world|168||7|Nhiều thứ cùng suy yếu
154|host||198,192|15|Có nhận ra bước ngoặt?
154|objects||198,192|15|Hay chỉ thêm một mùa khó khăn?
155|world|153||14|Ta nhìn lại một quãng dài
156|host|||7|Họ phải giải quyết từng ngày
157|host|||15|Trở lại câu hỏi ban đầu
158|choice||172,004|13|Nếu là bạn, khi nào sẽ rời đi?
159|choice||172,004|15|Ở lại: những gì đã gây dựng
160|choice||004,172|15|Rời đi: hy vọng và đánh đổi
161|host||004|15|Lựa chọn ấy đáng được nhìn thấy
162|water|collection||0|Nước chỉ là một phần cuộc sống
163|network||103,075,127,130|0|An toàn · thức ăn · hợp tác
164|route||004,128|0|Lịch sử đi tiếp cùng con người
165|photo|R01||0|Đền đài ở lại giữa rừng
165|photo|R06||0|Con người vẫn sống tiếp
166|host|||17|Câu chuyện chưa kết thúc
167|summary||182,060,195|13|Điều gì khiến bạn nghĩ khác?
168|host||123|2|Kể cho Mỏ Đen nghe nhé
168|timeline|next||0|Tập tới: đặt họ cùng một trục thời gian
169|host||198|16|Hóa ra họ sống gần thời nhau
'''

def plan_rows_v3():
    rows = []
    for line in PLAN_V3.strip().splitlines():
        ids, layout, source, props, emotion, title = line.split('|')
        values = [int(x) for x in ids.split('-')]
        rows.append(dict(first=values[0], last=values[-1], layout=layout,
                         source=source, props=props.split(',') if props else [],
                         emotion=int(emotion), title=title))
    return rows
