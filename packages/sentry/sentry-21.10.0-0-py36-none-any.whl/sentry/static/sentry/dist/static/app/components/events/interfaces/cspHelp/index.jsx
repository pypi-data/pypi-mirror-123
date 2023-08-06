Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const effectiveDirectives_1 = (0, tslib_1.__importDefault)(require("./effectiveDirectives"));
const linkOverrides = { 'script-src': 'script-src_2' };
const CSPHelp = ({ data: { effective_directive: key } }) => {
    const getHelp = () => ({
        __html: effectiveDirectives_1.default[key],
    });
    const getLinkHref = () => {
        const baseLink = 'https://developer.mozilla.org/en-US/docs/Web/Security/CSP/CSP_policy_directives#';
        if (key in linkOverrides) {
            return `${baseLink}${linkOverrides[key]}`;
        }
        return `${baseLink}${key}`;
    };
    const getLink = () => {
        const href = getLinkHref();
        return (<StyledExternalLink href={href}>
        {'developer.mozilla.org'}
        <icons_1.IconOpen size="xs" className="external-icon"/>
      </StyledExternalLink>);
    };
    return (<div>
      <h4>
        <code>{key}</code>
      </h4>
      <blockquote dangerouslySetInnerHTML={getHelp()}/>
      <StyledP>
        <span>{'\u2014 MDN ('}</span>
        <span>{getLink()}</span>
        <span>{')'}</span>
      </StyledP>
    </div>);
};
exports.default = CSPHelp;
const StyledP = (0, styled_1.default)('p') `
  text-align: right;
  display: grid;
  grid-template-columns: repeat(3, max-content);
  grid-gap: ${(0, space_1.default)(0.25)};
`;
const StyledExternalLink = (0, styled_1.default)(externalLink_1.default) `
  display: inline-flex;
  align-items: center;
`;
//# sourceMappingURL=index.jsx.map