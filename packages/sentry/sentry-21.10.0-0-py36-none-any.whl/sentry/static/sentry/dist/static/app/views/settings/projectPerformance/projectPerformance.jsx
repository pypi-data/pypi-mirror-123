Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
class ProjectPerformance extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = () => {
            const { orgId, projectId } = this.props.params;
            const { organization } = this.props;
            this.setState({
                loading: true,
            });
            this.api.request(`/projects/${orgId}/${projectId}/transaction-threshold/configure/`, {
                method: 'DELETE',
                success: () => {
                    (0, analytics_1.trackAnalyticsEvent)({
                        eventKey: 'performance_views.project_transaction_threshold.clear',
                        eventName: 'Project Transaction Threshold: Cleared',
                        organization_id: organization.id,
                    });
                },
                complete: () => this.fetchData(),
            });
        };
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Performance'), projectId, false);
    }
    getEndpoints() {
        const { params } = this.props;
        const { orgId, projectId } = params;
        const endpoints = [
            ['threshold', `/projects/${orgId}/${projectId}/transaction-threshold/configure/`],
        ];
        return endpoints;
    }
    getEmptyMessage() {
        return (0, locale_1.t)('There is no threshold set for this project.');
    }
    renderLoading() {
        return (<LoadingIndicatorContainer>
        <loadingIndicator_1.default />
      </LoadingIndicatorContainer>);
    }
    get formFields() {
        const fields = [
            {
                name: 'metric',
                type: 'select',
                label: (0, locale_1.t)('Calculation Method'),
                choices: [
                    ['duration', (0, locale_1.t)('Transaction Duration')],
                    ['lcp', (0, locale_1.t)('Largest Contentful Paint')],
                ],
                help: (0, locale_1.tct)('This determines which duration is used to set your thresholds. By default, we use transaction duration which measures the entire length of the transaction. You can also set this to use a [link:Web Vital].', {
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/performance/web-vitals/"/>),
                }),
            },
            {
                name: 'threshold',
                type: 'string',
                label: (0, locale_1.t)('Response Time Threshold (ms)'),
                placeholder: (0, locale_1.t)('300'),
                help: (0, locale_1.tct)('Define what a satisfactory response time is based on the calculation method above. This will affect how your [link1:Apdex] and [link2:User Misery] thresholds are calculated. For example, misery will be 4x your satisfactory response time.', {
                    link1: (<externalLink_1.default href="https://docs.sentry.io/performance-monitoring/performance/metrics/#apdex"/>),
                    link2: (<externalLink_1.default href="https://docs.sentry.io/product/performance/metrics/#user-misery"/>),
                }),
            },
        ];
        return fields;
    }
    get initialData() {
        const { threshold } = this.state;
        return {
            threshold: threshold.threshold,
            metric: threshold.metric,
        };
    }
    renderBody() {
        const { organization, project } = this.props;
        const endpoint = `/projects/${organization.slug}/${project.slug}/transaction-threshold/configure/`;
        return (<react_1.default.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Performance')}/>
        <permissionAlert_1.default />
        <form_1.default saveOnBlur allowUndo initialData={this.initialData} apiMethod="POST" apiEndpoint={endpoint} onSubmitSuccess={resp => {
                const initial = this.initialData;
                const changedThreshold = initial.metric === resp.metric;
                (0, analytics_1.trackAnalyticsEvent)({
                    eventKey: 'performance_views.project_transaction_threshold.change',
                    eventName: 'Project Transaction Threshold: Changed',
                    organization_id: organization.id,
                    from: changedThreshold ? initial.threshold : initial.metric,
                    to: changedThreshold ? resp.threshold : resp.metric,
                    key: changedThreshold ? 'threshold' : 'metric',
                });
                this.setState({ threshold: resp });
            }}>
          <jsonForm_1.default title={(0, locale_1.t)('General')} fields={this.formFields} renderFooter={() => (<Actions>
                <button_1.default type="button" onClick={() => this.handleDelete()}>
                  {(0, locale_1.t)('Reset All')}
                </button_1.default>
              </Actions>)}/>
        </form_1.default>
      </react_1.default.Fragment>);
    }
}
const Actions = (0, styled_1.default)(panels_1.PanelItem) `
  justify-content: flex-end;
`;
const LoadingIndicatorContainer = (0, styled_1.default)('div') `
  margin: 18px 18px 0;
`;
exports.default = ProjectPerformance;
//# sourceMappingURL=projectPerformance.jsx.map