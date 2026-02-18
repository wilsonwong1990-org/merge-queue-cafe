#!/usr/bin/env python3
"""Generate 18 branches and PRs for the Merge Queue Café demo.

Usage:
    python3 create_prs.py

Requires: gh CLI authenticated with push access to the repo.
"""

import subprocess
import sys
import textwrap

REPO = "wilsonwong1990-org/merge-queue-cafe"

# Each PR is: (branch_name, pr_title, pr_body, list_of_(filepath, content_patch))
# content_patch is a tuple of (mode, data) where mode is "replace" or "append_to_list"

PRS = []

# ---------------------------------------------------------------------------
# Helper to build a menu.py that adds a drink.
# Each PR adds to a DIFFERENT category list so they merge cleanly (no git
# conflicts), but collectively they break the menu size and avg price tests.
# Base: 2 items, MAX_MENU_SIZE=6.  Each PR adds 1 item → passes alone (3 items).
# But 5+ drink PRs merged = 7+ items → test_menu_size_within_limit FAILS.
# Also, expensive drinks push average price above $5 → test_average_price FAILS.
# ---------------------------------------------------------------------------

DRINK_PRS = [
    # (branch, title, drink_name, target_list, price, description)
    ("add-espresso", "Add Espresso to menu", "Espresso", "COFFEE_ITEMS", 4.00,
     "A bold, concentrated shot of pure coffee."),
    ("add-latte", "Add Latte to menu", "Latte", "COFFEE_ITEMS", 5.50,
     "Espresso with steamed milk and a touch of foam."),
    ("add-cappuccino", "Add Cappuccino to menu", "Cappuccino", "COFFEE_ITEMS", 5.25,
     "Equal parts espresso, steamed milk, and foam."),
    ("add-americano", "Add Americano to menu", "Americano", "COFFEE_ITEMS", 4.25,
     "Espresso diluted with hot water for a smooth finish."),
    ("add-cold-brew", "Add Cold Brew to menu", "Cold Brew", "COFFEE_ITEMS", 5.00,
     "Slow-steeped for 12 hours, served over ice."),
    ("add-matcha-latte", "Add Matcha Latte to menu", "Matcha Latte", "TEA_ITEMS", 5.75,
     "Ceremonial-grade matcha whisked with oat milk."),
    ("add-chai-latte", "Add Chai Latte to menu", "Chai Latte", "TEA_ITEMS", 5.50,
     "Spiced black tea with steamed milk and honey."),
    ("add-hot-chocolate", "Add Hot Chocolate to menu", "Hot Chocolate", "OTHER_ITEMS", 4.50,
     "Rich dark chocolate melted into steamed milk."),
]

for branch, title, name, target_list, price, desc in DRINK_PRS:
    # Determine the category from the target list
    cat = {"COFFEE_ITEMS": "coffee", "TEA_ITEMS": "tea", "OTHER_ITEMS": "other"}[target_list]

    new_item = (
        f'    {{\n'
        f'        "name": "{name}",\n'
        f'        "category": "{cat}",\n'
        f'        "price": {price:.2f},\n'
        f'        "description": "{desc}",\n'
        f'    }},\n'
    )

    # Each PR appends to the END of its specific category list.
    # We find the ']' that closes that list. To make the search unique,
    # we search for the last item in that list + the closing bracket.
    if target_list == "COFFEE_ITEMS":
        search_str = '    },\n]\n\nTEA_ITEMS'
        replace_str = '    },\n' + new_item + ']\n\nTEA_ITEMS'
    elif target_list == "TEA_ITEMS":
        search_str = '    },\n]\n\nOTHER_ITEMS'
        replace_str = '    },\n' + new_item + ']\n\nOTHER_ITEMS'
    else:  # OTHER_ITEMS
        search_str = 'OTHER_ITEMS = []'
        replace_str = 'OTHER_ITEMS = [\n' + new_item + ']'

    PRS.append({
        "branch": branch,
        "title": title,
        "body": f"Adds **{name}** (${price:.2f}) to the café menu under the *{cat}* category.\n\n✅ All tests pass — menu stays within the 6-item limit.",
        "changes": [
            {
                "file": "menu.py",
                "search": search_str,
                "replace": replace_str,
            }
        ],
    })

# ---------------------------------------------------------------------------
# Style PRs — each modifies styles.css
# ---------------------------------------------------------------------------

PRS.append({
    "branch": "dark-mode",
    "title": "Add dark mode support",
    "body": "Adds a `prefers-color-scheme: dark` media query for dark mode users.",
    "changes": [
        {
            "file": "static/styles.css",
            "search": "/* Merge Queue Café — base styles */",
            "replace": textwrap.dedent("""\
                /* Merge Queue Café — base styles */

                @media (prefers-color-scheme: dark) {
                    body {
                        background-color: #1a1a2e;
                        color: #e0d6cc;
                    }
                    header {
                        background-color: #16213e;
                    }
                    .menu-card {
                        background: #0f3460;
                        border-color: #1a1a2e;
                    }
                    .price {
                        color: #e9b872;
                    }
                }"""),
        }
    ],
})

