Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const copy_text_to_clipboard_1 = (0, tslib_1.__importDefault)(require("copy-text-to-clipboard"));
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
/**
 * copy-text-to-clipboard relies on `document.execCommand('copy')`
 */
function isSupported() {
    const support = !!document.queryCommandSupported;
    return support && !!document.queryCommandSupported('copy');
}
class Clipboard extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleClick = () => {
            const { value, hideMessages, successMessage, errorMessage, onSuccess, onError } = this.props;
            // Copy returns whether it succeeded to copy the text
            const success = (0, copy_text_to_clipboard_1.default)(value);
            if (!success) {
                if (!hideMessages) {
                    (0, indicator_1.addErrorMessage)(errorMessage);
                }
                onError === null || onError === void 0 ? void 0 : onError();
                return;
            }
            if (!hideMessages) {
                (0, indicator_1.addSuccessMessage)(successMessage);
            }
            onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
        };
        this.handleMount = (ref) => {
            var _a;
            if (!ref) {
                return;
            }
            // eslint-disable-next-line react/no-find-dom-node
            this.element = react_dom_1.default.findDOMNode(ref);
            (_a = this.element) === null || _a === void 0 ? void 0 : _a.addEventListener('click', this.handleClick);
        };
    }
    componentWillUnmount() {
        var _a;
        (_a = this.element) === null || _a === void 0 ? void 0 : _a.removeEventListener('click', this.handleClick);
    }
    render() {
        const { children, hideUnsupported } = this.props;
        // Browser doesn't support `execCommand`
        if (hideUnsupported && !isSupported()) {
            return null;
        }
        if (!(0, react_1.isValidElement)(children)) {
            return null;
        }
        return (0, react_1.cloneElement)(children, {
            ref: this.handleMount,
        });
    }
}
Clipboard.defaultProps = {
    hideMessages: false,
    successMessage: (0, locale_1.t)('Copied to clipboard'),
    errorMessage: (0, locale_1.t)('Error copying to clipboard'),
};
exports.default = Clipboard;
//# sourceMappingURL=clipboard.jsx.map