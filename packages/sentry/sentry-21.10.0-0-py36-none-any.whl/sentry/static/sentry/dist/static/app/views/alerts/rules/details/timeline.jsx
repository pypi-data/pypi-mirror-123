Object.defineProperty(exports, "__esModule", { value: true });
exports.getTriggerName = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const styles_1 = require("app/components/charts/styles");
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const seenByList_1 = (0, tslib_1.__importDefault)(require("app/components/seenByList"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const details_1 = require("app/views/alerts/details");
const types_1 = require("app/views/alerts/types");
function getTriggerName(value) {
    if (value === `${types_1.IncidentStatus.WARNING}`) {
        return (0, locale_1.t)('Warning');
    }
    if (value === `${types_1.IncidentStatus.CRITICAL}`) {
        return (0, locale_1.t)('Critical');
    }
    // Otherwise, activity type is not status change
    return '';
}
exports.getTriggerName = getTriggerName;
class TimelineIncident extends React.Component {
    renderActivity(activity, idx) {
        var _a, _b;
        const { incident, rule } = this.props;
        const { activities } = incident;
        const last = activities && idx === activities.length - 1;
        const authorName = (_b = (_a = activity.user) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Sentry';
        const isDetected = activity.type === types_1.IncidentActivityType.DETECTED;
        const isStarted = activity.type === types_1.IncidentActivityType.STARTED;
        const isClosed = activity.type === types_1.IncidentActivityType.STATUS_CHANGE &&
            activity.value === `${types_1.IncidentStatus.CLOSED}`;
        const isTriggerChange = activity.type === types_1.IncidentActivityType.STATUS_CHANGE && !isClosed;
        // Unknown activity, don't render anything
        if ((!isStarted && !isDetected && !isClosed && !isTriggerChange) ||
            !activities ||
            !activities.length) {
            return null;
        }
        const currentTrigger = getTriggerName(activity.value);
        let title;
        let subtext;
        if (isTriggerChange) {
            const nextActivity = activities.find(({ previousValue }) => previousValue === activity.value) ||
                (activity.value &&
                    activity.value === `${types_1.IncidentStatus.OPENED}` &&
                    activities.find(({ type }) => type === types_1.IncidentActivityType.DETECTED));
            const activityDuration = (nextActivity ? (0, moment_timezone_1.default)(nextActivity.dateCreated) : (0, moment_timezone_1.default)()).diff((0, moment_timezone_1.default)(activity.dateCreated), 'milliseconds');
            title = (0, locale_1.t)('Alert status changed');
            subtext =
                activityDuration !== null &&
                    (0, locale_1.tct)(`[currentTrigger]: [duration]`, {
                        currentTrigger,
                        duration: <duration_1.default abbreviation seconds={activityDuration / 1000}/>,
                    });
        }
        else if (isClosed && (incident === null || incident === void 0 ? void 0 : incident.statusMethod) === types_1.IncidentStatusMethod.RULE_UPDATED) {
            title = (0, locale_1.t)('Alert auto-resolved');
            subtext = (0, locale_1.t)('Alert rule modified or deleted');
        }
        else if (isClosed && (incident === null || incident === void 0 ? void 0 : incident.statusMethod) !== types_1.IncidentStatusMethod.RULE_UPDATED) {
            title = (0, locale_1.t)('Resolved');
            subtext = (0, locale_1.tct)('by [authorName]', { authorName });
        }
        else if (isDetected) {
            title = (incident === null || incident === void 0 ? void 0 : incident.alertRule)
                ? (0, locale_1.t)('Alert was created')
                : (0, locale_1.tct)('[authorName] created an alert', { authorName });
            subtext = <dateTime_1.default timeOnly date={activity.dateCreated}/>;
        }
        else if (isStarted) {
            const dateEnded = (0, moment_timezone_1.default)(activity.dateCreated)
                .add(rule.timeWindow, 'minutes')
                .utc()
                .format();
            const timeOnly = Boolean(dateEnded && (0, moment_timezone_1.default)(activity.dateCreated).date() === (0, moment_timezone_1.default)(dateEnded).date());
            title = (0, locale_1.t)('Trigger conditions were met');
            subtext = (<React.Fragment>
          <dateTime_1.default timeOnly={timeOnly} timeAndDate={!timeOnly} date={activity.dateCreated}/>
          {' — '}
          <dateTime_1.default timeOnly={timeOnly} timeAndDate={!timeOnly} date={dateEnded}/>
        </React.Fragment>);
        }
        else {
            return null;
        }
        return (<Activity key={activity.id}>
        <ActivityTrack>{!last && <VerticalDivider />}</ActivityTrack>

        <ActivityBody>
          <ActivityTime>
            <StyledTimeSince date={activity.dateCreated} suffix={(0, locale_1.t)('ago')}/>
            <HorizontalDivider />
          </ActivityTime>
          <ActivityText>
            {title}
            {subtext && <ActivitySubText>{subtext}</ActivitySubText>}
          </ActivityText>
        </ActivityBody>
      </Activity>);
    }
    render() {
        const { incident, organization } = this.props;
        return (<IncidentSection key={incident.identifier}>
        <IncidentHeader>
          <link_1.default to={{
                pathname: (0, details_1.alertDetailsLink)(organization, incident),
                query: { alert: incident.identifier },
            }}>
            {(0, locale_1.tct)('Alert #[id]', { id: incident.identifier })}
          </link_1.default>
          <SeenByTab>
            {incident && (<StyledSeenByList iconPosition="right" seenBy={incident.seenBy} iconTooltip={(0, locale_1.t)('People who have viewed this alert')}/>)}
          </SeenByTab>
        </IncidentHeader>
        {incident.activities && (<IncidentBody>
            {incident.activities
                    .filter(activity => activity.type !== types_1.IncidentActivityType.COMMENT)
                    .map((activity, idx) => this.renderActivity(activity, idx))}
          </IncidentBody>)}
      </IncidentSection>);
    }
}
class Timeline extends React.Component {
    constructor() {
        super(...arguments);
        this.renderEmptyMessage = () => {
            return (<StyledEmptyStateWarning small withIcon={false}>
        <p>{(0, locale_1.t)('No alerts triggered during this time')}</p>
      </StyledEmptyStateWarning>);
        };
    }
    render() {
        const { api, incidents, organization, rule } = this.props;
        return (<History>
        <styles_1.SectionHeading>{(0, locale_1.t)('History')}</styles_1.SectionHeading>
        <ScrollPanel>
          <panels_1.PanelBody withPadding>
            {incidents && rule && incidents.length
                ? incidents.map(incident => (<TimelineIncident key={incident.identifier} api={api} organization={organization} incident={incident} rule={rule}/>))
                : this.renderEmptyMessage()}
          </panels_1.PanelBody>
        </ScrollPanel>
      </History>);
    }
}
exports.default = Timeline;
const History = (0, styled_1.default)('div') `
  margin-bottom: 30px;
`;
const ScrollPanel = (0, styled_1.default)(panels_1.Panel) `
  max-height: 500px;
  overflow: scroll;
  -ms-overflow-style: none;
  scrollbar-width: none;
  &::-webkit-scrollbar {
    display: none;
  }

  p {
    font-size: ${p => p.theme.fontSizeMedium};
  }
`;
const StyledEmptyStateWarning = (0, styled_1.default)(emptyStateWarning_1.default) `
  padding: 0;
`;
const IncidentSection = (0, styled_1.default)('div') `
  &:not(:first-of-type) {
    margin-top: 15px;
  }
`;
const IncidentHeader = (0, styled_1.default)('div') `
  display: flex;
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const SeenByTab = (0, styled_1.default)('div') `
  flex: 1;
  margin-left: ${(0, space_1.default)(2)};
  margin-right: 0;

  .nav-tabs > & {
    margin-right: 0;
  }
`;
const StyledSeenByList = (0, styled_1.default)(seenByList_1.default) `
  margin-top: 0;
`;
const IncidentBody = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
const Activity = (0, styled_1.default)('div') `
  display: flex;
`;
const ActivityTrack = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: ${(0, space_1.default)(1)};

  &:before {
    content: '';
    width: ${(0, space_1.default)(1)};
    height: ${(0, space_1.default)(1)};
    background-color: ${p => p.theme.gray300};
    border-radius: ${(0, space_1.default)(1)};
  }
`;
const ActivityBody = (0, styled_1.default)('div') `
  flex: 1;
  display: flex;
  flex-direction: column;
`;
const ActivityTime = (0, styled_1.default)('li') `
  display: flex;
  align-items: center;
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeSmall};
  line-height: 1.4;
`;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
const ActivityText = (0, styled_1.default)('div') `
  flex-direction: row;
  margin-bottom: ${(0, space_1.default)(1.5)};
  font-size: ${p => p.theme.fontSizeMedium};
`;
const ActivitySubText = (0, styled_1.default)('span') `
  display: inline-block;
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  margin-left: ${(0, space_1.default)(0.5)};
`;
const HorizontalDivider = (0, styled_1.default)('div') `
  flex: 1;
  height: 0;
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  margin: 5px 0;
`;
const VerticalDivider = (0, styled_1.default)('div') `
  flex: 1;
  width: 0;
  margin: 0 5px;
  border-left: 1px dashed ${p => p.theme.innerBorder};
`;
//# sourceMappingURL=timeline.jsx.map