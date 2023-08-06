Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const projectIssueGrouping_1 = require("app/data/forms/projectIssueGrouping");
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const upgradeGrouping_1 = (0, tslib_1.__importDefault)(require("./upgradeGrouping"));
class ProjectIssueGrouping extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSubmit = (response) => {
            // This will update our project context
            projectActions_1.default.updateSuccess(response);
        };
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Issue Grouping'), projectId, false);
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { groupingConfigs: [] });
    }
    getEndpoints() {
        const { projectId, orgId } = this.props.params;
        return [['groupingConfigs', `/projects/${orgId}/${projectId}/grouping-configs/`]];
    }
    renderBody() {
        const { groupingConfigs } = this.state;
        const { organization, project, params, location } = this.props;
        const { orgId, projectId } = params;
        const endpoint = `/projects/${orgId}/${projectId}/`;
        const access = new Set(organization.access);
        const jsonFormProps = {
            additionalFieldProps: {
                organization,
                groupingConfigs,
            },
            features: new Set(organization.features),
            access,
            disabled: !access.has('project:write'),
        };
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Issue Grouping')}/>

        <textBlock_1.default>
          {(0, locale_1.tct)(`All events have a fingerprint. Events with the same fingerprint are grouped together into an issue. To learn more about issue grouping, [link: read the docs].`, {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/data-management-settings/event-grouping/"/>),
            })}
        </textBlock_1.default>

        <form_1.default saveOnBlur allowUndo initialData={project} apiMethod="PUT" apiEndpoint={endpoint} onSubmitSuccess={this.handleSubmit}>
          <jsonForm_1.default {...jsonFormProps} title={(0, locale_1.t)('Fingerprint Rules')} fields={[projectIssueGrouping_1.fields.fingerprintingRules]}/>

          <jsonForm_1.default {...jsonFormProps} title={(0, locale_1.t)('Stack Trace Rules')} fields={[projectIssueGrouping_1.fields.groupingEnhancements]}/>

          <feature_1.default features={['set-grouping-config']} organization={organization}>
            <jsonForm_1.default {...jsonFormProps} title={(0, locale_1.t)('Change defaults')} fields={[
                projectIssueGrouping_1.fields.groupingConfig,
                projectIssueGrouping_1.fields.secondaryGroupingConfig,
                projectIssueGrouping_1.fields.secondaryGroupingExpiry,
            ]}/>
          </feature_1.default>

          <upgradeGrouping_1.default groupingConfigs={groupingConfigs !== null && groupingConfigs !== void 0 ? groupingConfigs : []} organization={organization} projectId={params.projectId} project={project} api={this.api} onUpgrade={this.fetchData} location={location}/>
        </form_1.default>
      </react_1.Fragment>);
    }
}
exports.default = ProjectIssueGrouping;
//# sourceMappingURL=index.jsx.map