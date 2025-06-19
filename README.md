# 🧠 AccessAI

**AccessAI** is a prototype that uses AI to assess the accessibility of public transport stops.  
Users can upload a photo, answer a few short questions, and receive a combined analysis based on both their input and the AI's prediction.

## ✨ Features

- 🚉 Upload station photos (JPG or PNG)
- 🤖 Automatic analysis using an AI model
- ❓ Short questions about accessibility
- 📊 Results combining AI and user input
- 🔍 Search with autocomplete suggestions
- 🗃️ SQLite database storage

## 🛠️ Tech Stack

- Python 3 / Flask
- HTML / Bootstrap 5
- SQLite
- Optional: AI model via `ai_model.py`

## 🚀 Quickstart (local)

```bash
git clone https://github.com/ZehJulianLp/accessai.git
cd accessai
pip install -r requirements.txt
python app.py
```

Then open in your browser:  
👉 `http://localhost:5050`

## 📦 Deployment

For deployment on [Render](https://render.com):
- Ensure `start.sh` exists and is executable
- Use the following Start Command in Render:

```bash
./start.sh
```

- The SQLite database and `static/uploads` will be used automatically

## 📄 License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.

---

*Built with ❤️ by Julian ([@ZehJulianLp](https://github.com/ZehJulianLp))*
