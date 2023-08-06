Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const loadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/loadingMask"));
const TransparentLoadingMask = (0, styled_1.default)((_a) => {
    var { className, visible, children } = _a, props = (0, tslib_1.__rest)(_a, ["className", "visible", "children"]);
    const other = visible ? Object.assign(Object.assign({}, props), { 'data-test-id': 'loading-placeholder' }) : props;
    return (<loadingMask_1.default className={className} {...other}>
        {children}
      </loadingMask_1.default>);
}) `
  ${p => !p.visible && 'display: none;'};
  opacity: 0.4;
  z-index: 1;
`;
exports.default = TransparentLoadingMask;
//# sourceMappingURL=transparentLoadingMask.jsx.map