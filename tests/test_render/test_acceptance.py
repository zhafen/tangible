import xml.etree.ElementTree as ET

from tangible import render_svg

SVG = "{http://www.w3.org/2000/svg}"


class TestRender:
    def test_basic(self, tmp_path):
        """view_factory: each top level file or directory exists in the
        render as a rectangle with its name inside."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "nested.py").write_text("")
        (tmp_path / "tests").mkdir()
        (tmp_path / "README.md").write_text("")
        (tmp_path / "a&b <c>.txt").write_text("")
        expected = {"src", "tests", "README.md", "a&b <c>.txt"}

        svg = render_svg(tmp_path)
        print(svg)
        root = ET.fromstring(svg)

        rendered = {}
        for group in root.iter(f"{SVG}g"):
            rect, text = group.find(f"{SVG}rect"), group.find(f"{SVG}text")
            x, y, w, h = (float(rect.get(k)) for k in ("x", "y", "width", "height"))
            tx, ty = float(text.get("x")), float(text.get("y"))
            assert x < tx < x + w and y < ty < y + h, f"{text.text} outside its rect"
            assert text.text not in rendered, f"{text.text} rendered twice"
            rendered[text.text] = (x, y, w, h)

        assert set(rendered) == expected

        boxes = list(rendered.values())
        for i, (x1, y1, w1, h1) in enumerate(boxes):
            for x2, y2, w2, h2 in boxes[i + 1 :]:
                assert x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1
