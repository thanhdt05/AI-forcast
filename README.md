# Vietnam House Price Prediction - Assignment 01

Project xây dựng một intelligent system nhỏ để dự đoán giá nhà Việt Nam từ `gia_nha.csv`.

## Workflow
Notebook chính bám theo Chapter 12 của *Python Machine Learning*:

**Load data -> Clean data -> Examine correlation -> Prepare representation -> Evaluate algorithms -> Select best -> fit final model -> Save/load model -> Predict -> Deploy.**

Assignment bổ sung các yêu cầu: 3 biểu đồ phân phối, baseline, 5 mô hình, 5 độ đo, 3 controlled experiments, system demonstration 3 cases, reflection và application.

## 5 models
- Linear Regression
- Ridge Regression
- Decision Tree Regressor
- Random Forest Regressor
- Extra Trees Regressor

Mỗi model được train bằng `.fit()` rõ ràng trong notebook.

## 5 metrics
- MAE
- MSE
- RMSE
- R²
- MAPE

## Mobile demo
```bash
pip install -r requirements.txt
python app.py
```

Điện thoại và laptop cùng Wi-Fi, mở `http://<IPv4-laptop>:5000`.
