Object.defineProperty(exports, "__esModule", { value: true });
exports.Trend = exports.Score = exports.ScoreWrapper = exports.HeaderTitle = exports.ScorePanel = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
function ScoreCard({ title, score, help, trend, trendStatus, className }) {
    return (<exports.ScorePanel className={className}>
      <exports.HeaderTitle>
        <Title>{title}</Title>
        {help && <questionTooltip_1.default title={help} size="sm" position="top"/>}
      </exports.HeaderTitle>

      <exports.ScoreWrapper>
        <exports.Score>{score !== null && score !== void 0 ? score : '\u2014'}</exports.Score>
        {(0, utils_1.defined)(trend) && (<exports.Trend trendStatus={trendStatus}>
            <textOverflow_1.default>{trend}</textOverflow_1.default>
          </exports.Trend>)}
      </exports.ScoreWrapper>
    </exports.ScorePanel>);
}
function getTrendColor(p) {
    switch (p.trendStatus) {
        case 'good':
            return p.theme.green300;
        case 'bad':
            return p.theme.red300;
        default:
            return p.theme.gray300;
    }
}
exports.ScorePanel = (0, styled_1.default)(panels_1.Panel) `
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)};
  min-height: 96px;
`;
exports.HeaderTitle = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  width: fit-content;
`;
const Title = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default};
`;
exports.ScoreWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  max-width: 100%;
`;
exports.Score = (0, styled_1.default)('span') `
  flex-shrink: 1;
  font-size: 32px;
  line-height: 1;
  white-space: nowrap;
`;
exports.Trend = (0, styled_1.default)('div') `
  color: ${getTrendColor};
  margin-left: ${(0, space_1.default)(1)};
  line-height: 1;
  overflow: hidden;
`;
exports.default = ScoreCard;
//# sourceMappingURL=scoreCard.jsx.map