Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
function Input(_a) {
    var { className } = _a, otherProps = (0, tslib_1.__rest)(_a, ["className"]);
    return (<input className={(0, classnames_1.default)('form-control', className)} {...(0, omit_1.default)(otherProps, 'children')}/>);
}
exports.default = Input;
//# sourceMappingURL=input.jsx.map