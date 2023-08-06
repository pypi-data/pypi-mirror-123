Object.defineProperty(exports, "__esModule", { value: true });
exports.PackageName = exports.Package = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/components/events/interfaces/frame/utils");
const stacktracePreview_1 = require("app/components/stacktracePreview");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
class PackageLink extends React.Component {
    constructor() {
        super(...arguments);
        this.handleClick = (event) => {
            const { isClickable, onClick } = this.props;
            if (isClickable) {
                onClick(event);
            }
        };
    }
    render() {
        const { packagePath, isClickable, withLeadHint, children, includeSystemFrames, isHoverPreviewed, } = this.props;
        return (<exports.Package onClick={this.handleClick} isClickable={isClickable} withLeadHint={withLeadHint} includeSystemFrames={includeSystemFrames}>
        {(0, utils_2.defined)(packagePath) ? (<tooltip_1.default title={packagePath} delay={isHoverPreviewed ? stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY : undefined}>
            <exports.PackageName isClickable={isClickable} withLeadHint={withLeadHint} includeSystemFrames={includeSystemFrames}>
              {(0, utils_1.trimPackage)(packagePath)}
            </exports.PackageName>
          </tooltip_1.default>) : (<span>{'<unknown>'}</span>)}
        {children}
      </exports.Package>);
    }
}
exports.Package = (0, styled_1.default)('a') `
  font-size: 13px;
  font-weight: bold;
  padding: 0 0 0 ${(0, space_1.default)(0.5)};
  color: ${p => p.theme.textColor};
  :hover {
    color: ${p => p.theme.textColor};
  }
  cursor: ${p => (p.isClickable ? 'pointer' : 'default')};
  display: flex;
  align-items: center;

  ${p => p.withLeadHint && (p.includeSystemFrames ? `max-width: 89px;` : `max-width: 76px;`)}

  @media (min-width: ${p => p.theme.breakpoints[2]}) and (max-width: ${p => p.theme.breakpoints[3]}) {
    ${p => p.withLeadHint && (p.includeSystemFrames ? `max-width: 76px;` : `max-width: 63px;`)}
  }
`;
exports.PackageName = (0, styled_1.default)('span') `
  max-width: ${p => p.withLeadHint && p.isClickable && !p.includeSystemFrames ? '45px' : '104px'};
  ${overflowEllipsis_1.default}
`;
exports.default = PackageLink;
//# sourceMappingURL=packageLink.jsx.map