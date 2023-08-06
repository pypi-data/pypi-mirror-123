Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
const groupTombstones_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectFilters/groupTombstones"));
const projectFiltersChart_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectFilters/projectFiltersChart"));
const projectFiltersSettings_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectFilters/projectFiltersSettings"));
class ProjectFilters extends react_1.Component {
    render() {
        const { project, params, location } = this.props;
        const { orgId, projectId, filterType } = params;
        if (!project) {
            return null;
        }
        const features = new Set(project.features);
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Inbound Filters')} projectSlug={projectId}/>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Inbound Data Filters')}/>
        <permissionAlert_1.default />

        <textBlock_1.default>
          {(0, locale_1.t)('Filters allow you to prevent Sentry from storing events in certain situations. Filtered events are tracked separately from rate limits, and do not apply to any project quotas.')}
        </textBlock_1.default>

        <div>
          <projectFiltersChart_1.default project={project} params={this.props.params}/>

          {features.has('discard-groups') && (<navTabs_1.default underlined style={{ paddingTop: '30px' }}>
              <li className={filterType === 'data-filters' ? 'active' : ''}>
                <link_1.default to={(0, recreateRoute_1.default)('data-filters/', Object.assign(Object.assign({}, this.props), { stepBack: -1 }))}>
                  {(0, locale_1.t)('Data Filters')}
                </link_1.default>
              </li>
              <li className={filterType === 'discarded-groups' ? 'active' : ''}>
                <link_1.default to={(0, recreateRoute_1.default)('discarded-groups/', Object.assign(Object.assign({}, this.props), { stepBack: -1 }))}>
                  {(0, locale_1.t)('Discarded Issues')}
                </link_1.default>
              </li>
            </navTabs_1.default>)}

          {filterType === 'discarded-groups' ? (<groupTombstones_1.default orgId={orgId} projectId={project.slug} location={location}/>) : (<projectFiltersSettings_1.default project={project} params={this.props.params} features={features}/>)}
        </div>
      </react_1.Fragment>);
    }
}
exports.default = ProjectFilters;
//# sourceMappingURL=index.jsx.map