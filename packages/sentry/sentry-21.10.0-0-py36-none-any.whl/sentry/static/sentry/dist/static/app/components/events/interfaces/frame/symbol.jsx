Object.defineProperty(exports, "__esModule", { value: true });
exports.FunctionNameToggleIcon = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const stacktracePreview_1 = require("app/components/stacktracePreview");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const functionName_1 = (0, tslib_1.__importDefault)(require("./functionName"));
const groupingIndicator_1 = (0, tslib_1.__importDefault)(require("./groupingIndicator"));
const utils_2 = require("./utils");
const Symbol = ({ frame, onFunctionNameToggle, showCompleteFunctionName, isHoverPreviewed, isUsedForGrouping, className, }) => {
    const hasFunctionNameHiddenDetails = (0, utils_1.defined)(frame.rawFunction) &&
        (0, utils_1.defined)(frame.function) &&
        frame.function !== frame.rawFunction;
    const getFunctionNameTooltipTitle = () => {
        if (!hasFunctionNameHiddenDetails) {
            return undefined;
        }
        if (!showCompleteFunctionName) {
            return (0, locale_1.t)('Expand function details');
        }
        return (0, locale_1.t)('Hide function details');
    };
    const [hint, hintIcon] = (0, utils_2.getFrameHint)(frame);
    const enablePathTooltip = (0, utils_1.defined)(frame.absPath) && frame.absPath !== frame.filename;
    const functionNameTooltipTitle = getFunctionNameTooltipTitle();
    const tooltipDelay = isHoverPreviewed ? stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY : undefined;
    return (<Wrapper className={className}>
      <FunctionNameToggleTooltip title={functionNameTooltipTitle} containerDisplayMode="inline-flex" delay={tooltipDelay}>
        <exports.FunctionNameToggleIcon hasFunctionNameHiddenDetails={hasFunctionNameHiddenDetails} onClick={hasFunctionNameHiddenDetails ? onFunctionNameToggle : undefined} size="xs" color="purple300"/>
      </FunctionNameToggleTooltip>
      <Data>
        <StyledFunctionName frame={frame} showCompleteFunctionName={showCompleteFunctionName} hasHiddenDetails={hasFunctionNameHiddenDetails}/>
        {hint && (<HintStatus>
            <tooltip_1.default title={hint} delay={tooltipDelay}>
              {hintIcon}
            </tooltip_1.default>
          </HintStatus>)}
        {frame.filename && (<FileNameTooltip title={frame.absPath} disabled={!enablePathTooltip} delay={tooltipDelay}>
            <Filename>
              {'('}
              {frame.filename}
              {frame.lineNo && `:${frame.lineNo}`}
              {')'}
            </Filename>
          </FileNameTooltip>)}
        {isUsedForGrouping && <groupingIndicator_1.default />}
      </Data>
    </Wrapper>);
};
const Wrapper = (0, styled_1.default)('div') `
  text-align: left;
  grid-column-start: 1;
  grid-column-end: -1;
  order: 3;
  flex: 1;

  display: flex;

  code {
    background: transparent;
    color: ${p => p.theme.textColor};
    padding-right: ${(0, space_1.default)(0.5)};
  }

  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    order: 0;
    grid-column-start: auto;
    grid-column-end: auto;
  }
`;
const StyledFunctionName = (0, styled_1.default)(functionName_1.default) `
  margin-right: ${(0, space_1.default)(0.75)};
`;
const Data = (0, styled_1.default)('div') `
  max-width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
`;
const HintStatus = (0, styled_1.default)('span') `
  position: relative;
  top: ${(0, space_1.default)(0.25)};
  margin: 0 ${(0, space_1.default)(0.75)} 0 -${(0, space_1.default)(0.25)};
`;
const FileNameTooltip = (0, styled_1.default)(tooltip_1.default) `
  margin-right: ${(0, space_1.default)(0.75)};
`;
const Filename = (0, styled_1.default)('span') `
  color: ${p => p.theme.purple300};
`;
exports.FunctionNameToggleIcon = (0, styled_1.default)(icons_1.IconFilter, {
    shouldForwardProp: prop => prop !== 'hasFunctionNameHiddenDetails',
}) `
  cursor: pointer;
  visibility: hidden;
  display: none;
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: block;
  }
  ${p => !p.hasFunctionNameHiddenDetails && 'opacity: 0; cursor: inherit;'};
`;
const FunctionNameToggleTooltip = (0, styled_1.default)(tooltip_1.default) `
  height: 16px;
  align-items: center;
  margin-right: ${(0, space_1.default)(0.75)};
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: none;
  }
`;
exports.default = Symbol;
//# sourceMappingURL=symbol.jsx.map