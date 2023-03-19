from rtlsdr import RtlSdr
import time
import datetime
import keyboard
import re

def print_info(frequency, min_amplitude):
    print(f"\nListening: {frequency:.2f} MHz with minimum amplitude: {min_amplitude:.2f}\n")

def print_change(now, times, samples):
    print(f"\n| {now} | Change(s) detected {times} times.\t| Amplitude: {round(max(abs(samples)), 5)}\t|")

def print_banner():
    print("\n#################################################\n#      Welcome to Python LTR SDR detector!      #\n#################################################")

def get_frequency():
    while True:
        frequency = re.sub(r"[^\d\.]", "", input("\nSelect frequency: XXX.XX (MHz)\n").strip())
        try:
            frequency = float(frequency)
            return frequency
        except ValueError:
            print("Invalid input. Please enter a valid frequency in MHz.")

def get_amplitude():
    while True:
        min_amplitude = re.sub(r"[^\d\.]", "", input("\nSelect amplitude: ").strip())
        try:
            min_amplitude = float(min_amplitude)
            return min_amplitude
        except ValueError:
            print("Invalid input. Please enter a valid amplitude.")

def main():
    sdr = RtlSdr()
    min_amplitude = 0.1
    print_banner()
    while True:
        frequency = get_frequency()
        sdr.sample_rate = 2.4e6
        sdr.center_freq = frequency * 10**6
        sdr.gain = "auto"
        times = 0
        cooldown = 0.3
        last_detection = 0

        print_info(frequency, min_amplitude)
        print("\nPress left arrow if you want to change frequency. Press right arrow if you want to change minimum amplitude.")

        while True:
            if keyboard.is_pressed("left"):
                break
            if keyboard.is_pressed("right"):
                min_amplitude = get_amplitude()
                print_info(frequency, min_amplitude)

            samples = sdr.read_samples(256 * 1024)
            if any(abs(samples) > min_amplitude):
                current_time = time.time()
                now = datetime.datetime.now().strftime("%Y/%m/%d | %H:%M:%S")

                if current_time - last_detection > cooldown:
                    times += 1
                    last_detection = current_time
                    print_change(now, times, samples)

if __name__ == "__main__":
    main()
