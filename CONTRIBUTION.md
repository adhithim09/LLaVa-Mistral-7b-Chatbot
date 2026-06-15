# 🤝 Contributing to Converso (LLaVA · Mistral 7B Chatbot)

Thanks for your interest in contributing! 🚀
This project welcomes beginners and experienced developers alike.

---

## 📌 How to Contribute

### 1. Fork the Repository

Click the **Fork** button on the top right of the repo.

---

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/LLaVa-Mistral-7b-Chatbot.git
cd LLaVa-Mistral-7b-Chatbot
```

---

### 3. Create a Branch

Use descriptive branch prefixes to categorize your contributions:
* `feat/` for new features
* `fix/` for bug fixes
* `docs/` for documentation improvements
* `ci/` for CI/CD pipeline modifications
* `refactor/` for code refactoring

```bash
git checkout -b feat/your-feature-name
```

---

### 4. Set Up the Project

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

---

### 5. Make Your Changes

* **Fix bugs** 🐛: Identify and fix bugs. Ensure unit tests are added or updated.
* **Improve UI** 🎨: Streamlit UI improvements should follow responsive design and high aesthetic standards.
* **Add features** ✨: Keep functions modular, documented, and properly tested.
* **Update docs** 📄: Keep guides clear and update API references.

---

### 6. Code Style & Linting

We enforce clean, standard Python style guides:
* Code formatting: run `black .`
* Linting check: run `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
* Avoid committing hardcoded paths, API secrets, or credentials.

---

### 7. Test Your Changes

Ensure all tests pass before making a commit:
```bash
pytest
```
To run the Streamlit interface locally:
```bash
streamlit run app.py
```

---

### 8. Commit Your Changes

We follow **Conventional Commits**:
* `feat:` a new feature
* `fix:` a bug fix
* `docs:` documentation only changes
* `style:` changes that do not affect the meaning of the code (white-space, formatting, etc)
* `refactor:` a code change that neither fixes a bug nor adds a feature
* `perf:` a code change that improves performance
* `test:` adding missing tests or correcting existing tests
* `ci:` changes to our CI configuration files and scripts

```bash
git add .
git commit -m "feat: added XYZ feature"
```

---

### 9. Push to Your Fork

```bash
git push origin feat/your-feature-name
```

---

### 10. Create a Pull Request

* Go to your fork on GitHub.
* Click **Compare & Pull Request**.
* Fill out the PR template completely (reference related issue, list changes, describe testing).
* Add screenshots or screen recordings for any UI changes.

---

## ✅ Contribution Guidelines

* Follow clean code practices.
* Keep commits meaningful and focused.
* Do not include unrelated changes in a single branch.
* Add docstrings and comments where appropriate.

---

## 🏁 You're Done!

Once your PR is reviewed and merged, you’re officially a contributor 🎉