PRS.append({
    "branch": "responsive-layout",
    "title": "Make layout mobile-responsive",
    "body": "Adds responsive breakpoints so the menu looks great on phones and tablets.",
    "changes": [
        {
            "file": "static/styles.css",
            "search": """.menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
}""",
            "replace": textwrap.dedent("""\
                .menu-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                    gap: 1.5rem;
                }

                @media (max-width: 600px) {
                    .menu-grid {
                        grid-template-columns: 1fr;
                        gap: 1rem;
                    }
                    header h1 {
                        font-size: 1.8rem;
                    }
                    main {
                        padding: 0 0.5rem;
                    }
                }"""),
        }
    ],
})

PRS.append({
    "branch": "fancy-fonts",
    "title": "Switch to Google Fonts",
    "body": "Uses **Playfair Display** for headings and **Source Sans Pro** for body text.",
    "changes": [
        {
            "file": "static/styles.css",
            "search": """body {
    font-family: Georgia, "Times New Roman", serif;""",
            "replace": """body {
    font-family: "Source Sans Pro", Georgia, "Times New Roman", serif;""",
        },
        {
            "file": "templates/index.html",
            "search": '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'styles.css\') }}">',
            "replace": '    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+Pro&display=swap" rel="stylesheet">\n    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'styles.css\') }}">',
        },
    ],
})

PRS.append({
    "branch": "menu-card-redesign",
    "title": "Redesign menu item cards",
    "body": "Adds hover effects and a subtle shadow to menu cards for a more polished look.",
    "changes": [
        {
            "file": "static/styles.css",
            "search": """.menu-card {
    background: #fff;
    border: 1px solid #e0d6cc;
    border-radius: 8px;
    padding: 1.5rem;
}""",
            "replace": """.menu-card {
    background: #fff;
    border: 1px solid #e0d6cc;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(59, 47, 47, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.menu-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(59, 47, 47, 0.15);
}""",
        }
    ],
})

# ---------------------------------------------------------------------------
# Feature PRs — touch templates/index.html
# ---------------------------------------------------------------------------

PRS.append({
    "branch": "search-bar",
    "title": "Add search/filter bar",
    "body": "Adds a text input that filters menu items in real time using JavaScript.",
    "changes": [
        {
            "file": "templates/index.html",
            "search": '        <section class="menu">\n            <h2>Our Menu</h2>',
            "replace": textwrap.dedent("""\
                <section class="menu">
                        <h2>Our Menu</h2>
                        <div class="search-container">
                            <input type="text" id="search" placeholder="Search the menu..." onkeyup="filterMenu()">
                        </div>"""),
        },
        {
            "file": "templates/index.html",
            "search": "</footer>\n</body>",
            "replace": textwrap.dedent("""\
                </footer>
                    <script>
                    function filterMenu() {
                        const q = document.getElementById('search').value.toLowerCase();
                        document.querySelectorAll('.menu-card').forEach(card => {
                            const text = card.textContent.toLowerCase();
                            card.style.display = text.includes(q) ? '' : 'none';
                        });
                    }
                    </script>
                </body>"""),
        },
    ],
})

PRS.append({
    "branch": "category-tabs",
    "title": "Add drink category tabs",
    "body": "Adds clickable category tabs so users can filter by coffee, tea, etc.",
    "changes": [
        {
            "file": "templates/index.html",
            "search": '        <section class="menu">\n            <h2>Our Menu</h2>',
            "replace": textwrap.dedent("""\
                <section class="menu">
                        <h2>Our Menu</h2>
                        <div class="category-tabs">
                            <button class="tab active" onclick="filterCategory('all')">All</button>
                            {% for cat in categories %}
                            <button class="tab" onclick="filterCategory('{{ cat }}')">{{ cat|capitalize }}</button>
                            {% endfor %}
                        </div>"""),
        },
        {
            "file": "templates/index.html",
            "search": "</footer>\n</body>",
            "replace": textwrap.dedent("""\
                </footer>
                    <script>
                    function filterCategory(cat) {
                        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                        event.target.classList.add('active');
                        document.querySelectorAll('.menu-card').forEach(card => {
                            const cardCat = card.querySelector('.category').textContent.toLowerCase();
                            card.style.display = (cat === 'all' || cardCat === cat) ? '' : 'none';
                        });
                    }
                    </script>
                </body>"""),
        },
    ],
})

