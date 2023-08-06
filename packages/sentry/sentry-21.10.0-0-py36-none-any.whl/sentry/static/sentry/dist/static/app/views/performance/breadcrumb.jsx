Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const locale_1 = require("app/locale");
const queryString_1 = require("app/utils/queryString");
const tabs_1 = (0, tslib_1.__importDefault)(require("./transactionSummary/tabs"));
const utils_1 = require("./transactionSummary/transactionEvents/utils");
const utils_2 = require("./transactionSummary/transactionTags/utils");
const utils_3 = require("./transactionSummary/transactionVitals/utils");
const utils_4 = require("./transactionSummary/utils");
const utils_5 = require("./vitalDetail/utils");
const utils_6 = require("./utils");
class Breadcrumb extends react_1.Component {
    getCrumbs() {
        const crumbs = [];
        const { organization, location, transaction, vitalName, eventSlug, traceSlug, transactionComparison, tab, } = this.props;
        const performanceTarget = {
            pathname: (0, utils_6.getPerformanceLandingUrl)(organization),
            query: Object.assign(Object.assign({}, location.query), { 
                // clear out the transaction name
                transaction: undefined }),
        };
        crumbs.push({
            to: performanceTarget,
            label: (0, locale_1.t)('Performance'),
            preserveGlobalSelection: true,
        });
        if (vitalName) {
            const webVitalsTarget = (0, utils_5.vitalDetailRouteWithQuery)({
                orgSlug: organization.slug,
                vitalName: 'fcp',
                projectID: (0, queryString_1.decodeScalar)(location.query.project),
                query: location.query,
            });
            crumbs.push({
                to: webVitalsTarget,
                label: (0, locale_1.t)('Vital Detail'),
                preserveGlobalSelection: true,
            });
        }
        else if (transaction) {
            const routeQuery = {
                orgSlug: organization.slug,
                transaction: transaction.name,
                projectID: transaction.project,
                query: location.query,
            };
            switch (tab) {
                case tabs_1.default.Tags: {
                    const tagsTarget = (0, utils_2.tagsRouteWithQuery)(routeQuery);
                    crumbs.push({
                        to: tagsTarget,
                        label: (0, locale_1.t)('Tags'),
                        preserveGlobalSelection: true,
                    });
                    break;
                }
                case tabs_1.default.Events: {
                    const eventsTarget = (0, utils_1.eventsRouteWithQuery)(routeQuery);
                    crumbs.push({
                        to: eventsTarget,
                        label: (0, locale_1.t)('All Events'),
                        preserveGlobalSelection: true,
                    });
                    break;
                }
                case tabs_1.default.WebVitals: {
                    const webVitalsTarget = (0, utils_3.vitalsRouteWithQuery)(routeQuery);
                    crumbs.push({
                        to: webVitalsTarget,
                        label: (0, locale_1.t)('Web Vitals'),
                        preserveGlobalSelection: true,
                    });
                    break;
                }
                case tabs_1.default.TransactionSummary:
                default: {
                    const summaryTarget = (0, utils_4.transactionSummaryRouteWithQuery)(routeQuery);
                    crumbs.push({
                        to: summaryTarget,
                        label: (0, locale_1.t)('Transaction Summary'),
                        preserveGlobalSelection: true,
                    });
                }
            }
        }
        if (transaction && eventSlug) {
            crumbs.push({
                to: '',
                label: (0, locale_1.t)('Event Details'),
            });
        }
        else if (transactionComparison) {
            crumbs.push({
                to: '',
                label: (0, locale_1.t)('Compare to Baseline'),
            });
        }
        else if (traceSlug) {
            crumbs.push({
                to: '',
                label: (0, locale_1.t)('Trace View'),
            });
        }
        return crumbs;
    }
    render() {
        return <breadcrumbs_1.default crumbs={this.getCrumbs()}/>;
    }
}
exports.default = Breadcrumb;
//# sourceMappingURL=breadcrumb.jsx.map