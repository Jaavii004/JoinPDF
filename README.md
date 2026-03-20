# 🛡️ JoinPDF v2.5.1 — Premium PDF Merger for Windows

JoinPDF is a high-performance, professional-grade utility designed to merge PDF files directly from the Windows context menu. It combines enterprise-level stability with a stunning, minimalist user interface.

![JoinPDF Banner](frontend/index.html) <!-- Link to the landing page as a reference -->

## 💎 Key Features
- **⚡ 1-Click Context Menu**: Merge PDFs instantly without opening any application.
- **🛡️ Master Shield Technology v2.5**: Exclusive synchronization engine that prevents race conditions and ghost windows.
- **🚀 Ultra-Fast Engine**: Powered by optimized PyPDF, merging large batches in under 2 seconds.
- **🔒 Privacy First**: 100% offline. Your data stays on your local machine. No cloud, no risk.
- **🎨 Premium UI**: Modern, dark-mode-ready interface built with CustomTkinter.

## 🚀 Installation
1. Download the latest installer: [Instalar_JoinPDF.exe](Instalar_JoinPDF.exe)
2. Run the `.exe` and follow the instructions.
3. Select 2+ PDF files, right-click, and select **⚡ Join PDF**.

## 🛠️ Technology Stack
- **Backend**: Python 3.12 + PyPDF
- **Frontend**: CustomTkinter (Python) / HTML5 + CSS3 (Landing Page)
- **Installer**: Inno Setup 6
- **Architecture**: Multi-process synchronization with PID-based lock management.

## 🧠 How it Works: Master Shield Tech
The "Master Shield" technology ensures that even if you right-click and trigger "Join PDF" multiple times in quick succession (or for many files), the application coordinates itself:
1. **Lock Mechanism**: A global lock file is created in the temp directory.
2. **PID Validation**: The system checks if the PID in the lock file belongs to an active process.
3. **Queue Management**: Subsequent instances (slaves) pass their file paths to the first instance (master) and terminate immediately, preventing UI clutter.
4. **Cleanup**: The master instance safely removes the lock file upon completion.

## 🤝 Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ by [Jaavii004](https://github.com/Jaavii004)
