Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panel_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panel"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const text_1 = (0, tslib_1.__importDefault)(require("app/styles/text"));
const Text = (0, styled_1.default)('div') `
  ${text_1.default};

  ${ /* sc-selector */panel_1.default} & {
    padding-left: ${(0, space_1.default)(2)};
    padding-right: ${(0, space_1.default)(2)};

    &:first-child {
      padding-top: ${(0, space_1.default)(2)};
    }
  }
`;
exports.default = Text;
//# sourceMappingURL=text.jsx.map