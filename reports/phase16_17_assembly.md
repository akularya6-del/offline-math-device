# Phase 16 & 17: Home Assembly & Vibration Output

## Vibration Motor Specs
- **Motor:** 10mm x 2.7mm ERM (Eccentric Rotating Mass) Coin Motor.
- **Power:** 3.0V at 60mA (180mW).
- **Driver:** Since the SG2002 GPIO cannot source 60mA, a single N-channel MOSFET (e.g., 2N7002 or AO3400) is required, along with a flyback diode (1N4148) to protect the GPIO from inductive spikes.
- **Mapping:** 
  - Option A: 1 short pulse (150ms)
  - Option B: 2 short pulses
  - Option C: 3 short pulses
  - Option D: 4 short pulses
  - FAIL / Low Conf: 1 long pulse (800ms)

## Home Assembly Procedure
Designed for average home soldering experience. No BGA or microscopic rework required.

1. **Carrier PCB (Custom)**: Order a standard 2-layer FR4 PCB (1.0mm thickness).
2. **Surface Mount Components**: 
   - Solder the TP4056/MT3608 ICs, MOSFET, and passives. (MODERATE - Can be done with a soldering iron or cheap hot plate).
3. **Solder the LicheeRV Nano-B**:
   - The Nano-B is a castellated module (half-holes on the edge).
   - Place on carrier PCB. Solder the edge pins with a fine-tip soldering iron. (MODERATE).
4. **Connect Camera**:
   - The Nano-B has an FPC connector for the MIPI CSI camera. Simply insert the ribbon cable and clamp it. (EASY).
5. **Connect Battery & Motor**:
   - Solder wires to the through-hole pads for the battery and coin motor. (EASY).
