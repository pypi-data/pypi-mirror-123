Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const inlineStyle = p => p.inline
    ? (0, react_1.css) `
        width: 50%;
        padding-right: 10px;
        flex-shrink: 0;
      `
    : (0, react_1.css) `
        margin-bottom: ${(0, space_1.default)(1)};
      `;
const FieldDescription = (0, styled_1.default)('label') `
  font-weight: normal;
  margin-bottom: 0;

  ${inlineStyle};
`;
exports.default = FieldDescription;
//# sourceMappingURL=fieldDescription.jsx.map