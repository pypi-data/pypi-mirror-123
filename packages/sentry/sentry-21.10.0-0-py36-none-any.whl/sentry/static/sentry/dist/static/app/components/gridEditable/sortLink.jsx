Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
class SortLink extends React.Component {
    renderArrow() {
        const { direction } = this.props;
        if (!direction) {
            return null;
        }
        if (direction === 'desc') {
            return <StyledIconArrow size="xs" direction="down"/>;
        }
        return <StyledIconArrow size="xs" direction="up"/>;
    }
    render() {
        const { align, title, canSort, generateSortLink, onClick } = this.props;
        const target = generateSortLink();
        if (!target || !canSort) {
            return <StyledNonLink align={align}>{title}</StyledNonLink>;
        }
        return (<StyledLink align={align} to={target} onClick={onClick}>
        {title} {this.renderArrow()}
      </StyledLink>);
    }
}
const StyledLink = (0, styled_1.default)((props) => {
    const forwardProps = (0, omit_1.default)(props, ['align']);
    return <link_1.default {...forwardProps}/>;
}) `
  display: block;
  width: 100%;
  white-space: nowrap;
  color: inherit;

  &:hover,
  &:active,
  &:focus,
  &:visited {
    color: inherit;
  }

  ${(p) => (p.align ? `text-align: ${p.align};` : '')}
`;
const StyledNonLink = (0, styled_1.default)('div') `
  display: block;
  width: 100%;
  white-space: nowrap;
  ${(p) => (p.align ? `text-align: ${p.align};` : '')}
`;
const StyledIconArrow = (0, styled_1.default)(icons_1.IconArrow) `
  vertical-align: top;
`;
exports.default = SortLink;
//# sourceMappingURL=sortLink.jsx.map