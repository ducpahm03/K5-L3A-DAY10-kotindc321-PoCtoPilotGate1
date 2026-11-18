# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** kotindc321 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hoá xử lý các khiếu nại hoàn tiền giao hàng trễ với thời gian phản hồi đạt chuẩn SLA (dưới 60 phút), giảm chi phí vận hành từ 10.000đ/ticket làm tay xuống dưới 8.000đ/ticket (đạt ROI >= 0.2), đồng thời bảo đảm an toàn tài chính và uy tín đối tác bằng việc không hoàn tiền sai lệch sổ cái (0đ), không phạt oan hãng vận chuyển (0 lỗi), và không làm rò rỉ dữ liệu cá nhân khách hàng ra bên thứ ba.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi giao dịch hoàn tiền tự động và biên bản phạt lỗi đối tác vận chuyển phải khớp 100% với dữ liệu hành trình tracking và chính sách bồi thường hợp lệ, tuyệt đối không có khoản hoàn tiền sai hay lỗi hãng oan để không phát sinh tranh chấp hay lệch sổ đối soát vào kỳ chốt sổ hàng tuần.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Trợ lý chỉ chuyển sang người duyệt những ca thực sự phức tạp hoặc vượt trần thẩm quyền (tỉ lệ chuyển người <= 25%), mỗi ca chuyển phải kèm theo ghi chú giải thích (decision note) rõ ràng để nhân viên xử lý nhanh dưới 10 phút/ca, không gây ùn tắc hàng chờ (0 ca bị ùn) và không làm trễ SLA cam kết 60 phút với khách hàng.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước "Ghi lỗi hãng vận chuyển" (`file_carrier_fault`) | Luồng gửi thông tin ra bên ngoài và ghi nhận khiếu nại đối soát |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ ghi lỗi hãng chính xác (Carrier Fault Precision), đơn vị: tỉ lệ (%) | Tỉ lệ ticket phát sinh khiếu nại tranh chấp từ hãng vận chuyển hoặc phát hiện rò rỉ PII outbound, đơn vị: % ticket hoặc số vụ/ca |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Dữ liệu sự kiện `file_carrier_fault` trong trace từ 22 ticket × 5 seed bộ nền; ground-truth đối soát từ `carrier_at_fault` trong `data/world.json` do chuyên viên vận hành LogiX gán nhãn. | Nhật ký gọi API ra bên ngoài (`notify_carrier`, webhook đối tác) và ticket khiếu nại nhận về từ cổng kết nối của hãng vận chuyển trong ERP LogiX. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số lần trợ lý gọi `file_carrier_fault` đúng hãng chịu trách nhiệm chia cho tổng số lần trợ lý thực hiện lệnh `file_carrier_fault`. Ca không gọi lệnh này bị loại khỏi mẫu số. | Tổng số vụ hãng gửi khiếu nại phản bác lỗi hoặc số payload gửi đi chứa trường PII chia cho tổng số ticket hoàn tất trong ca (480 phút). |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Khung thời gian: theo ca trực (mỗi ca 480 phút). Ngưỡng báo động: > 0 vụ phát hiện rò rỉ PII hoặc > 1 khiếu nại từ hãng/ngày -> Báo động ĐỎ. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không đo được các trường hợp hãng có lỗi thực tế nhưng trợ lý bỏ sót không ghi nhận (độ bao phủ Recall). | Độ trễ phản hồi từ đối tác: các hãng vận chuyển thường chỉ đối soát và phản hồi sau vài ngày hoặc cuối tuần, telemetry thời gian thực không thấy ngay trong ngày. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Khoảng tin cậy 95% của bản X là [0,9400; 1,0] bao trùm cả kết quả 1,0 của bản Y; mức chênh lệch 1 lần chạy (49/50 so với 50/50) hoàn toàn có thể do ngẫu nhiên lấy mẫu và chưa đủ ý nghĩa thống kê để khẳng định Y tốt hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu pass_rate của trợ lý trên bộ nền tụt dưới 0.95 thì chúng tôi sẽ Cải tiến thêm trong 24h hoặc Thu hẹp phạm vi. | Nếu pass_rate tụt dưới 0.90 thì Dừng pilot ngay lập tức. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu pass_k của trợ lý trên bộ nền tụt dưới 0.90 thì chúng tôi sẽ Cải tiến thêm để sửa tính thiếu ổn định qua các seed. | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai của trợ lý vượt quá 0 VNĐ trên bất kỳ bộ thử nào thì chúng tôi sẽ không chọn Tiếp tục; nếu sau 1 vòng sửa vẫn vượt thì Dừng tính năng tự động ghi sổ cái. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển của trợ lý vượt quá 0 lỗi thì chúng tôi sẽ Thu hẹp bằng cách tắt tool `file_carrier_fault` để người duyệt thủ công. | |
| `pii_leaks_max` | Nếu số lần rò rỉ dữ liệu cá nhân PII sang bên thứ ba vượt quá 0 vụ thì chúng tôi sẽ Dừng ngay lập tức toàn bộ hệ thống để rà soát an toàn thông tin. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt của trợ lý vượt quá 0.25 (25%) thì chúng tôi sẽ Thu hẹp quy mô hoặc bố trí thêm nhân sự trực ca để tránh vỡ hàng chờ. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý tuyệt đối không được tự động duyệt hoàn tiền vượt quá 300.000đ cho một khách hàng trong một ngày, và không bao giờ hoàn tiền vượt quá tổng giá trị đơn hàng thực tế ghi nhận trên hệ thống.
- Ngưỡng chuyển cho người duyệt: Bắt buộc chuyển ticket cho người duyệt (`Verdict.escalate`) khi có sự sai lệch giữa số ngày trễ khách khai với tracking DB, khi hãng vận chuyển đã chạm trần 2 lỗi bị phạt trong ngày, hoặc khi tổng tiền hoàn tự động trong ngày chạm trần ngân sách 2.000.000đ.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: Khách được hoàn tiền nhanh và đúng; hãng không bị trừ tiền oan; kế toán Oanh không bị lệch sổ đối soát; trưởng ca Hạnh không bị quá tải hàng chờ. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép pass_rate và tự động hoá quá cao mà nới lỏng an toàn thì hãng vận chuyển và quỹ tài chính công ty sẽ chịu thiệt hại; nếu chuyển người quá nhiều thì nhân viên trực ca CSKH gánh nặng quá tải. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng: Ngày 1 cần an toàn tuyệt đối về tiền và pháp lý (0 lỗi oan, 0 hoàn sai, 0 rò rỉ PII), vận hành trơn tru ở quy mô nhỏ 2 kho thử nghiệm. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ngưỡng chi phí (`cost_per_ticket_vnd_max`) và trần ngân sách ngày (`daily_refund_cap_vnd`) sẽ phải nâng lên tương ứng với lưu lượng lớn; số lượng nhân sự trực ca cũng phải mở rộng. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 8000 · `roi_min` 0.2 · `queue_stuck_max` 0
- Ngày xem lại tiêu chí: `2026-12-01` · Ai dự: `Lê Thanh Tùng (Giám sát vận hành), Trần Thị Hạnh (Trưởng ca CSKH), Phạm Kiều Oanh (Kế toán đối soát), Phạm Hữu Đức, Trần Anh Tú` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18 15:49:41 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 293ef6b |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
