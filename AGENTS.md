# Story Motion Studio Local

Đọc PROGRESS.md và DECISIONS.md trước. Đặc tả gốc: docs/spec/00–05.
Một agent duy nhất. Không subagent, AI API trả phí, cloud publish hoặc tự thay lời.
Core là nguồn ghi duy nhất; mọi mutation dùng revision/idempotency, agent dùng lease.
Audio sample clock là chuẩn; preview/export dùng cùng scene evaluator theo frame.
Giữ source bất biến. Không khai hoàn thành tính năng/model chưa chạy thật.
Chỉ chạy kiểm chứng liên quan V01–V10; không A/B hay tự sinh lại vì thẩm mỹ.
Thư mục dữ liệu mặc định data/; Python core .venv; worker env tách riêng.
