Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const overflowEllipsisLeft_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsisLeft"));
const TextOverflow = (0, styled_1.default)(({ isParagraph, className, children, ['data-test-id']: dataTestId }) => {
    const Component = isParagraph ? 'p' : 'div';
    return (<Component className={className} data-test-id={dataTestId}>
        {children}
      </Component>);
}) `
  ${p => (p.ellipsisDirection === 'right' ? overflowEllipsis_1.default : overflowEllipsisLeft_1.default)};
  width: auto;
  line-height: 1.1;
`;
TextOverflow.defaultProps = {
    ellipsisDirection: 'right',
    isParagraph: false,
};
exports.default = TextOverflow;
//# sourceMappingURL=textOverflow.jsx.map