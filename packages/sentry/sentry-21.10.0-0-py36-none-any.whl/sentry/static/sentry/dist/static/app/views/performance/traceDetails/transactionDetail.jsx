Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const rowDetails_1 = require("app/components/performance/waterfall/rowDetails");
const utils_1 = require("app/components/quickTrace/utils");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const urls_1 = require("app/utils/discover/urls");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const constants_1 = require("app/utils/performance/vitals/constants");
const utils_2 = require("app/views/performance/transactionSummary/utils");
const utils_3 = require("app/views/performance/utils");
const styles_1 = require("./styles");
class TransactionDetail extends react_1.Component {
    constructor() {
        super(...arguments);
        this.scrollBarIntoView = (transactionId) => (e) => {
            // do not use the default anchor behaviour
            // because it will be hidden behind the minimap
            e.preventDefault();
            const hash = `#txn-${transactionId}`;
            this.props.scrollToHash(hash);
            // TODO(txiao): This is causing a rerender of the whole page,
            // which can be slow.
            //
            // make sure to update the location
            react_router_1.browserHistory.push(Object.assign(Object.assign({}, this.props.location), { hash }));
        };
    }
    renderTransactionErrors() {
        const { organization, transaction } = this.props;
        const { errors } = transaction;
        if (errors.length === 0) {
            return null;
        }
        return (<alert_1.default system type="error" icon={<icons_1.IconWarning size="md"/>} expand={errors.map(error => (<rowDetails_1.ErrorMessageContent key={error.event_id}>
            <rowDetails_1.ErrorDot level={error.level}/>
            <rowDetails_1.ErrorLevel>{error.level}</rowDetails_1.ErrorLevel>
            <rowDetails_1.ErrorTitle>
              <link_1.default to={(0, utils_1.generateIssueEventTarget)(error, organization)}>
                {error.title}
              </link_1.default>
            </rowDetails_1.ErrorTitle>
          </rowDetails_1.ErrorMessageContent>))}>
        <rowDetails_1.ErrorMessageTitle>
          {(0, locale_1.tn)('An error event occurred in this transaction.', '%s error events occurred in this transaction.', errors.length)}
        </rowDetails_1.ErrorMessageTitle>
      </alert_1.default>);
    }
    renderGoToTransactionButton() {
        const { location, organization, transaction } = this.props;
        const eventSlug = (0, urls_1.generateEventSlug)({
            id: transaction.event_id,
            project: transaction.project_slug,
        });
        const target = (0, utils_3.getTransactionDetailsUrl)(organization, eventSlug, transaction.transaction, (0, omit_1.default)(location.query, Object.values(globalSelectionHeader_1.PAGE_URL_PARAM)));
        return (<StyledButton size="xsmall" to={target}>
        {(0, locale_1.t)('View Transaction')}
      </StyledButton>);
    }
    renderGoToSummaryButton() {
        const { location, organization, transaction } = this.props;
        const target = (0, utils_2.transactionSummaryRouteWithQuery)({
            orgSlug: organization.slug,
            transaction: transaction.transaction,
            query: (0, omit_1.default)(location.query, Object.values(globalSelectionHeader_1.PAGE_URL_PARAM)),
            projectID: String(transaction.project_id),
        });
        return (<StyledButton size="xsmall" to={target}>
        {(0, locale_1.t)('View Summary')}
      </StyledButton>);
    }
    renderMeasurements() {
        const { transaction } = this.props;
        const { measurements = {} } = transaction;
        const measurementKeys = Object.keys(measurements)
            .filter(name => Boolean(constants_1.WEB_VITAL_DETAILS[`measurements.${name}`]))
            .sort();
        if (measurementKeys.length <= 0) {
            return null;
        }
        return (<react_1.Fragment>
        {measurementKeys.map(measurement => {
                var _a;
                return (<styles_1.Row key={measurement} title={(_a = constants_1.WEB_VITAL_DETAILS[`measurements.${measurement}`]) === null || _a === void 0 ? void 0 : _a.name}>
            {`${Number(measurements[measurement].value.toFixed(3)).toLocaleString()}ms`}
          </styles_1.Row>);
            })}
      </react_1.Fragment>);
    }
    renderTransactionDetail() {
        const { location, organization, transaction } = this.props;
        const startTimestamp = Math.min(transaction.start_timestamp, transaction.timestamp);
        const endTimestamp = Math.max(transaction.start_timestamp, transaction.timestamp);
        const duration = (endTimestamp - startTimestamp) * 1000;
        const durationString = `${Number(duration.toFixed(3)).toLocaleString()}ms`;
        return (<styles_1.TransactionDetails>
        <table className="table key-value">
          <tbody>
            <styles_1.Row title={<TransactionIdTitle onClick={this.scrollBarIntoView(transaction.event_id)}>
                  Transaction ID
                  <StyledIconAnchor />
                </TransactionIdTitle>} extra={this.renderGoToTransactionButton()}>
              {transaction.event_id}
            </styles_1.Row>
            <styles_1.Row title="Transaction" extra={this.renderGoToSummaryButton()}>
              {transaction.transaction}
            </styles_1.Row>
            <styles_1.Row title="Transaction Status">{transaction['transaction.status']}</styles_1.Row>
            <styles_1.Row title="Span ID">{transaction.span_id}</styles_1.Row>
            <styles_1.Row title="Project">{transaction.project_slug}</styles_1.Row>
            <styles_1.Row title="Start Date">
              {(0, getDynamicText_1.default)({
                fixed: 'Mar 19, 2021 11:06:27 AM UTC',
                value: (<react_1.Fragment>
                    <dateTime_1.default date={startTimestamp * 1000}/>
                    {` (${startTimestamp})`}
                  </react_1.Fragment>),
            })}
            </styles_1.Row>
            <styles_1.Row title="End Date">
              {(0, getDynamicText_1.default)({
                fixed: 'Mar 19, 2021 11:06:28 AM UTC',
                value: (<react_1.Fragment>
                    <dateTime_1.default date={endTimestamp * 1000}/>
                    {` (${endTimestamp})`}
                  </react_1.Fragment>),
            })}
            </styles_1.Row>
            <styles_1.Row title="Duration">{durationString}</styles_1.Row>
            <styles_1.Row title="Operation">{transaction['transaction.op'] || ''}</styles_1.Row>
            {this.renderMeasurements()}
            <styles_1.Tags location={location} organization={organization} transaction={transaction}/>
          </tbody>
        </table>
      </styles_1.TransactionDetails>);
    }
    render() {
        return (<styles_1.TransactionDetailsContainer onClick={event => {
                // prevent toggling the transaction detail
                event.stopPropagation();
            }}>
        {this.renderTransactionErrors()}
        {this.renderTransactionDetail()}
      </styles_1.TransactionDetailsContainer>);
    }
}
const TransactionIdTitle = (0, styled_1.default)('a') `
  display: flex;
  color: ${p => p.theme.textColor};
  :hover {
    color: ${p => p.theme.textColor};
  }
`;
const StyledIconAnchor = (0, styled_1.default)(icons_1.IconAnchor) `
  display: block;
  color: ${p => p.theme.gray300};
  margin-left: ${(0, space_1.default)(1)};
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  position: absolute;
  top: ${(0, space_1.default)(0.75)};
  right: ${(0, space_1.default)(0.5)};
`;
exports.default = TransactionDetail;
//# sourceMappingURL=transactionDetail.jsx.map