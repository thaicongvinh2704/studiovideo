import re
from pathlib import Path

OUT_DIR = Path("projects/mo_den_phong_than/voice_direction")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Full raw user text
full_text = """# Vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?

Kịch bản lời kể cho Mỏ Đen — bản 1.0, ngày 23/10/2026.

Phạm vi: kể và phân tích thế giới của tiểu thuyết **Phong Thần Diễn Nghĩa**, theo bản 100 hồi công khai trên Wikisource. Các sự kiện dưới đây là tình tiết của tác phẩm; những nhận xét về ý nghĩa được diễn đạt như cách đọc của người dẫn.

Thời lượng thiết kế: khoảng 16–18 phút với nhịp kể 245–275 đơn vị cách trắng/phút. Đây là ước tính từ lượng lời, chưa đo bằng bản thu. Nguồn và ghi chú hình đặt sau lời kể, không đọc thành tiếng.

---

## LỜI KỂ HOÀN CHỈNH

### 1. Hai mệnh lệnh

Khương Tử Nha vừa ra lệnh xử chém hai người.

Tội của họ được kể rất rõ: làm loạn triều chính, mê hoặc nhà vua, khiến đất nước sụp đổ. Đến khi chủ cũ chết, họ lại đem của báu sang cầu được làm quan cho triều đại mới.

Khương Tử Nha ra án.

Hai người bị đưa ra ngoài. Đao phủ thi hành án. Quân lính trở vào báo việc đã xong.

Rồi Khương Tử Nha bước lên đàn, gọi hồn chính hai người ấy đến… để phong thần.

Khoan đã.

Lệnh giết còn chưa nguội, sao đã có lệnh bổ nhiệm?

Nếu bạn nghĩ Phong Thần Bảng là danh sách khen thưởng sau chiến thắng, cảnh này thật khó hiểu. Người vừa bị kết tội nay lại có thần vị. Kẻ từng giúp Trụ Vương cũng được giao việc trong trật tự mới.

Mà đây còn chưa phải trường hợp khiến Mỏ Đen chú ý nhất.

Có một người chống Khương Tử Nha đến chết. Khi hồn được gọi lên nhận chức, ông vẫn không chịu quỳ. Một người khác gần như đi khắp nơi tìm đối thủ về đánh Tử Nha, cuối cùng cũng có tên được phong.

Trong khi đó, chính người cầm bảng, đọc sắc phong cho người khác, lại đi đến một kết cục rất khác.

Muốn hiểu chuyện này, trước hết hãy nhìn vào thứ Khương Tử Nha cầm trên tay. Ông có quyền tuyên bố các chức vị. Nhưng quyền ấy bắt đầu từ một mệnh lệnh mà chính ông cũng phải tuân theo.

### 2. Người đọc danh sách

Lùi về lúc Khương Tử Nha còn ở núi Côn Lôn.

Ông lên núi năm ba mươi hai tuổi. Đến khi được thầy gọi đến, ông đã bảy mươi hai. Bốn mươi năm tu hành, đủ lâu để một người đi gần hết cuộc đời với cùng một mong muốn.

Rồi Nguyên Thủy Thiên Tôn báo rằng đường tiên của ông khó thành. Phần dành cho ông là phúc ở nhân gian: xuống núi, giúp nhà Chu, làm tướng làm quan và thay thầy thực hiện việc phong thần.

Khương Tử Nha nghe vậy thì xin được ở lại.

Ông đã thật lòng xuất gia. Tuổi cũng đã cao. Ông vẫn muốn tiếp tục chịu khổ trên núi để theo đuổi việc tu hành. Nhưng lời thỉnh cầu không thay đổi được quyết định. Tử Nha đành thu xếp hành lý, bái biệt thầy, xuống núi.

Chi tiết này rất dễ bị những trận đánh về sau che mất. Người đứng ra phong thần vốn đã không được chọn con đường mình mong muốn ngay từ đầu.

Cũng trong hồi này, truyện cho biết việc phong thần đã được bàn định ở cấp các bậc giáo chủ. Có ba trăm sáu mươi lăm vị chính thần, chia thành các bộ và chức trách. Bên dưới là cuộc thay ngôi giữa nhà Thương và nhà Chu; bên trên là kiếp nạn của những người tu hành và việc sắp đặt các thần vị.

Hai việc ấy cùng diễn ra trong một câu chuyện.

Cho nên, khi một người chết trên chiến trường, câu hỏi không dừng ở chỗ họ đứng về bên nào. Còn phải xem họ có phần trong việc phong thần hay không, được giao chức gì và sắc phong nói thế nào về cuộc đời họ.

Đến lễ phong thần, Khương Tử Nha nhận phù sắc của Nguyên Thủy Thiên Tôn. Ông làm lễ, công bố chiếu lệnh rồi mới gọi từng người.

Hãy hình dung trên bàn Mỏ Đen có hai tờ giấy. Một tờ ghi ai thắng trận. Tờ kia ghi ai đảm nhiệm chức vụ sau khi chết. Có người xuất hiện trên cả hai. Có người chỉ xuất hiện ở một tờ.

Nhầm hai tờ thành một, chúng ta sẽ thấy hàng loạt chuyện vô lý.

Và người đầu tiên giúp tách chúng ra là một vị tướng thất bại, nhưng lòng trung thành vẫn còn nguyên cả sau khi chết.

### 3. Văn Trọng đã chết, nhưng chưa chịu cúi đầu

Văn Trọng là trụ cột của nhà Thương. Với quân Tây Kỳ, ông là một đối thủ phải đánh bại. Với chính mình, ông là bề tôi đang gắng giữ lấy cơ nghiệp của chủ.

Hồi năm mươi hai đưa ông vào những ngày cuối cùng của cuộc gắng sức ấy.

Đường rút liên tiếp bị chặn. Tướng dưới quyền lần lượt chết. Quân lính hao hụt, mỏi mệt và đói. Đến con mặc kỳ lân theo ông ra trận cũng bị đánh chết.

Có lúc Văn Trọng nghĩ mình vẫn có thể dùng phép thoát về Triều Ca, rồi chỉnh đốn binh mã đánh lại. Nhưng còn đoàn quân đang theo ông. Bỏ họ để một mình thoát thân là điều ông không đành.

Thế là cuộc rút lui tiếp tục.

Đến Tuyệt Long Lĩnh, Vân Trung Tử đã chờ sẵn. Những cột thần hỏa dựng lên, vây Văn Trọng vào giữa. Ông dùng phép tránh lửa, rồi tìm cách thoát lên phía trên. Nhưng lối ấy cũng đã bị chặn.

Vị thái sư chết trong vòng vây.

Nếu câu chuyện dừng ở đây, ta đã có một kết cục bi tráng quen thuộc. Nhưng tác giả còn cho Văn Trọng làm thêm một việc.

Hồn ông trở về Triều Ca, hiện vào giấc mộng của Trụ Vương.

Ông báo mình đã chết. Rồi vẫn khuyên nhà vua sửa sang chính sự, tìm người hiền giúp nước, đừng tiếp tục chìm trong hoang dâm. Đến lần cuối cùng gặp chủ, điều ông muốn nói vẫn là chuyện cứu lấy triều đại.

Trụ Vương tỉnh dậy, kể lại giấc mộng. Đát Kỷ giải thích rằng vì nhà vua lo Văn thái sư đi đánh giặc nên mới mộng thấy như thế.

Và nhà vua lại yên lòng.

Ở đây có một nỗi buồn rất cụ thể: người bề tôi đã chết vẫn cố nói lời can gián, còn người sống nghe xong lại gác nó sang một bên.

Mang theo điều đó trở lại đàn phong thần, ta sẽ hiểu vì sao Văn Trọng không phải một cái tên vô nghĩa trong danh sách kẻ bại trận.

Khi được gọi lên, ông vẫn giữ khí thế cũ, dẫn theo các vị thuộc Lôi bộ tiến đến mà chưa chịu quỳ. Khương Tử Nha phải cầm roi, yêu cầu ông quỳ nghe sắc lệnh, ông mới làm theo.

Người từng chống Tử Nha đến cùng nay được giao đứng đầu Lôi bộ, nhận chức Cửu Thiên Ứng Nguyên Lôi Thanh Phổ Hóa Thiên Tôn.

Sắc phong nhắc đến sự tận trung của ông với hai đời vua. Chức trách mới liên quan đến mây mưa, nuôi dưỡng vạn vật, trừ gian và việc họa phúc theo thiện ác.

Cuộc đời ông kết thúc bằng việc không giữ được nhà Thương. Công việc sau khi chết lại hướng ra một phạm vi lớn hơn triều đại ông từng bảo vệ.

Đến đây, có vẻ chúng ta đã tìm được lời giải: Khương Tử Nha vẫn nhìn nhận phẩm chất của một đối thủ.

Điều đó đúng với Văn Trọng. Nhưng hãy để chỗ trống trên bàn cho hai người ở đầu câu chuyện. Bởi với họ, lời giải ấy sẽ không còn đủ.

### 4. Có thần vị, tội vẫn còn

Hai người đó là Phi Liêm và Ác Lai.

Ở cuối hồi chín mươi chín, khi họ bị gọi đến, Khương Tử Nha kết tội họ mê hoặc nhà vua, phá hoại chính sự, làm mất cơ nghiệp nhà Thương. Sau khi nước mất, họ lại đem vật báu mong được hưởng bổng lộc dưới nhà Chu.

Tử Nha ra lệnh xử chém. Sang đầu hồi một trăm, án được thi hành.

Rồi hồn hai người được gọi lên đàn.

Điều đáng chú ý nằm ở chính lời sắc phong. Tội cũ được nhắc lại. Họ vẫn bị gọi là gian nịnh, làm hại vua và nước. Truyện không thêm một chiến công bí mật nào để biến họ thành người tốt.

Chức giao cho họ có tên Băng Tiêu Ngõa Giải, gợi đến băng tan và ngói vỡ. Kèm theo chức vị là lời răn phải làm đúng phận sự, không được tiếp tục gây điều hung dữ.

Vậy hai mệnh lệnh lúc đầu đã rõ hơn.

Một lệnh xử tội họ trong cuộc đời đã sống. Lệnh sau định việc cho họ trong thế giới thần linh. Cùng một người có thể bị kết án ở việc trước, rồi vẫn được đặt vào một chức ở việc sau.

Đây là lý do không thể nhìn thấy hai chữ phong thần rồi tự động hiểu thành được tuyên dương.

Ngay trong danh sách ấy đã có những chức gắn với tai họa, bệnh dịch và điều dữ. Thế giới mà truyện dựng lên có người quản việc mưa thuận, cũng có người quản những sức mạnh khiến con người sợ hãi.

Nhưng cũng đừng vội đổi sang một đáp án ngược lại, rằng được phong thần thì ai cũng bị trừng phạt.

Văn Trọng có lời ghi nhận lòng trung. Phi Liêm, Ác Lai bị nhắc tội. Cùng là nhận chức, ý nghĩa đối với từng người đã khác nhau.

Muốn biết một cuộc phong thần có nghĩa gì, phải đọc cả lời phán về người ấy và công việc được giao. Chỉ đọc tên chức sẽ bỏ mất một nửa câu chuyện.

Còn nếu bạn đang nghĩ Khương Tử Nha hẳn phải dành ngoại lệ cho người ghét mình nhất, thì tên tiếp theo lại xuất hiện.

Thân Công Báo.

### 5. Kẻ cản đường lại giúp danh sách thành hình

Văn Trọng đánh Tử Nha để giữ nhà Thương. Với Thân Công Báo, cuộc đối đầu còn mang theo sự thù hằn cá nhân.

Trong hồi bảy mươi hai, Khương Tử Nha vừa qua một trận nguy hiểm, thương tích mới lành, đã gặp Thân Công Báo chặn đường. Hai người nhắc lại mối bất hòa cũ. Thân Công Báo ra tay; Tử Nha phải chống đỡ trong lúc sức chưa hồi phục.

Nhưng lần này Thân Công Báo bị bắt và đưa đến trước Nguyên Thủy Thiên Tôn.

Tại đó, ông bị hỏi tội vì rủ người ở các núi, các đảo đi đánh Tây Kỳ, rồi còn tìm cách hại Tử Nha. Muốn được thả, Thân Công Báo phải thề rằng nếu tiếp tục xúi người tu tiên cản đường Khương Tử Nha, ông sẽ đem thân lấp mắt biển Bắc Hải.

Một lời thề rất cụ thể. Và sau đó truyện cho thấy nó được thực hiện cũng rất cụ thể.

Sau khi Vạn Tiên Trận bị phá, Thân Công Báo tìm đường chạy. Ông bị bắt lại, không có lời nào để chối lời thề trước đó. Nguyên Thủy sai người cuốn ông vào bồ đoàn, đem đi lấp mắt biển.

Đến lễ phong thần, tên ông vẫn được gọi.

Lời sắc nhắc lại việc chống đối và lỗi cũ. Nó cũng xét đến công tu hành, rồi giao cho ông chức Phân Thủy Tướng Quân, với nhiệm vụ ở Đông Hải.

Tuy nhiên, điều khiến trường hợp này đáng kể nhất lại nằm sớm hơn, ngay ở đoạn ông bị buộc phải thề.

Người kể chuyện chen vào giải thích rằng Nguyên Thủy biết Thân Công Báo có vai trò thu tụ những người thuộc số phong thần.

Nghĩa là việc ông đi tìm thêm người về chống Tử Nha, xét trong mạch truyện, đồng thời đưa thêm người vào cuộc đại chiến gắn với việc phong thần.

Càng cố cản đường người thi hành, ông càng góp phần kéo những nhân vật khác đến nơi số phận của họ được định đoạt.

Đây là một nghịch lý có ngay trong lời kể của nguyên tác. Ta không cần dựng thêm chuyện hai người bí mật bắt tay, hoặc khẳng định Thân Công Báo đang diễn theo một kế hoạch mà chính ông biết rõ.

Truyện cho thấy hành động chống đối của ông có một tác dụng lớn hơn ý định trước mắt. Nó vẫn khiến ông phải chịu trách nhiệm, phải giữ lời thề, và cuối cùng nhận một công việc theo sắc lệnh.

Vì thế, nếu hỏi tại sao Tử Nha còn phong cho Thân Công Báo, ta phải nhớ ông đang thực hiện việc phong thần theo mệnh lệnh. Mối thù giữa hai người không đủ để xóa phần đã được định cho người kia.

Đến lúc này, một câu hỏi khác sẽ xuất hiện: nhận được thần vị như vậy, rốt cuộc có đáng mừng không?

### 6. Một chức thần có thể đổi lấy điều gì?

Hãy nhìn một người tu hành trước khi bước vào chiến trận.

Họ có động phủ, có thầy, có pháp thuật, có những năm tháng tu luyện. Mong muốn của họ có thể là tiếp tục con đường ấy. Sau khi xuống núi, họ chết, hồn vào đài phong thần, rồi được giao một chức vụ.

Ta có thể thấy một danh hiệu rất lớn ở cuối hành trình. Nhưng nhân vật vừa mất những gì trên đường đến đó?

Triệu Công Minh là một trường hợp như thế.

Ông đứng về phía Văn Trọng, trở thành đối thủ đáng sợ của quân Tây Kỳ. Nhưng trước khi đi đến cái chết, ông từng có một lần được khuyên dừng lại.

Khi mất pháp bảo, Công Minh đến chỗ các em gái để mượn bảo vật khác. Vân Tiêu không muốn cho mượn. Nàng nhắc chuyện Phong Thần Bảng, lời thầy dặn phải ở yên trong động, rồi khuyên anh trở về núi. Đợi việc phong thần xong, nàng sẽ giúp đòi lại bảo vật.

Ở thời điểm ấy, điều nàng đề nghị khá rõ: tạm chịu mất thứ đang muốn lấy lại, để tránh bước sâu hơn vào cuộc chiến.

Công Minh không chịu. Ông thấy chính em mình còn từ chối thì người ngoài sẽ thế nào. Nỗi tức giận của người mất của va vào nỗi lo của người muốn giữ anh lại. Sau thêm lời thúc giục từ những người khác, bảo vật được cho mượn. Ông trở lại chiến trường.

Biết trước hồi cuối, ta có thể chỉ nhìn thấy một người có số phải chết. Đọc đến cuộc nói chuyện này, ta còn thấy một lựa chọn có lý do và sức nặng: lời cảnh báo đã được nói ra, nhưng mất mát trước mắt khiến ông không muốn dừng.

Để đối phó với ông, Lục Áp trao cho Khương Tử Nha phép Đinh Đầu Thất Tiễn: dựng người rơm có tên Triệu Công Minh, làm lễ theo ngày rồi dùng cung tên tác động vào hình ấy.

Đến hồi bốn mươi chín, người từng có pháp lực mạnh nằm yếu trong doanh trại. Văn Trọng ngồi cạnh, biết mình đã kéo bạn vào tai họa. Ông có thể nhìn người ấy chết mà không cứu được.

Khương Tử Nha bắn vào hình nhân; Triệu Công Minh chết ở doanh bên kia.

Về sau, ông được phong Huyền Đàn Chân Quân, có các vị dưới quyền gắn với việc chiêu tài, nạp trân và lợi thị.

Đó là một thần vị đáng trọng trong cách trình bày của truyện. Nhưng nó không biến cái chết trước đó thành điều nhân vật đã mong muốn. Văn Trọng khóc bạn ngay trong trận chiến, dù người đọc biết sau này còn có một lễ phong thần.

Câu chuyện cho phép cả hai điều cùng tồn tại: một sự tôn phong về sau và một mất mát có thật đối với nhân vật ở lúc ấy.

Ở hồi bảy mươi bảy, khi các giáo chủ đối thoại, nguyên tác còn phân biệt tiên đạo, thần đạo và nhân đạo theo căn hạnh. Con đường thành tiên và con đường nhận thần vị có sự khác nhau trong chính cách tác phẩm sắp đặt thế giới.

Vì vậy, một người tu tiên bị chết rồi nhận chức thần không thể được hiểu đơn giản như vừa lên thêm một bậc sức mạnh.

Sắc phong giao phạm vi phụ trách, quyền hạn và nghĩa vụ. Các vị thần phải làm việc theo chức; trong chiếu lệnh còn có lời răn về việc không được làm bậy, và nhắc đến khả năng thăng tiến theo công.

Nhưng từ đó kết luận mọi thần vị đều là nhà tù thì cũng quá tay. Truyện có lời thương xót, có ghi công, có tặng vinh dự cho những người đã chết. Có người từng là phàm nhân, có người vốn tu hành. Điểm xuất phát và kết cục của họ không giống nhau.

Cách đọc chắc hơn là nhìn phong thần như một sự sắp đặt số phận và chức trách, trong đó có cả ân điển lẫn kỷ luật.

Một khi đã nhận chức, những con người ấy còn đứng cạnh ai? Danh sách dưới quyền Triệu Công Minh có một cái tên khiến câu hỏi ấy trở nên khó chịu hơn ta tưởng.

### 7. Đứng dưới quyền người từng giết mình

Trước khi Triệu Công Minh mất mạng vì phép người rơm, chính ông đã giết một người đang giúp đối phương.

Người ấy tên Tiêu Thăng.

Câu chuyện bắt đầu rất yên bình. Tiêu Thăng và Cao Bảo đang ngồi đánh cờ dưới gốc thông. Rồi Nhiên Đăng chạy đến, phía sau là Triệu Công Minh đuổi theo. Một cuộc truy sát từ chiến trường tràn vào giữa ván cờ.

Hai người hỏi nguyên do và đứng ra can thiệp.

Triệu Công Minh dùng pháp bảo. Tiêu Thăng tung một đồng tiền có cánh, tên là Lạc Bảo Kim Tiền. Dây trói rồng của Công Minh rơi xuống. Tiếp đến, cả Định Hải Châu cũng bị đồng tiền làm rơi. Cao Bảo thu lấy những bảo vật ấy.

Trong vài nhịp ngắn, một người đang truy đuổi đối phương với thế mạnh áp đảo bỗng mất liền hai món đồ quan trọng.

Công Minh nổi giận, đánh ra roi. Tiêu Thăng tiếp tục tung đồng tiền.

Nhưng lần này không giống trước. Theo quy tắc truyện đưa ra ở đây, roi là binh khí, đồng tiền không làm rơi được nó. Tiêu Thăng trúng đòn và chết.

Điều khiến đoạn này dễ nhớ là người vừa thắng hai lần bằng cùng một cách đã không kịp nhận ra lần thứ ba thuộc một trường hợp khác. Một sự nhầm lẫn giữa bảo vật và binh khí kết thúc cuộc đời ông.

Sau đó Triệu Công Minh cũng chết, như ta vừa theo dõi.

Đến lễ phong thần, Công Minh nhận chức đứng đầu một nhóm có bốn vị dưới quyền. Trong bốn vị ấy có Tiêu Thăng, được phong Chiêu Bảo Thiên Tôn.

Người bị giết nay được xếp dưới quyền chính người đã giết mình.

Nếu mới nhìn một bức hình nhóm thần chức, chúng ta có thể thấy năm người đứng cùng nhau, ai cũng có chức danh, tưởng rằng họ vốn là một nhóm từ trước. Đọc lại truyện, quan hệ giữa những người trong hình bỗng đổi khác hoàn toàn.

Và còn một cặp khác: Trịnh Luân và Trần Kỳ.

Trong lời sắc, Trịnh Luân được nhắc là người bỏ Trụ theo Chu, còn Trần Kỳ từng cản quân đánh Trụ. Một người đã đổi sang bên thắng; người kia bị nhận xét là trái thiên mệnh, nhưng lòng trung với nước vẫn có chỗ được ghi nhận.

Họ được phong cùng làm Hanh Cáp Nhị Tướng, nhận việc trấn giữ cửa, bảo vệ pháp bảo và tuyên truyền giáo hóa.

Hai lý lịch thuộc hai phía chiến tuyến được đưa vào một phận sự chung.

Đến đây ta có thể nhìn thấy kết quả của việc phong thần bằng một hình rất cụ thể: các đường nối cũ bị thay. Trước kia chúng nối người này với chủ cũ, với bạn cùng trận, hoặc với kẻ mình muốn đánh bại. Bây giờ có thêm những đường nối theo bộ, theo chức và theo người chỉ huy.

Lễ phong thần đưa ra cách sắp đặt cho thế giới sau chiến tranh. Những tên từng đứng ở hai bên được chuyển vào những vị trí sẽ cùng tồn tại lâu dài.

Nhưng nguyên tác không dành một cuộc trò chuyện riêng để Tiêu Thăng tha thứ cho Công Minh. Ta cũng không biết sau khi nhận chức ông nghĩ gì. Chức vụ đã được sắp; sự hòa giải trong lòng từng người thì không được kể rõ như thế.

Chính khoảng cách này làm cảnh ấy gợi nghĩ. Những mối quan hệ mới đã hình thành, còn người đọc vẫn nhớ cái giá của các cuộc đời cũ.

Đặt lại câu hỏi ban đầu, ta sẽ thấy nó đã mở rộng: kẻ địch của Khương Tử Nha được phong thần; ngay cả những người từng đứng đối diện, từng giết nhau, cũng được sắp vào cùng hệ thống.

Vậy người thi hành cả việc ấy đi về đâu? Sau khi đọc xong phần của từng người, Khương Tử Nha nhận phần gì cho mình?

### 8. Người phong thần đi về đâu?

Đặt Khương Tử Nha trở lại bên cạnh những người vừa được gọi tên, ta mới thấy lời dặn ở Côn Lôn quan trọng thế nào.

Lúc ấy, ông xin được ở lại tu. Thầy nói phần của ông ở nhân gian. Đến cuối truyện, đường đời ấy vẫn được giữ.

Sau lễ phong thần là lễ phân phong ở cõi người. Nhà Chu có những người sống cần được ghi nhận công lao, có đất đai và chức tước cần sắp đặt. Khương Tử Nha được phong ở Tề, nhận quyền và phần thưởng tương ứng với địa vị của mình.

Ông không bước xuống khỏi đàn rồi quay sang gọi hồn bản thân để tự nhận một ghế trong danh sách vừa đọc.

Cũng ở cuối truyện, những người như Dương Tiễn, Na Tra cùng một số người khác xin trở về núi. Tác phẩm gọi nhóm bảy người này là nhục thân thành thánh. Họ đi theo một kết cục khác với những người đã chết rồi được gọi hồn nhận sắc.

Chỉ trong đoạn kết, đã có những ngả đường khác nhau: người nhận thần chức sau khi chết; người sống trở về tiếp tục việc tu hành; người ở lại với quyền vị và công việc nhân gian.

Điều ấy giải thích vì sao không thể xếp tất cả nhân vật trên một bảng thành tích rồi hỏi người nào đáng được phần thưởng lớn nhất.

Với Khương Tử Nha, có một nỗi ngậm ngùi mà người xem có thể tự cảm thấy khi nối đầu truyện với cuối truyện.

Ông đã dành bốn mươi năm trên núi. Ông từng xin được tiếp tục con đường đó. Cuối cùng, ông có công lớn, có quyền vị, có đất phong; nhưng phần đời được trao vẫn là phần ở nhân gian mà thầy đã báo từ trước.

Đây không phải bằng chứng rằng ông bị lừa mất thần vị. Truyện đã đặt lời báo ấy ngay lúc ông xuống núi. Cũng không có lý do từ bản này để kể rằng ông quên dành ghế cho mình, hoặc vừa định ngồi thì có người chiếm mất.

Khi bỏ những lời giải thích truyền miệng ấy sang một bên, kết cục của ông vẫn đủ sức gợi nghĩ.

Một người có thể hoàn thành việc rất lớn, rồi nhận một phần xứng đáng theo trật tự câu chuyện, trong khi mong muốn ban đầu của họ vẫn không trở thành hiện thực.

Và đó cũng là điều khiến cảnh phong thần bớt giống một buổi trao giải vui vẻ. Đứng trên đàn là một người từng phải rời con đường mình muốn. Bên dưới là những người đã chết, mang theo các cuộc đời rất khác nhau, chờ nghe phần tiếp theo của mình.

### 9. Trở lại trước đàn

Bây giờ, quay lại lúc Văn Trọng đứng trước Khương Tử Nha.

Trên chiến trường, ông đã mất quân, mất bạn, mất mạng và không giữ được triều đại. Đến đàn phong thần, ông vẫn mang khí thế của vị thái sư từng chống đối người trên đài.

Ông được ghi nhận lòng trung. Nhưng ông cũng phải quỳ nghe sắc.

Hai chi tiết ấy đặt cạnh nhau sẽ nói rõ hơn bất kỳ câu giải thích đơn lẻ nào. Tác phẩm giữ lại phẩm chất của ông, đồng thời đặt ông vào một trật tự mà ông phải chấp hành.

Phi Liêm và Ác Lai cũng nhận chức, nhưng tội của họ bị đọc lại ngay trong sắc phong. Thân Công Báo nhận việc sau khi phải chịu lời thề của mình. Triệu Công Minh có thần vị, còn cái chết của ông vẫn là một cảnh khiến người ở cạnh phải khóc.

Những cuộc đời khác nhau cùng đi qua một nghi lễ. Bởi vậy, ý nghĩa của nghi lễ ấy không thể chỉ có một màu.

Vậy vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?

Trong thế giới Phong Thần Diễn Nghĩa, việc ấy đã được bàn định vượt lên trên cuộc tranh thắng giữa hai đạo quân. Khương Tử Nha nhận mệnh thi hành; thần vị không chỉ dành cho người từng đứng bên ông. Khi tuyên phong, sắc lệnh vẫn xét phẩm chất, lỗi lầm, công tu hành và nhiệm vụ được giao.

Đánh bại một người ở chiến trường và định phần cho người ấy sau khi chết là hai việc khác nhau.

Từ đây, Mỏ Đen nghĩ điều đáng chú ý nhất khi nhìn Phong Thần Bảng là đọc từng cái tên cùng với cuộc đời vừa kết thúc của họ.

Một chức vị có thể an ủi người đã chết oan. Nó có thể ghi nhận lòng trung của người thua cuộc. Nó cũng có thể đi kèm lời kết tội và một mệnh lệnh phải tuân theo.

Cái bảng gom họ lại. Nhưng những dòng sắc phong vẫn giữ dấu vết của từng người.

Và khi nhìn Văn Trọng lần nữa, ta sẽ thấy trọn vẹn sự chuyển đổi ấy: người từng đem quân giữ lấy nhà Thương, giờ nhận công việc làm mây, làm mưa, nuôi dưỡng vạn vật.

Nhà vua ông cố cứu đã không nghe lời can gián cuối cùng. Còn từ đây, người bề tôi ấy được giao một phận sự vẫn tiếp tục, dù triều đại của ông đã qua.
"""

(OUT_DIR / "00_Kich_Ban_Goc_Day_Du.md").write_text(full_text, encoding="utf-8")

# Extract only the spoken text: from "Khương Tử Nha vừa ra lệnh xử chém hai người." to end of section 9
# Note: do not include markdown headers like "### 1. Hai mệnh lệnh" in the speech text.
sections = re.findall(r'### \d+\..*?\n\n(.*?)(?=\n###|\n---|\Z)', full_text, re.DOTALL)
spoken_paras = []
for sec in sections:
    paragraphs = [p.strip() for p in sec.strip().split('\n\n') if p.strip()]
    spoken_paras.extend(paragraphs)

clean_spoken_text = "\n\n".join(spoken_paras)
(OUT_DIR / "01_Loi_Ke_Sach.txt").write_text(clean_spoken_text, encoding="utf-8")

words = clean_spoken_text.split()
print(f"Saved 00_Kich_Ban_Goc_Day_Du.md and 01_Loi_Ke_Sach.txt.")
print(f"Total sections: {len(sections)}")
print(f"Total paragraphs: {len(spoken_paras)}")
print(f"Total whitespace-separated units: {len(words)}")
