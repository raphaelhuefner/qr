# QR Code Scanner & Generator

Most smartphones come with built-in QR code scanning and generation capabilities (for WiFi access and more), but laptops typically lack native QR code tools out of the box. This project bridges that gap by providing a simple, web-based interface to scan and generate QR codes on your computer, without the QR codes or the data within leaving your machine, everything stays local. The seemingly contradicting choice of a web UI came to be because browsers offer a simple way of accessing the built-in camera.

## Features

- **Scan QR codes** using your device's camera
- **Generate QR codes** from text or URLs
- **Web-based** – works in any modern browser
- **Lightweight** – serves static files with minimal dependencies

## Getting Started

### Prerequisites

- Python 3.7+
- A modern web browser

### Online Demo

A live preview is available at **https://raphaelhuefner.github.io/qr/**

This demonstrates how the application works when served locally. Since all processing happens in your browser and data never leaves your machine, you can safely use the GitHub Pages version for non-sensitive QR code scanning and generation. For sensitive data, we recommend running the project locally using the instructions below.

### Running the Project Locally

Simply run the startup script:

```bash
./run.sh
```

This will start a local HTTP server and open the application in your default browser at `http://127.0.0.1:8080/`.

Press `Enter` in the terminal to stop the server.

## Customization

You can customize the server by modifying `run.sh` or running `serve.py` directly with command-line arguments:

```bash
python3 serve.py --port 9000 --bind 0.0.0.0 --directory docs
```

Available options:
- `--port PORT` – port to bind to (default: 8080)
- `--bind ADDR` – address to bind to (default: 127.0.0.1)
- `--directory DIR` – directory to serve (default: docs)

## Project Structure

- `run.sh` – startup script
- `serve.py` – Python HTTP server with background thread support
- `build.sh` – script to download and prepare vendor dependencies on third-party libraries
- `docs/` – web assets (HTML, CSS, JavaScript, minified libraries)

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

This project includes third-party libraries:
- [Spectre CSS](https://picturepan2.github.io/spectre/) – CSS framework (MIT License)
- [html5-qrcode](https://github.com/mebjas/html5-qrcode) – QR code scanning (Apache-2.0 License)
- [QRCode.js](https://github.com/davidshimjs/qrcodejs) – QR code generation (MIT License)
