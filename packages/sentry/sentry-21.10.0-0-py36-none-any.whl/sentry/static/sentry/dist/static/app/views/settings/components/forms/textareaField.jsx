Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const textarea_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/textarea"));
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
function TextareaField(_a) {
    var { monospace, rows, autosize } = _a, props = (0, tslib_1.__rest)(_a, ["monospace", "rows", "autosize"]);
    return (<inputField_1.default {...props} field={fieldProps => (<textarea_1.default {...{ monospace, rows, autosize }} {...(0, omit_1.default)(fieldProps, ['onKeyDown', 'children'])}/>)}/>);
}
exports.default = TextareaField;
//# sourceMappingURL=textareaField.jsx.map