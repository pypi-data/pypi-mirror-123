Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const locale_1 = require("app/locale");
const u2finterface_1 = (0, tslib_1.__importDefault)(require("./u2finterface"));
const MESSAGES = {
    signin: (0, locale_1.t)('Insert your U2F device or tap the button on it to confirm the sign-in request.'),
    sudo: (0, locale_1.t)('Alternatively you can use your U2F device to confirm the action.'),
    enroll: (0, locale_1.t)('To enroll your U2F device insert it now or tap the button on it to activate it.'),
};
class U2fSign extends react_1.Component {
    render() {
        const _a = this.props, { displayMode } = _a, props = (0, tslib_1.__rest)(_a, ["displayMode"]);
        const flowMode = displayMode === 'enroll' ? 'enroll' : 'sign';
        return (<u2finterface_1.default {...props} silentIfUnsupported={displayMode === 'sudo'} flowMode={flowMode}>
        <p>{MESSAGES[displayMode] || null}</p>
      </u2finterface_1.default>);
    }
}
U2fSign.defaultProps = {
    displayMode: 'signin',
};
exports.default = U2fSign;
//# sourceMappingURL=u2fsign.jsx.map