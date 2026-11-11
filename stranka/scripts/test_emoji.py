#!/usr/bin/env python3
"""Build an isolated copy; never edit content or public/ in the source project."""
import json
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix="tesla-emoji-") as tmp:
        site = Path(tmp) / "site"
        out = Path(tmp) / "out"
        shutil.copytree(ROOT, site, ignore=shutil.ignore_patterns("public", "resources", ".hugo_build.lock"))
        config = site / "hugo.yaml"
        s = config.read_text()
        for old, new in [
            ('text: "Tesla katalóg"', 'text: "Značka 🔧 :wrench: <b>brand</b>"'),
            ('name: "Docs 📚"', 'name: "Menu 🔧 :wrench: <b>menu</b>"'),
            ('owner: "Roran60"', 'owner: "Majiteľ 🔧 :wrench: <b>owner</b>"'),
            ('notice: "Autorské práva patria pôvodným vlastníkom"', 'notice: "Oznam 🔧 :wrench: <b>notice</b>"'),
        ]:
            assert old in s, old
            s = s.replace(old, new, 1)
        config.write_text(s)
        # Test a section and a child page without relying on sample site content.
        category = site / 'content/docs/test-emoji'
        category.mkdir()
        (category / '_index.md').write_text('---\ntitle: "Test"\noutputs: [html, rss, markdown]\ncontextMenu: true\n---\n\nTestovacia kategória.\n')
        (category / 'ukazka.md').write_text('---\ntitle: "Test"\noutputs: [html, markdown]\ncontextMenu: true\n---\n\nTestovacia stránka.\n')
        for file, title in [
            ('docs/test-emoji/_index.md', 'Kategória 🔧 :wrench:'),
            ('docs/test-emoji/ukazka.md', 'Súčiastka 🔧 :wrench:'),
            ('blog/ukazka-archivu.md', 'Článok 🔧 :wrench: <b>article</b>'),
        ]:
            p = site / 'content' / file
            text, n = re.subn(r'^title:.*$', f'title: "{title}"', p.read_text(), count=1, flags=re.M)
            assert n == 1
            p.write_text(text)
        subprocess.run(['hugo', '--baseURL', 'https://example.org/tesla/', '--destination', str(out)], cwd=site, check=True)
        def page(name):
            return (out / name / 'index.html').read_text()
        home, docs, category, item, blog, article = (page(n) for n in ['', 'docs', 'docs/test-emoji', 'docs/test-emoji/ukazka', 'blog', 'blog/ukazka-archivu'])
        for text in (home, docs, category, item, blog, article):
            assert 'Značka 🔧 🔧 &lt;b&gt;brand&lt;/b&gt;' in text
            assert 'Menu 🔧 🔧 &lt;b&gt;menu&lt;/b&gt;' in text
            assert 'Majiteľ 🔧 🔧 &lt;b&gt;owner&lt;/b&gt;' in text
            assert 'Oznam 🔧 🔧 &lt;b&gt;notice&lt;/b&gt;' in text
        for text in (docs, category, item):
            assert 'Kategória 🔧 🔧' in text
        for text in (category, item):
            assert 'Súčiastka 🔧 🔧' in text
        for text in (blog, article):
            assert 'Článok 🔧 🔧 &lt;b&gt;article&lt;/b&gt;' in text
        assert '<h1 class="hx:mb-0">Súčiastka 🔧 🔧</h1>' in item
        assert 'content="Súčiastka 🔧 🔧"' in item
        assert '/tesla/docs/test-emoji/ukazka/' in category
        assert '/tesla/blog/ukazka-archivu/' in blog
        assert '/tesla/docs/test-emoji/ukazka.md' in item
        assert (out / 'docs/test-emoji/ukazka.md').exists()
        assert ':wrench:' in (out / 'docs/test-emoji/ukazka.md').read_text()  # source export
        rss = ET.parse(out / 'blog/index.xml')
        assert any(x.text == 'Článok 🔧 🔧 <b>article</b>' for x in rss.findall('./channel/item/title'))
        data = json.loads(next(out.glob('*.search-data*.json')).read_text())
        assert data['/tesla/docs/test-emoji/ukazka/']['title'] == 'Súčiastka 🔧 🔧'
        assert data['/tesla/docs/test-emoji/']['title'] == 'Kategória 🔧 🔧'
        assert data['/tesla/blog/ukazka-archivu/']['title'] == 'Článok 🔧 🔧 <b>article</b>'
        assert not re.search(r'<b>(brand|menu|owner|notice|article)</b>', '\n'.join((home, docs, category, item, blog, article)))
        print('Emoji, escaping, navigation, RSS, search, Markdown and subpath: OK')


if __name__ == '__main__':
    main()
