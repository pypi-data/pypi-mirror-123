Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const utils_1 = require("app/components/quickTrace/utils");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const platformCategories_1 = require("app/data/platformCategories");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const docs_1 = require("app/utils/docs");
const formatters_1 = require("app/utils/formatters");
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
const utils_2 = require("app/utils/performance/quickTrace/utils");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const FRONTEND_PLATFORMS = [...platformCategories_1.frontend, ...platformCategories_1.mobile];
const BACKEND_PLATFORMS = [...platformCategories_1.backend, ...platformCategories_1.serverless];
const styles_1 = require("./styles");
const TOOLTIP_PREFIX = {
    root: 'root',
    ancestors: 'ancestor',
    parent: 'parent',
    current: '',
    children: 'child',
    descendants: 'descendant',
};
function QuickTrace({ event, quickTrace, location, organization, anchor, errorDest, transactionDest, }) {
    let parsedQuickTrace;
    try {
        parsedQuickTrace = (0, utils_2.parseQuickTrace)(quickTrace, event, organization);
    }
    catch (error) {
        return <React.Fragment>{'\u2014'}</React.Fragment>;
    }
    const traceLength = quickTrace.trace && quickTrace.trace.length;
    const { root, ancestors, parent, children, descendants, current } = parsedQuickTrace;
    const nodes = [];
    if (root) {
        nodes.push(<EventNodeSelector key="root-node" location={location} organization={organization} events={[root]} currentEvent={event} text={(0, locale_1.t)('Root')} anchor={anchor} nodeKey="root" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<styles_1.TraceConnector key="root-connector"/>);
    }
    if (ancestors === null || ancestors === void 0 ? void 0 : ancestors.length) {
        nodes.push(<EventNodeSelector key="ancestors-node" location={location} organization={organization} events={ancestors} currentEvent={event} text={(0, locale_1.tn)('%s Ancestor', '%s Ancestors', ancestors.length)} anchor={anchor} nodeKey="ancestors" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<styles_1.TraceConnector key="ancestors-connector"/>);
    }
    if (parent) {
        nodes.push(<EventNodeSelector key="parent-node" location={location} organization={organization} events={[parent]} currentEvent={event} text={(0, locale_1.t)('Parent')} anchor={anchor} nodeKey="parent" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<styles_1.TraceConnector key="parent-connector"/>);
    }
    const currentNode = (<EventNodeSelector key="current-node" location={location} organization={organization} text={(0, locale_1.t)('This Event')} events={[current]} currentEvent={event} anchor={anchor} nodeKey="current" errorDest={errorDest} transactionDest={transactionDest}/>);
    if (traceLength === 1) {
        nodes.push(<projects_1.default key="missing-services" orgId={organization.slug} slugs={[current.project_slug]}>
        {({ projects }) => {
                const project = projects.find(p => p.slug === current.project_slug);
                if (project === null || project === void 0 ? void 0 : project.platform) {
                    if (BACKEND_PLATFORMS.includes(project.platform)) {
                        return (<React.Fragment>
                  <MissingServiceNode anchor={anchor} organization={organization} platform={project.platform} connectorSide="right"/>
                  {currentNode}
                </React.Fragment>);
                    }
                    else if (FRONTEND_PLATFORMS.includes(project.platform)) {
                        return (<React.Fragment>
                  {currentNode}
                  <MissingServiceNode anchor={anchor} organization={organization} platform={project.platform} connectorSide="left"/>
                </React.Fragment>);
                    }
                }
                return currentNode;
            }}
      </projects_1.default>);
    }
    else {
        nodes.push(currentNode);
    }
    if (children.length) {
        nodes.push(<styles_1.TraceConnector key="children-connector"/>);
        nodes.push(<EventNodeSelector key="children-node" location={location} organization={organization} events={children} currentEvent={event} text={(0, locale_1.tn)('%s Child', '%s Children', children.length)} anchor={anchor} nodeKey="children" errorDest={errorDest} transactionDest={transactionDest}/>);
    }
    if (descendants === null || descendants === void 0 ? void 0 : descendants.length) {
        nodes.push(<styles_1.TraceConnector key="descendants-connector"/>);
        nodes.push(<EventNodeSelector key="descendants-node" location={location} organization={organization} events={descendants} currentEvent={event} text={(0, locale_1.tn)('%s Descendant', '%s Descendants', descendants.length)} anchor={anchor} nodeKey="descendants" errorDest={errorDest} transactionDest={transactionDest}/>);
    }
    return <styles_1.QuickTraceContainer>{nodes}</styles_1.QuickTraceContainer>;
}
exports.default = QuickTrace;
function handleNode(key, organization) {
    (0, analytics_1.trackAnalyticsEvent)({
        eventKey: 'quick_trace.node.clicked',
        eventName: 'Quick Trace: Node clicked',
        organization_id: parseInt(organization.id, 10),
        node_key: key,
    });
}
function handleDropdownItem(key, organization, extra) {
    (0, analytics_1.trackAnalyticsEvent)({
        eventKey: 'quick_trace.dropdown.clicked' + (extra ? '_extra' : ''),
        eventName: 'Quick Trace: Dropdown clicked',
        organization_id: parseInt(organization.id, 10),
        node_key: key,
    });
}
function EventNodeSelector({ location, organization, events = [], text, currentEvent, nodeKey, anchor, errorDest, transactionDest, numEvents = 5, }) {
    let errors = events.flatMap(event => { var _a; return (_a = event.errors) !== null && _a !== void 0 ? _a : []; });
    let type = nodeKey === 'current' ? 'black' : 'white';
    const hasErrors = errors.length > 0;
    if (hasErrors) {
        type = nodeKey === 'current' ? 'error' : 'warning';
        text = (<styles_1.ErrorNodeContent>
        <icons_1.IconFire size="xs"/>
        {text}
      </styles_1.ErrorNodeContent>);
    }
    // make sure to exclude the current event from the dropdown
    events = events.filter(event => event.event_id !== currentEvent.id);
    errors = errors.filter(error => error.event_id !== currentEvent.id);
    if (events.length + errors.length === 0) {
        return <styles_1.EventNode type={type}>{text}</styles_1.EventNode>;
    }
    else if (events.length + errors.length === 1) {
        /**
         * When there is only 1 event, clicking the node should take the user directly to
         * the event without additional steps.
         */
        const hoverText = errors.length ? ((0, locale_1.t)('View the error for this Transaction')) : (<styles_1.SingleEventHoverText event={events[0]}/>);
        const target = errors.length
            ? (0, utils_1.generateSingleErrorTarget)(errors[0], organization, location, errorDest)
            : (0, utils_1.generateSingleTransactionTarget)(events[0], organization, location, transactionDest);
        return (<StyledEventNode text={text} hoverText={hoverText} to={target} onClick={() => handleNode(nodeKey, organization)} type={type} shouldOffset={hasErrors}/>);
    }
    else {
        /**
         * When there is more than 1 event, clicking the node should expand a dropdown to
         * allow the user to select which event to go to.
         */
        const hoverText = (0, locale_1.tct)('View [eventPrefix] [eventType]', {
            eventPrefix: TOOLTIP_PREFIX[nodeKey],
            eventType: errors.length && events.length
                ? 'events'
                : events.length
                    ? 'transactions'
                    : 'errors',
        });
        return (<styles_1.DropdownContainer>
        <dropdownLink_1.default caret={false} title={<StyledEventNode text={text} hoverText={hoverText} type={type} shouldOffset={hasErrors}/>} anchorRight={anchor === 'right'}>
          {errors.length > 0 && (<styles_1.DropdownMenuHeader first>
              {(0, locale_1.tn)('Related Error', 'Related Errors', errors.length)}
            </styles_1.DropdownMenuHeader>)}
          {errors.slice(0, numEvents).map(error => {
                const target = (0, utils_1.generateSingleErrorTarget)(error, organization, location, errorDest);
                return (<DropdownNodeItem key={error.event_id} event={error} to={target} allowDefaultEvent onSelect={() => handleDropdownItem(nodeKey, organization, false)} organization={organization} anchor={anchor}/>);
            })}
          {events.length > 0 && (<styles_1.DropdownMenuHeader first={errors.length === 0}>
              {(0, locale_1.tn)('Transaction', 'Transactions', events.length)}
            </styles_1.DropdownMenuHeader>)}
          {events.slice(0, numEvents).map(event => {
                const target = (0, utils_1.generateSingleTransactionTarget)(event, organization, location, transactionDest);
                return (<DropdownNodeItem key={event.event_id} event={event} to={target} onSelect={() => handleDropdownItem(nodeKey, organization, false)} allowDefaultEvent organization={organization} subtext={(0, formatters_1.getDuration)(event['transaction.duration'] / 1000, event['transaction.duration'] < 1000 ? 0 : 2, true)} anchor={anchor}/>);
            })}
          {(errors.length > numEvents || events.length > numEvents) && (<styles_1.DropdownItem to={(0, utils_1.generateTraceTarget)(currentEvent, organization)} allowDefaultEvent onSelect={() => handleDropdownItem(nodeKey, organization, true)}>
              {(0, locale_1.t)('View all events')}
            </styles_1.DropdownItem>)}
        </dropdownLink_1.default>
      </styles_1.DropdownContainer>);
    }
}
function DropdownNodeItem({ event, onSelect, to, allowDefaultEvent, organization, subtext, anchor, }) {
    return (<styles_1.DropdownItem to={to} onSelect={onSelect} allowDefaultEvent={allowDefaultEvent}>
      <styles_1.DropdownItemSubContainer>
        <projects_1.default orgId={organization.slug} slugs={[event.project_slug]}>
          {({ projects }) => {
            const project = projects.find(p => p.slug === event.project_slug);
            return (<projectBadge_1.default disableLink hideName project={project ? project : { slug: event.project_slug }} avatarSize={16}/>);
        }}
        </projects_1.default>
        {(0, utils_1.isQuickTraceEvent)(event) ? (<styles_1.QuickTraceValue value={event.transaction} 
        // expand in the opposite direction of the anchor
        expandDirection={anchor === 'left' ? 'right' : 'left'} maxLength={35} leftTrim trimRegex={/\.|\//g}/>) : (<styles_1.QuickTraceValue value={event.title} 
        // expand in the opposite direction of the anchor
        expandDirection={anchor === 'left' ? 'right' : 'left'} maxLength={45}/>)}
      </styles_1.DropdownItemSubContainer>
      {subtext && <styles_1.SectionSubtext>{subtext}</styles_1.SectionSubtext>}
    </styles_1.DropdownItem>);
}
function StyledEventNode({ text, hoverText, to, onClick, type = 'white', shouldOffset = false, }) {
    return (<tooltip_1.default position="top" containerDisplayMode="inline-flex" title={hoverText}>
      <styles_1.EventNode type={type} icon={null} to={to} onClick={onClick} shouldOffset={shouldOffset}>
        {text}
      </styles_1.EventNode>
    </tooltip_1.default>);
}
const HIDE_MISSING_SERVICE_KEY = 'quick-trace:hide-missing-services';
// 30 days
const HIDE_MISSING_EXPIRES = 1000 * 60 * 60 * 24 * 30;
function readHideMissingServiceState() {
    const value = localStorage_1.default.getItem(HIDE_MISSING_SERVICE_KEY);
    if (value === null) {
        return false;
    }
    const expires = parseInt(value, 10);
    const now = new Date().getTime();
    return expires > now;
}
class MissingServiceNode extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            hideMissing: readHideMissingServiceState(),
        };
        this.dismissMissingService = () => {
            const { organization, platform } = this.props;
            const now = new Date().getTime();
            localStorage_1.default.setItem(HIDE_MISSING_SERVICE_KEY, (now + HIDE_MISSING_EXPIRES).toString());
            this.setState({ hideMissing: true });
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'quick_trace.missing_service.dismiss',
                eventName: 'Quick Trace: Missing Service Dismissed',
                organization_id: parseInt(organization.id, 10),
                platform,
            });
        };
        this.trackExternalLink = () => {
            const { organization, platform } = this.props;
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'quick_trace.missing_service.docs',
                eventName: 'Quick Trace: Missing Service Clicked',
                organization_id: parseInt(organization.id, 10),
                platform,
            });
        };
    }
    render() {
        const { hideMissing } = this.state;
        const { anchor, connectorSide, platform } = this.props;
        if (hideMissing) {
            return null;
        }
        const docPlatform = (0, docs_1.getDocsPlatform)(platform, true);
        const docsHref = docPlatform === null || docPlatform === 'javascript'
            ? 'https://docs.sentry.io/platforms/javascript/performance/connect-services/'
            : `https://docs.sentry.io/platforms/${docPlatform}/performance#connecting-services`;
        return (<React.Fragment>
        {connectorSide === 'left' && <styles_1.TraceConnector />}
        <styles_1.DropdownContainer>
          <dropdownLink_1.default caret={false} title={<StyledEventNode type="white" hoverText={(0, locale_1.t)('No services connected')} text="???"/>} anchorRight={anchor === 'right'}>
            <styles_1.DropdownItem width="small">
              <styles_1.ExternalDropdownLink href={docsHref} onClick={this.trackExternalLink}>
                {(0, locale_1.t)('Connect to a service')}
              </styles_1.ExternalDropdownLink>
            </styles_1.DropdownItem>
            <styles_1.DropdownItem onSelect={this.dismissMissingService} width="small">
              {(0, locale_1.t)('Dismiss')}
            </styles_1.DropdownItem>
          </dropdownLink_1.default>
        </styles_1.DropdownContainer>
        {connectorSide === 'right' && <styles_1.TraceConnector />}
      </React.Fragment>);
    }
}
//# sourceMappingURL=index.jsx.map