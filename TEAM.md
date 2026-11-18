# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): kotindc321
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-kotindc321-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): 

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Phạm Hữu Đức | 03380 | Kỹ sư cổng | x |
|   2 | Trần Anh Tú | 2A202603368 | Sản phẩm và kinh doanh · Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên:
`["PhamHuuDuc-03380", "TranAnhTu-2A202603368"]`

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## PhamHuuDuc-03380

### Phần việc phụ trách

Vai: Kỹ sư cổng. Phụ trách chạy toàn bộ các lệnh kiểm tra, trace mã lỗi, code và chốt cổng an toàn trong `lab10/guards.py`, chỉ số theo dõi trong `lab10/monitors.py`, quản lý ký duyệt tiêu chí và file cấu hình trong `config/`.

### Đóng góp cụ thể

- Ký và chốt Bản tiêu chí chấp nhận `acceptance_criteria.json`.
- Chạy đánh giá mốc base, trace ticket lỗi T-002@55.
- Cài đặt các cổng phòng ngừa `pre_guard` và `write_gate` trong `lab10/guards.py`.
- Thiết kế chỉ số monitor mới cho sự cố vòng 2.

### Bằng chứng

- Commit `293ef6b` (Sign acceptance criteria).
- Các mã lần chạy kiểm thử trong `runs/journal.jsonl`.

### Exit ticket

- Một điều học được: Sự khác biệt lớn giữa pass_rate và pass^k (tính nhất quán qua nhiều seed).
- Một điều còn chưa chắc: Khả năng tổng quát hóa của cổng chặn trước các bài test hiểm chưa biết.

---

## TranAnhTu-2A202603368

### Phần việc phụ trách

Vai: Sản phẩm và kinh doanh · Vận hành và pháp lý.
Phụ trách điền các nội dung phân tích nghiệp vụ, pháp lý và tài chính trong các phiếu:
- Phiếu A: Mục A1 (Mục tiêu hệ thống & các bên liên quan), A2 (Chỉ số Telemetry production), A3 (Giải thích khoảng tin cậy), A4 (Câu tiêu chí thành công, 4 câu hỏi soát, ranh giới đầu ra).
- Phiếu B: Mục B3 (Bản đồ dữ liệu & kịch bản drift 3 tháng), B4 (HAZOP vòng 1 kỹ thuật & ngoài kỹ thuật), B5 (Checklist 9 nhóm việc có PIC), B6 (Pre-mortem 4 lăng kính), B7.4 (Cổng kinh doanh), B7.5 & B7.6 (Runbook 1-3 & Giờ cao điểm).

### Đóng góp cụ thể

- Phân tích chi tiết rủi ro tài chính và vận hành từ `data/world.json` để xác định các ngưỡng trần ngân sách hoàn tiền ngày (1.500.000đ), ngân sách trần chi phí LLM mỗi ticket (1.500đ), và công suất trực duyệt ca (6 ca/giờ).
- Lập bảng HAZOP mở rộng bao quát cả góc độ con người (CSKH), tài chính (kế toán đối soát) và pháp lý (bảo vệ dữ liệu cá nhân khách hàng PII).
- Soạn thảo Runbook chi tiết cho nhân viên trực ca với ngưỡng cảnh báo Vàng/Đỏ và quy trình dừng khẩn cấp trong vòng 5 phút.

### Bằng chứng

- Phiếu A: Mục A1, A2, A3, A4, A5 (`templates/form-a-criteria.md`).
- Phiếu B: Mục B3, B4, B5, B6, B7.4, B7.5, B7.6 (`templates/form-b-evaluation-gates.md`).

### Exit ticket

- Một điều học được: Một trợ lý AI triển khai thực tế không chỉ cần mô hình trả lời đúng mà phải có hệ thống cổng an toàn, giới hạn vận hành và trách nhiệm con người (human-in-the-loop) bảo bọc bên ngoài.
- Một điều còn chưa chắc: Cách cân bằng tối ưu giữa việc giảm tải cho con người và nguy cơ tích tụ độ trễ hàng chờ khi lượng ticket bất ngờ tăng đột biến.
