from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Base de données des produits
PRODUCTS = {
    'cpu': {
        'r5_5600x': {'name': 'AMD Ryzen 5 5600X', 'price': 126, 'url': 'https://www.reichelt.com/fr/fr/shop/produit/amd_am4_ryzen_5_5600x_6_x_3_70_ghz_plateau-336031'},
        'r7_5700x': {'name': 'AMD Ryzen 7 5700X', 'price': 154, 'url': 'https://www.reichelt.com/fr/fr/shop/produit/amd_am4_ryzen_7_5700x_8_x_3_40_ghz_plateau-336037'},
        'r7_7800x3d': {'name': 'AMD Ryzen 7 7800X3D', 'price': 314, 'url': 'https://www.amazon.de/-/en/Ryzen-7800X3D-4-2GHz-Processor-Socket/dp/B0CTD76W9C'}
    },
    'gpu': {
        'rtx3060ti': {'name': 'NVIDIA RTX 3060 Ti 8GB', 'price': 280, 'url': 'https://www.idealo.fr/cat/4574/cartes-graphiques.html'},
        'rtx4060': {'name': 'NVIDIA RTX 4060 8GB', 'price': 320, 'url': 'https://www.idealo.fr/cat/4574/cartes-graphiques.html'},
        'rtx4060ti': {'name': 'NVIDIA RTX 4060 Ti 8GB', 'price': 481, 'url': 'https://amazon.fr/dp/B0CJ9D1VBH'},
        'rtx4070': {'name': 'NVIDIA RTX 4070 12GB', 'price': 787, 'url': 'https://www.amazon.de/-/en/Graphics-Card-VCG4070S12DFXPB1-Super-GDDR6X/dp/B0D363JYTH'},
        'rtx4070ti': {'name': 'NVIDIA RTX 4070 Ti 12GB', 'price': 743, 'url': 'https://www.amazon.fr/ASUS-GeForce-Super-Carte-Graphique/dp/B086ZS934X'},
        'rtx4080': {'name': 'NVIDIA RTX 4080 Super 16GB', 'price': 1289, 'url': 'https://www.amazon.de/-/en/nVidia-GeForce-RTX-4080-Founders/dp/B0BMZ9TGH1'}
    },
    'ram': {
        'ddr4_16gb': {'name': '16GB DDR4 3200MHz', 'price': 40, 'url': 'https://www.idealo.fr/cat/3610/memoire-vive.html'},
        'ddr4_32gb': {'name': '32GB DDR4 3600MHz', 'price': 80, 'url': 'https://www.idealo.fr/cat/3610/memoire-vive.html'},
        'ddr5_16gb_kingston': {'name': '16GB DDR5 6000MT/s Kingston FURY Beast CL30', 'price': 232, 'url': 'https://www.amazon.fr/Kingston-6000MT-Desktop-Gaming-Memory/dp/B0CYM58GFS'},
        'ddr5_32gb': {'name': '32GB DDR5 6000MHz', 'price': 130, 'url': 'https://www.idealo.fr/cat/3610/memoire-vive.html'}
    },
    'ssd': {
        'kingston500': {'name': 'Kingston NV2 500GB NVMe', 'price': 1000, 'url': 'https://www.idealo.fr/cat/4605/disques-durs-ssd.html'},
        'samsung1tb': {'name': 'Samsung 980 1TB NVMe', 'price': 209, 'url': 'https://amazon.fr/dp/B08V83JZH4'},
        'samsung2tb': {'name': 'Samsung 990 PRO 2TB NVMe Gen4', 'price': 285, 'url': 'https://www.darty.com/nav/achat/console_jeux/composant/disque_ssd/samsung_ssd_int_990_pro_2to.html'}
    },
    'mobo': {
        'b550': {'name': 'MSI B550 Gaming Plus', 'price': 115, 'url': 'https://www.amazon.fr/dp/B08B4V6H3N'},
        'b650': {'name': 'MSI B650 Gaming Plus WiFi', 'price': 148, 'url': 'https://www.reichelt.com/fr/fr/shop/produit/carte_m_re_msi_b650_gaming_plus_wifi_am5_-357793'}
    },
    'psu': {
        'cv650': {'name': 'Corsair CV650 650W 80+ Bronze', 'price': 99, 'url': 'https://amazon.fr/dp/B0DMTMK2Q5'},
        'rm750': {'name': 'Corsair RM750 750W 80+ Bronze', 'price': 159, 'url': 'https://amazon.fr/dp/B0D9C1DT62'},
        'rm850': {'name': 'Corsair RM850 850W 80+ Bronze', 'price': 189, 'url': 'https://amazon.fr/dp/B0D9C1DT62'}
    },
    'case': {
        'default_case': {'name': 'Foikin F300 (7ventilateur)', 'price': 75, 'url': 'https://www.amazon.fr/FOIFKIN-Boitier-pr%C3%A9install%C3%A9s-Ventilateur-panoramique/dp/B0DFR66MM5/ref=sr_1_4?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=21X9CIH5OJ41F&dib=eyJ2IjoiMSJ9.CVDVyZiep4KbIs38RGSYIkO7f3ZDs4K0r2sn1xn7MJwN1GSnpU5dF8SDzFmcT5pkcQ-bSK_zjI9rwxcqekNkjE92ZoDyNqeuOTaxbfwCFSEvPAK_T0jDH1l__Fq5Z8h7yQNYYn-Ay_03nIxPGv1u07RMmAbXUpIVF_Ln3tLNWU6ubYVK38bQp7y0yqwzf7Aemayq-qTtvZ23CZa_tNFZ_dgm9cQNVp5GIh2DH0RIhP8.aWloAIDHC-ypL0cel99ReettaoMJlPN8DjL405cRJH8&dib_tag=se&keywords=foikin+aquarium+atx+black&qid=1768690112&s=electronics&sprefix=foikin+quarium+atx+black%2Celectronics%2C246&sr=1-4'}
    },
    'monitor': {
        'aoc24': {'name': 'AOC 24G2U 24" 144Hz IPS', 'price': 154, 'url': 'https://www.electrodepot.fr/moniteur-aoc-27-q27g42ze-qhd-240hz-0-3ms.html'},
        'lg27': {'name': 'LG 27GP850-B 27" 165Hz IPS', 'price': 189, 'url': 'https://www.amazon.fr/dp/B0FWCJYML5'},
        'asus_oled': {'name': 'ASUS ROG Swift PG27AQDM 27" 240Hz OLED', 'price': 640, 'url': 'https://amazon.fr/dp/B0BXY85B9F'}
    },
    'mount': {
        'ergotron': {'name': 'Ergotron LX Desk Mount', 'price': 19, 'url': 'https://amazon.de/-/en/MD01A-Monitor-Rotatable-Adjustable-Swivelling-black/dp/B0CGX7BY2T'}
    },
    'keyboard': {
        'geeky': {'name': 'Geeky GK61 60% Rétroéclairées Mechanical Keyboard', 'price': 30, 'url': 'https://www.amazon.fr/Geeky-GK61-60-R%C3%A9tro%C3%A9clair%C3%A9es-Mechanical/dp/B0C77DHJSZ'}
    },
    'mouse': {
        'redgragon': {'name': 'Redragon M652 Pro', 'price': 30, 'url': 'https://www.amazon.fr/Wireless-Redragon-Rechargeable-Programmable-Ergonomic/dp/B0B66RHD7B'}
    },
    'mousepad': {
        'razer': {'name': 'Razer Gigantus V2 XXL', 'price': 36, 'url': 'https://www.amazon.fr/Gigantus-rapidit%C3%A9-Caoutchouc-antid%C3%A9rapant-microtextur%C3%A9/dp/B086RGYBY9'}
    }
}

