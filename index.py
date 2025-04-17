import serial
from pyubx2 import UBXReader, UBXMessage

PORT = "/dev/ttyUSB0"
BAUDRATE = 38400

def render_cno_bar(cno):
    max_cno = 60
    bar = '█' * int((cno / max_cno) * 40)
    return f"{bar} {cno:.1f} dB-Hz"

def main():
    with serial.Serial(PORT, BAUDRATE, timeout=1) as stream:
        ubr = UBXReader(stream, protfilter=2)  # UBX only
        print("Listening for UBX-NAV-SAT messages...")
        for raw, parsed in ubr:
            if isinstance(parsed, UBXMessage) and parsed.identity == "NAV-SAT":
                print("\033c", end="")  # Clear terminal
                num_svs = parsed.numSvs
                for i in range(num_svs):
                    svid = getattr(parsed, f"svId_{i+1:02d}")
                    cno = getattr(parsed, f"cno_{i+1:02d}")

                    print(f"SV {svid:02d} {render_cno_bar(cno)}")

if __name__ == "__main__":
    main()

