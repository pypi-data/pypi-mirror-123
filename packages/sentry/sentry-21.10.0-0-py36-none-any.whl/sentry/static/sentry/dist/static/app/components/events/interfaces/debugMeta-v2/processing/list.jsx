Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
function List({ items, className }) {
    if (!items.length) {
        return null;
    }
    return <Wrapper className={className}>{items}</Wrapper>;
}
exports.default = List;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
  font-size: ${p => p.theme.fontSizeSmall};
`;
//# sourceMappingURL=list.jsx.map