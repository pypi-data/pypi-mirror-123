Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const projectApdexScoreCard_1 = (0, tslib_1.__importDefault)(require("./projectApdexScoreCard"));
const projectStabilityScoreCard_1 = (0, tslib_1.__importDefault)(require("./projectStabilityScoreCard"));
const projectVelocityScoreCard_1 = (0, tslib_1.__importDefault)(require("./projectVelocityScoreCard"));
function ProjectScoreCards({ organization, selection, isProjectStabilized, hasSessions, hasTransactions, query, }) {
    return (<CardWrapper>
      <projectStabilityScoreCard_1.default organization={organization} selection={selection} isProjectStabilized={isProjectStabilized} hasSessions={hasSessions} query={query}/>

      <projectVelocityScoreCard_1.default organization={organization} selection={selection} isProjectStabilized={isProjectStabilized} query={query}/>

      <projectApdexScoreCard_1.default organization={organization} selection={selection} isProjectStabilized={isProjectStabilized} hasTransactions={hasTransactions} query={query}/>
    </CardWrapper>);
}
const CardWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  grid-column-gap: ${(0, space_1.default)(2)};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(3, 1fr);
  }
`;
exports.default = ProjectScoreCards;
//# sourceMappingURL=projectScoreCards.jsx.map