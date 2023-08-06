Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const events_1 = require("app/utils/events");
const formatters_1 = require("app/utils/formatters");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const utils_1 = require("app/utils/performance/quickTrace/utils");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const quickTraceMeta_1 = (0, tslib_1.__importDefault)(require("./quickTraceMeta"));
const styles_1 = require("./styles");
/**
 * This should match the breakpoint chosen for the `EventDetailHeader` below
 */
const BREAKPOINT_MEDIA_QUERY = `(min-width: ${theme_1.default.breakpoints[2]})`;
class EventMetas extends React.Component {
    constructor() {
        var _a, _b, _c;
        super(...arguments);
        this.state = {
            isLargeScreen: (_b = (_a = window.matchMedia) === null || _a === void 0 ? void 0 : _a.call(window, BREAKPOINT_MEDIA_QUERY)) === null || _b === void 0 ? void 0 : _b.matches,
        };
        this.mq = (_c = window.matchMedia) === null || _c === void 0 ? void 0 : _c.call(window, BREAKPOINT_MEDIA_QUERY);
        this.handleMediaQueryChange = (changed) => {
            this.setState({
                isLargeScreen: changed.matches,
            });
        };
    }
    componentDidMount() {
        if (this.mq) {
            this.mq.addListener(this.handleMediaQueryChange);
        }
    }
    componentWillUnmount() {
        if (this.mq) {
            this.mq.removeListener(this.handleMediaQueryChange);
        }
    }
    render() {
        const { event, organization, projectId, location, quickTrace, meta, errorDest, transactionDest, } = this.props;
        const { isLargeScreen } = this.state;
        const type = (0, utils_1.isTransaction)(event) ? 'transaction' : 'event';
        const timestamp = (<timeSince_1.default date={event.dateCreated || (event.endTimestamp || 0) * 1000}/>);
        const httpStatus = <HttpStatus event={event}/>;
        return (<projects_1.default orgId={organization.slug} slugs={[projectId]}>
        {({ projects }) => {
                var _a, _b, _c;
                const project = projects.find(p => p.slug === projectId);
                return (<EventDetailHeader type={type}>
              <styles_1.MetaData headingText={(0, locale_1.t)('Event ID')} tooltipText={(0, locale_1.t)('The unique ID assigned to this %s.', type)} bodyText={<EventID event={event}/>} subtext={<projectBadge_1.default project={project ? project : { slug: projectId }} avatarSize={16}/>}/>
              {(0, utils_1.isTransaction)(event) ? (<styles_1.MetaData headingText={(0, locale_1.t)('Event Duration')} tooltipText={(0, locale_1.t)('The time elapsed between the start and end of this transaction.')} bodyText={(0, formatters_1.getDuration)(event.endTimestamp - event.startTimestamp, 2, true)} subtext={timestamp}/>) : (<styles_1.MetaData headingText={(0, locale_1.t)('Created')} tooltipText={(0, locale_1.t)('The time at which this event was created.')} bodyText={timestamp} subtext={(0, getDynamicText_1.default)({
                            value: <dateTime_1.default date={event.dateCreated}/>,
                            fixed: 'May 6, 2021 3:27:01 UTC',
                        })}/>)}
              {(0, utils_1.isTransaction)(event) && (<styles_1.MetaData headingText={(0, locale_1.t)('Status')} tooltipText={(0, locale_1.t)('The status of this transaction indicating if it succeeded or otherwise.')} bodyText={(_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.status) !== null && _c !== void 0 ? _c : '\u2014'} subtext={httpStatus}/>)}
              <QuickTraceContainer>
                <quickTraceMeta_1.default event={event} project={project} location={location} quickTrace={quickTrace} traceMeta={meta} anchor={isLargeScreen ? 'right' : 'left'} errorDest={errorDest} transactionDest={transactionDest}/>
              </QuickTraceContainer>
            </EventDetailHeader>);
            }}
      </projects_1.default>);
    }
}
const EventDetailHeader = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(${p => (p.type === 'transaction' ? 3 : 2)}, 1fr);
  grid-template-rows: repeat(2, auto);
  grid-gap: ${(0, space_1.default)(2)};
  margin-bottom: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin-bottom: 0;
  }

  /* This should match the breakpoint chosen for BREAKPOINT_MEDIA_QUERY above. */
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    ${p => p.type === 'transaction'
    ? 'grid-template-columns: minmax(160px, 1fr) minmax(160px, 1fr) minmax(160px, 1fr) 6fr;'
    : 'grid-template-columns: minmax(160px, 1fr) minmax(200px, 1fr) 6fr;'};
    grid-row-gap: 0;
  }
`;
const QuickTraceContainer = (0, styled_1.default)('div') `
  grid-column: 1/4;

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    justify-self: flex-end;
    min-width: 325px;
    grid-column: unset;
  }
`;
function EventID({ event }) {
    return (<clipboard_1.default value={event.eventID}>
      <EventIDContainer>
        <EventIDWrapper>{(0, events_1.getShortEventId)(event.eventID)}</EventIDWrapper>
        <tooltip_1.default title={event.eventID} position="top">
          <icons_1.IconCopy color="subText"/>
        </tooltip_1.default>
      </EventIDContainer>
    </clipboard_1.default>);
}
const EventIDContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  cursor: pointer;
`;
const EventIDWrapper = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(1)};
`;
function HttpStatus({ event }) {
    const { tags } = event;
    const emptyStatus = <React.Fragment>{'\u2014'}</React.Fragment>;
    if (!Array.isArray(tags)) {
        return emptyStatus;
    }
    const tag = tags.find(tagObject => tagObject.key === 'http.status_code');
    if (!tag) {
        return emptyStatus;
    }
    return <React.Fragment>HTTP {tag.value}</React.Fragment>;
}
exports.default = EventMetas;
//# sourceMappingURL=eventMetas.jsx.map