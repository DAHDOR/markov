import csv
import random

def gen_data(n_days: int, probs: dict):
    estados = list(probs.keys())
    weights   = list(probs.values())
    with open('datos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['dia', 'estado'])
        for dia in range(1, n_days + 1):
            estado = random.choices(estados, weights=weights, k=1)[0]
            writer.writerow([dia, estado])
            
if __name__ == '__main__':
    initial_probs = {'sol': 0.5, 'nublado': 0.3, 'lluvia': 0.2}
    gen_data(n_days=100, probs=initial_probs)
