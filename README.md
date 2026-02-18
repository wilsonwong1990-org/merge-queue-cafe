# ☕ Merge Queue Café

A demo repository for showcasing [GitHub Pull Request Merge Queues](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).

## The Problem This Demonstrates

Imagine 18 developers all working on the same café menu app. Each one opens a PR,
each PR passes CI on its own — **but merging them together breaks the build.**

This is called a **semantic conflict**: changes that are individually correct but
collectively incompatible. Merge queues solve this by testing PRs *in combination*
before they reach `main`.

## Prerequisites

- Python 3.12+
- [GitHub CLI](https://cli.github.com/) (`gh`), authenticated with push access to this repo

## Quick Start

```bash
# Clone the repo
git clone https://github.com/SAML-test/merge-queue-cafe.git
cd merge-queue-cafe

# Install dependencies
pip install -r requirements.txt

# Run the app locally (optional)
python app.py

# Run the test suite
pytest tests/ -v
```

---

## 🎬 Running the Demo

### Part 1: The Problem (without merge queue)

Show what happens when PRs are merged without a queue:

1. **Disable the merge queue** — Go to **Settings → Rules → Rulesets → "Merge Queue"**
   and set enforcement to **Disabled**
2. **Merge drink PRs one at a time** (#1 through #3)
   - Each PR passes CI individually ✅
   - After the 3rd merges, `main` has **5 menu items** — exceeding `MAX_MENU_SIZE = 4`
   - The 4th drink PR's CI now **fails** when rebased on `main` ❌
3. **Talking point:** _"Each developer did their job correctly. Each PR passed CI.
   But the combination broke the build. This is the semantic conflict problem."_

### Part 2: The Solution (with merge queue)

1. **Reset the repo** (see [Resetting for a Fresh Demo](#-resetting-for-a-fresh-demo) below)
2. **Re-enable the merge queue** — Set the "Merge Queue" ruleset enforcement back to **Active**
3. Open the [PR list](https://github.com/SAML-test/merge-queue-cafe/pulls)
   and click **"Merge when ready"** on all 18 PRs
4. Watch the **merge queue tab** — GitHub will:
   - Batch compatible PRs together
   - Run CI on the **combined result**, not just each PR alone
   - Catch the size/price failures **before** they reach `main`
   - Dequeue the failing PRs and notify the authors

### What Breaks and When

Each drink PR adds 1 item. Base has 2 items. The tests enforce a max of 4 items
and a max average price of $4.50.

| Drink PRs merged | Total items | Size test (max 4) | Avg price test (max $4.50) |
|:----------------:|:-----------:|:-----------------:|:--------------------------:|
| 1                | 3           | ✅ Pass           | ✅ Pass                    |
| 2                | 4           | ✅ Pass           | ✅ Pass                    |
| **3**            | **5**       | ❌ **Fail**       | ✅ Pass                    |
| 4                | 6           | ❌ Fail           | ✅ Pass                    |
| 5                | 7           | ❌ Fail           | ✅ Pass                    |
| 6                | 8           | ❌ Fail           | ✅ Pass                    |
| 7                | 9           | ❌ Fail           | ✅ Pass                    |
| **8 (all)**      | **10**      | ❌ Fail           | ❌ **Fail**                |

---

## 🔄 Resetting for a Fresh Demo

Run the reset script from the repo root **before each demo**:

```bash
python3 scripts/reset_demo.py
```

This will:

1. **Close** all open PRs and delete their branches
2. **Force-reset** `main` to the `demo-base` tag (the clean starting state)
3. **Clean up** any leftover local and remote branches
4. **Recreate** all 18 PRs from scratch

> **Note:** The reset script relies on the `demo-base` git tag and the admin bypass
> on the merge queue ruleset to force-push to `main`. Don't delete either of these.

If you only want to create the PRs without resetting (e.g., on first setup):

```bash
python3 scripts/create_prs.py
```

---

## 📋 The 18 PRs

### Drink PRs (cause CI breakage when combined)

| #  | Branch              | Drink         | Price  | Why it breaks                |
|:--:|---------------------|---------------|:------:|------------------------------|
| 1  | `add-espresso`      | Espresso      | $4.00  | Contributes to size overflow |
| 2  | `add-latte`         | Latte         | $5.50  | Size overflow + raises avg   |
| 3  | `add-cappuccino`    | Cappuccino    | $5.25  | Size overflow + raises avg   |
| 4  | `add-americano`     | Americano     | $4.25  | Size overflow                |
| 5  | `add-cold-brew`     | Cold Brew     | $5.00  | Size overflow + raises avg   |
| 6  | `add-matcha-latte`  | Matcha Latte  | $5.75  | Size overflow + raises avg   |
| 7  | `add-chai-latte`    | Chai Latte    | $5.50  | Size overflow + raises avg   |
| 8  | `add-hot-chocolate`  | Hot Chocolate | $4.50  | Size overflow                |

### Style, Feature, and Config PRs (merge cleanly)

| #  | Branch               | What it does                    | Files changed                |
|:--:|----------------------|---------------------------------|------------------------------|
| 9  | `dark-mode`          | Dark mode via media query       | `styles.css`                 |
| 10 | `responsive-layout`  | Mobile-responsive breakpoints   | `styles.css`                 |
| 11 | `fancy-fonts`        | Google Fonts integration        | `styles.css`, `index.html`   |
| 12 | `menu-card-redesign` | Hover effects + shadows         | `styles.css`                 |
| 13 | `search-bar`         | Real-time search filter         | `index.html`                 |
| 14 | `category-tabs`      | Category filter tabs            | `index.html`                 |
| 15 | `price-sort`         | Sort-by-price button            | `index.html`                 |
| 16 | `favorites-feature`  | Heart/favorite toggle           | `index.html`, `styles.css`   |
| 17 | `add-ruff-config`    | Ruff linter config              | `ruff.toml` (new)            |
| 18 | `add-pyproject`      | Project metadata                | `pyproject.toml` (new)       |

---

## ⚙️ Merge Queue Configuration

The repo has a ruleset called **"Merge Queue"** configured at
**Settings → Rules → Rulesets**:

| Setting                  | Value      | Why                                      |
|--------------------------|------------|------------------------------------------|
| Grouping strategy        | ALLGREEN   | Batches are tested together              |
| Max entries to build     | 5          | Limits parallel CI load                  |
| Min entries to merge     | 1          | Doesn't wait to batch                    |
| Merge method             | MERGE      | Standard merge commits                   |
| Admin bypass             | Enabled    | Allows `reset_demo.py` to force-push     |

## Repo Structure

```
merge-queue-cafe/
├── README.md                      ← You are here
├── app.py                         ← Flask app
├── menu.py                        ← Menu data (what the drink PRs modify)
├── conftest.py                    ← pytest path config
├── requirements.txt
├── .github/workflows/ci.yml      ← CI: pytest + ruff
├── scripts/
│   ├── create_prs.py              ← Creates all 18 PRs
│   └── reset_demo.py              ← Resets repo for fresh demo
├── static/styles.css
├── templates/index.html
└── tests/test_menu.py             ← Tests including size + price limits
```
