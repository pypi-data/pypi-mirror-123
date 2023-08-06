Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const icons_1 = require("app/icons");
describe('AlertLink', function () {
    it('renders', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<alertLink_1.default to="/settings/accounts/notifications">
        This is an external link button
      </alertLink_1.default>);
        expect(container).toSnapshot();
    });
    it('renders with icon', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<alertLink_1.default to="/settings/accounts/notifications" icon={<icons_1.IconMail />}>
        This is an external link button
      </alertLink_1.default>);
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=alertLink.spec.jsx.map