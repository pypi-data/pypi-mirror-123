Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Panel = (0, styled_1.default)('div') `
  background: ${p => (p.dashedBorder ? p.theme.backgroundSecondary : p.theme.background)};
  border-radius: ${p => p.theme.borderRadius};
  border: 1px
    ${p => (p.dashedBorder ? 'dashed' + p.theme.gray300 : 'solid ' + p.theme.border)};
  box-shadow: ${p => (p.dashedBorder ? 'none' : p.theme.dropShadowLight)};
  margin-bottom: ${(0, space_1.default)(3)};
  position: relative;
`;
exports.default = Panel;
//# sourceMappingURL=panel.jsx.map