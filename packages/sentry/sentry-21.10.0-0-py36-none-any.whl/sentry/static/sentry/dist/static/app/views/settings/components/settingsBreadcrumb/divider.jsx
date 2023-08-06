Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const Divider = ({ isHover, isLast }) => isLast ? null : (<StyledDivider>
      <StyledIconChevron direction={isHover ? 'down' : 'right'} size="14px"/>
    </StyledDivider>);
const StyledIconChevron = (0, styled_1.default)(icons_1.IconChevron) `
  display: block;
`;
const StyledDivider = (0, styled_1.default)('span') `
  display: inline-block;
  margin-left: 6px;
  color: ${p => p.theme.gray200};
  position: relative;
`;
exports.default = Divider;
//# sourceMappingURL=divider.jsx.map