Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const footerWithButtons_1 = (0, tslib_1.__importDefault)(require("./components/footerWithButtons"));
const headerWithHelp_1 = (0, tslib_1.__importDefault)(require("./components/headerWithHelp"));
function AwsLambdaFailureDetails({ lambdaFunctionFailures, successCount, }) {
    const baseDocsUrl = 'https://docs.sentry.io/product/integrations/cloud-monitoring/aws-lambda/';
    return (<react_1.Fragment>
      <headerWithHelp_1.default docsUrl={baseDocsUrl}/>
      <Wrapper>
        <div>
          <StyledCheckmark isCircled color="green300"/>
          <h3>
            {(0, locale_1.tn)('successfully updated %s function', 'successfully updated %s functions', successCount)}
          </h3>
        </div>
        <div>
          <StyledWarning color="red300"/>
          <h3>
            {(0, locale_1.tn)('Failed to update %s function', 'Failed to update %s functions', lambdaFunctionFailures.length)}
          </h3>
          <Troubleshooting>
            {(0, locale_1.tct)('See [link:Troubleshooting Docs]', {
            link: <externalLink_1.default href={baseDocsUrl + '#troubleshooting'}/>,
        })}
          </Troubleshooting>
        </div>
        <StyledPanel>{lambdaFunctionFailures.map(SingleFailure)}</StyledPanel>
      </Wrapper>
      <footerWithButtons_1.default buttonText={(0, locale_1.t)('Finish Setup')} href="?finish_pipeline=1"/>
    </react_1.Fragment>);
}
exports.default = AwsLambdaFailureDetails;
function SingleFailure(errorDetail) {
    return (<StyledRow key={errorDetail.name}>
      <span>{errorDetail.name}</span>
      <Error>{errorDetail.error}</Error>
    </StyledRow>);
}
const Wrapper = (0, styled_1.default)('div') `
  padding: 100px 50px 50px 50px;
`;
const StyledRow = (0, styled_1.default)(panels_1.PanelItem) `
  display: flex;
  flex-direction: column;
`;
const Error = (0, styled_1.default)('span') `
  color: ${p => p.theme.subText};
`;
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  overflow: hidden;
  margin-left: 34px;
`;
const Troubleshooting = (0, styled_1.default)('p') `
  margin-left: 34px;
`;
const StyledCheckmark = (0, styled_1.default)(icons_1.IconCheckmark) `
  float: left;
  margin-right: 10px;
  height: 24px;
  width: 24px;
`;
const StyledWarning = (0, styled_1.default)(icons_1.IconWarning) `
  float: left;
  margin-right: 10px;
  height: 24px;
  width: 24px;
`;
//# sourceMappingURL=awsLambdaFailureDetails.jsx.map