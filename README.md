# 🍌 Banana Launcher 🍌

**A Free, Open-Source Minecraft Non-Premium Launcher Built Entirely in Python**

![License](https://img.shields.io/badge/License-Open%20Source-brightgreen)
![Language](https://img.shields.io/badge/Language-Python-blue)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

---

## 📌 Overview

**Banana Launcher** is a lightweight, feature-rich Minecraft launcher designed for players who want to play Minecraft without premium authentication. Built completely in Python with a modern GUI, it offers an intuitive and fun gaming experience with additional features like music controls and an animated interface.

Whether you're a casual player or a developer, Banana Launcher provides everything you need to download and launch multiple Minecraft versions effortlessly.

---

## ⭐ Features

✨ **Easy Version Management**
- Automatically download Minecraft versions from 1.16.5 to 1.20.1
- One-click version selection and installation
- Automatic file management and caching

🎵 **Built-in Music Player**
- Play your favorite bananas-themed playlist
- Support for multiple audio files
- Volume control and play/pause buttons

🎨 **Modern GUI Interface**
- Animated breathing logo (top center)
- Clean, dark-themed Tkinter interface
- Real-time console logging
- Responsive and smooth animations

👤 **Simple Username Authentication**
- Offline username-based authentication
- Local storage of player credentials
- One-click logout

🌙 **Offline Mode Support**
- Play offline without internet authentication
- Perfect for single-player adventures

📋 **Console Logging**
- Real-time installation and launch logs
- Copy and view detailed error messages
- Full traceback support for debugging

🍌 **Banana-Themed Design**
- Fun, banana-inspired UI elements
- Animated logo with breathing effect
- Playful color scheme (#FFD400 yellow theme)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11 or higher**
- **Windows, macOS, or Linux**
- Internet connection (for downloading Minecraft versions)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/BananaLauncher.git
   cd BananaLauncher
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or manually install required packages:
   ```bash
   pip install pygame pillow minecraft-launcher-lib msal
   ```

3. **Run the Launcher**
   ```bash
   python BananaLauncher.py
   ```

---

## 📖 Usage

### Step 1: Set Your Username
Click the **Login** button (bottom left) and enter your Minecraft username.

### Step 2: Select Version
Choose your desired Minecraft version (1.16.5 to 1.20.1) from the dropdown menu.

### Step 3: Launch Minecraft
Click the **PLAY** button and the launcher will:
- Automatically download the selected version (if not already cached)
- Install all required files
- Launch Minecraft with your username

### Step 4: Enjoy!
Play Minecraft offline with your custom username!

### Music Player
- Click ▶ to play background music
- Use ⏸ to pause and ⏭ to skip to the next track
- Adjust volume with the slider

---

## 📁 Project Structure

```
BananaLauncher/
├── BananaLauncher.py          # Main launcher application
├── banana_launcher_logo.png    # Logo image (custom banana logo)
├── join.png                    # Optional play button image
├── banany.mp3                  # Soundtrack files
├── banany2.mp3
├── banany3.mp3
├── minecraft/                  # Auto-created: Minecraft installations
├── auth_cache.json             # Local: Stored username data
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

---

## 🛠️ Customization

### Add Your Own Music
1. Place MP3 files in the launcher directory
2. Modify the `PLAYLIST` variable in `BananaLauncher.py`:
   ```python
   PLAYLIST = [
       ("your_song.mp3", "Song Title"),
       ("another_song.mp3", "Another Title"),
   ]
   ```

### Change the Logo
Replace `banana_launcher_logo.png` with your own image file (same name).

### Custom Play Button
Add a `join.png` image (100x100 pixels) to replace the text PLAY button.

### Modify Colors
Edit the color codes in `BananaLauncher.py`:
- Main color: `#FFD400` (banana yellow)
- Background: `#0f0f0f` (dark black)
- Accent: `#90EE90` (light green)

---

## 🔧 Dependencies

- **tkinter** — GUI framework (built-in with Python)
- **pygame** — Audio playback and music control
- **pillow (PIL)** — Image processing and animation
- **minecraft-launcher-lib** — Minecraft version management and launching
- **msal** — Microsoft authentication (optional, for future updates)

Install all dependencies:
```bash
pip install pygame pillow minecraft-launcher-lib msal
```

---

## 📋 Supported Minecraft Versions

The launcher currently supports the following Minecraft Java Edition versions:

- **1.20.1** ✅
- **1.20** ✅
- **1.19.2** ✅
- **1.18.2** ✅
- **1.17.1** ✅
- **1.16.5** ✅

Additional versions can be easily added by modifying the `versions` list in the code.

---

## 🔐 Offline Mode & Authentication

This launcher operates in **offline mode**, meaning:
- No premium Minecraft account required
- Username-based authentication
- Credentials stored locally (safe and private)
- No internet connection needed after version download

⚠️ **Note**: Online multiplayer servers may not accept offline mode players. Use single-player worlds or private servers.

---

## 🐛 Troubleshooting

### "Minecraft not launching"
- Check the console window for error messages
- Ensure Java is installed and in your PATH
- Try downloading the version again

### "Song not found"
- Place MP3 files in the launcher directory
- Ensure filenames match exactly in the PLAYLIST

### "Permission denied" (macOS/Linux)
```bash
chmod +x BananaLauncher.py
```

### Launcher freezes during download
- Check your internet connection
- Large versions may take several minutes
- Monitor the console for progress

---

## 🎮 How It Works

1. **Version Management**: Uses `minecraft-launcher-lib` to manage Minecraft installations
2. **Downloading**: Automatically fetches game files from official Mojang servers
3. **Launching**: Generates launch commands with proper Java parameters
4. **Authentication**: Offline username-based system (no premium account needed)
5. **Music**: Pygame mixer for audio playback

---

## 🚀 Future Updates

This project is **actively maintained** and planned improvements include:

- ✨ Microsoft account integration (premium mode)
- ✨ Fabric/Forge mod loader support
- ✨ Custom theme and color selection
- ✨ Launch options customization (RAM allocation, etc.)
- ✨ More Minecraft versions support
- ✨ Settings/configuration UI
- ✨ Profile management (multiple players)
- ✨ Built-in mod browser
- ✨ Server browser integration
- ✨ Crash report analyzer

**Stay tuned for updates!** 🍌

---

## 📄 License

This project is **100% Open Source** and free to use, modify, and distribute.

Feel free to:
- ✅ Fork the repository
- ✅ Create pull requests
- ✅ Report issues and suggest features
- ✅ Modify and customize for your needs
- ✅ Use for personal or educational purposes

---

## ⭐ Support This Project

If you love Banana Launcher, please help us grow:

### 🌟 **Star this repository** — It means a lot!
### 🍴 **Fork and contribute** — Submit pull requests
### 🐛 **Report bugs** — Help us improve
### 💬 **Share feedback** — Tell us what you think

---

## 🤝 Contributing

We welcome contributions from the community!

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

---

## 📞 Support & Contact

- **Issues & Bugs**: Open an issue on GitHub
- **Feature Requests**: Suggest ideas in the discussions section
- **Questions**: Check existing issues first

---

## 🎮 Screenshots

*Banana Launcher in action:*

- Animated breathing logo at the top
- Music player with volume control (top right)
- Username login panel (bottom left)
- Version selector and PLAY button (bottom center)
- Real-time console logs
- Dark theme with banana-yellow accents

---

## 🍌 Fun Fact

Why "Banana Launcher"? Because launching Minecraft should be as fun and delightful as a bunch of bananas! 🍌

---

## 📝 Changelog

### Version 1.0 (Current)
- ✅ Full Minecraft launcher implementation
- ✅ Offline username authentication
- ✅ Automatic version downloading (1.16.5 - 1.20.1)
- ✅ Music player integration
- ✅ Real-time console logging
- ✅ Animated GUI with breathing logo
- ✅ Volume control and playlist support

---

## 🏆 Credits

Built with ❤️ using:
- **Python** — Core language
- **Tkinter** — GUI framework
- **Pygame** — Audio engine
- **minecraft-launcher-lib** — Game management
- **Pillow** — Image processing

---

## ⚖️ Disclaimer

This is an **unofficial** Minecraft launcher. It is not affiliated with, endorsed by, or associated with Mojang Studios or Microsoft Corporation. Minecraft is a trademark of Microsoft Corporation.

This launcher is provided as-is for educational and personal use. Use at your own risk.

---

## 🌟 Let's Connect

**Have you installed Banana Launcher?** 
- ⭐ Star the repo
- 🍴 Fork it
- 📢 Share it with friends
- 💬 Give feedback

---

**Happy Mining! 🍌⛏️**

*Made with passion by the Banana Launcher community (so Lajmonek x chatgpt ❤)*
