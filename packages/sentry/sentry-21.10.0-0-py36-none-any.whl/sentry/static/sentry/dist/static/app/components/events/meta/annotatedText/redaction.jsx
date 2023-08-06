Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Redaction = (0, styled_1.default)(({ children, className }) => (<span className={className}>{children}</span>)) `
  cursor: default;
  vertical-align: middle;
  ${p => !p.withoutBackground && `background: rgba(255, 0, 0, 0.05);`}
`;
exports.default = Redaction;
//# sourceMappingURL=redaction.jsx.map