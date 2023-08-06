Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const Category = (0, react_1.memo)(function Category({ category, searchTerm }) {
    const title = !(0, utils_1.defined)(category) ? (0, locale_1.t)('generic') : category;
    return (<Wrapper title={title}>
      <highlight_1.default text={searchTerm}>{title}</highlight_1.default>
    </Wrapper>);
});
exports.default = Category;
const Wrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 700;
`;
//# sourceMappingURL=category.jsx.map