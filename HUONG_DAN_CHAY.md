# HƯỚNG DẪN CHẠY ASSIGNMENT

## 1. Chạy notebook
Mở Anaconda Prompt/Terminal tại thư mục project:

```bash
jupyter lab
```

Mở `house_price_assignment.ipynb` và chọn **Run -> Run All Cells**.

Notebook được viết theo luồng Chapter 12:

`Load data -> Clean data -> Correlation -> Prepare representation -> Evaluate models -> Select model -> fit final model -> Save/load -> Predict -> Deploy`.

Điểm cần chú ý khi thầy hỏi: cả 5 model đều có dòng `model.fit(X_train_ready, y_train)` rõ ràng. Random Forest trong các experiment cũng dùng `.fit()`, và final model có `final_model.fit(...)`.

Khi Run All, notebook tự tạo lại:
- 8 hình trong `figures/`;
- các bảng kết quả trong `results/`;
- `house_price_model.pkl`.

## 2. Chạy giao diện mobile/web
Sau khi notebook đã chạy xong:

```bash
pip install -r requirements.txt
python app.py
```

Trên laptop mở:

```text
http://127.0.0.1:5000
```

## 3. Mở bằng điện thoại miễn phí
Điện thoại và laptop nối cùng Wi-Fi.

Trên Windows chạy:

```cmd
ipconfig
```

Tìm IPv4 của laptop, ví dụ `192.168.1.20`, rồi trên điện thoại mở:

```text
http://192.168.1.20:5000
```

Nếu không vào được, cho phép Python qua Windows Firewall ở mạng Private.

## 4. File chính để nộp/demo
- `house_price_assignment.ipynb`: notebook chính.
- `technical_report.docx`: báo cáo kỹ thuật.
- `gia_nha.csv`: dữ liệu assignment.
- `app.py`: application/mobile web.
- `house_price_model.pkl`: model + preprocessing đã lưu.
- `README.md`: mô tả project.
- `chapter12_diabetes_demo.ipynb`: notebook tham chiếu Chapter 12 với `diabetes.csv`.

## 5. Kết quả hiện tại (sinh trực tiếp khi Run All)
Random Forest là model tốt nhất trên validation set. Kết quả final test hiện tại xấp xỉ:
- MAE: 1.0551 tỷ VNĐ
- MSE: 1.9942
- RMSE: 1.4122 tỷ VNĐ
- R²: 0.5910
- MAPE: 22.36%

Không sửa tay các con số này trong notebook. Nếu dữ liệu/code thay đổi, Run All sẽ tính lại.
