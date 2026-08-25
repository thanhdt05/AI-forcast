/**
 * Vietnam PropTech AI - Clean & Desktop-Balanced Frontend Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('predictForm');
  const addressInput = document.getElementById('addressInput');
  const parsedLoc = document.getElementById('parsedLoc');
  const themeToggle = document.getElementById('themeToggle');
  const resultsContainer = document.getElementById('resultsContainer');
  const predictBtn = document.getElementById('predictBtn');
  const resetBtn = document.getElementById('resetBtn');
  const randomBtn = document.getElementById('randomBtn');

  // Presets Data
  const PRESETS = {
    binhthanh: {
      address: 'Đường Phan Văn Trị, Phường 12, Bình Thạnh, Hồ Chí Minh',
      area: 85, frontage: 5.2, accessRoad: 6.0, floors: 3, bedrooms: 3, bathrooms: 3,
      houseDirection: 'Đông - Nam', balconyDirection: 'Đông - Nam', legalStatus: 'Have certificate', furnitureState: 'Full'
    },
    caugiay: {
      address: 'Đường Cầu Giấy, Phường Dịch Vọng, Cầu Giấy, Hà Nội',
      area: 140, frontage: 7.5, accessRoad: 10.0, floors: 4, bedrooms: 4, bathrooms: 4,
      houseDirection: 'Nam', balconyDirection: 'Nam', legalStatus: 'Have certificate', furnitureState: 'Full'
    },
    nguhanhson: {
      address: 'Đường Võ Nguyên Giáp, Phường Mỹ An, Ngũ Hành Sơn, Đà Nẵng',
      area: 100, frontage: 6.0, accessRoad: 7.5, floors: 3, bedrooms: 3, bathrooms: 3,
      houseDirection: 'Đông', balconyDirection: 'Đông', legalStatus: 'Have certificate', furnitureState: 'Basic'
    },
    ninhkieu: {
      address: 'Đường 30 Tháng 4, Phường Xuân Khánh, Ninh Kiều, Cần Thơ',
      area: 95, frontage: 4.8, accessRoad: 5.0, floors: 2, bedrooms: 3, bathrooms: 2,
      houseDirection: 'Tây - Nam', balconyDirection: 'Nam', legalStatus: 'Have certificate', furnitureState: 'Basic'
    }
  };

  const RANDOM_SAMPLES = [
    {
      address: 'Đường Nguyễn Văn Hưởng, Thảo Điền, Quận 2, Hồ Chí Minh',
      area: 180, frontage: 9.0, accessRoad: 12.0, floors: 3, bedrooms: 4, bathrooms: 5,
      houseDirection: 'Đông - Nam', balconyDirection: 'Đông - Nam', legalStatus: 'Have certificate', furnitureState: 'Full'
    },
    {
      address: 'Đường Hoàng Hoa Thám, Ba Đình, Hà Nội',
      area: 65, frontage: 4.5, accessRoad: 4.0, floors: 4, bedrooms: 3, bathrooms: 3,
      houseDirection: 'Đông', balconyDirection: 'Đông', legalStatus: 'Have certificate', furnitureState: 'Basic'
    },
    {
      address: 'Đường Lê Duẩn, Hải Châu, Đà Nẵng',
      area: 75, frontage: 5.0, accessRoad: 6.0, floors: 3, bedrooms: 3, bathrooms: 3,
      houseDirection: 'Bắc', balconyDirection: 'Bắc', legalStatus: 'Have certificate', furnitureState: 'Full'
    },
    {
      address: 'Đường Đại Lộ Bình Dương, Thủ Dầu Một, Bình Dương',
      area: 120, frontage: 6.0, accessRoad: 8.0, floors: 3, bedrooms: 4, bathrooms: 3,
      houseDirection: 'Đông - Nam', balconyDirection: 'Nam', legalStatus: 'Have certificate', furnitureState: 'Full'
    }
  ];

  // Theme Handling
  const savedTheme = localStorage.getItem('proptech_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('proptech_theme', next);
      updateThemeIcon(next);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeToggle) return;
    themeToggle.innerHTML = theme === 'dark'
      ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>`
      : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`;
  }

  // Address Live Location Parser
  function parseLocation(val) {
    if (!val) return null;
    const parts = val.split(',').map(s => s.trim().replace(/[.\s]+$/, '')).filter(Boolean);
    const province = parts.length >= 1 ? parts[parts.length - 1] : '';
    const district = parts.length >= 2 ? parts[parts.length - 2] : '';
    if (!province) return null;
    return district ? `${district}, ${province}` : province;
  }

  function updateLocationBadge() {
    if (!addressInput || !parsedLoc) return;
    const loc = parseLocation(addressInput.value);
    parsedLoc.textContent = loc ? `📍 ${loc}` : '';
  }

  if (addressInput) {
    addressInput.addEventListener('input', updateLocationBadge);
    updateLocationBadge();
  }

  // City chips click handler
  document.querySelectorAll('.city-chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      e.preventDefault();
      const city = chip.getAttribute('data-city');
      if (addressInput) {
        if (!addressInput.value.includes(city)) {
          addressInput.value = addressInput.value ? `${addressInput.value}, ${city}` : `Đường chính, ${city}`;
        }
        updateLocationBadge();
        addressInput.focus();
      }
    });
  });

  // Preset Handlers
  document.querySelectorAll('.pill-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const presetKey = btn.getAttribute('data-preset');
      const data = PRESETS[presetKey];
      if (data) {
        fillForm(data);
        document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        triggerPrediction();
      }
    });
  });

  // Randomize Button
  if (randomBtn) {
    randomBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const randomData = RANDOM_SAMPLES[Math.floor(Math.random() * RANDOM_SAMPLES.length)];
      fillForm(randomData);
      triggerPrediction();
    });
  }

  // Reset Button
  if (resetBtn) {
    resetBtn.addEventListener('click', (e) => {
      e.preventDefault();
      form.reset();
      updateLocationBadge();
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
    });
  }

  function fillForm(data) {
    if (!form) return;
    form.querySelector('[name="Address"]').value = data.address || '';
    form.querySelector('[name="Area"]').value = data.area || '';
    form.querySelector('[name="Frontage"]').value = data.frontage || '';
    form.querySelector('[name="Access Road"]').value = data.accessRoad || '';
    form.querySelector('[name="Floors"]').value = data.floors || '';
    form.querySelector('[name="Bedrooms"]').value = data.bedrooms || '';
    form.querySelector('[name="Bathrooms"]').value = data.bathrooms || '';
    form.querySelector('[name="House direction"]').value = data.houseDirection || '';
    form.querySelector('[name="Balcony direction"]').value = data.balconyDirection || '';
    form.querySelector('[name="Legal status"]').value = data.legalStatus || '';
    form.querySelector('[name="Furniture state"]').value = data.furnitureState || '';
    updateLocationBadge();
  }

  // Form Submit Handler (AJAX)
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await triggerPrediction();
    });
  }

  async function triggerPrediction() {
    if (!form) return;
    const formData = new FormData(form);
    const payload = {};
    formData.forEach((value, key) => {
      payload[key] = value;
    });

    if (!payload['Address'] || !payload['Area']) {
      form.reportValidity();
      return;
    }

    // Loading button state
    if (predictBtn) {
      predictBtn.disabled = true;
      predictBtn.innerHTML = `<span>⏳ Đang phân tích mô hình...</span>`;
    }

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error('Dự đoán thất bại');
      const res = await response.json();
      
      if (res.status === 'success') {
        renderResults(res.metrics, res.location, payload);
        if (window.innerWidth <= 1024 && resultsContainer) {
          resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      if (predictBtn) {
        predictBtn.disabled = false;
        predictBtn.innerHTML = `
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span>🚀 Phân Tích & Dự Đoán Giá</span>
        `;
      }
    }
  }

  // Render Result Dashboard
  function renderResults(metrics, location, inputData) {
    if (!resultsContainer) return;

    const priceBillionFormatted = metrics.price_billion_formatted;
    const priceWords = metrics.price_words;
    const priceVnd = metrics.price_vnd_formatted;
    const priceUsd = metrics.price_usd_formatted;
    const pricePerM2 = metrics.price_per_m2_million ? `~ ${metrics.price_per_m2_million} tr/m²` : '--';
    const minRange = metrics.price_min_billion;
    const maxRange = metrics.price_max_billion;

    resultsContainer.innerHTML = `
      <div class="hero-price-card">
        <div class="price-top-meta">
          <span class="price-meta-label">Định giá ước tính bởi AI</span>
          <span style="font-size: 0.82rem; color: var(--accent-emerald); font-weight: 700;">±6% Biên độ thị trường</span>
        </div>

        <div class="price-big-row">
          <span class="price-num" id="animatedPrice">${priceBillionFormatted}</span>
          <span class="price-unit-tag">TỶ VNĐ</span>
        </div>

        <div class="price-words-sub">
          ✨ ${priceWords}
        </div>

        <div class="metric-grid">
          <div class="metric-cell">
            <div class="metric-cell-label">Tổng giá trị (VND)</div>
            <div class="metric-cell-val">${priceVnd}</div>
          </div>
          <div class="metric-cell">
            <div class="metric-cell-label">Quy đổi Ngoại tệ</div>
            <div class="metric-cell-val" style="color: #38bdf8;">${priceUsd}</div>
          </div>
          <div class="metric-cell">
            <div class="metric-cell-label">Đơn giá đất</div>
            <div class="metric-cell-val" style="color: #34d399;">${pricePerM2}</div>
          </div>
          <div class="metric-cell">
            <div class="metric-cell-label">Khoảng giá ước lượng</div>
            <div class="metric-cell-val" style="color: #f59e0b;">${minRange} - ${maxRange} tỷ</div>
          </div>
        </div>

        <div class="range-box">
          <div class="range-minmax">
            <span>Thấp: ${minRange} tỷ</span>
            <span style="color: #a5b4fc; font-weight: 700;">★ Giá chuẩn: ${priceBillionFormatted} tỷ</span>
            <span>Cao: ${maxRange} tỷ</span>
          </div>
          <div class="range-bar">
            <div class="range-bar-inner"></div>
          </div>
        </div>

        <div class="util-actions">
          <button class="btn-util" id="copyResultBtn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
            Sao chép kết quả
          </button>
          <button class="btn-util" onclick="window.print()">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg>
            In báo cáo
          </button>
        </div>
      </div>

      <div class="card">
        <div class="card-title" style="font-size: 0.95rem; margin-bottom: 14px;">Tóm tắt đặc điểm bất động sản</div>
        <div class="spec-summary">
          <div class="spec-chip">📍 ${location.district ? location.district + ', ' : ''}${location.province}</div>
          <div class="spec-chip">📐 ${inputData.Area || '--'} m²</div>
          <div class="spec-chip">🏢 ${inputData.Floors ? inputData.Floors + ' Tầng' : '1 Tầng'}</div>
          <div class="spec-chip">🛏️ ${inputData.Bedrooms || 0} PN • ${inputData.Bathrooms || 0} WC</div>
          ${inputData['House direction'] ? `<div class="spec-chip">🧭 ${inputData['House direction']}</div>` : ''}
          ${inputData['Legal status'] ? `<div class="spec-chip">⚖️ ${inputData['Legal status']}</div>` : ''}
        </div>
      </div>

      <div class="card">
        <div class="card-title" style="font-size: 0.95rem; margin-bottom: 12px;">Trọng số định giá chính (Feature Importance)</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted);">
            <span>1. Diện tích đất (Area)</span>
            <span style="color: var(--accent-cyan); font-weight: 700;">42%</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted);">
            <span>2. Vị trí địa lý (Tỉnh/Thành, Quận/Huyện)</span>
            <span style="color: var(--accent-primary); font-weight: 700;">26%</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted);">
            <span>3. Số tầng & Quy mô công trình</span>
            <span style="color: var(--accent-emerald); font-weight: 700;">18%</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted);">
            <span>4. Mặt tiền & Đường vào</span>
            <span style="color: var(--accent-amber); font-weight: 700;">14%</span>
          </div>
        </div>
      </div>
    `;

    // Copy Handler
    const copyBtn = document.getElementById('copyResultBtn');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const txt = `ĐỊNH GIÁ BẤT ĐỘNG SẢN AI\nĐịa chỉ: ${inputData.Address}\nDiện tích: ${inputData.Area} m²\nGiá ước tính: ${priceBillionFormatted} Tỷ VNĐ (${priceWords})\nĐơn giá: ${pricePerM2}`;
        navigator.clipboard.writeText(txt).then(() => {
          copyBtn.textContent = '✓ Đã sao chép';
          setTimeout(() => {
            copyBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg> Sao chép kết quả`;
          }, 1500);
        });
      });
    }

    // Number Count Up Animation
    const targetNumber = parseFloat(priceBillionFormatted);
    animateValue('animatedPrice', 0, targetNumber, 600);
  }

  function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    if (!obj) return;
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const current = start + (end - start) * easeProgress;
      obj.textContent = current.toFixed(2);
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        obj.textContent = end.toFixed(2);
      }
    };
    window.requestAnimationFrame(step);
  }
});
