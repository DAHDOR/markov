import pandas as pd
import numpy as np

def main():
    try:
        data = pd.read_csv('datos.csv')
    except FileNotFoundError:
        print("❌  Error: datos.csv no encontrado.")
        return

    # 1. Entrenamiento por refuerzo (Preparación): Ordenar los datos
    data = data.sort_values(by='dia').reset_index(drop=True)

    # 2. Inicialización del modelo: Identificar estados únicos
    states = sorted(data['estado'].unique())
    num_states = len(states)
    state_to_index = {state: i for i, state in enumerate(states)}

    # Inicializar matriz de conteo
    transition_counts = np.zeros((num_states, num_states))

    # 3. Entrenamiento por refuerzo: Iterar sobre filas consecutivas
    for i in range(len(data) - 1):
        # Comprobar si son días consecutivos
        if data['dia'][i+1] == data['dia'][i] + 1:
            current_state = data['estado'][i]
            next_state = data['estado'][i+1]
            
            current_state_idx = state_to_index[current_state]
            next_state_idx = state_to_index[next_state]
            
            transition_counts[current_state_idx, next_state_idx] += 1

    # 4. Normalización
    # Evitar la división por cero para estados sin transiciones de salida
    row_sums = transition_counts.sum(axis=1, keepdims=True)
    # Reemplazar los 0 con 1 en el denominador para evitar la división por cero.
    # El resultado de la división será 0 donde la suma era 0.
    transition_matrix = np.divide(transition_counts, row_sums, out=np.zeros_like(transition_counts, dtype=float), where=row_sums!=0)

    # 5. Salida
    print("Matriz de Transición:")
    transition_df = pd.DataFrame(transition_matrix, index=states, columns=states)
    print(transition_df.to_string(float_format="%.2f"))

    # 6. Modo Interactivo

    # Emojis para los estados
    state_emojis = {
        "lluvia": "🌧️",
        "sol": "☀️",
        "nublado": "☁️",
    }
    
    print("\n--- 🔮  Modo Interactivo 🔮  ---")
    print("Introduce un estado para ver las probabilidades del día siguiente.")
    print("Escribe 'exit' para salir.")

    while True:
        try:
            current_state_input = input("\n🌦️   Introduce el estado actual: ").strip()
        except EOFError:
            print("\n👋  Saliendo del modo interactivo.")
            break

        if current_state_input.lower() in ['exit']:
            print("\n👋  Saliendo del modo interactivo.")
            break

        if current_state_input not in states:
            print(f"❌  Error: Estado '{current_state_input}' no reconocido. Estados válidos: {', '.join(states)}")
            continue

        # Calcular y mostrar la distribución de probabilidad
        current_state_idx = state_to_index[current_state_input]
        next_day_probs = transition_matrix[current_state_idx]

        print("\n📊  Probabilidades del siguiente día:")
        for i, state in enumerate(states):
            emoji = state_emojis.get(state, "")
            print(f"  - {emoji}  {state.capitalize()}: {next_day_probs[i]:.2f}")


if __name__ == "__main__":
    main()
