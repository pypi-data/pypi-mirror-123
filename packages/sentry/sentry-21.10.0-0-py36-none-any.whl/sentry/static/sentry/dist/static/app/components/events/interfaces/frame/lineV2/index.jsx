Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const packageStatus_1 = require("app/components/events/interfaces/packageStatus");
const togglableAddress_1 = require("app/components/events/interfaces/togglableAddress");
const strictClick_1 = (0, tslib_1.__importDefault)(require("app/components/strictClick"));
const withSentryAppComponents_1 = (0, tslib_1.__importDefault)(require("app/utils/withSentryAppComponents"));
const context_1 = (0, tslib_1.__importDefault)(require("../context"));
const symbol_1 = require("../symbol");
const utils_1 = require("../utils");
const default_1 = (0, tslib_1.__importDefault)(require("./default"));
const native_1 = (0, tslib_1.__importDefault)(require("./native"));
function Line(_a) {
    var _b, _c, _d;
    var { frame, nextFrame, prevFrame, timesRepeated, includeSystemFrames, onAddressToggle, onFunctionNameToggle, showingAbsoluteAddress, showCompleteFunctionName, isFrameAfterLastNonApp, isUsedForGrouping, maxLengthOfRelativeAddress, image, registers, isOnlyFrame, event, components, emptySourceNotation = false, 
    /**
     * Is the stack trace being previewed in a hovercard?
     */
    isHoverPreviewed = false } = _a, props = (0, tslib_1.__rest)(_a, ["frame", "nextFrame", "prevFrame", "timesRepeated", "includeSystemFrames", "onAddressToggle", "onFunctionNameToggle", "showingAbsoluteAddress", "showCompleteFunctionName", "isFrameAfterLastNonApp", "isUsedForGrouping", "maxLengthOfRelativeAddress", "image", "registers", "isOnlyFrame", "event", "components", "emptySourceNotation", "isHoverPreviewed"]);
    /* Prioritize the frame platform but fall back to the platform
     of the stack trace / exception */
    const platform = (0, utils_1.getPlatform)(frame.platform, (_b = props.platform) !== null && _b !== void 0 ? _b : 'other');
    const leadsToApp = !frame.inApp && ((nextFrame && nextFrame.inApp) || !nextFrame);
    const expandable = !leadsToApp || includeSystemFrames
        ? (0, utils_1.isExpandable)({
            frame,
            registers,
            platform,
            emptySourceNotation,
            isOnlyFrame,
        })
        : false;
    const [isExpanded, setIsExpanded] = (0, react_1.useState)(expandable ? (_c = props.isExpanded) !== null && _c !== void 0 ? _c : false : false);
    function toggleContext(evt) {
        evt.preventDefault();
        setIsExpanded(!isExpanded);
    }
    function renderLine() {
        switch (platform) {
            case 'objc':
            // fallthrough
            case 'cocoa':
            // fallthrough
            case 'native':
                return (<native_1.default leadsToApp={leadsToApp} frame={frame} prevFrame={prevFrame} nextFrame={nextFrame} isHoverPreviewed={isHoverPreviewed} platform={platform} isExpanded={isExpanded} isExpandable={expandable} onAddressToggle={onAddressToggle} onFunctionNameToggle={onFunctionNameToggle} includeSystemFrames={includeSystemFrames} showingAbsoluteAddress={showingAbsoluteAddress} showCompleteFunctionName={showCompleteFunctionName} isFrameAfterLastNonApp={isFrameAfterLastNonApp} onToggleContext={toggleContext} image={image} maxLengthOfRelativeAddress={maxLengthOfRelativeAddress} isUsedForGrouping={isUsedForGrouping}/>);
            default:
                return (<default_1.default leadsToApp={leadsToApp} frame={frame} nextFrame={nextFrame} timesRepeated={timesRepeated} isHoverPreviewed={isHoverPreviewed} platform={platform} isExpanded={isExpanded} isExpandable={expandable} onToggleContext={toggleContext} isUsedForGrouping={isUsedForGrouping}/>);
        }
    }
    const className = (0, classnames_1.default)({
        frame: true,
        'is-expandable': expandable,
        expanded: isExpanded,
        collapsed: !isExpanded,
        'system-frame': !frame.inApp,
        'frame-errors': !!((_d = frame.errors) !== null && _d !== void 0 ? _d : []).length,
        'leads-to-app': leadsToApp,
    });
    return (<StyledLi className={className}>
      <strictClick_1.default onClick={expandable ? toggleContext : undefined}>
        {renderLine()}
      </strictClick_1.default>
      <context_1.default frame={frame} event={event} registers={registers} components={components} hasContextSource={(0, utils_1.hasContextSource)(frame)} hasContextVars={(0, utils_1.hasContextVars)(frame)} hasContextRegisters={(0, utils_1.hasContextRegisters)(registers)} emptySourceNotation={emptySourceNotation} hasAssembly={(0, utils_1.hasAssembly)(frame, platform)} expandable={expandable} isExpanded={isExpanded}/>
    </StyledLi>);
}
exports.default = (0, withSentryAppComponents_1.default)(Line, { componentType: 'stacktrace-link' });
const StyledLi = (0, styled_1.default)('li') `
  overflow: hidden;

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
//# sourceMappingURL=index.jsx.map