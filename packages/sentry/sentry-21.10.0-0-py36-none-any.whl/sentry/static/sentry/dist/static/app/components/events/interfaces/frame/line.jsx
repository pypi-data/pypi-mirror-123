Object.defineProperty(exports, "__esModule", { value: true });
exports.Line = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const scroll_to_element_1 = (0, tslib_1.__importDefault)(require("scroll-to-element"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const utils_1 = require("app/components/events/interfaces/debugMeta/utils");
const packageLink_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/packageLink"));
const packageStatus_1 = (0, tslib_1.__importStar)(require("app/components/events/interfaces/packageStatus"));
const togglableAddress_1 = (0, tslib_1.__importStar)(require("app/components/events/interfaces/togglableAddress"));
const types_1 = require("app/components/events/interfaces/types");
const stacktracePreview_1 = require("app/components/stacktracePreview");
const strictClick_1 = (0, tslib_1.__importDefault)(require("app/components/strictClick"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const debugMetaStore_1 = require("app/stores/debugMetaStore");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withSentryAppComponents_1 = (0, tslib_1.__importDefault)(require("app/utils/withSentryAppComponents"));
const context_1 = (0, tslib_1.__importDefault)(require("./context"));
const defaultTitle_1 = (0, tslib_1.__importDefault)(require("./defaultTitle"));
const symbol_1 = (0, tslib_1.__importStar)(require("./symbol"));
const utils_2 = require("./utils");
function makeFilter(addr, addrMode, image) {
    if (!(!addrMode || addrMode === 'abs') && image) {
        return `${image.debug_id}!${addr}`;
    }
    return addr;
}
class Line extends React.Component {
    constructor() {
        super(...arguments);
        // isExpanded can be initialized to true via parent component;
        // data synchronization is not important
        // https://facebook.github.io/react/tips/props-in-getInitialState-as-anti-pattern.html
        this.state = {
            isExpanded: this.props.isExpanded,
        };
        this.toggleContext = evt => {
            evt && evt.preventDefault();
            this.setState({
                isExpanded: !this.state.isExpanded,
            });
        };
        this.scrollToImage = event => {
            event.stopPropagation(); // to prevent collapsing if collapsible
            const { instructionAddr, addrMode } = this.props.data;
            if (instructionAddr) {
                debugMetaStore_1.DebugMetaActions.updateFilter(makeFilter(instructionAddr, addrMode, this.props.image));
            }
            (0, scroll_to_element_1.default)('#images-loaded');
        };
        this.preventCollapse = evt => {
            evt.stopPropagation();
        };
    }
    getPlatform() {
        var _a;
        // prioritize the frame platform but fall back to the platform
        // of the stack trace / exception
        return (0, utils_2.getPlatform)(this.props.data.platform, (_a = this.props.platform) !== null && _a !== void 0 ? _a : 'other');
    }
    isInlineFrame() {
        return (this.props.prevFrame &&
            this.getPlatform() === (this.props.prevFrame.platform || this.props.platform) &&
            this.props.data.instructionAddr === this.props.prevFrame.instructionAddr);
    }
    isExpandable() {
        const { registers, platform, emptySourceNotation, isOnlyFrame, data } = this.props;
        return (0, utils_2.isExpandable)({
            frame: data,
            registers,
            platform,
            emptySourceNotation,
            isOnlyFrame,
        });
    }
    shouldShowLinkToImage() {
        const { isHoverPreviewed, data } = this.props;
        const { symbolicatorStatus } = data;
        return (!!symbolicatorStatus &&
            symbolicatorStatus !== types_1.SymbolicatorStatus.UNKNOWN_IMAGE &&
            !isHoverPreviewed);
    }
    packageStatus() {
        // this is the status of image that belongs to this frame
        const { image } = this.props;
        if (!image) {
            return 'empty';
        }
        const combinedStatus = (0, utils_1.combineStatus)(image.debug_status, image.unwind_status);
        switch (combinedStatus) {
            case 'unused':
                return 'empty';
            case 'found':
                return 'success';
            default:
                return 'error';
        }
    }
    renderExpander() {
        if (!this.isExpandable()) {
            return null;
        }
        const { isHoverPreviewed } = this.props;
        const { isExpanded } = this.state;
        return (<ToggleContextButtonWrapper>
        <ToggleContextButton className="btn-toggle" data-test-id={`toggle-button-${isExpanded ? 'expanded' : 'collapsed'}`} css={(0, utils_2.isDotnet)(this.getPlatform()) && { display: 'block !important' }} // remove important once we get rid of css files
         title={(0, locale_1.t)('Toggle Context')} tooltipProps={isHoverPreviewed ? { delay: stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY } : undefined} onClick={this.toggleContext}>
          <icons_1.IconChevron direction={isExpanded ? 'up' : 'down'} size="8px"/>
        </ToggleContextButton>
      </ToggleContextButtonWrapper>);
    }
    leadsToApp() {
        const { data, nextFrame } = this.props;
        return !data.inApp && ((nextFrame && nextFrame.inApp) || !nextFrame);
    }
    isFoundByStackScanning() {
        const { data } = this.props;
        return data.trust === 'scan' || data.trust === 'cfi-scan';
    }
    renderLeadHint() {
        const { isExpanded } = this.state;
        if (isExpanded) {
            return null;
        }
        const leadsToApp = this.leadsToApp();
        if (!leadsToApp) {
            return null;
        }
        const { nextFrame } = this.props;
        return !nextFrame ? (<LeadHint className="leads-to-app-hint" width="115px">
        {(0, locale_1.t)('Crashed in non-app')}
        {': '}
      </LeadHint>) : (<LeadHint className="leads-to-app-hint">
        {(0, locale_1.t)('Called from')}
        {': '}
      </LeadHint>);
    }
    renderRepeats() {
        const timesRepeated = this.props.timesRepeated;
        if (timesRepeated && timesRepeated > 0) {
            return (<RepeatedFrames title={`Frame repeated ${timesRepeated} time${timesRepeated === 1 ? '' : 's'}`}>
          <RepeatedContent>
            <StyledIconRefresh />
            <span>{timesRepeated}</span>
          </RepeatedContent>
        </RepeatedFrames>);
        }
        return null;
    }
    renderDefaultLine() {
        var _a;
        const { isHoverPreviewed } = this.props;
        return (<strictClick_1.default onClick={this.isExpandable() ? this.toggleContext : undefined}>
        <DefaultLine className="title" data-test-id="title">
          <VertCenterWrapper>
            <div>
              {this.renderLeadHint()}
              <defaultTitle_1.default frame={this.props.data} platform={(_a = this.props.platform) !== null && _a !== void 0 ? _a : 'other'} isHoverPreviewed={isHoverPreviewed}/>
            </div>
            {this.renderRepeats()}
          </VertCenterWrapper>
          {this.renderExpander()}
        </DefaultLine>
      </strictClick_1.default>);
    }
    renderNativeLine() {
        const { data, showingAbsoluteAddress, onAddressToggle, onFunctionNameToggle, image, maxLengthOfRelativeAddress, includeSystemFrames, isFrameAfterLastNonApp, showCompleteFunctionName, isHoverPreviewed, } = this.props;
        const leadHint = this.renderLeadHint();
        const packageStatus = this.packageStatus();
        return (<strictClick_1.default onClick={this.isExpandable() ? this.toggleContext : undefined}>
        <DefaultLine className="title as-table" data-test-id="title">
          <NativeLineContent isFrameAfterLastNonApp={!!isFrameAfterLastNonApp}>
            <PackageInfo>
              {leadHint}
              <packageLink_1.default includeSystemFrames={!!includeSystemFrames} withLeadHint={leadHint !== null} packagePath={data.package} onClick={this.scrollToImage} isClickable={this.shouldShowLinkToImage()} isHoverPreviewed={isHoverPreviewed}>
                {!isHoverPreviewed && (<packageStatus_1.default status={packageStatus} tooltip={(0, locale_1.t)('Go to Images Loaded')}/>)}
              </packageLink_1.default>
            </PackageInfo>
            {data.instructionAddr && (<togglableAddress_1.default address={data.instructionAddr} startingAddress={image ? image.image_addr : null} isAbsolute={!!showingAbsoluteAddress} isFoundByStackScanning={this.isFoundByStackScanning()} isInlineFrame={!!this.isInlineFrame()} onToggle={onAddressToggle} relativeAddressMaxlength={maxLengthOfRelativeAddress} isHoverPreviewed={isHoverPreviewed}/>)}
            <symbol_1.default frame={data} showCompleteFunctionName={!!showCompleteFunctionName} onFunctionNameToggle={onFunctionNameToggle} isHoverPreviewed={isHoverPreviewed}/>
          </NativeLineContent>
          {this.renderExpander()}
        </DefaultLine>
      </strictClick_1.default>);
    }
    renderLine() {
        switch (this.getPlatform()) {
            case 'objc':
            // fallthrough
            case 'cocoa':
            // fallthrough
            case 'native':
                return this.renderNativeLine();
            default:
                return this.renderDefaultLine();
        }
    }
    render() {
        const data = this.props.data;
        const className = (0, classnames_1.default)({
            frame: true,
            'is-expandable': this.isExpandable(),
            expanded: this.state.isExpanded,
            collapsed: !this.state.isExpanded,
            'system-frame': !data.inApp,
            'frame-errors': data.errors,
            'leads-to-app': this.leadsToApp(),
        });
        const props = { className };
        return (<StyledLi {...props}>
        {this.renderLine()}
        <context_1.default frame={data} event={this.props.event} registers={this.props.registers} components={this.props.components} hasContextSource={(0, utils_2.hasContextSource)(data)} hasContextVars={(0, utils_2.hasContextVars)(data)} hasContextRegisters={(0, utils_2.hasContextRegisters)(this.props.registers)} emptySourceNotation={this.props.emptySourceNotation} hasAssembly={(0, utils_2.hasAssembly)(data, this.props.platform)} expandable={this.isExpandable()} isExpanded={this.state.isExpanded}/>
      </StyledLi>);
    }
}
exports.Line = Line;
Line.defaultProps = {
    isExpanded: false,
    emptySourceNotation: false,
    isHoverPreviewed: false,
};
exports.default = (0, withOrganization_1.default)((0, withSentryAppComponents_1.default)(Line, { componentType: 'stacktrace-link' }));
const PackageInfo = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto 1fr;
  order: 2;
  align-items: flex-start;
  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    order: 0;
  }
`;
const RepeatedFrames = (0, styled_1.default)('div') `
  display: inline-block;
  border-radius: 50px;
  padding: 1px 3px;
  margin-left: ${(0, space_1.default)(1)};
  border-width: thin;
  border-style: solid;
  border-color: ${p => p.theme.orange500};
  color: ${p => p.theme.orange500};
  background-color: ${p => p.theme.backgroundSecondary};
  white-space: nowrap;
`;
const VertCenterWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const RepeatedContent = (0, styled_1.default)(VertCenterWrapper) `
  justify-content: center;
`;
const NativeLineContent = (0, styled_1.default)('div') `
  display: grid;
  flex: 1;
  grid-gap: ${(0, space_1.default)(0.5)};
  grid-template-columns: ${p => `minmax(${p.isFrameAfterLastNonApp ? '167px' : '117px'}, auto)  1fr`};
  align-items: center;
  justify-content: flex-start;

  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    grid-template-columns:
      ${p => (p.isFrameAfterLastNonApp ? '200px' : '150px')} minmax(117px, auto)
      1fr;
  }

  @media (min-width: ${props => props.theme.breakpoints[2]}) and (max-width: ${props => props.theme.breakpoints[3]}) {
    grid-template-columns:
      ${p => (p.isFrameAfterLastNonApp ? '180px' : '140px')} minmax(117px, auto)
      1fr;
  }
`;
const DefaultLine = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
`;
const StyledIconRefresh = (0, styled_1.default)(icons_1.IconRefresh) `
  margin-right: ${(0, space_1.default)(0.25)};
`;
const LeadHint = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
  max-width: ${p => (p.width ? p.width : '67px')}
`;
const ToggleContextButtonWrapper = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(1)};
`;
// the Button's label has the padding of 3px because the button size has to be 16x16 px.
const ToggleContextButton = (0, styled_1.default)(button_1.default) `
  span:first-child {
    padding: 3px;
  }
`;
const StyledLi = (0, styled_1.default)('li') `
  ${packageStatus_1.PackageStatusIcon} {
    flex-shrink: 0;
  }
  :hover {
    ${packageStatus_1.PackageStatusIcon} {
      visibility: visible;
    }
    ${togglableAddress_1.AddressToggleIcon} {
      visibility: visible;
    }
    ${symbol_1.FunctionNameToggleIcon} {
      visibility: visible;
    }
  }
`;
//# sourceMappingURL=line.jsx.map