def build_pc(budget):
    """Construit un PC optimal avec le budget donné"""
    remaining = budget
    config = []
    
    is_high_end_build = budget >= 2100
    
    # 1. CPU
    if remaining >= 326:
        cpu = PRODUCTS['cpu']['r7_7800x3d']
        mobo_key = 'b650'
        ram_key = 'ddr5_32gb' if is_high_end_build else 'ddr5_16gb_kingston'
    elif remaining >= 154:
        cpu = PRODUCTS['cpu']['r7_5700x']
        mobo_key = 'b550'
        ram_key = 'ddr4_32gb' if is_high_end_build else 'ddr4_16gb'
    else:
        cpu = PRODUCTS['cpu']['r5_5600x']
        mobo_key = 'b550'
        ram_key = 'ddr4_16gb'
    
    config.append({'type': 'CPU', **cpu})
    remaining -= cpu['price']
    
    # 2. Carte mère
    mobo = PRODUCTS['mobo'][mobo_key]
    config.append({'type': 'Carte mère', **mobo})
    remaining -= mobo['price']
    
    # 3. RAM
    ram = PRODUCTS['ram'][ram_key]
    config.append({'type': 'RAM', **ram})
    remaining -= ram['price']
    
    # 4. GPU
    max_gpu_price_for_budget = 800 if budget < 3000 else float('inf')
    available_gpus = [(k, v) for k, v in PRODUCTS['gpu'].items() if v['price'] <= max_gpu_price_for_budget]
    available_gpus.sort(key=lambda x: x[1]['price'], reverse=True)
    
    gpu = None
    for key, details in available_gpus:
        if remaining >= details['price']:
            gpu = details
            break
    if gpu is None:
        gpu = min((v for v in PRODUCTS['gpu'].values()), key=lambda x: x['price'])
    
    config.append({'type': 'GPU', **gpu})
    remaining -= gpu['price']
    
    # 5. Stockage
    if remaining < 1:
        ssd_key = 'kingston500'
    else:
        ssd_key = 'samsung1tb'
    
    ssd = PRODUCTS['ssd'][ssd_key]
    config.append({'type': 'Stockage', **ssd})
    remaining -= ssd['price']
    
    # 6. Alimentation
    total_tdp = 150 + 220
    if total_tdp > 500 or gpu['price'] > 700:
        psu = PRODUCTS['psu']['rm850']
    elif total_tdp > 400:
        psu = PRODUCTS['psu']['rm750']
    else:
        psu = PRODUCTS['psu']['cv650']
    
    config.append({'type': 'Alimentation', **psu})
    remaining -= psu['price']
    
    # 7. Boîtier
    case = PRODUCTS['case']['default_case']
    config.append({'type': 'Boîtier', **case})
    remaining -= case['price']
    
    total = sum(p['price'] for p in config)
    
    return {
        'config': config,
        'total': total,
        'remaining': remaining
    }

