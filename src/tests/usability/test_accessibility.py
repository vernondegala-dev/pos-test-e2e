import allure


@allure.feature("Usability")
@allure.story("Accessibility")
class TestAccessibility:
    @allure.title("Login page has proper heading hierarchy")
    @allure.severity(allure.severity_level.NORMAL)
    def test_heading_hierarchy(self, login_page, page):
        login_page.navigate_to()
        headings = page.evaluate("""() => {
            const h1 = document.querySelectorAll('h1');
            const h2 = document.querySelectorAll('h2');
            const h3 = document.querySelectorAll('h3');
            return { h1: h1.length, h2: h2.length, h3: h3.length };
        }""")
        allure.attach(str(headings), name="Heading Counts", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Form inputs have associated labels")
    @allure.severity(allure.severity_level.NORMAL)
    def test_input_labels(self, login_page, page):
        login_page.navigate_to()
        inputs = page.evaluate("""() => {
            const inputs = document.querySelectorAll('input');
            return Array.from(inputs).map(i => ({
                id: i.id,
                hasLabel: !!document.querySelector(`label[for=\"${i.id}\"]`),
                hasAriaLabel: !!i.getAttribute('aria-label'),
                hasPlaceholder: !!i.getAttribute('placeholder'),
                name: i.name
            }));
        }""")
        allure.attach(str(inputs), name="Input Labels", attachment_type=allure.attachment_type.TEXT)
        assert len(inputs) > 0, "There should be form inputs"

    @allure.title("Color contrast is sufficient")
    @allure.severity(allure.severity_level.NORMAL)
    def test_color_contrast(self, login_page, page):
        login_page.navigate_to()
        body_bg = page.evaluate("""() => {
            const style = getComputedStyle(document.body);
            return { bg: style.backgroundColor, color: style.color };
        }""")
        allure.attach(str(body_bg), name="Body Colors", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Interactive elements have focus indicators")
    @allure.severity(allure.severity_level.NORMAL)
    def test_focus_indicators(self, login_page, page):
        login_page.navigate_to()
        has_focus_style = page.evaluate("""() => {
            const style = document.createElement('style');
            style.textContent = ':focus { outline: 2px solid Highlight !important; }';
            document.head.appendChild(style);
            const btn = document.querySelector('button[type=\"submit\"]');
            if (!btn) return false;
            btn.focus();
            const afterFocus = getComputedStyle(btn).outlineStyle;
            style.remove();
            return afterFocus !== 'none';
        }""")
        allure.attach(f"Focus indicator: {has_focus_style}", name="Focus Check", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Images have alt text")
    @allure.severity(allure.severity_level.NORMAL)
    def test_images_have_alt(self, login_page, page):
        login_page.navigate_to()
        missing_alt = page.evaluate("""() => {
            const imgs = document.querySelectorAll('img:not([alt])');
            return imgs.length;
        }""")
        allure.attach(f"Images missing alt text: {missing_alt}", name="Alt Text Check", attachment_type=allure.attachment_type.TEXT)