PRS.append({
    "branch": "price-sort",
    "title": "Add sort-by-price button",
    "body": "Adds a button to sort menu items by price (ascending).",
    "changes": [
        {
            "file": "templates/index.html",
            "search": '        <section class="menu">\n            <h2>Our Menu</h2>',
            "replace": textwrap.dedent("""\
                <section class="menu">
                        <h2>Our Menu</h2>
                        <div class="sort-controls">
                            <button onclick="sortByPrice()">Sort by Price ↑</button>
                        </div>"""),
        },
        {
            "file": "templates/index.html",
            "search": "</footer>\n</body>",
            "replace": textwrap.dedent("""\
                </footer>
                    <script>
                    function sortByPrice() {
                        const grid = document.querySelector('.menu-grid');
                        const cards = Array.from(grid.querySelectorAll('.menu-card'));
                        cards.sort((a, b) => {
                            const pa = parseFloat(a.querySelector('.price').textContent.replace('$', ''));
                            const pb = parseFloat(b.querySelector('.price').textContent.replace('$', ''));
                            return pa - pb;
                        });
                        cards.forEach(card => grid.appendChild(card));
                    }
                    </script>
                </body>"""),
        },
    ],
})

PRS.append({
    "branch": "favorites-feature",
    "title": "Add favorite heart button",
    "body": "Adds a ❤️ toggle button to each menu card so users can favorite drinks.",
    "changes": [
        {
            "file": "templates/index.html",
            "search": '                    <p class="price">${{ "%.2f" | format(item.price) }}</p>',
            "replace": '                    <p class="price">${{ "%.2f" | format(item.price) }}</p>\n                    <button class="fav-btn" onclick="this.classList.toggle(\'liked\')">♡</button>',
        },
        {
            "file": "static/styles.css",
            "search": """footer {""",
            "replace": """.fav-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #ccc;
    transition: color 0.2s;
}

.fav-btn.liked {
    color: #e74c3c;
}

.fav-btn:hover {
    color: #e74c3c;
}

footer {""",
        },
    ],
})

# ---------------------------------------------------------------------------
# Infrastructure PRs
# ---------------------------------------------------------------------------

PRS.append({
    "branch": "add-ruff-config",
    "title": "Add ruff configuration",
    "body": "Adds a `ruff.toml` with opinionated linting rules for the project.",
    "changes": [
        {
            "file": "ruff.toml",
            "search": None,  # new file
            "replace": textwrap.dedent("""\
                line-length = 100
                target-version = "py312"

                [lint]
                select = ["E", "F", "I", "N", "W"]
                ignore = ["E501"]"""),
        },
    ],
})

PRS.append({
    "branch": "add-pyproject",
    "title": "Add pyproject.toml project metadata",
    "body": "Adds a `pyproject.toml` with project metadata and tool configuration.",
    "changes": [
        {
            "file": "pyproject.toml",
            "search": None,  # new file
            "replace": textwrap.dedent("""\
                [project]
                name = "merge-queue-cafe"
                version = "0.1.0"
                description = "A demo café menu app for GitHub merge queue demos"
                requires-python = ">=3.12"
                dependencies = [
                    "flask>=3.0",
                ]

                [project.optional-dependencies]
                dev = [
                    "pytest>=8.0",
                    "ruff>=0.4",
                ]"""),
        },
    ],
})


# ===========================================================================
# Script execution
# ===========================================================================

def run(cmd, check=True):
    """Run a shell command and return stdout."""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  STDERR: {result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()


def main():
    # Make sure we're on main and up to date
    run("git checkout main")
    run("git pull origin main")

    for i, pr in enumerate(PRS, 1):
        branch = pr["branch"]
        title = pr["title"]
        body = pr["body"]
        changes = pr["changes"]

        print(f"\n[{i}/{len(PRS)}] Creating PR: {title} ({branch})")

        # Create branch from main
        run(f"git checkout -b {branch} main")

        for change in changes:
            filepath = change["file"]
            search = change["search"]
            replace = change["replace"]

            if search is None:
                # New file
                print(f"  Creating new file: {filepath}")
                with open(filepath, "w") as f:
                    f.write(replace + "\n")
            else:
                # Search and replace in existing file
                print(f"  Patching: {filepath}")
                with open(filepath, "r") as f:
                    content = f.read()

                if search not in content:
                    print(f"  WARNING: search string not found in {filepath}, skipping")
                    continue

                content = content.replace(search, replace, 1)
                with open(filepath, "w") as f:
                    f.write(content)

        # Commit and push
        run("git add -A")
        run(f'git commit -m "{title}\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"')
        run(f"git push origin {branch}")

        # Create PR
        run(f'gh pr create --repo {REPO} --base main --head {branch} --title "{title}" --body "{body}"')

        # Go back to main
        run("git checkout main")

    print(f"\n✅ All {len(PRS)} PRs created! Visit https://github.com/{REPO}/pulls")


if __name__ == "__main__":
    main()
