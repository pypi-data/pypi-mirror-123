Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const commandLine_1 = (0, tslib_1.__importDefault)(require("app/components/commandLine"));
describe('CommandLine', () => {
    it('renders', () => {
        const children = 'sentry devserver --workers';
        const wrapper = (0, enzyme_1.mountWithTheme)(<commandLine_1.default>{children}</commandLine_1.default>);
        expect(wrapper.find('CommandLine').text()).toBe(children);
    });
});
//# sourceMappingURL=commandLine.spec.jsx.map