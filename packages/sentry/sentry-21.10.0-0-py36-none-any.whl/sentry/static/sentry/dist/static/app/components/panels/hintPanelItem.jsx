Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const HintPanelItem = (0, styled_1.default)('div') `
  display: flex;
  padding: ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  background: ${p => p.theme.backgroundSecondary};
  font-size: ${p => p.theme.fontSizeMedium};

  h2 {
    font-size: ${p => p.theme.fontSizeLarge};
    margin-bottom: 0;
  }

  &:last-child {
    border: 0;
  }
`;
exports.default = HintPanelItem;
//# sourceMappingURL=hintPanelItem.jsx.map