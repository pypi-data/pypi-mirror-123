Object.defineProperty(exports, "__esModule", { value: true });
exports.SectionContents = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const styles_1 = require("app/components/events/styles");
const iconAnchor_1 = require("app/icons/iconAnchor");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const defaultProps = {
    wrapTitle: true,
    raw: false,
    isCentered: false,
    showPermalink: true,
};
class EventDataSection extends React.Component {
    constructor() {
        super(...arguments);
        this.dataSectionDOMRef = React.createRef();
    }
    componentDidMount() {
        const dataSectionDOM = this.dataSectionDOMRef.current;
        if (location.hash && dataSectionDOM) {
            const [, hash] = location.hash.split('#');
            try {
                const anchorElement = hash && dataSectionDOM.querySelector('div#' + hash);
                if (anchorElement) {
                    anchorElement.scrollIntoView();
                }
            }
            catch (_a) {
                // Since we're blindly taking the hash from the url and shoving
                // it into a querySelector, it's possible that this may
                // raise an exception if the input is invalid. So let's just ignore
                // this instead of blowing up.
                // e.g. `document.querySelector('div#=')`
                // > Uncaught DOMException: Failed to execute 'querySelector' on 'Document': 'div#=' is not a valid selector.
            }
        }
    }
    render() {
        const _a = this.props, { children, className, type, title, toggleRaw, raw, wrapTitle, actions, isCentered, showPermalink } = _a, props = (0, tslib_1.__rest)(_a, ["children", "className", "type", "title", "toggleRaw", "raw", "wrapTitle", "actions", "isCentered", "showPermalink"]);
        const titleNode = wrapTitle ? <h3>{title}</h3> : title;
        return (<styles_1.DataSection ref={this.dataSectionDOMRef} className={className || ''} {...props}>
        {title && (<SectionHeader id={type} isCentered={isCentered}>
            <Title>
              {showPermalink ? (<Permalink href={'#' + type} className="permalink">
                  <StyledIconAnchor />
                  {titleNode}
                </Permalink>) : (<div>{titleNode}</div>)}
            </Title>
            {type === 'extra' && (<buttonBar_1.default merged active={raw ? 'raw' : 'formatted'}>
                <button_1.default barId="formatted" size="xsmall" onClick={() => (0, callIfFunction_1.callIfFunction)(toggleRaw, false)}>
                  {(0, locale_1.t)('Formatted')}
                </button_1.default>
                <button_1.default barId="raw" size="xsmall" onClick={() => (0, callIfFunction_1.callIfFunction)(toggleRaw, true)}>
                  {(0, locale_1.t)('Raw')}
                </button_1.default>
              </buttonBar_1.default>)}
            {actions && <ActionContainer>{actions}</ActionContainer>}
          </SectionHeader>)}
        <exports.SectionContents>{children}</exports.SectionContents>
      </styles_1.DataSection>);
    }
}
EventDataSection.defaultProps = defaultProps;
const Title = (0, styled_1.default)('div') `
  display: flex;
`;
const StyledIconAnchor = (0, styled_1.default)(iconAnchor_1.IconAnchor) `
  display: none;
  position: absolute;
  top: 4px;
  left: -22px;
`;
const Permalink = (0, styled_1.default)('a') `
  :hover ${StyledIconAnchor} {
    display: block;
    color: ${p => p.theme.gray300};
  }
`;
const SectionHeader = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(1)};

  > * {
    margin-bottom: ${(0, space_1.default)(0.5)};
  }

  & h3,
  & h3 a {
    font-size: 14px;
    font-weight: 600;
    line-height: 1.2;
    color: ${p => p.theme.gray300};
  }

  & h3 {
    font-size: 14px;
    font-weight: 600;
    line-height: 1.2;
    padding: ${(0, space_1.default)(0.75)} 0;
    margin-bottom: 0;
    text-transform: uppercase;
  }

  & small {
    color: ${p => p.theme.textColor};
    font-size: ${p => p.theme.fontSizeMedium};
    margin-right: ${(0, space_1.default)(0.5)};
    margin-left: ${(0, space_1.default)(0.5)};

    text-transform: none;
  }
  & small > span {
    color: ${p => p.theme.textColor};
    border-bottom: 1px dotted ${p => p.theme.border};
    font-weight: normal;
  }

  @media (min-width: ${props => props.theme.breakpoints[2]}) {
    & > small {
      margin-left: ${(0, space_1.default)(1)};
      display: inline-block;
    }
  }

  ${p => p.isCentered &&
    (0, react_1.css) `
      align-items: center;
      @media (max-width: ${p.theme.breakpoints[0]}) {
        display: block;
      }
    `}

  >*:first-child {
    position: relative;
    flex-grow: 1;
  }
`;
exports.SectionContents = (0, styled_1.default)('div') `
  position: relative;
`;
const ActionContainer = (0, styled_1.default)('div') `
  flex-shrink: 0;
  max-width: 100%;
`;
exports.default = EventDataSection;
//# sourceMappingURL=eventDataSection.jsx.map