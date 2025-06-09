# GEE Navigation System – Visualized

This project demonstrates how the World War II-era **GEE hyperbolic navigation system** works, using two Python scripts:
- `animation.py` – animated signal propagation and triangulation
- `static.py` – static visualization showing GEE range circles

---

## 🛰 What is GEE?

GEE was a **hyperbolic radio navigation system** used by the Royal Air Force during World War II. It allowed aircraft to determine their location by comparing the **time delays between pulses** received from synchronized ground-based radio transmitters.

Unlike systems requiring precise clocks on the aircraft, GEE relied on **differential time measurements** from pulse pairs. It allowed for reasonably accurate positioning even under wartime conditions with limited instrumentation.

---

## 🧠 How GEE Works

1. A **Master Station** emits a radio pulse at a fixed interval.
2. **Slave Stations** wait to receive the master’s pulse and then transmit their own pulse **after a small delay** (e.g., 0.1 ms).
3. An aircraft receives the master pulse and the delayed slave pulses.
4. By measuring the **difference in arrival times**, the aircraft determines:
   - The **distance to each station**.
   - The **difference in distance between stations**, which defines a **hyperbola of possible positions**.
5. With two slave stations, the aircraft determines **two hyperbolas**.
6. The **intersection** of those hyperbolas gives the aircraft's position.

---

## 💻 Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/gee-nav-visualized.git
cd gee-nav-visualized
````

### 2. Set up a Python virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

* **Windows (PowerShell):**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

  If you get a security error, run:

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

* **macOS/Linux:**

  ```bash
  source .venv/bin/activate
  ```

### 4. Install dependencies

```bash
pip install matplotlib numpy
```

---

## 📽 Usage

### `animation.py` – Dynamic Visualization

```bash
python animation.py
```

* Randomly places 3 stations and an aircraft.
* Simulates real-time pulse emission, propagation, and reception.
* Shows:

  * Expanding master/slave signals
  * Aircraft-calculated distance circles
  * Triangulation rings from each station
  * Time difference labels

### `static.py` – Static Snapshot

```bash
python static.py
```

* Displays a frozen version of the above simulation.
* Ideal for printed teaching materials or step-by-step analysis.

---

## 🧮 Manual GEE Calculations (Simplified)

If you want to simulate GEE calculations by hand using this visual output:

1. **Measure the time difference** between pulses (from oscilloscope or simulated data).
2. Convert time difference to **distance**:

   ```
   Distance = Time × Speed of Radio Waves
            = Time (ms) × 300 km/ms
   ```
3. For each station:

   * Draw a circle with radius = distance from station to aircraft.
   * If comparing master to slave stations:

     * The **difference in distances** gives a **hyperbolic line of position**.
4. The intersection of two hyperbolas = aircraft location.

Example:

* Master pulse received at 0.70 ms → 0.70 × 300 = 210 km
* Slave A pulse received at 1.23 ms (sent at 0.85 ms) → 0.38 ms delay → 114 km distance
* Aircraft is 210 km from Master, 114 km from Slave A → lies at the intersection of those two ranges

---

## 📦 Files

| File           | Purpose                                     |
| -------------- | ------------------------------------------- |
| `animation.py` | Animated simulation of GEE in real-time     |
| `static.py`    | Static visual snapshot of GEE triangulation |
| `README.md`    | You're reading it!                          |

---

## 🧩 Future Enhancements (optional ideas)

* Draw **true hyperbolic lines of position**
* Add **oscilloscope waveform simulation**
* Export visuals to image/PDF
* Add a **CLI tool** to input manual Δt values

---

## 📜 License

MIT License. Free for educational and research use.

```

---