def build_setup(total_budget):
    """Construit un setup complet (80% PC + 20% périphériques)"""
    pc_budget = int(total_budget * 0.8)
    periph_budget = total_budget - pc_budget
    
    pc_result = build_pc(pc_budget)
    
    peripherals = []
    remaining = periph_budget
    
    # Écran
    if remaining >= 649:
        monitor = PRODUCTS['monitor']['asus_oled']
    elif remaining >= 91:
        monitor = PRODUCTS['monitor']['aoc24']
    else:
        monitor = PRODUCTS['monitor']['lg27']
    
    peripherals.append({'type': 'Écran', **monitor})
    remaining -= monitor['price']
    
    # Support écran
    mount = PRODUCTS['mount']['ergotron']
    peripherals.append({'type': 'Support écran', **mount})
    remaining -= mount['price']
    
    # Clavier
    keyboard = PRODUCTS['keyboard']['geeky']
    peripherals.append({'type': 'Clavier', **keyboard})
    remaining -= keyboard['price']
    
    # Souris
    mouse = PRODUCTS['mouse']['redgragon']
    peripherals.append({'type': 'Souris', **mouse})
    remaining -= mouse['price']
    
    # Tapis
    mousepad = PRODUCTS['mousepad']['razer']
    peripherals.append({'type': 'Tapis souris', **mousepad})
    remaining -= mousepad['price']
    
    total_pc = pc_result['total']
    total_periph = sum(p['price'] for p in peripherals)
    
    return {
        'pc': pc_result['config'],
        'pc_budget': pc_budget,
        'pc_total': total_pc,
        'peripherals': peripherals,
        'periph_budget': periph_budget,
        'periph_total': total_periph,
        'grand_total': total_pc + total_periph
    }

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Build Optimizer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e1b4b 0%, #581c87 50%, #1e1b4b 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 40px; }
        .header h1 { font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .form-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .form-group { display: flex; flex-direction: column; }
        label { color: white; margin-bottom: 8px; font-weight: 600; }
        input, select {
            padding: 12px;
            border-radius: 10px;
            border: none;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 16px;
        }
        input::placeholder { color: rgba(255, 255, 255, 0.5); }
        button {
            background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
            width: 100%;
        }
        button:hover { transform: scale(1.05); }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .results { display: none; }
        .results.active { display: block; }
        .summary-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .summary-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .summary-header h2 { color: white; font-size: 2em; }
        .total-price { color: #4ade80; font-size: 2.5em; font-weight: bold; }
        .parts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 15px;
        }
        .part-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 15px;
            padding: 20px;
            transition: all 0.3s;
        }
        .part-card:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }
        .part-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .part-type { color: #c084fc; font-size: 0.9em; font-weight: 600; }
        .part-price { color: #4ade80; font-size: 1.3em; font-weight: bold; }
        .part-name { color: white; font-size: 1.1em; margin-bottom: 10px; }
        .part-link {
            display: inline-block;
            background: #a855f7;
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 0.9em;
            transition: background 0.2s;
        }
        .part-link:hover { background: #9333ea; }
        .section-title {
            color: white;
            font-size: 1.5em;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(167, 139, 250, 0.5);
        }
        .budget-info {
            background: rgba(234, 179, 8, 0.2);
            border: 1px solid rgba(234, 179, 8, 0.5);
            border-radius: 10px;
            padding: 15px;
            color: #fef08a;
            margin-bottom: 20px;
        }
        .loading { display: none; text-align: center; color: white; font-size: 1.2em; margin: 20px 0; }
        .loading.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖥️ PC Build Optimizer</h1>
            <p>Trouvez la configuration parfaite selon votre budget</p>
        </div>
        <div class="form-card">
            <form id="buildForm">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="budget">Budget (€)</label>
                        <input type="number" id="budget" name="budget" placeholder="Ex: 1000" min="400" required>
                    </div>
                    <div class="form-group">
                        <label for="category">Catégorie</label>
                        <select id="category" name="category" required>
                            <option value="pc">PC Uniquement</option>
                            <option value="setup">Setup Complet (PC + Périphériques)</option>
                        </select>
                    </div>
                </div>
                <button type="submit" id="submitBtn">🔍 Trouver ma config idéale</button>
            </form>
        </div>
        <div class="loading" id="loading">⏳ Optimisation en cours...</div>
        <div class="results" id="results"></div>
    </div>
    <script>
        document.getElementById('buildForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const budget = document.getElementById('budget').value;
            const category = document.getElementById('category').value;
            if (budget < 400) { alert('Le budget minimum est de 400€'); return; }
            document.getElementById('loading').classList.add('active');
            document.getElementById('results').classList.remove('active');
            document.getElementById('submitBtn').disabled = true;
            try {
                const response = await fetch('/build', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ budget: parseInt(budget), category })
                });
                const data = await response.json();
                displayResults(data, category);
            } catch (error) {
                alert('Erreur lors de la génération de la configuration');
                console.error(error);
            } finally {
                document.getElementById('loading').classList.remove('active');
                document.getElementById('submitBtn').disabled = false;
            }
        });
        function displayResults(data, category) {
            const resultsDiv = document.getElementById('results');
            if (category === 'pc') {
                resultsDiv.innerHTML = `
                    <div class="summary-card">
                        <div class="summary-header">
                            <h2>💻 Configuration PC</h2>
                            <div class="total-price">${data.total}€</div>
                        </div>
                        <div class="parts-grid">
                            ${data.config.map(part => `
                                <div class="part-card">
                                    <div class="part-header">
                                        <span class="part-type">${part.type}</span>
                                        <span class="part-price">${part.price}€</span>
                                    </div>
                                    <div class="part-name">${part.name}</div>
                                    <a href="${part.url}" target="_blank" class="part-link">🛒 Acheter</a>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            } else {
                resultsDiv.innerHTML = `
                    <div class="summary-card">
                        <div class="summary-header">
                            <h2>🎮 Setup Complet</h2>
                            <div class="total-price">${data.grand_total}€</div>
                        </div>
                        <div class="budget-info">
                            💰 Budget PC: ${data.pc_budget}€ (utilisé: ${data.pc_total}€) |
                            🖱️ Budget Périphériques: ${data.periph_budget}€ (utilisé: ${data.periph_total}€)
                        </div>
                        <h3 class="section-title">💻 Configuration PC (${data.pc_total}€)</h3>
                        <div class="parts-grid">
                            ${data.pc.map(part => `
                                <div class="part-card">
                                    <div class="part-header">
                                        <span class="part-type">${part.type}</span>
                                        <span class="part-price">${part.price}€</span>
                                    </div>
                                    <div class="part-name">${part.name}</div>
                                    <a href="${part.url}" target="_blank" class="part-link">🛒 Acheter</a>
                                </div>
                            `).join('')}
                        </div>
                        <h3 class="section-title">🖱️ Périphériques (${data.periph_total}€)</h3>
                        <div class="parts-grid">
                            ${data.peripherals.map(part => `
                                <div class="part-card">
                                    <div class="part-header">
                                        <span class="part-type">${part.type}</span>
                                        <span class="part-price">${part.price}€</span>
                                    </div>
                                    <div class="part-name">${part.name}</div>
                                    <a href="${part.url}" target="_blank" class="part-link">🛒 Acheter</a>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }
            resultsDiv.classList.add('active');
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/build', methods=['POST'])
def build():
    data = request.json
    budget = data.get('budget')
    category = data.get('category')
    
    if not budget or budget < 400:
        return jsonify({'error': 'Budget minimum de 400€'}), 400
    
    if category == 'pc':
        result = build_pc(budget)
        return jsonify(result)
    else:
        result = build_setup(budget)
        return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
