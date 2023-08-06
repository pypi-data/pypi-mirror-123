Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const breadcrumb_1 = (0, tslib_1.__importDefault)(require("app/views/performance/breadcrumb"));
const traceView_1 = (0, tslib_1.__importDefault)(require("./traceView"));
const transactionSummary_1 = (0, tslib_1.__importDefault)(require("./transactionSummary"));
const utils_1 = require("./utils");
class TransactionComparisonContent extends react_1.Component {
    getTransactionName() {
        const { baselineEvent, regressionEvent } = this.props;
        if ((0, utils_1.isTransactionEvent)(baselineEvent) && (0, utils_1.isTransactionEvent)(regressionEvent)) {
            if (baselineEvent.title === regressionEvent.title) {
                return baselineEvent.title;
            }
            return (0, locale_1.t)('mixed transaction names');
        }
        if ((0, utils_1.isTransactionEvent)(baselineEvent)) {
            return baselineEvent.title;
        }
        if ((0, utils_1.isTransactionEvent)(regressionEvent)) {
            return regressionEvent.title;
        }
        return (0, locale_1.t)('no transaction title found');
    }
    render() {
        const { baselineEvent, regressionEvent, organization, location, params } = this.props;
        // const transactionName =
        //   baselineEvent.title === regressionEvent.title ? baselineEvent.title : undefined;
        return (<react_1.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumb_1.default organization={organization} location={location} 
        // TODO: add this back in if transaction comparison is used
        // transaction={{
        //   project: <insert project id>,
        //   name: transactionName,
        // }}
        transactionComparison/>
            <Layout.Title>{this.getTransactionName()}</Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <transactionSummary_1.default organization={organization} location={location} params={params} baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <StyledPanel>
            <traceView_1.default baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>
          </StyledPanel>
        </Layout.Body>
      </react_1.Fragment>);
    }
}
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  grid-column: 1 / span 2;
  overflow: hidden;
`;
exports.default = TransactionComparisonContent;
//# sourceMappingURL=content.jsx.map