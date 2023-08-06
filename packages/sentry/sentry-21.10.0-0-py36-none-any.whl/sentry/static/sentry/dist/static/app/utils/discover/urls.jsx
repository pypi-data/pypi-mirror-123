Object.defineProperty(exports, "__esModule", { value: true });
exports.getDiscoverLandingUrl = exports.eventDetailsRouteWithEventView = exports.eventDetailsRoute = exports.generateEventSlug = void 0;
/**
 * Create a slug that can be used with discover details views
 * or as a reference event for event-stats requests
 */
function generateEventSlug(eventData) {
    const id = eventData.id || eventData.latest_event;
    const projectSlug = eventData.project || eventData['project.name'];
    return `${projectSlug}:${id}`;
}
exports.generateEventSlug = generateEventSlug;
/**
 * Create a URL to an event details view.
 */
function eventDetailsRoute({ eventSlug, orgSlug, }) {
    return `/organizations/${orgSlug}/discover/${eventSlug}/`;
}
exports.eventDetailsRoute = eventDetailsRoute;
/**
 * Create a URL target to event details with an event view in the query string.
 */
function eventDetailsRouteWithEventView({ orgSlug, eventSlug, eventView, }) {
    const pathname = eventDetailsRoute({
        orgSlug,
        eventSlug,
    });
    return {
        pathname,
        query: eventView.generateQueryStringObject(),
    };
}
exports.eventDetailsRouteWithEventView = eventDetailsRouteWithEventView;
/**
 * Get the URL for the discover entry page which changes based on organization
 * feature flags.
 */
function getDiscoverLandingUrl(organization) {
    if (organization.features.includes('discover-query')) {
        return `/organizations/${organization.slug}/discover/queries/`;
    }
    return `/organizations/${organization.slug}/discover/results/`;
}
exports.getDiscoverLandingUrl = getDiscoverLandingUrl;
//# sourceMappingURL=urls.jsx.map