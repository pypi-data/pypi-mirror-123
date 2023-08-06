Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const autoSelectText_1 = (0, tslib_1.__importDefault)(require("app/components/autoSelectText"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
function ShortId({ shortId, avatar, onClick, to, className }) {
    if (!shortId) {
        return null;
    }
    return (<StyledShortId onClick={onClick} className={className}>
      {avatar}
      {to ? (<link_1.default to={to}>{shortId}</link_1.default>) : (<StyledAutoSelectText>{shortId}</StyledAutoSelectText>)}
    </StyledShortId>);
}
const StyledShortId = (0, styled_1.default)('div') `
  font-family: ${p => p.theme.text.familyMono};
  display: grid;
  grid-auto-flow: column;
  grid-gap: 0.5em;
  align-items: center;
  justify-content: flex-end;
`;
const StyledAutoSelectText = (0, styled_1.default)(autoSelectText_1.default) `
  min-width: 0;

  a & {
    color: ${p => p.theme.linkColor};
  }
`;
exports.default = ShortId;
//# sourceMappingURL=shortId.jsx.map