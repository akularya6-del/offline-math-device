def calculate_stackup():
    print("--- Z-AXIS (HEIGHT) STACKUP ---")
    
    # 1. Enclosure Top Wall
    t_top = 1.0
    print(f"Top Enclosure: {t_top} mm")
    
    # 2. Camera / Lens Protrusion
    # The OV5647 module has a lens that protrudes.
    # The sensor + lens assembly is typically ~5.5mm thick.
    # It will sit next to the compute module, OR if it's placed on top, it adds height.
    # Let's assume it sits side-by-side with the battery/Nano-B if footprint allows, 
    # OR we need a cutout in the enclosure for the lens.
    # Assuming side-by-side layout:
    # Nano-B + Carrier PCB + Battery stack vs Camera stack.
    
    # Let's calculate the main compute stack:
    # A. Nano-B is castellated. It solders FLUSH to the carrier PCB.
    # But it has components on its TOP side.
    # PCB thickness: 1.2mm. Top components (SoC, inductor): ~2.2mm.
    # Bottom components: There are some small passives on the bottom of Nano-B! ~0.5mm.
    # So Nano-B is not perfectly flat on the bottom unless the carrier PCB has a cutout.
    # Let's assume standard surface mount: Nano-B rests on its bottom components.
    
    h_nano_b_pcb = 1.2
    h_nano_b_top_comp = 2.2
    h_nano_b_bot_comp = 0.5
    h_nano_b_total = h_nano_b_pcb + h_nano_b_top_comp + h_nano_b_bot_comp # 3.9mm
    
    # B. Carrier PCB
    h_carrier_pcb = 1.0 # Thin FR4
    
    # C. Battery (250mAh)
    # A 250mAh LiPo (e.g., 402030 size: 4.0mm thick, 20mm wide, 30mm long)
    h_battery = 4.0
    h_battery_swell_allowance = 0.5 # Safety margin for LiPo swell
    
    # D. Enclosure Bottom Wall
    t_bot = 1.0
    
    # Let's stack them:
    # Enclosure Top (1.0)
    # Clearance (0.5)
    # Nano-B Top Components (2.2)
    # Nano-B PCB (1.2)
    # Nano-B Bot Components (0.5)
    # Solder paste/gap (0.1)
    # Carrier PCB (1.0)
    # Tape/Adhesive (0.2)
    # Battery (4.0)
    # Battery Swell Gap (0.5)
    # Enclosure Bottom (1.0)
    
    stack = [
        ("Top Wall", 1.0),
        ("Air Gap / Clearance", 0.3),
        ("Nano-B Top Comps", 2.2),
        ("Nano-B PCB", 1.2),
        ("Nano-B Bot Comps", 0.5),
        ("Carrier PCB", 1.0),
        ("VHB Tape", 0.2),
        ("Battery (250mAh)", 4.0),
        ("Battery Swell Gap", 0.5),
        ("Bottom Wall", 1.0)
    ]
    
    total_z = sum(v for n, v in stack)
    for n, v in stack:
        print(f"{n:20}: {v:.1f} mm")
        
    print("-" * 30)
    print(f"TOTAL THICKNESS: {total_z:.1f} mm")
    print(f"Target: 10.0 mm -> Exceeds by {total_z - 10.0:.1f} mm")
    
    print("\n--- X/Y AXIS (FOOTPRINT) ---")
    # Nano-B footprint: 35.56 x 22.86 mm
    # If we put the camera NEXT to it in the Y axis (width), it takes 35.56 x (22.86 + 10mm camera) = 35.56 x 32.86. Exceeds 25mm.
    # If we put camera NEXT to it in the X axis (length), it takes (35.56 + 10mm camera) x 22.86 = 45.56 x 22.86. Exceeds 40mm.
    
    # Wait! The camera MUST be placed either:
    # 1. On TOP of the Nano-B (adds 5mm to Z axis -> 16.9mm total thickness)
    # 2. Next to the Nano-B (adds to X or Y footprint).
    
    # Let's evaluate placing a tiny camera (e.g. GC2083 bare module, 8x8mm) next to the Nano-B.
    # Length = Nano-B (35.56) + Camera (8.0) + clearance (1.0) = 44.56 mm.
    # Exceeds the 40mm length target.
    
    print("Can we fit inside 40x25mm?")
    print("Nano-B length alone is 35.56mm. That leaves 40 - 35.56 = 4.44mm for the camera.")
    print("A standard bare camera module is 8mm x 8mm.")
    print("Therefore, placing the camera beside the Nano-B in the X-axis requires 35.56 + 8.0 = 43.56mm.")
    print("Placing it beside in the Y-axis requires 22.86 + 8.0 = 30.86mm.")
    
    print("\nCONCLUSION: A 40x25mm footprint is IMPOSSIBLE with the LicheeRV Nano-B unless the camera is stacked ON TOP of the board, which makes the thickness ~17mm.")
    
    print("\nMinimum physically valid dimensions (Side-by-side camera):")
    print("Length: 44.56 mm (Nano-B + Camera) + 2mm (walls) = 46.56 mm")
    print("Width: 22.86 mm (Nano-B) + 2mm (walls) = 24.86 mm")
    print(f"Height: {total_z} mm")
    print("Result: ~47 x 25 x 12 mm")

if __name__ == "__main__":
    calculate_stackup()
