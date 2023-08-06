Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const EventAnnotation = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeSmall};
  border-left: 1px solid ${p => p.theme.innerBorder};
  padding-left: ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray300};

  a {
    color: ${p => p.theme.gray300};

    &:hover {
      color: ${p => p.theme.subText};
    }
  }
`;
exports.default = EventAnnotation;
//# sourceMappingURL=eventAnnotation.jsx.map