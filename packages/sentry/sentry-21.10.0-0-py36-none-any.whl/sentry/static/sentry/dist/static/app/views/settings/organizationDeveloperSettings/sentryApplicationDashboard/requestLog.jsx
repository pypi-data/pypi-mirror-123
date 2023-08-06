Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const memoize_1 = (0, tslib_1.__importDefault)(require("lodash/memoize"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const ALL_EVENTS = (0, locale_1.t)('All Events');
const MAX_PER_PAGE = 10;
const componentHasSelectUri = (issueLinkComponent) => {
    const hasSelectUri = (fields) => fields.some(field => field.type === 'select' && 'uri' in field);
    const createHasSelectUri = hasSelectUri(issueLinkComponent.create.required_fields) ||
        hasSelectUri(issueLinkComponent.create.optional_fields || []);
    const linkHasSelectUri = hasSelectUri(issueLinkComponent.link.required_fields) ||
        hasSelectUri(issueLinkComponent.link.optional_fields || []);
    return createHasSelectUri || linkHasSelectUri;
};
const getEventTypes = (0, memoize_1.default)((app) => {
    // TODO(nola): ideally this would be kept in sync with EXTENDED_VALID_EVENTS on the backend
    let issueLinkEvents = [];
    const issueLinkComponent = (app.schema.elements || []).find(element => element.type === 'issue-link');
    if (issueLinkComponent) {
        issueLinkEvents = ['external_issue.created', 'external_issue.linked'];
        if (componentHasSelectUri(issueLinkComponent)) {
            issueLinkEvents.push('select_options.requested');
        }
    }
    const events = [
        ALL_EVENTS,
        // Internal apps don't have installation webhooks
        ...(app.status !== 'internal'
            ? ['installation.created', 'installation.deleted']
            : []),
        ...(app.events.includes('error') ? ['error.created'] : []),
        ...(app.events.includes('issue')
            ? ['issue.created', 'issue.resolved', 'issue.ignored', 'issue.assigned']
            : []),
        ...(app.isAlertable
            ? [
                'event_alert.triggered',
                'metric_alert.open',
                'metric_alert.resolved',
                'metric_alert.critical',
                'metric_alert.warning',
            ]
            : []),
        ...issueLinkEvents,
    ];
    return events;
});
const ResponseCode = ({ code }) => {
    let type = 'error';
    if (code <= 399 && code >= 300) {
        type = 'warning';
    }
    else if (code <= 299 && code >= 100) {
        type = 'success';
    }
    return (<Tags>
      <StyledTag type={type}>{code === 0 ? 'timeout' : code}</StyledTag>
    </Tags>);
};
const TimestampLink = ({ date, link }) => link ? (<externalLink_1.default href={link}>
      <dateTime_1.default date={date}/>
      <StyledIconOpen size="12px"/>
    </externalLink_1.default>) : (<dateTime_1.default date={date}/>);
class RequestLog extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldReload = true;
        this.handleChangeEventType = (eventType) => {
            this.setState({
                eventType,
                currentPage: 0,
            }, this.remountComponent);
        };
        this.handleChangeErrorsOnly = () => {
            this.setState({
                errorsOnly: !this.state.errorsOnly,
                currentPage: 0,
            }, this.remountComponent);
        };
        this.handleNextPage = () => {
            this.setState({
                currentPage: this.state.currentPage + 1,
            });
        };
        this.handlePrevPage = () => {
            this.setState({
                currentPage: this.state.currentPage - 1,
            });
        };
    }
    get hasNextPage() {
        return (this.state.currentPage + 1) * MAX_PER_PAGE < this.state.requests.length;
    }
    get hasPrevPage() {
        return this.state.currentPage > 0;
    }
    getEndpoints() {
        const { slug } = this.props.app;
        const query = {};
        if (this.state) {
            if (this.state.eventType !== ALL_EVENTS) {
                query.eventType = this.state.eventType;
            }
            if (this.state.errorsOnly) {
                query.errorsOnly = true;
            }
        }
        return [['requests', `/sentry-apps/${slug}/requests/`, { query }]];
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { requests: [], eventType: ALL_EVENTS, errorsOnly: false, currentPage: 0 });
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        const { requests, eventType, errorsOnly, currentPage } = this.state;
        const { app } = this.props;
        const currentRequests = requests.slice(currentPage * MAX_PER_PAGE, (currentPage + 1) * MAX_PER_PAGE);
        return (<React.Fragment>
        <h5>{(0, locale_1.t)('Request Log')}</h5>

        <div>
          <p>
            {(0, locale_1.t)('This log shows the status of any outgoing webhook requests from Sentry to your integration.')}
          </p>

          <RequestLogFilters>
            <dropdownControl_1.default label={eventType} menuWidth="220px" button={({ isOpen, getActorProps }) => (<StyledDropdownButton {...getActorProps()} isOpen={isOpen}>
                  {eventType}
                </StyledDropdownButton>)}>
              {getEventTypes(app).map(type => (<dropdownControl_1.DropdownItem key={type} onSelect={this.handleChangeEventType} eventKey={type} isActive={eventType === type}>
                  {type}
                </dropdownControl_1.DropdownItem>))}
            </dropdownControl_1.default>

            <StyledErrorsOnlyButton onClick={this.handleChangeErrorsOnly}>
              <ErrorsOnlyCheckbox>
                <checkbox_1.default checked={errorsOnly} onChange={() => { }}/>
                {(0, locale_1.t)('Errors Only')}
              </ErrorsOnlyCheckbox>
            </StyledErrorsOnlyButton>
          </RequestLogFilters>
        </div>

        <panels_1.Panel>
          <panels_1.PanelHeader>
            <TableLayout hasOrganization={app.status !== 'internal'}>
              <div>{(0, locale_1.t)('Time')}</div>
              <div>{(0, locale_1.t)('Status Code')}</div>
              {app.status !== 'internal' && <div>{(0, locale_1.t)('Organization')}</div>}
              <div>{(0, locale_1.t)('Event Type')}</div>
              <div>{(0, locale_1.t)('Webhook URL')}</div>
            </TableLayout>
          </panels_1.PanelHeader>

          {!this.state.loading ? (<panels_1.PanelBody>
              {currentRequests.length > 0 ? (currentRequests.map((request, idx) => (<panels_1.PanelItem key={idx}>
                    <TableLayout hasOrganization={app.status !== 'internal'}>
                      <TimestampLink date={request.date} link={request.errorUrl}/>
                      <ResponseCode code={request.responseCode}/>
                      {app.status !== 'internal' && (<div>
                          {request.organization ? request.organization.name : null}
                        </div>)}
                      <div>{request.eventType}</div>
                      <OverflowBox>{request.webhookUrl}</OverflowBox>
                    </TableLayout>
                  </panels_1.PanelItem>))) : (<emptyMessage_1.default icon={<icons_1.IconFlag size="xl"/>}>
                  {(0, locale_1.t)('No requests found in the last 30 days.')}
                </emptyMessage_1.default>)}
            </panels_1.PanelBody>) : (<loadingIndicator_1.default />)}
        </panels_1.Panel>

        <PaginationButtons>
          <button_1.default icon={<icons_1.IconChevron direction="left" size="sm"/>} onClick={this.handlePrevPage} disabled={!this.hasPrevPage} label={(0, locale_1.t)('Previous page')}/>
          <button_1.default icon={<icons_1.IconChevron direction="right" size="sm"/>} onClick={this.handleNextPage} disabled={!this.hasNextPage} label={(0, locale_1.t)('Next page')}/>
        </PaginationButtons>
      </React.Fragment>);
    }
}
exports.default = RequestLog;
const TableLayout = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr 0.5fr ${p => (p.hasOrganization ? '1fr' : '')} 1fr 1fr;
  grid-column-gap: ${(0, space_1.default)(1.5)};
  width: 100%;
  align-items: center;
`;
const OverflowBox = (0, styled_1.default)('div') `
  word-break: break-word;
`;
const PaginationButtons = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  align-items: center;

  > :first-child {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }

  > :nth-child(2) {
    margin-left: -1px;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
  }
`;
const RequestLogFilters = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding-bottom: ${(0, space_1.default)(1)};
`;
const ErrorsOnlyCheckbox = (0, styled_1.default)('div') `
  input {
    margin: 0 ${(0, space_1.default)(1)} 0 0;
  }

  display: flex;
  align-items: center;
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  z-index: ${p => p.theme.zIndex.header - 1};
  white-space: nowrap;

  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
`;
const StyledErrorsOnlyButton = (0, styled_1.default)(button_1.default) `
  margin-left: -1px;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
`;
const StyledIconOpen = (0, styled_1.default)(icons_1.IconOpen) `
  margin-left: 6px;
  color: ${p => p.theme.subText};
`;
const Tags = (0, styled_1.default)('div') `
  margin: -${(0, space_1.default)(0.5)};
`;
const StyledTag = (0, styled_1.default)(tag_1.default) `
  padding: ${(0, space_1.default)(0.5)};
  display: inline-flex;
`;
//# sourceMappingURL=requestLog.jsx.map