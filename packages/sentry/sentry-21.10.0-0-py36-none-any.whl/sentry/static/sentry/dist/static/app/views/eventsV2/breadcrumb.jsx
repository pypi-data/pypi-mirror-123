Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const locale_1 = require("app/locale");
const urls_1 = require("app/utils/discover/urls");
class DiscoverBreadcrumb extends react_1.Component {
    getCrumbs() {
        const crumbs = [];
        const { eventView, event, organization, location } = this.props;
        const discoverTarget = organization.features.includes('discover-query')
            ? {
                pathname: (0, urls_1.getDiscoverLandingUrl)(organization),
                query: Object.assign(Object.assign(Object.assign({}, location.query), eventView.generateBlankQueryStringObject()), eventView.getGlobalSelectionQuery()),
            }
            : null;
        crumbs.push({
            to: discoverTarget,
            label: (0, locale_1.t)('Discover'),
        });
        if (eventView && eventView.isValid()) {
            crumbs.push({
                to: eventView.getResultsViewUrlTarget(organization.slug),
                label: eventView.name || '',
            });
        }
        if (event) {
            crumbs.push({
                label: (0, locale_1.t)('Event Detail'),
            });
        }
        return crumbs;
    }
    render() {
        return <breadcrumbs_1.default crumbs={this.getCrumbs()}/>;
    }
}
DiscoverBreadcrumb.defaultProps = {
    event: undefined,
};
exports.default = DiscoverBreadcrumb;
//# sourceMappingURL=breadcrumb.jsx.map