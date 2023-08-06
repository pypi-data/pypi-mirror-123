Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
function LeadHint({ leadsToApp, isExpanded, nextFrame }) {
    if (isExpanded || !leadsToApp) {
        return null;
    }
    return (<Wrapper className="leads-to-app-hint" width={!nextFrame ? '115px' : ''}>
      {!nextFrame ? (0, locale_1.t)('Crashed in non-app') : (0, locale_1.t)('Called from')}
      {': '}
    </Wrapper>);
}
exports.default = LeadHint;
const Wrapper = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
  max-width: ${p => (p.width ? p.width : '67px')}
`;
//# sourceMappingURL=leadHint.jsx.map