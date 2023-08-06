Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const PanelItem = (0, styled_1.default)('div') `
  display: flex;
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  ${p => p.noPadding || `padding: ${(0, space_1.default)(2)}`};
  ${p => p.center && 'align-items: center'};

  &:last-child {
    border: 0;
  }
`;
exports.default = PanelItem;
//# sourceMappingURL=panelItem.jsx.map