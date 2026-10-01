import math

def calculate_power():
    # SG2002 TRM / Measurements
    # https://milkv.io/docs/duo/getting-started/duo256m#power-consumption
    # "Booting: 90mA avg, Idle: 62mA avg" (at 5V input to the board, but typical LDO/Buck drops it to 3.3V/1.8V/0.9V)
    # Let's use 5V input current for the whole board to be safe.
    # So Idle = 5V * 62mA = 310 mW (This is higher than previous 229 mW estimate which assumed 3.7V)
    
    # Active CPU + RAM + NPU: ~200mA at 5V = 1000 mW
    
    # Camera OV5647
    # Active: 90mW (from datasheet)
    
    # Vibration Motor (10mm ERM)
    # Active: 60mA at 3.0V = 180 mW
    
    # Let's run scenarios based on a 3.7V LiPo battery.
    # The battery goes through an MT3608 Boost converter to 5V.
    # MT3608 Efficiency at ~200mA load from 3.7V to 5V is ~85%.
    
    boost_efficiency = 0.85
    
    p_idle_5v = 310 # mW
    p_active_5v = 1000 + 90 # mW (Board + Camera)
    p_vibrate_5v = 180 # mW (assuming run from a 3V LDO powered by 5V, or directly from 3.7V. If from 3.7V, it bypasses boost. Let's assume it bypasses boost for efficiency: 180mW from 3.7V)
    
    # Calculate battery draw
    p_idle_bat = p_idle_5v / boost_efficiency
    p_active_bat = p_active_5v / boost_efficiency
    p_vibrate_bat = 180 # direct from battery
    
    print(f"Idle Battery Power: {p_idle_bat:.1f} mW")
    print(f"Active Battery Power: {p_active_bat:.1f} mW")
    print(f"Vibrate Battery Power: {p_vibrate_bat:.1f} mW")
    
    # Duty cycle
    t_active = 5.0 # seconds (capture + OCR + solve)
    t_vibrate = 1.0 # seconds (output)
    t_idle = 24.0 # seconds
    t_cycle = t_active + t_vibrate + t_idle
    
    energy_per_cycle_mJ = (p_active_bat * t_active) + (p_idle_bat * t_vibrate) + (p_vibrate_bat * t_vibrate) + (p_idle_bat * t_idle)
    avg_power_bat = energy_per_cycle_mJ / t_cycle
    
    print(f"Average Power (1 question / 30s): {avg_power_bat:.1f} mW")
    
    # Battery runtime
    capacities = [100, 150, 200, 250]
    derating = 0.80 # usable capacity before voltage drops below boost converter min (usually ~3.0V)
    
    print("\nRuntime Estimates:")
    for cap in capacities:
        energy_mWh = cap * 3.7 * derating
        runtime_h = energy_mWh / avg_power_bat
        print(f"{cap} mAh -> {runtime_h:.2f} hours")

if __name__ == "__main__":
    calculate_power()
