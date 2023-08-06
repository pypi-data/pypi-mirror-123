Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Item = ({ children, icon, className }) => (<Wrapper className={(0, classnames_1.default)('context-item', className)} data-test-id="context-item">
    {icon}
    {children && <Details>{children}</Details>}
  </Wrapper>);
exports.default = Item;
const Details = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 100%;
  min-height: 48px;
`;
const Wrapper = (0, styled_1.default)('div') `
  border-top: 1px solid ${p => p.theme.innerBorder};
  padding: ${(0, space_1.default)(0.5)} 0 ${(0, space_1.default)(0.5)} 40px;
  display: flex;
  align-items: center;
  position: relative;
  min-width: 0;

  :not(:last-child) {
    margin-right: ${(0, space_1.default)(3)};
  }

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    max-width: 25%;
    border: 0;
    padding: 0px 0px 0px 42px;
  }
`;
//# sourceMappingURL=item.jsx.map