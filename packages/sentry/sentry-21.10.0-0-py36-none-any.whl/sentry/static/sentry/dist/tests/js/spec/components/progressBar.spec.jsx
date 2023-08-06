Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const progressBar_1 = (0, tslib_1.__importDefault)(require("app/components/progressBar"));
describe('ProgressBar', function () {
    it('basic', function () {
        const progressBarValue = 50;
        const wrapper = (0, enzyme_1.mountWithTheme)(<progressBar_1.default value={progressBarValue}/>);
        // element exists
        expect(wrapper.length).toEqual(1);
        const elementProperties = wrapper.find('div').props();
        expect(elementProperties).toHaveProperty('role', 'progressbar');
        // check aria attributes
        expect(elementProperties).toHaveProperty('aria-valuenow', progressBarValue);
        expect(elementProperties).toHaveProperty('aria-valuemin', 0);
        expect(elementProperties).toHaveProperty('aria-valuemax', 100);
    });
});
//# sourceMappingURL=progressBar.spec.jsx.map