Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const activityFeedItem_1 = (0, tslib_1.__importDefault)(require("./activityFeedItem"));
class OrganizationActivity extends asyncView_1.default {
    getTitle() {
        const { orgId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Activity'), orgId);
    }
    getEndpoints() {
        return [['activity', `/organizations/${this.props.params.orgId}/activity/`]];
    }
    renderLoading() {
        return this.renderBody();
    }
    renderEmpty() {
        return (<emptyStateWarning_1.default>
        <p>{(0, locale_1.t)('Nothing to show here, move along.')}</p>
      </emptyStateWarning_1.default>);
    }
    renderError(error, disableLog = false, disableReport = false) {
        const { errors } = this.state;
        const notFound = Object.values(errors).find(resp => resp && resp.status === 404);
        if (notFound) {
            return this.renderBody();
        }
        return super.renderError(error, disableLog, disableReport);
    }
    renderBody() {
        const { loading, activity, activityPageLinks } = this.state;
        return (<organization_1.PageContent>
        <pageHeading_1.default withMargins>{(0, locale_1.t)('Activity')}</pageHeading_1.default>
        <panels_1.Panel>
          {loading && <loadingIndicator_1.default />}
          {!loading && !(activity === null || activity === void 0 ? void 0 : activity.length) && this.renderEmpty()}
          {!loading && (activity === null || activity === void 0 ? void 0 : activity.length) > 0 && (<div data-test-id="activity-feed-list">
              {activity.map(item => (<errorBoundary_1.default mini css={{ marginBottom: (0, space_1.default)(1), borderRadius: 0 }} key={item.id}>
                  <activityFeedItem_1.default organization={this.props.organization} item={item}/>
                </errorBoundary_1.default>))}
            </div>)}
        </panels_1.Panel>
        {activityPageLinks && (<pagination_1.default pageLinks={activityPageLinks} {...this.props}/>)}
      </organization_1.PageContent>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationActivity);
//# sourceMappingURL=index.jsx.map