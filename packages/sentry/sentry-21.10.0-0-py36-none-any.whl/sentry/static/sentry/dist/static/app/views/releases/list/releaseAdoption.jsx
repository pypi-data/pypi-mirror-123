Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const progressBar_1 = (0, tslib_1.__importDefault)(require("app/components/progressBar"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("../utils");
function ReleaseAdoption({ adoption, releaseCount, projectCount, displayOption, withLabels, }) {
    const theme = (0, react_1.useTheme)();
    return (<div>
      {withLabels && (<Labels>
          <textOverflow_1.default>
            <count_1.default value={releaseCount}/>/<count_1.default value={projectCount}/>{' '}
            {(0, utils_1.releaseDisplayLabel)(displayOption, projectCount)}
          </textOverflow_1.default>

          <span>{!adoption ? 0 : adoption < 1 ? '<1' : Math.round(adoption)}%</span>
        </Labels>)}

      <tooltip_1.default containerDisplayMode="block" popperStyle={{
            background: theme.gray500,
            maxWidth: '300px',
        }} title={<TooltipWrapper>
            <TooltipRow>
              <Title>
                <Dot color={theme.progressBar}/>
                {(0, locale_1.t)('This Release')}
              </Title>
              <Value>
                <count_1.default value={releaseCount}/>{' '}
                {(0, utils_1.releaseDisplayLabel)(displayOption, releaseCount)}
              </Value>
            </TooltipRow>
            <TooltipRow>
              <Title>
                <Dot color={theme.progressBackground}/>
                {(0, locale_1.t)('Total Project')}
              </Title>
              <Value>
                <count_1.default value={projectCount}/>{' '}
                {(0, utils_1.releaseDisplayLabel)(displayOption, projectCount)}
              </Value>
            </TooltipRow>
            <Divider />

            <Time>{(0, locale_1.t)('Last 24 hours')}</Time>
          </TooltipWrapper>}>
        <ProgressBarWrapper>
          <progressBar_1.default value={Math.ceil(adoption)}/>
        </ProgressBarWrapper>
      </tooltip_1.default>
    </div>);
}
const Labels = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-template-columns: 1fr max-content;
`;
const TooltipWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(0.75)};
  font-size: ${p => p.theme.fontSizeMedium};
  line-height: 21px;
  font-weight: normal;
`;
const TooltipRow = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto auto;
  grid-gap: ${(0, space_1.default)(3)};
  justify-content: space-between;
  padding-bottom: ${(0, space_1.default)(0.25)};
`;
const Title = (0, styled_1.default)('div') `
  text-align: left;
`;
const Dot = (0, styled_1.default)('div') `
  display: inline-block;
  margin-right: ${(0, space_1.default)(0.75)};
  border-radius: 10px;
  width: 10px;
  height: 10px;
  background-color: ${p => p.color};
`;
const Value = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  text-align: right;
`;
const Divider = (0, styled_1.default)('div') `
  border-top: 1px solid ${p => p.theme.gray400};
  margin: ${(0, space_1.default)(0.75)} -${(0, space_1.default)(2)} ${(0, space_1.default)(1)};
`;
const Time = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  text-align: center;
`;
const ProgressBarWrapper = (0, styled_1.default)('div') `
  /* A bit of padding makes hovering for tooltip easier */
  padding: ${(0, space_1.default)(0.5)} 0;
`;
exports.default = ReleaseAdoption;
//# sourceMappingURL=releaseAdoption.jsx.map