import os
import re
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'house_price_model.pkl')
with open(MODEL_PATH, 'rb') as f:
    bundle = pickle.load(f)

preprocessor = bundle['preprocessor']
model = bundle['model']
feature_cols = bundle['feature_cols']


def extract_location(address):
    if not address:
        return 'Unknown', 'Unknown'
    parts = [re.sub(r'[.\s]+$', '', p.strip()) for p in str(address).split(',') if p.strip()]
    province = parts[-1] if len(parts) >= 1 and parts[-1] else 'Unknown'
    district = parts[-2] if len(parts) >= 2 and parts[-2] else 'Unknown'
    return province, district


def number_or_nan(value):
    if value is None or str(value).strip() == '':
        return np.nan
    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan


def make_sample(data):
    province, district = extract_location(data.get('Address', ''))
    sample = pd.DataFrame([{
        'Area': number_or_nan(data.get('Area')),
        'Frontage': number_or_nan(data.get('Frontage')),
        'Access Road': number_or_nan(data.get('Access Road')),
        'Floors': number_or_nan(data.get('Floors')),
        'Bedrooms': number_or_nan(data.get('Bedrooms')),
        'Bathrooms': number_or_nan(data.get('Bathrooms')),
        'House direction': data.get('House direction') or np.nan,
        'Balcony direction': data.get('Balcony direction') or np.nan,
        'Legal status': data.get('Legal status') or np.nan,
        'Furniture state': data.get('Furniture state') or np.nan,
        'Province': province,
        'District': district,
    }])
    return sample[feature_cols], province, district


def predict_price(sample):
    prepared = preprocessor.transform(sample)
    pred = float(model.predict(prepared)[0])
    return max(0.1, pred)


def format_vietnamese_words(billion_val):
    if billion_val is None or np.isnan(billion_val):
        return "0 VNĐ"
    vnd = int(round(billion_val * 1_000_000_000))
    tys = vnd // 1_000_000_000
    trieus = (vnd % 1_000_000_000) // 1_000_000
    parts = []
    if tys > 0:
        parts.append(f"{tys} tỷ")
    if trieus > 0:
        parts.append(f"{trieus} triệu")
    if not parts:
        parts.append(f"{vnd:,} VNĐ")
    else:
        parts.append("VNĐ")
    return " ".join(parts)


def compute_metrics(price_billion, area=None):
    price_billion = float(price_billion)
    vnd_total = int(round(price_billion * 1_000_000_000))
    usd_total = int(round(vnd_total / 25400))
    
    price_per_m2 = None
    if area and not np.isnan(area) and area > 0:
        price_per_m2 = round((vnd_total / area) / 1_000_000, 2)
        
    return {
        'price_billion': round(price_billion, 3),
        'price_billion_formatted': f"{price_billion:.2f}",
        'price_vnd_formatted': f"{vnd_total:,.0f} ₫".replace(",", "."),
        'price_words': format_vietnamese_words(price_billion),
        'price_usd_formatted': f"${usd_total:,.0f} USD",
        'price_per_m2_million': price_per_m2,
        'price_min_billion': round(price_billion * 0.94, 2),
        'price_max_billion': round(price_billion * 1.06, 2),
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_data = None
    form_data = {}
    
    if request.method == 'POST':
        raw_data = request.get_json(silent=True) or request.form.to_dict()
        form_data = raw_data
        sample, province, district = make_sample(raw_data)
        pred = predict_price(sample)
        area_val = number_or_nan(raw_data.get('Area'))
        
        metrics = compute_metrics(pred, area_val)
        prediction_data = {
            **metrics,
            'province': province,
            'district': district,
            'address': raw_data.get('Address', ''),
            'area': area_val,
            'floors': number_or_nan(raw_data.get('Floors')),
            'bedrooms': number_or_nan(raw_data.get('Bedrooms')),
            'bathrooms': number_or_nan(raw_data.get('Bathrooms')),
            'direction': raw_data.get('House direction', ''),
            'legal': raw_data.get('Legal status', ''),
            'furniture': raw_data.get('Furniture state', ''),
        }
        
        # If AJAX / JSON requested
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('format') == 'json':
            return jsonify({
                'status': 'success',
                'prediction': prediction_data,
                'raw_prediction_billion': round(pred, 4)
            })
            
    return render_template('index.html', prediction=prediction_data, form_data=form_data)


@app.route('/api/predict', methods=['POST'])
def api_predict_rich():
    raw_data = request.get_json(force=True, silent=True) or request.form.to_dict()
    sample, province, district = make_sample(raw_data)
    pred = predict_price(sample)
    area_val = number_or_nan(raw_data.get('Area'))
    metrics = compute_metrics(pred, area_val)
    return jsonify({
        'status': 'success',
        'metrics': metrics,
        'location': {'province': province, 'district': district},
        'input': raw_data
    })


@app.route('/house/v1/predict', methods=['POST'])
def api_predict():
    data = request.get_json(force=True, silent=True) or request.form.to_dict()
    sample, _, _ = make_sample(data)
    prediction = predict_price(sample)
    return jsonify({'predicted_price_billion_vnd': round(prediction, 3)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

