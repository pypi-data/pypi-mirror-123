Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const globalAppStoreConnectUpdateAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalAppStoreConnectUpdateAlert"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const navigationButtonGroup_1 = (0, tslib_1.__importDefault)(require("app/components/navigationButtonGroup"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const quickTrace_1 = (0, tslib_1.__importDefault)(require("./quickTrace"));
const formatDateDelta = (reference, observed) => {
    const duration = moment_timezone_1.default.duration(Math.abs(+observed - +reference));
    const hours = Math.floor(+duration / (60 * 60 * 1000));
    const minutes = duration.minutes();
    const results = [];
    if (hours) {
        results.push(`${hours} hour${hours !== 1 ? 's' : ''}`);
    }
    if (minutes) {
        results.push(`${minutes} minute${minutes !== 1 ? 's' : ''}`);
    }
    if (results.length === 0) {
        results.push('a few seconds');
    }
    return results.join(', ');
};
class GroupEventToolbar extends react_1.Component {
    shouldComponentUpdate(nextProps) {
        return this.props.event.id !== nextProps.event.id;
    }
    handleTraceLink(organization) {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'quick_trace.trace_id.clicked',
            eventName: 'Quick Trace: Trace ID clicked',
            organization_id: parseInt(organization.id, 10),
            source: 'issues',
        });
    }
    getDateTooltip() {
        var _a;
        const evt = this.props.event;
        const user = configStore_1.default.get('user');
        const options = (_a = user === null || user === void 0 ? void 0 : user.options) !== null && _a !== void 0 ? _a : {};
        const format = options.clock24Hours ? 'HH:mm:ss z' : 'LTS z';
        const dateCreated = (0, moment_timezone_1.default)(evt.dateCreated);
        const dateReceived = evt.dateReceived ? (0, moment_timezone_1.default)(evt.dateReceived) : null;
        return (<DescriptionList className="flat">
        <dt>Occurred</dt>
        <dd>
          {dateCreated.format('ll')}
          <br />
          {dateCreated.format(format)}
        </dd>
        {dateReceived && (<react_1.Fragment>
            <dt>Received</dt>
            <dd>
              {dateReceived.format('ll')}
              <br />
              {dateReceived.format(format)}
            </dd>
            <dt>Latency</dt>
            <dd>{formatDateDelta(dateCreated, dateReceived)}</dd>
          </react_1.Fragment>)}
      </DescriptionList>);
    }
    render() {
        const evt = this.props.event;
        const { group, organization, location, project } = this.props;
        const groupId = group.id;
        const baseEventsPath = `/organizations/${organization.slug}/issues/${groupId}/events/`;
        // TODO: possible to define this as a route in react-router, but without a corresponding
        //       React component?
        const jsonUrl = `/organizations/${organization.slug}/issues/${groupId}/events/${evt.id}/json/`;
        const latencyThreshold = 30 * 60 * 1000; // 30 minutes
        const isOverLatencyThreshold = evt.dateReceived &&
            Math.abs(+(0, moment_timezone_1.default)(evt.dateReceived) - +(0, moment_timezone_1.default)(evt.dateCreated)) > latencyThreshold;
        return (<Wrapper>
        <StyledNavigationButtonGroup hasPrevious={!!evt.previousEventID} hasNext={!!evt.nextEventID} links={[
                { pathname: `${baseEventsPath}oldest/`, query: location.query },
                { pathname: `${baseEventsPath}${evt.previousEventID}/`, query: location.query },
                { pathname: `${baseEventsPath}${evt.nextEventID}/`, query: location.query },
                { pathname: `${baseEventsPath}latest/`, query: location.query },
            ]} size="small"/>
        <Heading>
          {(0, locale_1.t)('Event')}{' '}
          <EventIdLink to={`${baseEventsPath}${evt.id}/`}>{evt.eventID}</EventIdLink>
          <LinkContainer>
            <externalLink_1.default href={jsonUrl}>
              {'JSON'} (<fileSize_1.default bytes={evt.size}/>)
            </externalLink_1.default>
          </LinkContainer>
        </Heading>
        <tooltip_1.default title={this.getDateTooltip()} disableForVisualTest>
          <StyledDateTime date={(0, getDynamicText_1.default)({ value: evt.dateCreated, fixed: 'Dummy timestamp' })}/>
          {isOverLatencyThreshold && <StyledIconWarning color="yellow300"/>}
        </tooltip_1.default>
        <StyledGlobalAppStoreConnectUpdateAlert project={project} organization={organization} isCompact/>
        <quickTrace_1.default event={evt} group={group} organization={organization} location={location}/>
      </Wrapper>);
    }
}
const Wrapper = (0, styled_1.default)('div') `
  position: relative;
  margin-bottom: -5px;
  /* z-index seems unnecessary, but increasing (instead of removing) just in case(billy) */
  /* Fixes tooltips in toolbar having lower z-index than .btn-group .btn.active */
  z-index: 3;
  padding: 20px 30px 20px 40px;

  @media (max-width: 767px) {
    display: none;
  }
`;
const EventIdLink = (0, styled_1.default)(link_1.default) `
  font-weight: normal;
`;
const Heading = (0, styled_1.default)('h4') `
  line-height: 1.3;
  margin: 0;
  font-size: ${p => p.theme.fontSizeLarge};
`;
const StyledNavigationButtonGroup = (0, styled_1.default)(navigationButtonGroup_1.default) `
  float: right;
`;
const StyledIconWarning = (0, styled_1.default)(icons_1.IconWarning) `
  margin-left: ${(0, space_1.default)(0.5)};
  position: relative;
  top: ${(0, space_1.default)(0.25)};
`;
const StyledDateTime = (0, styled_1.default)(dateTime_1.default) `
  border-bottom: 1px dotted #dfe3ea;
  color: ${p => p.theme.subText};
`;
const StyledGlobalAppStoreConnectUpdateAlert = (0, styled_1.default)(globalAppStoreConnectUpdateAlert_1.default) `
  margin-top: ${(0, space_1.default)(0.5)};
  margin-bottom: ${(0, space_1.default)(1)};
`;
const LinkContainer = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(1)};
  padding-left: ${(0, space_1.default)(1)};
  position: relative;
  font-weight: normal;

  &:before {
    display: block;
    position: absolute;
    content: '';
    left: 0;
    top: 2px;
    height: 14px;
    border-left: 1px solid ${p => p.theme.border};
  }
`;
const DescriptionList = (0, styled_1.default)('dl') `
  text-align: left;
  margin: 0;
  min-width: 200px;
  max-width: 250px;
`;
exports.default = GroupEventToolbar;
//# sourceMappingURL=eventToolbar.jsx.map