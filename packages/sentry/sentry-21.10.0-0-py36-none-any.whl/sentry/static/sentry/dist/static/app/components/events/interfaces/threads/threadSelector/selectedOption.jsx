Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const SelectedOption = ({ id, details }) => (<Wrapper>
    <ThreadId>{(0, locale_1.tct)('Thread #[id]:', { id })}</ThreadId>
    <Label>{(details === null || details === void 0 ? void 0 : details.label) || `<${(0, locale_1.t)('unknown')}>`}</Label>
  </Wrapper>);
exports.default = SelectedOption;
const Wrapper = (0, styled_1.default)('div') `
  grid-template-columns: auto 1fr;
  display: grid;
`;
const ThreadId = (0, styled_1.default)(textOverflow_1.default) `
  padding-right: ${(0, space_1.default)(1)};
  max-width: 100%;
  text-align: left;
`;
const Label = (0, styled_1.default)(ThreadId) `
  color: ${p => p.theme.blue300};
`;
//# sourceMappingURL=selectedOption.jsx.map