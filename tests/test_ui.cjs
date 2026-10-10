const fs=require('node:fs');const assert=require('node:assert/strict');const {test}=require('node:test');
const html=fs.readFileSync('app/index.html','utf8');const js=fs.readFileSync('app/app.js','utf8');
test('UI has explicit non-dispatch safety warning',()=>{assert.match(html,/No reemplaza al 911/);assert.match(html,/no envía rescatistas/)});
test('WhatsApp link is opt-in; does not fake group creation',()=>{assert.match(js,/https:\/\/wa\.me\/\?text=/);assert.match(html,/no crea ni administra grupos/)});
test('Google Maps integration is configurable; OSM fallback available',()=>{assert.match(js,/maps\.googleapis\.com\/maps\/api\/js/);assert.match(js,/tile\.openstreetmap\.org/)});
test('UI escapes user text via textContent',()=>{assert.match(js,/e\.textContent=text/);assert.match(js,/description'/)});
test('contains platform visual variants',()=>{assert.match(html,/id="theme"/);assert.match(fs.readFileSync('app/app.css','utf8'),/theme-ios/)});

test('offline safety guide describes constraints',()=>{assert.match(html,/Plan rápido si se corta Internet/);assert.match(html,/datos sísmicos necesitan conexión/)});
