<<<<<<< HEAD
## How to Run

### 🐳 Docker (Recommended)

```bash
# Build container (first time)
docker buildx build --platform=linux/amd64 -t digital-twin-ospf .

# Run container
docker run -it --platform=linux/amd64 digital-twin-ospf

# Inside container:
cd /app/simulator
python3 simulate_network.py
=======
## How to Run

### 🐳 Docker (Recommended)

```bash
# Build container (first time)
docker buildx build --platform=linux/amd64 -t digital-twin-ospf .

# Run container
docker run -it --platform=linux/amd64 digital-twin-ospf

# Inside container:
cd /app/simulator
python3 simulate_network.py
>>>>>>> 5e118deefcbde0297550a26e6986c495cfe06bfa
