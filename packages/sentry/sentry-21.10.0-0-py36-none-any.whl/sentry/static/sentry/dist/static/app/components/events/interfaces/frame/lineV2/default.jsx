Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const iconRefresh_1 = require("app/icons/iconRefresh");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const defaultTitle_1 = (0, tslib_1.__importDefault)(require("../defaultTitle"));
const expander_1 = (0, tslib_1.__importDefault)(require("./expander"));
const leadHint_1 = (0, tslib_1.__importDefault)(require("./leadHint"));
const wrapper_1 = (0, tslib_1.__importDefault)(require("./wrapper"));
function Default(_a) {
    var { frame, nextFrame, isHoverPreviewed, isExpanded, platform, timesRepeated, isUsedForGrouping, leadsToApp, onMouseDown, onClick } = _a, props = (0, tslib_1.__rest)(_a, ["frame", "nextFrame", "isHoverPreviewed", "isExpanded", "platform", "timesRepeated", "isUsedForGrouping", "leadsToApp", "onMouseDown", "onClick"]);
    function renderRepeats() {
        if ((0, utils_1.defined)(timesRepeated) && timesRepeated > 0) {
            return (<RepeatedFrames title={(0, locale_1.tn)('Frame repeated %s time', 'Frame repeated %s times', timesRepeated)}>
          <RepeatedContent>
            <StyledIconRefresh />
            <span>{timesRepeated}</span>
          </RepeatedContent>
        </RepeatedFrames>);
        }
        return null;
    }
    return (<wrapper_1.default className="title" onMouseDown={onMouseDown} onClick={onClick}>
      <VertCenterWrapper>
        <Title>
          <leadHint_1.default isExpanded={isExpanded} nextFrame={nextFrame} leadsToApp={leadsToApp}/>
          <defaultTitle_1.default frame={frame} platform={platform} isHoverPreviewed={isHoverPreviewed} isUsedForGrouping={isUsedForGrouping}/>
        </Title>
        {renderRepeats()}
      </VertCenterWrapper>
      <expander_1.default isExpanded={isExpanded} isHoverPreviewed={isHoverPreviewed} platform={platform} {...props}/>
    </wrapper_1.default>);
}
exports.default = Default;
const VertCenterWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const Title = (0, styled_1.default)('div') `
  > * {
    vertical-align: middle;
    line-height: 1;
  }
`;
const RepeatedContent = (0, styled_1.default)(VertCenterWrapper) `
  justify-content: center;
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
const StyledIconRefresh = (0, styled_1.default)(iconRefresh_1.IconRefresh) `
  margin-right: ${(0, space_1.default)(0.25)};
`;
//# sourceMappingURL=default.jsx.map