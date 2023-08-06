Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
describe('NotAvailable', function () {
    it('renders', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<notAvailable_1.default />);
        expect(wrapper.text()).toEqual('\u2014');
    });
    it('renders with tooltip', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<notAvailable_1.default tooltip="Tooltip text"/>);
        expect(wrapper.text()).toEqual('\u2014');
        expect(wrapper.find('Tooltip').prop('title')).toBe('Tooltip text');
    });
});
//# sourceMappingURL=notAvailable.spec.jsx.map