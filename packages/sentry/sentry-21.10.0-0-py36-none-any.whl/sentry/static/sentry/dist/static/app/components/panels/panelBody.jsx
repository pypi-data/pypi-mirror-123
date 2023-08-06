Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const text_1 = (0, tslib_1.__importDefault)(require("app/styles/text"));
const PanelBody = (0, styled_1.default)('div') `
  ${p => p.withPadding && `padding: ${(0, space_1.default)(2)}`};
  ${text_1.default};
`;
exports.default = PanelBody;
//# sourceMappingURL=panelBody.jsx.map