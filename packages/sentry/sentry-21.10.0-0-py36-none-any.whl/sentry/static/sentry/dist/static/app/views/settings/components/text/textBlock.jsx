Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const TextBlock = (0, styled_1.default)('div') `
  line-height: 1.5;
  ${p => (p.noMargin ? '' : 'margin-bottom:' + (0, space_1.default)(3))};
`;
exports.default = TextBlock;
//# sourceMappingURL=textBlock.jsx.map