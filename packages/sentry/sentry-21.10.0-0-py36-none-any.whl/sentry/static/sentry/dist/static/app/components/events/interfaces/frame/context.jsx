Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const assembly_1 = require("app/components/events/interfaces/assembly");
const contextLine_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/contextLine"));
const frameRegisters_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/frameRegisters"));
const frameVariables_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/frameVariables"));
const openInContextLine_1 = require("app/components/events/interfaces/openInContextLine");
const stacktraceLink_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/stacktraceLink"));
const utils_1 = require("app/components/events/interfaces/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const Context = ({ hasContextVars = false, hasContextSource = false, hasContextRegisters = false, isExpanded = false, hasAssembly = false, expandable = false, emptySourceNotation = false, registers, components, frame, event, organization, }) => {
    var _a, _b;
    if (!hasContextSource && !hasContextVars && !hasContextRegisters && !hasAssembly) {
        return emptySourceNotation ? (<div className="empty-context">
        <StyledIconFlag size="xs"/>
        <p>{(0, locale_1.t)('No additional details are available for this frame.')}</p>
      </div>) : null;
    }
    const getContextLines = () => {
        if (isExpanded) {
            return frame.context;
        }
        return frame.context.filter(l => l[0] === frame.lineNo);
    };
    const contextLines = getContextLines();
    const startLineNo = hasContextSource ? frame.context[0][0] : undefined;
    return (<ol start={startLineNo} className={`context ${isExpanded ? 'expanded' : ''}`}>
      {(0, utils_2.defined)(frame.errors) && (<li className={expandable ? 'expandable error' : 'error'} key="errors">
          {frame.errors.join(', ')}
        </li>)}

      {frame.context &&
            contextLines.map((line, index) => {
                const isActive = frame.lineNo === line[0];
                const hasComponents = isActive && components.length > 0;
                return (<StyledContextLine key={index} line={line} isActive={isActive}>
              {hasComponents && (<errorBoundary_1.default mini>
                  <openInContextLine_1.OpenInContextLine key={index} lineNo={line[0]} filename={frame.filename || ''} components={components}/>
                </errorBoundary_1.default>)}
              {(organization === null || organization === void 0 ? void 0 : organization.features.includes('integrations-stacktrace-link')) &&
                        isActive &&
                        isExpanded &&
                        frame.inApp &&
                        frame.filename && (<errorBoundary_1.default customComponent={null}>
                    <stacktraceLink_1.default key={index} lineNo={line[0]} frame={frame} event={event}/>
                  </errorBoundary_1.default>)}
            </StyledContextLine>);
            })}

      {(hasContextRegisters || hasContextVars) && (<StyledClippedBox clipHeight={100}>
          {hasContextRegisters && (<frameRegisters_1.default registers={registers} deviceArch={(_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.device) === null || _b === void 0 ? void 0 : _b.arch}/>)}
          {hasContextVars && <frameVariables_1.default data={frame.vars || {}}/>}
        </StyledClippedBox>)}

      {hasAssembly && (<assembly_1.Assembly {...(0, utils_1.parseAssembly)(frame.package)} filePath={frame.absPath}/>)}
    </ol>);
};
exports.default = (0, withOrganization_1.default)(Context);
const StyledClippedBox = (0, styled_1.default)(clippedBox_1.default) `
  margin-left: 0;
  margin-right: 0;

  &:first-of-type {
    margin-top: 0;
  }

  :first-child {
    margin-top: -${(0, space_1.default)(3)};
  }

  > *:first-child {
    padding-top: 0;
    border-top: none;
  }
`;
const StyledIconFlag = (0, styled_1.default)(icons_1.IconFlag) `
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledContextLine = (0, styled_1.default)(contextLine_1.default) `
  background: inherit;
  padding: 0;
  text-indent: 20px;
  z-index: 1000;
`;
//# sourceMappingURL=context.jsx.map