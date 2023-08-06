Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
describe('ButtonBar', function () {
    const createWrapper = () => (0, reactTestingLibrary_1.mountWithTheme)(<buttonBar_1.default active="2" merged>
        <button_1.default barId="1">First Button</button_1.default>
        <button_1.default barId="2">Second Button</button_1.default>
        <button_1.default barId="3">Third Button</button_1.default>
        <button_1.default barId="4">Fourth Button</button_1.default>
      </buttonBar_1.default>);
    it('has "Second Button" as the active button in the bar', function () {
        createWrapper();
        expect(reactTestingLibrary_1.screen.getByLabelText('First Button')).not.toHaveClass('active');
        expect(reactTestingLibrary_1.screen.getByLabelText('Second Button')).toHaveClass('active');
    });
});
//# sourceMappingURL=buttonBar.spec.jsx.map