Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const sentryStatusPageLink = 'https://status.sentry.io/';
// This alert makes the user aware that one or more projects have been selected for the Low Priority Queue
function GlobalEventProcessingAlert({ className, projects }) {
    const projectsInTheLowPriorityQueue = projects.filter(project => project.eventProcessing.symbolicationDegraded);
    if (!projectsInTheLowPriorityQueue.length) {
        return null;
    }
    return (<alert_1.default className={className} type="info" icon={<icons_1.IconInfo size="sm"/>}>
      {projectsInTheLowPriorityQueue.length === 1
            ? (0, locale_1.tct)('Event Processing for this project is currently degraded. Events may appear with larger delays than usual or get dropped. Please check the [link:Status] page for a potential outage.', {
                link: <externalLink_1.default href={sentryStatusPageLink}/>,
            })
            : (0, locale_1.tct)('Event Processing for the [projectSlugs] projects is currently degraded. Events may appear with larger delays than usual or get dropped. Please check the [link:Status] page for a potential outage.', {
                projectSlugs: projectsInTheLowPriorityQueue.map(({ slug }, index) => (<react_1.Fragment key={slug}>
                  <strong>{slug}</strong>
                  {index !== projectsInTheLowPriorityQueue.length - 1 && ', '}
                </react_1.Fragment>)),
                link: <externalLink_1.default href={sentryStatusPageLink}/>,
            })}
    </alert_1.default>);
}
exports.default = GlobalEventProcessingAlert;
//# sourceMappingURL=globalEventProcessingAlert.jsx.map