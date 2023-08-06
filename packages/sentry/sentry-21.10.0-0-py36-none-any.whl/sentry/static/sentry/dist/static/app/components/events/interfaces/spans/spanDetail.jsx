Object.defineProperty(exports, "__esModule", { value: true });
exports.Tags = exports.Row = exports.SpanDetails = exports.SpanDetailContainer = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const map_1 = (0, tslib_1.__importDefault)(require("lodash/map"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const discoverButton_1 = (0, tslib_1.__importDefault)(require("app/components/discoverButton"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const rowDetails_1 = require("app/components/performance/waterfall/rowDetails");
const pill_1 = (0, tslib_1.__importDefault)(require("app/components/pill"));
const pills_1 = (0, tslib_1.__importDefault)(require("app/components/pills"));
const utils_1 = require("app/components/quickTrace/utils");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/types/utils");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const urls_1 = require("app/utils/discover/urls");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const SpanEntryContext = (0, tslib_1.__importStar)(require("./context"));
const inlineDocs_1 = (0, tslib_1.__importDefault)(require("./inlineDocs"));
const types_1 = require("./types");
const utils_3 = require("./utils");
const DEFAULT_ERRORS_VISIBLE = 5;
const SIZE_DATA_KEYS = ['Encoded Body Size', 'Decoded Body Size', 'Transfer Size'];
class SpanDetail extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            errorsOpened: false,
        };
        this.toggleErrors = () => {
            this.setState(({ errorsOpened }) => ({ errorsOpened: !errorsOpened }));
        };
    }
    renderTraversalButton() {
        if (!this.props.childTransactions) {
            // TODO: Amend size to use theme when we eventually refactor LoadingIndicator
            // 12px is consistent with theme.iconSizes['xs'] but theme returns a string.
            return (<StyledDiscoverButton size="xsmall" disabled>
          <StyledLoadingIndicator size={12}/>
        </StyledDiscoverButton>);
        }
        if (this.props.childTransactions.length <= 0) {
            return (<StyledDiscoverButton size="xsmall" disabled>
          {(0, locale_1.t)('No Children')}
        </StyledDiscoverButton>);
        }
        const { span, trace, event, organization } = this.props;
        (0, utils_2.assert)(!(0, utils_3.isGapSpan)(span));
        if (this.props.childTransactions.length === 1) {
            // Note: This is rendered by this.renderSpanChild() as a dedicated row
            return null;
        }
        const orgFeatures = new Set(organization.features);
        const { start, end } = (0, utils_3.getTraceDateTimeRange)({
            start: trace.traceStartTimestamp,
            end: trace.traceEndTimestamp,
        });
        const childrenEventView = eventView_1.default.fromSavedQuery({
            id: undefined,
            name: `Children from Span ID ${span.span_id}`,
            fields: [
                'transaction',
                'project',
                'trace.span',
                'transaction.duration',
                'timestamp',
            ],
            orderby: '-timestamp',
            query: `event.type:transaction trace:${span.trace_id} trace.parent_span:${span.span_id}`,
            projects: orgFeatures.has('global-views')
                ? [globalSelectionHeader_1.ALL_ACCESS_PROJECTS]
                : [Number(event.projectID)],
            version: 2,
            start,
            end,
        });
        return (<StyledDiscoverButton data-test-id="view-child-transactions" size="xsmall" to={childrenEventView.getResultsViewUrlTarget(organization.slug)}>
        {(0, locale_1.t)('View Children')}
      </StyledDiscoverButton>);
    }
    renderSpanChild() {
        const { childTransactions } = this.props;
        if (!childTransactions || childTransactions.length !== 1) {
            return null;
        }
        const childTransaction = childTransactions[0];
        const transactionResult = {
            'project.name': childTransaction.project_slug,
            transaction: childTransaction.transaction,
            'trace.span': childTransaction.span_id,
            id: childTransaction.event_id,
        };
        const eventSlug = generateSlug(transactionResult);
        const viewChildButton = (<SpanEntryContext.Consumer>
        {({ getViewChildTransactionTarget }) => {
                const to = getViewChildTransactionTarget(Object.assign(Object.assign({}, transactionResult), { eventSlug }));
                if (!to) {
                    return null;
                }
                return (<StyledButton data-test-id="view-child-transaction" size="xsmall" to={to}>
              {(0, locale_1.t)('View Transaction')}
            </StyledButton>);
            }}
      </SpanEntryContext.Consumer>);
        return (<exports.Row title="Child Transaction" extra={viewChildButton}>
        {`${transactionResult.transaction} (${transactionResult['project.name']})`}
      </exports.Row>);
    }
    renderTraceButton() {
        const { span, organization, event } = this.props;
        if ((0, utils_3.isGapSpan)(span)) {
            return null;
        }
        return (<StyledButton size="xsmall" to={(0, utils_1.generateTraceTarget)(event, organization)}>
        {(0, locale_1.t)('View Trace')}
      </StyledButton>);
    }
    renderOrphanSpanMessage() {
        const { span } = this.props;
        if (!(0, utils_3.isOrphanSpan)(span)) {
            return null;
        }
        return (<alert_1.default system type="info" icon={<icons_1.IconWarning size="md"/>}>
        {(0, locale_1.t)('This is a span that has no parent span within this transaction. It has been attached to the transaction root span by default.')}
      </alert_1.default>);
    }
    renderSpanErrorMessage() {
        const { span, organization, relatedErrors } = this.props;
        const { errorsOpened } = this.state;
        if (!relatedErrors || relatedErrors.length <= 0 || (0, utils_3.isGapSpan)(span)) {
            return null;
        }
        const visibleErrors = errorsOpened
            ? relatedErrors
            : relatedErrors.slice(0, DEFAULT_ERRORS_VISIBLE);
        return (<alert_1.default system type="error" icon={<icons_1.IconWarning size="md"/>}>
        <rowDetails_1.ErrorMessageTitle>
          {(0, locale_1.tn)('An error event occurred in this transaction.', '%s error events occurred in this transaction.', relatedErrors.length)}
        </rowDetails_1.ErrorMessageTitle>
        <rowDetails_1.ErrorMessageContent>
          {visibleErrors.map(error => (<React.Fragment key={error.event_id}>
              <rowDetails_1.ErrorDot level={error.level}/>
              <rowDetails_1.ErrorLevel>{error.level}</rowDetails_1.ErrorLevel>
              <rowDetails_1.ErrorTitle>
                <link_1.default to={(0, utils_1.generateIssueEventTarget)(error, organization)}>
                  {error.title}
                </link_1.default>
              </rowDetails_1.ErrorTitle>
            </React.Fragment>))}
        </rowDetails_1.ErrorMessageContent>
        {relatedErrors.length > DEFAULT_ERRORS_VISIBLE && (<ErrorToggle size="xsmall" onClick={this.toggleErrors}>
            {errorsOpened ? (0, locale_1.t)('Show less') : (0, locale_1.t)('Show more')}
          </ErrorToggle>)}
      </alert_1.default>);
    }
    partitionSizes(data) {
        const sizeKeys = SIZE_DATA_KEYS.reduce((keys, key) => {
            if (data.hasOwnProperty(key)) {
                keys[key] = data[key];
            }
            return keys;
        }, {});
        const nonSizeKeys = Object.assign({}, data);
        SIZE_DATA_KEYS.forEach(key => delete nonSizeKeys[key]);
        return {
            sizeKeys,
            nonSizeKeys,
        };
    }
    renderSpanDetails() {
        var _a, _b, _c;
        const { span, event, location, organization, scrollToHash } = this.props;
        if ((0, utils_3.isGapSpan)(span)) {
            return (<exports.SpanDetails>
          <inlineDocs_1.default platform={((_a = event.sdk) === null || _a === void 0 ? void 0 : _a.name) || ''} orgSlug={organization.slug} projectSlug={event.projectSlug}/>
        </exports.SpanDetails>);
        }
        const startTimestamp = span.start_timestamp;
        const endTimestamp = span.timestamp;
        const duration = (endTimestamp - startTimestamp) * 1000;
        const durationString = `${Number(duration.toFixed(3)).toLocaleString()}ms`;
        const unknownKeys = Object.keys(span).filter(key => {
            return !types_1.rawSpanKeys.has(key);
        });
        const { sizeKeys, nonSizeKeys } = this.partitionSizes((_b = span === null || span === void 0 ? void 0 : span.data) !== null && _b !== void 0 ? _b : {});
        const allZeroSizes = SIZE_DATA_KEYS.map(key => sizeKeys[key]).every(value => value === 0);
        return (<React.Fragment>
        {this.renderOrphanSpanMessage()}
        {this.renderSpanErrorMessage()}
        <exports.SpanDetails>
          <table className="table key-value">
            <tbody>
              <exports.Row title={(0, utils_3.isGapSpan)(span) ? (<SpanIdTitle>Span ID</SpanIdTitle>) : (<SpanIdTitle onClick={(0, utils_3.scrollToSpan)(span.span_id, scrollToHash, location)}>
                      Span ID
                      <StyledIconAnchor />
                    </SpanIdTitle>)} extra={this.renderTraversalButton()}>
                {span.span_id}
              </exports.Row>
              <exports.Row title="Parent Span ID">{span.parent_span_id || ''}</exports.Row>
              {this.renderSpanChild()}
              <exports.Row title="Trace ID" extra={this.renderTraceButton()}>
                {span.trace_id}
              </exports.Row>
              <exports.Row title="Description">{(_c = span === null || span === void 0 ? void 0 : span.description) !== null && _c !== void 0 ? _c : ''}</exports.Row>
              <exports.Row title="Status">{span.status || ''}</exports.Row>
              <exports.Row title="Start Date">
                {(0, getDynamicText_1.default)({
                fixed: 'Mar 16, 2020 9:10:12 AM UTC',
                value: (<React.Fragment>
                      <dateTime_1.default date={startTimestamp * 1000}/>
                      {` (${startTimestamp})`}
                    </React.Fragment>),
            })}
              </exports.Row>
              <exports.Row title="End Date">
                {(0, getDynamicText_1.default)({
                fixed: 'Mar 16, 2020 9:10:13 AM UTC',
                value: (<React.Fragment>
                      <dateTime_1.default date={endTimestamp * 1000}/>
                      {` (${endTimestamp})`}
                    </React.Fragment>),
            })}
              </exports.Row>
              <exports.Row title="Duration">{durationString}</exports.Row>
              <exports.Row title="Operation">{span.op || ''}</exports.Row>
              <exports.Row title="Same Process as Parent">
                {span.same_process_as_parent !== undefined
                ? String(span.same_process_as_parent)
                : null}
              </exports.Row>
              <exports.Tags span={span}/>
              {allZeroSizes && (<TextTr>
                  The following sizes were not collected for security reasons. Check if
                  the host serves the appropriate
                  <externalLink_1.default href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Timing-Allow-Origin">
                    <span className="val-string">Timing-Allow-Origin</span>
                  </externalLink_1.default>
                  header. You may have to enable this collection manually.
                </TextTr>)}
              {(0, map_1.default)(sizeKeys, (value, key) => (<exports.Row title={key} key={key}>
                  <React.Fragment>
                    <fileSize_1.default bytes={value}/>
                    {value >= 1024 && (<span>{` (${JSON.stringify(value, null, 4) || ''} B)`}</span>)}
                  </React.Fragment>
                </exports.Row>))}
              {(0, map_1.default)(nonSizeKeys, (value, key) => (<exports.Row title={key} key={key}>
                  {JSON.stringify(value, null, 4) || ''}
                </exports.Row>))}
              {unknownKeys.map(key => (<exports.Row title={key} key={key}>
                  {JSON.stringify(span[key], null, 4) || ''}
                </exports.Row>))}
            </tbody>
          </table>
        </exports.SpanDetails>
      </React.Fragment>);
    }
    render() {
        return (<exports.SpanDetailContainer data-component="span-detail" onClick={event => {
                // prevent toggling the span detail
                event.stopPropagation();
            }}>
        {this.renderSpanDetails()}
      </exports.SpanDetailContainer>);
    }
}
const StyledDiscoverButton = (0, styled_1.default)(discoverButton_1.default) `
  position: absolute;
  top: ${(0, space_1.default)(0.75)};
  right: ${(0, space_1.default)(0.5)};
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  position: absolute;
  top: ${(0, space_1.default)(0.75)};
  right: ${(0, space_1.default)(0.5)};
`;
exports.SpanDetailContainer = (0, styled_1.default)('div') `
  border-bottom: 1px solid ${p => p.theme.border};
  cursor: auto;
`;
exports.SpanDetails = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
`;
const ValueTd = (0, styled_1.default)('td') `
  position: relative;
`;
const StyledLoadingIndicator = (0, styled_1.default)(loadingIndicator_1.default) `
  display: flex;
  align-items: center;
  height: ${(0, space_1.default)(2)};
  margin: 0;
`;
const StyledText = (0, styled_1.default)('p') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin: ${(0, space_1.default)(2)} ${(0, space_1.default)(0)};
`;
const TextTr = ({ children }) => (<tr>
    <td className="key"/>
    <ValueTd className="value">
      <StyledText>{children}</StyledText>
    </ValueTd>
  </tr>);
const ErrorToggle = (0, styled_1.default)(button_1.default) `
  margin-top: ${(0, space_1.default)(0.75)};
`;
const SpanIdTitle = (0, styled_1.default)('a') `
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
const Row = ({ title, keep, children, extra = null, }) => {
    if (!keep && !children) {
        return null;
    }
    return (<tr>
      <td className="key">{title}</td>
      <ValueTd className="value">
        <pre className="val">
          <span className="val-string">{children}</span>
        </pre>
        {extra}
      </ValueTd>
    </tr>);
};
exports.Row = Row;
const Tags = ({ span }) => {
    const tags = span === null || span === void 0 ? void 0 : span.tags;
    if (!tags) {
        return null;
    }
    const keys = Object.keys(tags);
    if (keys.length <= 0) {
        return null;
    }
    return (<tr>
      <td className="key">Tags</td>
      <td className="value">
        <pills_1.default style={{ padding: '8px' }}>
          {keys.map((key, index) => (<pill_1.default key={index} name={key} value={String(tags[key]) || ''}/>))}
        </pills_1.default>
      </td>
    </tr>);
};
exports.Tags = Tags;
function generateSlug(result) {
    return (0, urls_1.generateEventSlug)({
        id: result.id,
        'project.name': result['project.name'],
    });
}
exports.default = (0, withApi_1.default)((0, react_router_1.withRouter)(SpanDetail));
//# sourceMappingURL=spanDetail.jsx.map